# Changelog

All notable changes to the project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3] - 07/31/2024
This update significantly enhances the Gemini AI Toolkit with the introduction of multimodal support, improved error handling, and a more robust architecture. The toolkit now offers a more versatile and user-friendly experience, capable of handling a wider range of input types and providing more detailed feedback to users.

Below is an overview of the key changes:

### Added
- Multimodal support: New Multimodal class for handling multiple input types (text, images, audio, video) in a single request
- File handling: Implemented FileHandler class for managing file uploads, downloads, and caching
- Input validation: New InputValidator class to ensure user inputs meet API requirements
- Caching mechanism: Implemented file caching to improve performance

### Fixed
- Robust error handling: Implemented comprehensive error catching and reporting across all modules
- Rate limiting: Improved handling of API rate limits with automatic retries and clear user feedback

### Changed
- Architecture refactor: Introduced GeminiBase class to centralize common functionality
- CLI interface: Updated to support new multimodal features and provide more detailed help information
- Configuration management: Enhanced config validation and error reporting
- Client functionality: Upgraded to support new API endpoints and improved streaming capabilities

### Improved 
- Loading animation: Enhanced with graceful termination and better error handling
- Safety settings: Expanded safety categories and thresholds for finer control over content filtering
- Documentation: Updated README and inline comments to reflect new features and usage patterns
- Examples: Added new multimodal example to demonstrate advanced toolkit capabilities

## [1.2.1] - 04/18/2024
This update enhances the Gemini AI Toolkit with additional features, improved error handling, and expanded functionality, particularly introducing support for audio inputs and refining multimedia interaction. These improvements aim to make the toolkit more versatile and user-friendly, addressing community feedback and the evolving needs of developers.

Below is an overview of the key changes:

## Added
- Audio support: Introduced the Audio class to handle audio file inputs, enabling the toolkit to interact using sound, supporting a broader range of multimedia.
- System Instruction Support: Allows users to provide system-level instructions to models, enhancing control over AI responses (supported only in Gemini Pro 1.5 and later).
- JSON Output Format: Users can now receive responses in JSON format, facilitating integration with web technologies and data pipelines.
- Enhanced Streaming and Error Handling in client.py: Improved mechanisms for handling streaming responses and sophisticated error handling, particularly for API rate limits.
- Expanded CLI Options in cli.py: Added new CLI options to support audio mode, system prompts, and JSON output, enhancing functionality and user accessibility.

## Fixed
- Robust Error Handling: Improved error responses and handling, ensuring clearer feedback and guidance for resolving issues, particularly in streaming operations and API interactions.
- Enhanced Safety Settings: Refined checks and validations to adhere to API constraints more strictly, enhancing the safety and reliability of interactions with the API.

## Changed
- Updated client.py to handle new error scenarios and provide better feedback during API rate limits.
- Enhanced the configurability and flexibility of API interactions, making the toolkit adaptable to more specific user needs and preferences.
- Refined documentation and in-line comments to improve clarity and maintainability of the codebase.


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
