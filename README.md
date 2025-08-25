# Droidify

![React](https://img.shields.io/badge/-React-blue?logo=react&logoColor=white)

## 📝 Description

Unlock the full potential of your Android device with Droidify, the ultimate platform for streamlined customization. Tired of spending hours searching for the right ROMs, recovery images, and tools? Droidify consolidates everything you need in one convenient location. Featuring a user-friendly React-powered interface, Droidify offers device-specific guides and direct downloads, empowering you to transform your Android experience in minutes. Harnessing a robust database, Droidify ensures you have access to the latest and greatest resources, personalized for your specific device. Say goodbye to complicated procedures and hello to effortless Android customization with Droidify!

## ✨ Features

- 🗄️ Database


## 🛠️ Tech Stack

- ⚛️ React


## 📦 Key Dependencies

```
react: ^19.1.1
react-dom: ^19.1.1
```

## 🚀 Run Commands

- **dev**: `npm run dev`
- **build**: `npm run build`
- **lint**: `npm run lint`
- **preview**: `npm run preview`
- **Run**: `go run .`
- **Build**: `go build`


## 📁 Project Structure

```
.
├── backend
│   ├── Dockerfile
│   ├── droidify
│   ├── go.mod
│   ├── go.sum
│   ├── internal
│   │   ├── agent
│   │   │   ├── agent.go
│   │   │   └── agent_test.go
│   │   └── database
│   │       ├── db.go
│   │       ├── devices.sql.go
│   │       └── models.go
│   ├── main.go
│   ├── sql
│   │   ├── queries
│   │   │   └── devices.sql
│   │   └── schema
│   │       ├── 001_devices.sql
│   │       ├── 002_remove_id.sql
│   │       └── 003_make_model_primary_key.sql
│   └── sqlc.yaml
├── eslint.config.js
├── index.html
├── package.json
├── public
│   └── favicon.svg
├── src
│   ├── App.css
│   ├── App.jsx
│   ├── assets
│   │   └── favicon.svg
│   ├── components
│   │   ├── CTA.css
│   │   ├── CTA.jsx
│   │   ├── Features.css
│   │   ├── Features.jsx
│   │   ├── Footer.css
│   │   ├── Footer.jsx
│   │   ├── Header.css
│   │   ├── Header.jsx
│   │   ├── Hero.css
│   │   ├── Hero.jsx
│   │   ├── HowItWorks.css
│   │   ├── HowItWorks.jsx
│   │   ├── PopularDevices.css
│   │   └── PopularDevices.jsx
│   ├── index.css
│   └── main.jsx
└── vite.config.js
```

## 🛠️ Development Setup

### Node.js/JavaScript Setup
1. Install Node.js (v18+ recommended)
2. Install dependencies: `npm install` or `yarn install`
3. Start development server: (Check scripts in `package.json`, e.g., `npm run dev`)


## 👥 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/eliekh05/Droidify.git`
3. **Create** a new branch: `git checkout -b feature/your-feature`
4. **Commit** your changes: `git commit -am 'Add some feature'`
5. **Push** to your branch: `git push origin feature/your-feature`
6. **Open** a pull request

Please ensure your code follows the project's style guidelines and includes tests where applicable.

---
*This README was generated with ❤️ by ReadmeBuddy*