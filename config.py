import os

def load_required_env_variables(var_name: str):
    value = os.getenv(var_name)
    if value is None:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            value = os.getenv(var_name)
            if value is None or value.strip() == "":
                print(f"Error: {var_name} environment variable is not defined. Please define it in a .env file or directly in your environment. You can also pass it as an argument to the function.")
                exit(1)
        except ImportError:
            print("Error: dotenv package is not installed. Please install it with 'pip install python-dotenv' or define the environment variables directly.")
            exit(1)
        except Exception as e:
            print(f"Error loading environment variables: {e}")
            exit(1)
    return value

def load_config(api_key=None):
    if not api_key:
        api_key = load_required_env_variables('GEMINI_API_KEY')
    
    return {
        'api_key': api_key,
        'model': os.getenv('GEMINI_MODEL', 'gemini-1.0-pro-latest'),
        'base_url': os.getenv('GEMINI_BASE_URL', 'https://generativelanguage.googleapis.com'),
        'timeout': int(os.getenv('GEMINI_TIMEOUT', 20)),
        'version': os.getenv('GEMINI_VERSION', 'v1beta')
    }
