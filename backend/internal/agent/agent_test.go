package agent

import (
	"bytes"
	"encoding/json"
	"errors"
	"net/http/httptest"
	"os"
	"testing"
)

// MockConfigurator implements the Configurator interface for testing.
type MockConfigurator struct {
	GetResponseFunc func() (string, error)
	// Message, APIKey, and Endpoint are stored to verify that the NewConfig call passed correct arguments.
	Message  string
	APIKey   string
	Endpoint string
}

func (m *MockConfigurator) GetResponse() (string, error) {
	if m.GetResponseFunc != nil {
		return m.GetResponseFunc()
	}
	return "", errors.New("GetResponseFunc not set in MockConfigurator")
}

func TestGetData(t *testing.T) {
	// Save original newConfigFunc and restore it after the test
	originalNewConfigFunc := newConfigFunc
	defer func() { newConfigFunc = originalNewConfigFunc }()

	// Set a dummy API key for the test
	os.Setenv("GEMINI_API_KEY", "dummy_api_key")
	defer os.Unsetenv("GEMINI_API_KEY")

	tests := []struct {
		name          string
		requestBody   RequestData
		mockResponse  string // The JSON string to be returned by mock GetResponse
		mockError     error  // The error to be returned by mock GetResponse
		expectedData  Data
		expectedError string
	}{
		{
			name: "Successful data retrieval",
			requestBody: RequestData{
				Model: "Samsung S23",
			},
			mockResponse: `{
				  "Model": "Samsung S23",
				  "Twrp": "http://example.com/s23_twrp",
				  "Stock_firmware": "http://example.com/s23_stock",
				  "Odin": "http://example.com/s23_odin",
				  "Orange_fox_recovery": "http://example.com/s23_orangefox",
				  "Custom_firmware": "http://example.com/s23_custom",
				  "Shrp_recovery": "http://example.com/s23_shrp"
				}`,
			mockError: nil,
			expectedData: Data{
				Model:               "Samsung S23",
				Twrp:                "http://example.com/s23_twrp",
				Stock_firmware:      "http://example.com/s23_stock",
				Odin:                "http://example.com/s23_odin",
				Orange_fox_recovery: "http://example.com/s23_orangefox",
				Custom_firmware:     "http://example.com/s23_custom",
				Shrp_recovery:       "http://example.com/s23_shrp",
			},
			expectedError: "",
		},
		{
			name: "GetResponse returns an error",
			requestBody: RequestData{
				Model: "SomeModel",
			},
			mockResponse:  "",
			mockError:     errors.New("mock GetResponse error"),
			expectedData:  Data{},
			expectedError: "mock GetResponse error",
		},
		{
			name: "Invalid JSON response from GetResponse",
			requestBody: RequestData{
				Model: "SomeModel",
			},
			mockResponse:  "this is not valid json",
			mockError:     nil,
			expectedData:  Data{},
			expectedError: "invalid character 'h' in literal true (expecting 'r')", // Expected JSON unmarshalling error from `json.Unmarshal`
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Set up the mock configurator for this test case
			newConfigFunc = func(message, apiKey, endpoint string) Configurator {
				return &MockConfigurator{
					GetResponseFunc: func() (string, error) {
						return tt.mockResponse, tt.mockError
					},
					Message:  message,
					APIKey:   apiKey,
					Endpoint: endpoint,
				}
			}

			// Prepare the request body
			jsonBody, _ := json.Marshal(tt.requestBody)
			req := httptest.NewRequest("POST", "/getdata", bytes.NewBuffer(jsonBody))
			req.Header.Set("Content-Type", "application/json")

			data, err := GetData(req)

			// Check for errors
			if tt.expectedError != "" {
				if err == nil || err.Error() != tt.expectedError {
					t.Errorf("Expected error '%s', got '%v'", tt.expectedError, err)
				}
				if data != (Data{}) {
					t.Errorf("Expected empty Data on error, got '%+v'", data)
				}
				return
			}

			if err != nil {
				t.Errorf("Unexpected error: %v", err)
				return
			}

			// Compare the results
			if data != tt.expectedData {
				t.Errorf("Expected %+v, got %+v", tt.expectedData, data)
			}
		})
	}

	// Separate test cases for json.NewDecoder errors that need specific request body setups
	t.Run("Invalid request body (malformed JSON)", func(t *testing.T) {
		// No need to mock newConfigFunc here as the error occurs before it's called
		req := httptest.NewRequest("POST", "/getdata", bytes.NewBuffer([]byte("this is not json")))
		req.Header.Set("Content-Type", "application/json")

		data, err := GetData(req)

		expectedError := "Invalid request body"
		if err == nil || err.Error() != expectedError {
			t.Errorf("Expected error '%s', got '%v'", expectedError, err)
		}
		if data != (Data{}) {
			t.Errorf("Expected empty Data on error, got '%+v'", data)
		}
	})

	t.Run("Empty request body (actual empty bytes)", func(t *testing.T) {
		// No need to mock newConfigFunc here as the error occurs before it's called
		req := httptest.NewRequest("POST", "/getdata", bytes.NewBuffer([]byte{}))
		req.Header.Set("Content-Type", "application/json")

		data, err := GetData(req)

		expectedError := "Invalid request body"
		if err == nil || err.Error() != expectedError {
			t.Errorf("Expected error '%s', got '%v'", expectedError, err)
		}
		if data != (Data{}) {
			t.Errorf("Expected empty Data on error, got '%+v'", data)
		}
	})
}
