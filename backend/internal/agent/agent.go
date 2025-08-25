package agent

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"os"
	"strings"

	"github.com/kanjelkheir/droidify/internal/database"
)

// Data struct for the device information
type Data struct {
	Model               string `json:"model"`
	Twrp                string `json:"twrp"`
	Stock_firmware      string `json:"stock_firmware"`
	Odin                string `json:"odin"`
	Orange_fox_recovery string `json:"orange_fox_recovery"`
	Custom_firmware     string `json:"custom_firmware"`
	Shrp_recovery       string `json:"shrp_recovery"`
}

// RequestData struct for the incoming HTTP request body
type RequestData struct {
	Model string `json:"model"`
}

// Configurator defines the interface for configuration objects that can get responses.
type Configurator interface {
	GetResponse() (string, error)
}

// newConfigFunc is a package-level variable to create Configurator instances, allowing for mocking in tests.
var newConfigFunc func(message, apiKey, endpoint string) Configurator = func(message, apiKey, endpoint string) Configurator {
	return &Config{
		message:  message,
		api_key:  apiKey,
		endpoint: endpoint,
	}
}

// GetData handles retrieving device information, either from DB or Gemini API
func GetData(r *http.Request, db *database.Queries) (Data, error) {
	api_key := os.Getenv("GEMINI_API_KEY")
	endpoint := "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
	var reqData RequestData
	var resultData Data

	decoder := json.NewDecoder(r.Body)
	if err := decoder.Decode(&reqData); err != nil {
		return Data{}, errors.New("Invalid request body")
	}

	// Check if it already exists on the db
	data, err := db.GetDevice(context.Background(), reqData.Model)
	if err == nil {
		// If found in DB, return existing data
		resultData = Data{
			Model:               data.Model,
			Twrp:                data.Twrp.String,
			Stock_firmware:      data.StockFirmware.String,
			Odin:                data.Odin.String,
			Orange_fox_recovery: data.OrangeFoxRecovery.String,
			Custom_firmware:     data.CustomFirmeware.String,
			Shrp_recovery:       data.ShrpRecovery.String,
		}
		return resultData, nil
	}

	// If not in DB, generate prompt for Gemini API
	prompt := fmt.Sprintf(`I want you to generate similar results for the following device-model: %v.
		Provide the output in JSON format following this structure:
		{
			"Model": "device model",
			"Twrp": "twrp link",
			"Stock_firmware": "stock firmware link",
			"Odin": "odin link",
			"Orange_fox_recovery": "orange fox recovery link",
			"Custom_firmware": "custom firmware link",
			"Shrp_recovery": "shrp recovery link"
		}
 		The device model is: %s`, reqData.Model, reqData.Model)

	configurator := newConfigFunc(prompt, api_key, endpoint)

	generated_response, err := configurator.GetResponse()
	if err != nil {
		return Data{}, err
	}

	// Check if the response is wrapped in markdown code block and extract the JSON
	if strings.HasPrefix(generated_response, "```json\n") && strings.HasSuffix(generated_response, "\n```") {
		generated_response = strings.TrimPrefix(generated_response, "```json\n")
		generated_response = strings.TrimSuffix(generated_response, "\n```")
	}

	bytes := []byte(generated_response)
	err = json.Unmarshal(bytes, &resultData)
	if err != nil {
		return Data{}, err
	}

	// TODO: Save resultData to database here if needed.
	// For example:
	// _, err = db.CreateDevice(context.Background(), database.CreateDeviceParams{
	// 	Model: reqData.Model,
	// 	Twrp: sql.NullString{String: resultData.Twrp, Valid: resultData.Twrp != ""},
	// 	// ... populate other fields
	// })
	// if err != nil {
	// 	fmt.Printf("Error saving data to DB: %v\n", err)
	// }

	return resultData, nil

}

// Config struct holds configuration for Gemini API requests
type Config struct {
	message  string
	api_key  string
	endpoint string
}

// GetResponse sends a POST request to the Gemini API and returns the generated text.
func (c *Config) GetResponse() (string, error) {
	if c.message == "" {
		return "", errors.New("Invalid Message")
	}

	url := c.endpoint

	requestBody := map[string]any{
		"contents": []map[string]any{
			{
				"parts": []map[string]string{
					{"text": c.message},
				},
			},
		},
		"generationConfig": map[string]any{
			"temperature": 0.7,
			"topK":        40,
			"topP":        0.95,
		},
	}

	// Marshal the request body to JSON
	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		return "", fmt.Errorf("failed to marshal request body: %w", err)
	}

	// Create a new HTTP request
	buffer := bytes.NewBuffer(jsonData)
	req, err := http.NewRequest("POST", url, buffer)
	if err != nil {
		return "", fmt.Errorf("failed to create new request: %w", err)
	}

	// Set required headers
	req.Header.Add("Content-Type", "application/json")
	req.Header.Add("X-goog-api-key", c.api_key) // Add the API key to the header

	// Initialize a new HTTP client and send the request
	client := &http.Client{}
	res, err := client.Do(req)
	if err != nil {
		return "", fmt.Errorf("failed to send request to Gemini API: %w", err)
	}
	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		return "", fmt.Errorf("Gemini API returned non-200 status code: %d", res.StatusCode)
	}

	var data GeminiResponse
	decoder := json.NewDecoder(res.Body)
	if err := decoder.Decode(&data); err != nil {
		return "", fmt.Errorf("failed to decode Gemini API response: %w", err)
	}

	if len(data.Candidates) == 0 || len(data.Candidates[0].Content.Parts) == 0 {
		return "", errors.New("no content found in Gemini response")
	}

	result := data.Candidates[0].Content.Parts[0].Text
	return result, nil
}

// GeminiResponse structs for unmarshalling the API response
type GeminiResponse struct {
	Candidates []Candidate `json:"candidates"`
}

type Candidate struct {
	Content       Content        `json:"content"`
	FinishReason  string         `json:"finishReason"`
	SafetyRatings []SafetyRating `json:"safetyRatings"`
}

type Content struct {
	Parts []Part `json:"parts"`
}

type Part struct {
	Text string `json:"text"`
}

type SafetyRating struct {
	Category    string `json:"category"`
	Probability string `json:"probability"`
}
