# Google Sheets Export Setup

## Quick Setup (5 minutes)

### 1. Install Required Package

```bash
pip install gspread google-auth
```

### 2. Create Google Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Enable **Google Sheets API**:
   - Search "Google Sheets API" in the search bar
   - Click "Enable"
4. Create credentials:
   - Go to "Credentials" → "Create Credentials" → "Service Account"
   - Give it a name (e.g., "chatbot-exporter")
   - Skip optional steps
5. Download credentials:
   - Click on the service account you created
   - Go to "Keys" tab → "Add Key" → "Create new key"
   - Choose **JSON** format
   - Save as `credentials.json` in your project root

### 3. Share Your Google Sheet

1. Create a new Google Sheet or use existing one
2. Click "Share" button
3. Copy the **service account email** from `credentials.json`:
   ```json
   {
     "client_email": "chatbot-exporter@project.iam.gserviceaccount.com"
   }
   ```
4. Paste it in the "Share" dialog and give **Editor** permissions

### 4. Use in App

1. Click "Export" button in sidebar
2. Select "Google Sheets"
3. Paste your Google Sheet URL
4. Click "Export to Sheet"

Done! Your chat history will be appended to the sheet.

## File Structure

```
brainstorm/
├── credentials.json          # Your service account credentials
├── export.py                 # Export functions
└── ...
```

## Example Sheet Format

| Timestamp           | Role      | Content                    |
|---------------------|-----------|----------------------------|
| 2024-01-15 14:30:00 | user      | What is Python?            |
| 2024-01-15 14:30:05 | assistant | Python is a programming... |

## Troubleshooting

**Error: "Credentials file not found"**
- Make sure `credentials.json` is in project root
- Check the filename is exactly `credentials.json`

**Error: "Permission denied"**
- Share the sheet with service account email
- Give "Editor" permissions

**Error: "API not enabled"**
- Enable Google Sheets API in Cloud Console


