import sys
import os
from dotenv import load_dotenv

def load_config(api_key=None):
    try:
        if not api_key:
            api_key = load_required_env_variables('GEMINI_API_KEY')
        
        if not api_key:
            print("[ ERROR ]: Failed to load API key. Please ensure it's set in your environment variables or .env file.")
            print("You can set it by running: export GEMINI_API_KEY=your_api_key_here")
            sys.exit(1)

        config = {
            'api_key': api_key,
            'model': os.getenv('GEMINI_MODEL', 'gemini-1.5-pro'),
            'base_url': os.getenv('GEMINI_BASE_URL', 'https://generativelanguage.googleapis.com'),
            'version': os.getenv('GEMINI_VERSION', 'v1beta')
        }

        if not validate_config(config):
            print("[ ERROR ]: Invalid configuration. Please check your environment variables and try again.")
            sys.exit(1)

        return config
    except Exception as e:
        print(f"[ ERROR ]: An unexpected error occurred while loading configuration: {str(e)}")
        print("Please ensure all required environment variables are set correctly.")
        sys.exit(1)

def load_required_env_variables(var_name):
    value = os.getenv(var_name)
    if value is None:
        try:
            load_dotenv()
            value = os.getenv(var_name)
            if not value:
                print(f"[ ERROR ]: {var_name} environment variable is not defined.")
                return None
        except ImportError:
            print("[ ERROR ]: dotenv package is not installed. Please install it with 'pip install python-dotenv' or define the environment variables directly.")
            return None
        except Exception as e:
            print(f"[ ERROR ]: Encountered an error loading environment variables: {str(e)}")
            return None
    return value

def validate_config(config):
    required_keys = ['api_key', 'model', 'base_url', 'version']
    for key in required_keys:
        if key not in config or not config[key]:
            print(f"[ ERROR ]: Missing or empty required configuration: {key}")
            return False

    if not config['api_key'].strip():
        print("[ ERROR ]: API key is empty or consists only of whitespace")
        return False

    if not config['base_url'].startswith(('http://', 'https://')):
        print("[ ERROR ]: Invalid base URL format")
        return False

    return True