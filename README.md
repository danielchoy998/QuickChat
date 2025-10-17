# Model Testing Platform

A Streamlit-based chatbot platform for testing local GGUF models with Google Sheets export capabilities.

## Features

- 💬 **Local GGUF Model Support** - Run models locally with llama-cpp-python
- 🤗 **HuggingFace Integration** - Download models directly from HuggingFace Hub
- 📊 **Google Sheets Export** - Export conversations to Google Sheets for analysis
- 🎨 **Clean UI** - Simple and intuitive Streamlit interface
- ⚙️ **Configurable** - Adjust temperature, system prompts, and model selection

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd brainstorm

# Install dependencies
pip install -r requirements.txt

# For macOS with Metal support
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/metal
```

## Quick Start

```bash
streamlit run main.py
```

## Usage

### 1. Load a Model

**Option A: Local File**
- Select "Local File" in the sidebar
- Enter the path to your GGUF model
- Example: `./models/Qwen/Qwen3-0.6B-GGUF/Qwen3-0.6B-Q8_0.gguf`

**Option B: Download from HuggingFace**
- Select "HuggingFace Hub"
- Enter repository ID (e.g., `Qwen/Qwen3-0.6B-GGUF`)
- Enter GGUF filename (e.g., `Qwen3-0.6B-Q8_0.gguf`)
- Click "Download"

### 2. Chat with the Model

- Type your message in the chat input
- Adjust temperature and system prompt in the sidebar
- View conversation history

### 3. Export to Google Sheets (Optional)

**Setup Required:**

1. **Get Google API Credentials**
   - Follow [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md) for detailed instructions
   - Create a Google service account
   - Download credentials JSON file

2. **Configure Your Environment**
   ```bash
   # Copy the template
   cp copy.env .env
   
   # Edit .env and add your credentials path
   GOOGLE_API_KEY="./credentials.json"
   ```

3. **Share Your Sheet**
   - Open your Google Sheet
   - Share it with the service account email (found in credentials.json)
   - Give "Editor" permissions

4. **Export from App**
   - Click "Export" button in sidebar
   - Paste your Google Sheet ID
   - Click "Export to Google Sheets"

**Export Schema:**
| Timestamp | UUID | Model | Prompt | Response |
|-----------|------|-------|--------|----------|

## Project Structure

```
brainstorm/
├── main.py              # Main entry point
├── ui/
│   └── sidebar.py       # Sidebar UI components
├── inference.py         # Model inference logic
├── export.py           # Google Sheets export
├── utils.py            # Download & utilities
├── requirements.txt    # Python dependencies
└── credentials.json    # Google API credentials (not in git)
```

## Configuration

### Temperature
- **0.0** - Deterministic, consistent outputs
- **0.7** - Balanced (default)
- **2.0** - Very creative, random

### System Prompt
Customize the AI's behavior by editing the system prompt in the sidebar.

## Requirements

- Python 3.8+
- 4GB+ RAM (depends on model size)
- Metal GPU support (macOS) or CUDA (Linux/Windows) for better performance

## Security Notes

⚠️ **IMPORTANT**: Never commit sensitive files to git!

The `.gitignore` file is configured to exclude:
- `credentials.json` - Google API credentials
- `.env` - Environment variables (your actual config)
- `models/` - Large model files
- `*.gguf` - Model weight files

**What to commit:**
- ✅ `copy.env` - Template file with empty values
- ❌ `.env` - Your actual credentials (never commit this!)

**Setup for new users:**
```bash
# 1. Copy template
cp copy.env .env

# 2. Edit .env with your actual credentials
# 3. Never commit .env to git
```

## Troubleshooting

**"No module named 'gspread'"**
```bash
# Make sure you install in the same Python environment as Streamlit
which streamlit  # Check which Python Streamlit uses
/path/to/pip install gspread google-auth
```

**Model not loading**
- Check the file path is correct
- Ensure you have enough RAM
- Verify the file is a valid GGUF format

**Google Sheets export fails**
- Verify `credentials.json` exists
- Check the sheet is shared with service account email
- Ensure Google Sheets API is enabled

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

