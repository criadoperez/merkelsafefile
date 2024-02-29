import requests

def upload_file(url, file_path):
    """Uploads a file to the specified URL."""
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    return response

def download_file(url, params=None):
    """Downloads a file from the specified URL."""
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.content, response.json()
    return None, None
