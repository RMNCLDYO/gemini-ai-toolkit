import sys
import argparse
from gemini import Chat, Text, Multimodal

def main():
    parser = argparse.ArgumentParser(
        description="""
    ------------------------------------------------------------------
                            Gemini AI Toolkit                          
                   API Wrapper & Command-line Interface               
                            [v1.3] by @rmncldyo                      
    ------------------------------------------------------------------

    Gemini AI toolkit is an API wrapper and command-line interface for Google's latest large language models.

    Modes:
    - Chat: Interactive conversation with the model
    - Text: Single prompt-response interaction
    - Multimodal: Interaction with text and file inputs

    For detailed usage information, visit: github.com/RMNCLDYO/gemini-ai-toolkit
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('-c', '--chat', action='store_true', help='Start an interactive chat session with the model')
    mode_group.add_argument('-t', '--text', action='store_true', help='Generate a single text response from the model')
    mode_group.add_argument('-m', '--multimodal', action='store_true', help='Enable processing of multiple input types (text, images, etc.)')

    parser.add_argument('-p', '--prompt', type=str, help='The initial text prompt to send to the model')
    parser.add_argument('-f', '--files', nargs='+', help='Paths or URLs to files for multimodal input (images, audio, etc.)')
    parser.add_argument('-s', '--stream', action='store_true', help='Receive model output as a continuous stream rather than all at once')
    parser.add_argument('-js', '--json', action='store_true', help='Request model output in JSON format')
    parser.add_argument('-ak', '--api_key', type=str, help='Your Gemini API key for authentication')
    parser.add_argument('-md', '--model', type=str, help='Specify which Gemini model version to use')
    parser.add_argument('-sp', '--system_prompt', type=str, help='Provide specific instructions or context to guide the model\'s behavior')
    parser.add_argument('-mt', '--max_tokens', type=int, help='Set the maximum length of the model\'s response in tokens')
    parser.add_argument('-tm', '--temperature', type=float, help='Control the randomness of the model\'s output (0.0 to 2.0)')
    parser.add_argument('-tp', '--top_p', type=float, help='Set the cumulative probability threshold for token selection (0.0 to 1.0)')
    parser.add_argument('-tk', '--top_k', type=int, help='Limit token selection to the top K most likely tokens')
    parser.add_argument('-cc', '--candidate_count', type=int, help='Number of alternative responses to generate (currently limited to 1)')
    parser.add_argument('-ss', '--stop_sequences', nargs='+', help='Specify sequences that will cause the model to stop generating')
    parser.add_argument('-sc', '--safety_categories', nargs='+', help='Categories of content to filter for safety concerns')
    parser.add_argument('-st', '--safety_thresholds', nargs='+', help='Threshold levels for each safety category specified')

    try:
        args = parser.parse_args()
    except SystemExit:
        print("[ ERROR ]: Invalid command-line arguments. Please check the usage and try again.")
        sys.exit(1)

    common_args = {
        'api_key': args.api_key,
        'model': args.model,
        'prompt': args.prompt,
        'stream': args.stream,
        'json': args.json,
        'system_prompt': args.system_prompt,
        'max_tokens': args.max_tokens,
        'temperature': args.temperature,
        'top_p': args.top_p,
        'top_k': args.top_k,
        'candidate_count': args.candidate_count,
        'stop_sequences': args.stop_sequences,
        'safety_categories': args.safety_categories,
        'safety_thresholds': args.safety_thresholds
    }

    try:
        if args.chat:
            Chat().run(**common_args)
        elif args.text:
            Text().run(**common_args)
        elif args.multimodal:
            Multimodal().run(**common_args, files=args.files)  # files are now optional
    except Exception as e:
        print(f"[ ERROR ]: An unexpected error occurred during execution: {str(e)}")
        print("If this error persists, please check your input parameters and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()