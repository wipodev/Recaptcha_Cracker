from verbose_terminal import console
import requests
import re

def download_file(url: str, file_name: str, verbose: bool = True) -> bool:
  try:
    response = requests.get(url)
    with open(file_name, 'wb') as f:
        f.write(response.content)
    console.success(f"File downloaded successfully: {file_name}", verbose)
    return True
  except Exception as e:
    console.error(f"Error downloading file: {e}")
    return False

def clean_alphanumeric_text(raw_text: str, verbose: bool = True) -> str:
    console.info(f'formatting text: {raw_text}', verbose)
    formatted_text = re.sub(r'[^a-zA-Z0-9]', '', raw_text)    
    console.success(f'Formatted text: {formatted_text}', verbose)
    return formatted_text