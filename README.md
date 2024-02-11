<p align="center">
    <a href="https://python.org" title="Go to Python homepage"><img src="https://img.shields.io/badge/Python-&gt;=3.x-blue?logo=python&amp;logoColor=white" alt="Made with Python"></a>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/maintained-yes-2ea44f" alt="maintained - yes">
    <a href="/CONTRIBUTING.md" title="Go to contributions doc"><img src="https://img.shields.io/badge/contributions-welcome-2ea44f" alt="contributions - welcome"></a>
</p>

<p align="center">
    <a href="https://pypi.org/project/requests"><img src="https://img.shields.io/badge/dependency-requests-critical" alt="dependency - requests"></a>
    <a href="https://pypi.org/project/python-dotenv"><img src="https://img.shields.io/badge/dependency-python--dotenv-critical" alt="dependency - python-dotenv"></a>
</p>

<p align="center">
    <img width="450" src="https://raw.githubusercontent.com/RMNCLDYO/Gemini-API-Wrapper/main/.github/logo.png">
</p>

<p align="center">
    <img src="https://img.shields.io/badge/dynamic/json?label=Gemini+API+Wrapper&query=version&url=https%3A%2F%2Fraw.githubusercontent.com%2FRMNCLDYO%2FGemini-API-Wrapper%2Fmain%2F.github%2Fversion.json" alt="Gemini API Wrapper">
</p>

## Overview
A simple python wrapper for Google's latest AI model Gemini Pro, enabling programatic access to the text, chat and vision features.

## Key Features
- **Text API Integration**: Process and analyze text using Gemini's Text API.
- **Vision API Integration**: Analyze images and extract insights with the Vision API.
- **Chat API Integration**: Build conversational interfaces and interact with the model using Gemini's Chat API.

## Prerequisites
- `Python 3.x`

## Dependencies
The following Python packages are required:
- `requests`: For making HTTP requests to the Google API.
- `python-dotenv`: For loading environment variables from an `.env` file.

## Installation
To use this wrapper, clone the repository and install dependencies:
```bash
git clone https://github.com/RMNCLDYO/Gemini-AI-Wrapper-and-CLI.git
cd Gemini-API-Wrapper
pip install -r requirements.txt
```

## Configuration
1. To use the Gemini API, you'll need an API key. If you don't already have one, create a key in [Google AI Studio](https://makersuite.google.com/app/apikey).
2. Once you have your API key, create a new file named `.env` in the root directory (main folder), or rename the `example.env` file in the root directory of this project to `.env`.
3. Add your API key to the `.env` file as follows:
   ```
   API_KEY=your_api_key_here
   ```
4. The program will automatically load and use your API key when chatting with the language model.
   

## Usage

### Text API
```python
from gemini_text import TextAPI

# Initialize the Text API
request = TextAPI()

# Provide a text prompt
text_prompt = "Your text prompt"

# Request a response for your text prompt
response = request.response(text_prompt)

print(response)
```

### Vision API
```python
from gemini_vision import VisionAPI

# Initialize the Vision API
request = VisionAPI()

# Provide the path to your image
image_path = "path/to/image.jpg"

# Provide a prompt for your image
vision_prompt = "Describe the image"

# Request a response for your vision and text prompt
response = request.response(image_path, vision_prompt)

print(response)
```

### Chat API
```python
from gemini_chat import ChatAPI

# Initialize the Chat History
chat_history = []
print("Start chatting with the model (type 'exit' or 'quit' to end the chat)")

# Create a while loop for chatting with the model
while True:
    # Wait for user input
    user_input = input("[User]:").strip()

    # Method for exiting the chat
    if user_input.lower() in ['exit', 'quit']:
        print("Exiting chat.")
        break

    # Method for catching user errors without exiting
    if not user_input:
        print("Invalid input detected. Please enter a valid message.")
        continue
    
    # Update chat history
    chat_history.append({"role": "user", "parts": [{"text": user_input}]})

    # Initialize the Chat API
    request = ChatAPI()

    # Request a response for your chat message
    response = request.response(chat_history)

    # If the AI responds, print the message, otherwise print the error and save it to the chat history
    if response:
        print(f"------------------[AI]:{response}------------------")
        chat_history.append({"role": "model", "parts": [{"text": response}]})
    else:
        error_message = f"An error occurred after your input: '{user_input}'. Attempting to continue."
        print(error_message)
        chat_history.append({"role": "model", "parts": [{"text": error_message}]})

```

### VisionAPI - *Limitations and Requirements*

- Images must be in one of the following image data `MIME types`:
    - PNG - `image/png`
    - JPEG - `image/jpeg`
    - WEBP - `image/webp`
    - HEIC - `image/heic`
    - HEIF - `image/heif`

- Maximum of 16 individual images.
- Maximum of 4MB of data, including images and text.
- No specific limits to the number of pixels in an image; however, larger images are scaled down to fit a maximum resolution of 3072 x 3072 while preserving their original aspect ratio.

Prompts with a single image tend to yield better results.

## Contributing
Contributions are welcome!

Please refer to [CONTRIBUTING.md](.github/CONTRIBUTING.md) for detailed guidelines on how to contribute to this project.

## Reporting Issues
Encountered a bug? We'd love to hear about it. Please follow these steps to report any issues:

1. Check if the issue has already been reported.
2. Use the [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) template to create a detailed report.
3. Submit the report [here](https://github.com/RMNCLDYO/Gemini-API-Wrapper/issues).

Your report will help us make the project better for everyone.

## Feature Requests
Got an idea for a new feature? Feel free to suggest it. Here's how:

1. Check if the feature has already been suggested or implemented.
2. Use the [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) template to create a detailed request.
3. Submit the request [here](https://github.com/RMNCLDYO/Gemini-API-Wrapper/issues).

Your suggestions for improvements are always welcome.

## Versioning and Changelog
Stay up-to-date with the latest changes and improvements in each version:

- [CHANGELOG.md](.github/CHANGELOG.md) provides detailed descriptions of each release.

## Security
Your security is important to us. If you discover a security vulnerability, please follow our responsible disclosure guidelines found in [SECURITY.md](.github/SECURITY.md). Please refrain from disclosing any vulnerabilities publicly until said vulnerability has been reported and addressed.

## License
Licensed under the MIT License. See [LICENSE](LICENSE) for details.
