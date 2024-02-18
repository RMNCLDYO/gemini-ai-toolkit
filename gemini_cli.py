import argparse
from gemini_chat import ChatAPI
from gemini_text import TextAPI
from gemini_vision import VisionAPI

print("------------------------------------------------------------------\n")
print("                             Gemini AI                            \n")
print("               API Wrapper & Command-line Interface               \n")
print("                       [v1.0.0] by @rmncldyo                      \n")
print("------------------------------------------------------------------\n")

def main():
    parser = argparse.ArgumentParser(
                    prog="Gemini AI Wrapper & CLI",
                    description="A simple wrapper and command-line interface for Google's Gemini API.",
                    epilog="For more information, visit https://github.com/RMNCLDYO/Gemini-AI-Wrapper-and-CLI")
    
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('chat', help='Start a chat session')

    text_parser = subparsers.add_parser('text', help='Generate text from a prompt')
    text_parser.add_argument('text_prompt', type=str, help='Text prompt for the API')

    vision_parser = subparsers.add_parser('vision', help='Generate caption from an image')
    vision_parser.add_argument('image_path', type=str, help='Path to the image file')
    vision_parser.add_argument('vision_prompt', type=str, help='Vision prompt for the API')

    args = parser.parse_args()

    if args.command == 'chat':
        ChatAPI().chat()
    elif args.command == 'text':
        TextAPI().text(args.text_prompt)
    elif args.command == 'vision':
        VisionAPI().vision(args.image_path, args.vision_prompt)

if __name__ == "__main__":
    main()