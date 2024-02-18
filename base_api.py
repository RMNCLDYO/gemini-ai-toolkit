import os
import requests

class BaseAPI:
    def __init__(self):
        self.api_key = self.get_env_variable('API_KEY')

        self.headers = {
            "Content-Type": "application/json",
        }

    def post(self, url, payload):
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ValueError(f"Error communicating with API: {e}")

    def get_env_variable(self, var_name):
        try:
            return os.environ[var_name]
        except:
            try:
                from dotenv import load_dotenv
                load_dotenv()
                return os.environ[var_name]
            except ImportError:
                raise ImportError("dotenv package is not installed and the environment variable is not set.")
            except KeyError:
                raise KeyError(f"Environment variable {var_name} not found after loading dotenv.")