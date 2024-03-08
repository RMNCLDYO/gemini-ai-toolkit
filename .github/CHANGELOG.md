# Changelog

All notable changes to the project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 03/08/2024

This update transforms the Gemini AI Toolkit from a basic API wrapper into a comprehensive, user-friendly, and highly customizable interface for interacting with Google's Gemini API. The changes encompass a complete redesign of the codebase, introducing new functionalities, improving modularization, enhancing user experience, and providing advanced configuration options. 

Below is an overview of the key changes:

### Added
- config.py: A new module for dynamic configuration management, allowing users to set and manage environment variables and API configurations more flexibly.
- client.py: Introduced to encapsulate all HTTP request handling, including GET and POST requests, with robust error handling and user feedback via loading animations.
- gemini.py: Defines specialized classes (Chat, Text, and Vision) for handling specific types of interactions with the Gemini API, with support for advanced configuration options.
- Loading Animations: To provide immediate feedback to the user during network requests, improving the interaction experience.
- Comprehensive Error Handling: Detailed error messages and handling mechanisms across the toolkit to guide users through resolving issues efficiently.
- Streaming API Response Support: For real-time feedback and interaction, particularly beneficial for lengthy operations.
- Advanced Command-Line Interface in cli.py: Offers extensive customization options for API interactions, including safety settings, generation configurations, and operation modes.
- Safety and Generation Configuration Options: Users can specify detailed safety settings and generation parameters for fine-tuned control over API response content and behavior.

### Fixed
- Error Handling Improvements: Refined error handling across the codebase, ensuring that errors are caught and reported more clearly and helpfully.
- Configuration Load Handling: Enhanced the loading and validation of environment variables to prevent issues related to missing or incorrect configurations.

### Removed
- Redundant Code and Modules: Removed base_api.py, gemini_chat.py, gemini_text.py, gemini_vision.py, and gemini_cli.py due to their functionalities being integrated into the new, more efficient modules.
- Hardcoded Configuration Values: Eliminated the need for directly editing source code to change API keys, model choices, etc., in favor of using environment variables and .env configuration.

### Changed
- Modularization and Organization of the Codebase: Restructured the toolkit into more logical, focused modules for better maintainability, scalability, and ease of use.
- Enhanced User Feedback Mechanisms: Loading animations and improved error messages for a more interactive and informative user experience.
- Increased Flexibility in API Interactions: Through the introduction of advanced configuration and customization options, making the toolkit adaptable to a wide range of use cases and preferences.
- Documentation and Inline Comments: Updated and added comprehensive comments and documentation throughout the codebase to facilitate understanding and future modifications.

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
