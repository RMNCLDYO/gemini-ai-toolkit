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
This Python library serves as an intuitive wrapper for Google's A.I. Gemini, facilitating seamless interactions with its Text, Vision, and Chat API endpoints. It is designed to simplify the integration of Gemini's powerful AI functionalities into Python applications, making it easier for developers to leverage Google's AI technology in their projects.

## Key Features
- **Text API Integration**: Process and analyze text using Gemini's Text API.
- **Vision API Integration**: Analyze images and extract insights with the Vision API.
- **Chat API Integration**: Build conversational interfaces and interact with the model using Gemini's Chat API.

## Prerequisites
- Python 3.x
- An API key for Google's A.I. model, Gemini

## Installation
To use this wrapper, clone the repository and install dependencies:
```bash
git clone https://github.com/your-github-username/gemini-api-wrapper.git
cd Gemini-API-Wrapper
pip install -r requirements.txt
```

## Dependencies
The following Python packages are required:
- `requests`
- `python-dotenv`

## Configuration
1. Obtain an API key from Google's AI Studio [here](https://makersuite.google.com/app/apikey).
2. Create a new file named `.env` in the root directory, or rename the `example.env` file in the root directory of the project to `.env`.
3. Add your API key to the `.env` file as follows:
   ```
   API_KEY=your_api_key_here
   ```
4. The application will automatically load and use this API key when making API requests.

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

## Contributing
Contributions are welcome. Please follow the guidelines in [CONTRIBUTING](.github/CONTRIBUTING.md).

## Reporting Issues
Report issues via the GitHub issue tracker.

## License
Licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgements
This project is built upon Google's A.I. Gemini APIs and aims to provide a user-friendly interface for developers to integrate AI capabilities into their applications.
