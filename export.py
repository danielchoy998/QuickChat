import datetime
import os
from typing import List, Dict

def validate_credentials(credentials_path='credentials.json'):
    """
    Check if credentials file exists.
    
    Returns:
        tuple: (valid: bool, message: str)
    """
    if not os.path.exists(credentials_path):
        return False, f"Credentials file not found: {credentials_path}"
    
    if not os.path.isfile(credentials_path):
        return False, f"Path exists but is not a file: {credentials_path}"
    
    try:
        with open(credentials_path, 'r') as f:
            content = f.read()
            if not content:
                return False, "Credentials file is empty"
    except Exception as e:
        return False, f"Cannot read credentials file: {str(e)}"
    
    return True, "Credentials file found"

def export_to_google_sheets(messages: List[Dict], sheet_ID: str, model_name: str = None, credentials_path: str = None):
    f"""
    Export chat history to Google Sheets.
    Schema: timestamp, uuid, model_name, prompt, response

    Args :
        messages: List[Dict] - List of messages from the chat eg. [{"role": "user", "content": "Hello, how are you?"}, {"role": "assistant", "content": "I'm good, thank you!"}]

        sheet_ID: str - ID of the Google Sheet to export to eg. 1mDtzoBDuow3YtV0OYxqZUsljPHZSUtP6yaUX1UuSF30

        model_name: str , optional, will be auto-generated if not provided

    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        import uuid
        
        # Setup credentials
        if credentials_path is None:
            credentials_path = "./credentials.json"
        
        # Validate credentials first
        valid, message = validate_credentials(credentials_path)
        if not valid:
            return False, message
        
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Open sheet
        sheet = client.open_by_key(sheet_ID)
        
        worksheet = sheet.sheet1
        
        # Prepare data
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conversation_id = str(uuid.uuid4())[:8]  # Short UUID
        
        # Get next empty row (start from row 2)
        all_values = worksheet.get_all_values()
        next_row = len(all_values) + 1 if all_values else 2
        
        # Prepare batch data 
        rows_to_add = []
        i = 0
        while i < len(messages):
            msg = messages[i]
            
            # Skip system messages
            if msg["role"] == "system":
                i += 1
                continue
            
            # If user message, pair with next assistant message
            if msg["role"] == "user":
                prompt = msg["content"]
                response = ""
                
                # Look for assistant response
                if i + 1 < len(messages) and messages[i + 1]["role"] == "assistant":
                    response = messages[i + 1]["content"]
                    i += 2  
                else:
                    i += 1
                
                rows_to_add.append([
                    timestamp,
                    conversation_id,
                    model_name or "unknown",
                    prompt,
                    response
                ])
            else:
                i += 1
        
        # Append starting from row 2 or next available row
        if next_row < 2:
            next_row = 2
        
        if rows_to_add:
            worksheet.update(f'A{next_row}', rows_to_add)
        
        return True, f"Exported {len(rows_to_add)} conversation(s)"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

