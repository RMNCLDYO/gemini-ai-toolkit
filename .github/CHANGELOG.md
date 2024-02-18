# Changelog

All notable changes to the project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 02/17/2024

Refactored code structure:
- Moved common functionalities such as API communication and loading indicator into separate modules (base_api.py and loading.py) to promote code reuse and maintainability.

Added command-line interface (CLI) support:
- Implemented a CLI interface to provide a user-friendly way to interact with the Gemini AI APIs.
- Added command-line options for text generation (text command) and image captioning (vision command).
- Implemented a chat command to start a chat session with the model directly from the command line.

Improved error handling and user feedback:
- Enhanced error handling to provide more informative error messages in case of API communication errors or unsupported image formats.
- Implemented better user feedback messages, such as indicating when the chat session is exiting or when an invalid input is detected.

Removed dependency on dotenv:
- Eliminated the dependency on the dotenv module by integrating environment variable loading directly into the BaseAPI class.
This simplifies the setup process for users by reducing the number of required dependencies.

Enhanced user experience:
- Added a loading indicator during API requests to provide visual feedback to the user while waiting for a response.
- Improved user prompts and messages to guide users through the CLI interface and provide helpful information.

## [1.0.1] - 02/10/2024

### Added
- Added vision support for WebP, HEIC (High Efficiency Image Container), and HEIF(High Efficiency Image File Format) image formats.

## [1.0.0] - 12/21/2023

### Added
- Initial release.
