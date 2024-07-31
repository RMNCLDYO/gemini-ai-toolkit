import os
import time
import shutil
import requests
from urllib.parse import urlparse, unquote

class FileHandler:
    def __init__(self, api_key, directory_path):
        self.api_key = api_key
        self.directory_path = directory_path
        self.cache_folder_path = os.path.join(directory_path, '.gemini_ai_toolkit_cache')
        os.makedirs(self.cache_folder_path, exist_ok=True)

    def handle_upload_command(self, user_input):
        new_files, new_prompt = self.parse_upload_command(user_input)
        if new_files:
            processed_new_files = self.process_files(new_files)
            return processed_new_files, new_prompt
        else:
            print("[ ERROR ]: No valid files were provided with the upload command.")
            print("[ ERROR ]: Please check your file path and try again.")
            return None, None

    def process_files(self, files):
        processed_files = []
        for file in files:
            file_info = self.process_file(file)
            if file_info:
                file_uri = file_info["fileData"]["fileUri"]
                file_name = os.path.basename(file)
                if self.wait_for_file_to_be_active(file_uri, file_name):
                    processed_files.append(file_info)
                else:
                    print(f"[ ERROR ]: File {file_name} did not become active in the expected time frame.")
        
        if not processed_files:
            print("[ ERROR ]: No valid files were processed.")
            return None
        
        return processed_files

    def process_file(self, file_input):
        if self.is_valid_url(file_input):
            return self.download_and_process_file(file_input)
        elif os.path.isfile(file_input):
            extension = os.path.splitext(file_input)[1].lstrip('.')
            mime_type = self.get_mime_type(extension)
            return self.upload_file(file_input, mime_type)
        else:
            print(f"[ ERROR ]: Invalid file input: {file_input}")
            return None

    def download_and_process_file(self, url):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            extension = self.get_extension_from_url(url)
            if not extension:
                content_type = response.headers.get('Content-Type', '').split(';')[0].strip()
                extension = self.guess_extension_from_mime_type(content_type)
                if not extension:
                    print(f"[ ERROR ]: Could not determine file extension for URL: {url}")
                    return None
            
            mime_type = self.get_mime_type(extension)
            filename = f"{int(time.time())}.{extension}"
            file_path = os.path.join(self.cache_folder_path, filename)
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            uploaded_file = self.upload_file(file_path, mime_type)
            if uploaded_file:
                uploaded_file["fileData"]["mimeType"] = mime_type
            return uploaded_file
        except requests.exceptions.RequestException as e:
            print(f"[ ERROR ]: Failed to download file at url: {url}. [ ERROR ]: {str(e)}")
            return None
        except Exception as e:
            print(f"[ ERROR ]: Failed to process downloaded file: {str(e)}")
            return None

    def upload_file(self, file_path, mime_type):
        print(f"Uploading file: {file_path}")
        print("Please wait while the file is being uploaded. This may take a few moments...")
        try:
            upload_url = f"https://generativelanguage.googleapis.com/upload/v1beta/files?key={self.api_key}"

            with open(file_path, 'rb') as file:
                file_content = file.read()
                num_bytes = len(file_content)

            data = {"file": {"display_name": os.path.basename(file_path)}}

            headers = {
                "X-Goog-Upload-Command": "start, upload, finalize",
                "X-Goog-Upload-Header-Content-Length": str(num_bytes),
                "X-Goog-Upload-Header-Content-Type": mime_type,
                "Content-Type": mime_type
            }

            response = requests.post(upload_url, headers=headers, json=data, data=file_content)

            if response.status_code == 200:
                response_data = response.json()
                file_uri = response_data.get("file", {}).get("uri")
                response_mime_type = response_data.get("file", {}).get("mimeType")
                if not file_uri:
                    print(f"[ ERROR ]: File upload successful, but no file URI returned. Response: {response.text}")
                    return None
                if response_mime_type != mime_type:
                    print(f"[ WARNING ]: Uploaded file MIME type ({response_mime_type}) differs from original ({mime_type})")
                return {"fileData": {"mimeType": mime_type, "fileUri": file_uri}}
            else:
                print(f"[ ERROR ]: Failed to upload file. Status code: {response.status_code}, Response: {response.text}")
                return None

        except Exception as e:
            print(f"[ ERROR ]: Encountered an error uploading file: {str(e)}")
            return None

    def wait_for_file_to_be_active(self, file_uri, file_name, timeout=90, interval=5):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if (time.time() - start_time) % 30 == 0:
                print(f"Still waiting on the status of file {file_name} to update. One moment please...")
            try:
                response = requests.get(f"{file_uri}?key={self.api_key}")
                response.raise_for_status()
                file_status = response.json().get("state")
                if file_status == "ACTIVE":
                    print(f"[ {file_name} ] was uploaded to the Google cloud servers successfully.\n")
                    return True
                elif file_status == "FAILED":
                    print(f"[ ERROR ]: File {file_name} failed to process.")
                    return False
            except requests.exceptions.RequestException as e:
                print(f"[ ERROR ]: Failed to check file status: {str(e)}")
            time.sleep(interval)
        print(f"[ ERROR ]: File {file_name} did not become active within the timeout period.")
        return False

    def cleanup_cache(self):
        try:
            if os.path.exists(self.cache_folder_path):
                shutil.rmtree(self.cache_folder_path)
                print("\nThe cache folder has been cleaned and all temporary files have been removed.")
            else:
                print("\nNo cache files to clean up.")
        except Exception as e:
            print(f"[ ERROR ]: Encountered an error while cleaning up cache files: {str(e)}")
        finally:
            os.makedirs(self.cache_folder_path, exist_ok=True)

    def is_valid_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
        
    def get_extension_from_url(self, url):
        path = unquote(urlparse(url).path)
        return os.path.splitext(path)[1].lstrip('.').lower()

    def guess_extension_from_mime_type(self, mime_type):
        ext_map = {v: k for k, v in self.get_mime_type_map().items()}
        return ext_map.get(mime_type.lower(), '')

    def get_mime_type(self, extension):
        mime_map = self.get_mime_type_map()
        mime_type = mime_map.get(extension.lower())
        if not mime_type:
            print(f"[ ERROR ]: Unsupported file format: {extension}")
            return None
        return mime_type

    def get_mime_type_map(self):
        return {
            "jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
            "webp": "image/webp", "gif": "image/gif",
            "heic": "image/heic", "heif": "image/heif",
            "mp4": "video/mp4", "mpeg": "video/mpeg", "mov": "video/quicktime",
            "avi": "video/x-msvideo", "flv": "video/x-flv", "mpg": "video/mpeg",
            "webm": "video/webm", "wmv": "video/x-ms-wmv", "3gp": "video/3gpp",
            "wav": "audio/wav", "mp3": "audio/mpeg", "aiff": "audio/x-aiff",
            "aac": "audio/aac", "ogg": "audio/ogg", "flac": "audio/flac",
            "txt": "text/plain", "html": "text/html", "css": "text/css",
            "js": "text/javascript", "ts": "application/typescript", 
            "csv": "text/csv", "md": "text/markdown", "py": "text/x-python", 
            "json": "application/json", "xml": "application/xml", 
            "rtf": "application/rtf", "pdf": "application/pdf"
        }

    def parse_upload_command(self, user_input):
        parts = user_input.split()
        if len(parts) < 2:
            print("[ ERROR ]: Please provide file path(s) after the /upload command.")
            return [], None
        
        files = []
        prompt = ""
        for part in parts[1:]:
            if os.path.exists(part) or self.is_valid_url(part):
                files.append(part)
            else:
                prompt = " ".join(parts[parts.index(part):])
                break
        
        return files, prompt if prompt else None