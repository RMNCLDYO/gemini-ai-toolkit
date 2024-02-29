<p align="center">
    <a href="https://gemini.google.com/" title="Go to Gemini homepage">
        <img src="https://img.shields.io/badge/Google%20Gemini%20AI-45a5ff?style=for-the-badge&logo=googlebard&logoColor=fff" alt="Google Gemini AI">
    </a>
</p>

<p align="center">
    <a href="https://github.com/RMNCLDYO/Gemini-AI-Wrapper-and-CLI" title="Go to repo">
        <img src="https://img.shields.io/badge/dynamic/json?style=for-the-badge&label=Gemini+AI+Wrapper+and+CLI&query=version&url=https%3A%2F%2Fraw.githubusercontent.com%2FRMNCLDYO%2FGemini-AI-Wrapper-and-CLI%2Fmain%2F.github%2Fversion.json" alt="Gemini AI Wrapper and CLI">
    </a>
</p>

<p align="center">
    <a href=".github/CHANGELOG.md" title="Go to changelog"><img src="https://img.shields.io/badge/maintained-yes-2ea44f?style=for-the-badge" alt="maintained - yes"></a>
    <a href=".github/CONTRIBUTING.md" title="Go to contributions doc"><img src="https://img.shields.io/badge/contributions-welcome-2ea44f?style=for-the-badge" alt="contributions - welcome"></a>
</p>

<p align="center">
    <a href="https://github.com/RMNCLDYO/Gemini-AI-Wrapper-and-CLI" title="Go to repo">
        <img width="800" src="https://raw.githubusercontent.com/RMNCLDYO/Gemini-AI-Wrapper-and-CLI/main/.github/logo.png" alt="Gemini AI Wrapper and CLI">
    </a>
</p>

## Overview
This toolkit provides a straightforward interface for interacting with Google's Gemini Pro 1.0 and upcoming 1.5 AI models. It facilitates tasks such as text generation, image captioning & analysis, and multi-turn chat (chatbot) functionality by abstracting complex API calls into simpler, more accessible commands. This tool is especially useful for everyday users, developers and researchers who wish to incorporate advanced AI capabilities into their projects without delving into the intricacies of direct API communication offering access to the full suite of Google's Gemini Pro and soon Gemini Ultra large language models.

## Key Features
- **Chat Functionality**: Chat with Gemini's advanced conversational models.
- **Image Captioning**: Analyze images and generate descriptive captions or insights.
- **Text Generation**: Generate creative and contextually relevant text based on prompts.
- **Command-Line Interface (CLI)**: Access Gemini AI functionalities directly from the command line for quick integrations and testing.
- **Python Wrapper**: Enables seamless interaction with the full suite of Gemini models offered by Google using just two lines of code.

## Prerequisites
- `Python 3.x`
- An API key from Google AI Studio

## Dependencies
The following Python packages are required:
- `requests`: For making HTTP requests to Google's Gemini API.

The following Python packages are optional:
- `python-dotenv`: For managing API keys and other environment variables.

## Installation
Follow these steps to set up the Gemini AI Wrapper and CLI on your system:

Clone the repository:
```bash
git clone https://github.com/RMNCLDYO/Gemini-AI-Wrapper-and-CLI.git
cd Gemini-AI-Wrapper-and-CLI
```

Install required Python packages:
```bash
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

## CLI Usage
#### Start a Chat Session:
```bash
python gemini_cli.py chat
```

#### Generate Text from a Prompt:
```bash
python gemini_cli.py text "Your text prompt here"
```

#### Generate Caption from an Image:
```bash
python gemini_cli.py vision path/to/your/image.jpg "Vision prompt"
```

## Python Wrapper Usage
#### Start a Chat Session:
```python
from gemini_chat import ChatAPI

ChatAPI().chat()
```

#### Generate Text from a Prompt:
```python
from gemini_text import TextAPI

TextAPI().text("Your text prompt here")
```

#### Generate Caption from an Image:
```python
from gemini_vision import VisionAPI

VisionAPI().vision("path/to/your/image.jpg", "Vision prompt")
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
3. Submit the report [here](https://github.com/RMNCLDYO/Gemini-AI-Wrapper-and-CLI/issues).

Your report will help us make the project better for everyone.

## Feature Requests
Got an idea for a new feature? Feel free to suggest it. Here's how:

1. Check if the feature has already been suggested or implemented.
2. Use the [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) template to create a detailed request.
3. Submit the request [here](https://github.com/RMNCLDYO/Gemini-AI-Wrapper-and-CLI/issues).

Your suggestions for improvements are always welcome.

## Versioning and Changelog
Stay up-to-date with the latest changes and improvements in each version:

- [CHANGELOG.md](.github/CHANGELOG.md) provides detailed descriptions of each release.

## Security
Your security is important to us. If you discover a security vulnerability, please follow our responsible disclosure guidelines found in [SECURITY.md](.github/SECURITY.md). Please refrain from disclosing any vulnerabilities publicly until said vulnerability has been reported and addressed.

## License
Licensed under the MIT License. See [LICENSE](LICENSE) for details.
