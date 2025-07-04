
# GenAI Studio

A Streamlit-based application for experimenting with Generative AI models. This project runs in a GitHub Codespace with a Python Dev Container pre-configured for quick startup and ease of development.

## 🚀 Features

- Built with **Streamlit** for interactive UI
- Powered by **Python 3.11**
- Ready-to-use **Dev Container** setup
- Supports easy deployment in GitHub Codespaces
- Automatic installation of dependencies from `requirements.txt` and `packages.txt`

## 📦 Requirements

Before running the app, ensure that you have:

- `packages.txt` for system packages (optional)
- `requirements.txt` for Python dependencies

These files will be automatically used to install necessary packages on container start.

## 🛠️ Development Setup

This project uses [Dev Containers](https://containers.dev/) with the following setup:

- **Python Dev Container**: `mcr.microsoft.com/devcontainers/python:1-3.11-bullseye`
- **VSCode Extensions**:
  - `ms-python.python`
  - `ms-python.vscode-pylance`

## 📂 File Structure

```
├── .devcontainer/
│   └── devcontainer.json      # Dev container configuration
├── genai_studio.py.py         # Main Streamlit app
├── packages.txt               # Optional system dependencies
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## ▶️ Run the App

Once the Codespace starts, the following command is run automatically:

```bash
streamlit run genai_studio.py.py --server.enableCORS false --server.enableXsrfProtection false
```

Access the app at port **8501** (auto-forwarded in the Codespace).

## 📬 Contributing

Feel free to fork and contribute! Pull requests are welcome.

## 📝 License

This project is licensed under the MIT License.

---

✅ Happy coding with GenAI!
