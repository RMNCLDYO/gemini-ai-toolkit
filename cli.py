import argparse
from gemini import Chat, Text, Vision, Audio

def main():
    class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,
                      argparse.RawDescriptionHelpFormatter):
        pass
    parser = argparse.ArgumentParser(
        description="""
    ------------------------------------------------------------------
                            Gemini AI Toolkit                          
                   API Wrapper & Command-line Interface               
                          [v1.2.1] by @rmncldyo                      
    ------------------------------------------------------------------

    Gemini AI toolit is an API wrapper and command-line interface for Google's latest Gemini Pro and Gemini Ultra large-language models.

    | Option(s)                | Description                               | Example Usage                                                                 |
    |--------------------------|-------------------------------------------|-------------------------------------------------------------------------------|
    | -c,  --chat              | Enable chat mode                          | --chat                                                                        |
    | -t,  --text              | Enable text mode                          | --text                                                                        |
    | -v,  --vision            | Enable vision mode                        | --vision                                                                      |
    | -a,  --audio             | Enable audio mode                         | --audio                                                                       |
    | -p,  --prompt            | User prompt                               | --prompt "Write a story about a magic backpack."                              |
    | -m,  --media             | Media file path or url                    | --media "path_to_media_file"                                                  |
    | -s,  --stream            | Enable streaming output                   | --stream                                                                      |
    | -js, --json              | Enable JSON output                        | --json                                                                        |
    | -ak, --api_key           | Gemini API key for authentication         | --api_key "api_key_goes_here"                                                 |
    | -md, --model             | The model you would like to use           | --model "model_name_goes_here"                                                |
    | -sp, --system_prompt     | System prompt (instructions) for model    | --system_prompt "Write a story about a magic backpack."                       |
    | -mt, --max_tokens        | Maximum number of tokens to generate      | --max_tokens 1024                                                             |
    | -tm, --temperature       | Sampling temperature                      | --temperature 0.7                                                             |
    | -tp, --top_p             | Nucleus sampling threshold                | --top_p 0.9                                                                   |
    | -tk, --top_k             | Top-k sampling threshold                  | --top_k 40                                                                    |
    | -cc, --candidate_count   | Number of candidates to generate          | --candidate_count 1                                                           |
    | -ss, --stop_sequences    | Stop sequences for completion             | --stop_sequences ["SAFETY_WORD_1", "SAFETY_WORD_2"]                           |
    | -sc, --safety_categories | Safety categories for filtering           | --safety_categories ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH"] |
    | -st, --safety_thresholds | Safety thresholds for filtering           | --safety_thresholds ["BLOCK_ONLY_HIGH", "BLOCK_NONE"]                         |
    """,
        formatter_class=CustomFormatter,
        epilog="For detailed usage information, visit our ReadMe here: github.com/RMNCLDYO/gemini-ai-toolkit"
    )
    parser.add_argument('-c', '--chat', action='store_true', help='Enable chat mode')
    parser.add_argument('-t', '--text', action='store_true', help='Enable text mode')
    parser.add_argument('-v', '--vision', action='store_true', help='Enable vision mode')
    parser.add_argument('-a', '--audio', action='store_true', help='Enable audio mode')
    parser.add_argument('-p', '--prompt', type=str, help='Text or Vision prompt', metavar='')
    parser.add_argument('-m', '--media', type=str, help='Media file path or url', metavar='')
    parser.add_argument('-s', '--stream', action='store_true', help='Enable streaming output')
    parser.add_argument('-js', '--json', action='store_true', help='Enable JSON output')
    parser.add_argument('-ak', '--api_key', type=str, help='Gemini API key for authentication', metavar='')
    parser.add_argument('-md', '--model', type=str, default='gemini-1.0-pro-latest', help='The model you would like to use', metavar='')
    parser.add_argument('-sp', '--system_prompt', type=str, help='System prompt (instructions) for model', metavar='')
    parser.add_argument('-mt', '--max_tokens', type=int, help='Maximum number of tokens to generate', metavar='')
    parser.add_argument('-tm', '--temperature', type=float, help='Sampling temperature', metavar='')
    parser.add_argument('-tp', '--top_p', type=float, help='Nucleus sampling threshold', metavar='')
    parser.add_argument('-tk', '--top_k', type=int, help='Top-k sampling threshold', metavar='')
    parser.add_argument('-cc', '--candidate_count', type=int, help='Number of candidates to generate', metavar='')
    parser.add_argument('-ss', '--stop_sequences', type=str, nargs='+', help='Stop sequences for completion', metavar='')
    parser.add_argument('-sc', '--saftey_categories', type=str, help='Safety category/categories for completion', metavar='')
    parser.add_argument('-st', '--saftey_thresholds', type=str, help='Safety threshold(s) for completion', metavar='')

    args = parser.parse_args()
    
    if args.chat:
        Chat().run(args.api_key, args.model, args.prompt, args.stream, args.json, args.system_prompt, args.max_tokens, args.temperature, args.top_p, args.top_k, args.candidate_count, args.stop_sequences, args.saftey_categories, args.saftey_thresholds)
    elif args.text:
        Text().run(args.api_key, args.model, args.prompt, args.stream, args.json, args.system_prompt, args.max_tokens, args.temperature, args.top_p, args.top_k, args.candidate_count, args.stop_sequences, args.saftey_categories, args.saftey_thresholds)
    elif args.vision:
        Vision().run(args.api_key, args.model, args.prompt, args.media, args.stream, args.json, args.system_prompt, args.max_tokens, args.temperature, args.top_p, args.top_k, args.candidate_count, args.stop_sequences, args.saftey_categories, args.saftey_thresholds)
    elif args.audio:
        Audio().run(args.api_key, args.model, args.prompt, args.media, args.stream, args.json, args.system_prompt, args.max_tokens, args.temperature, args.top_p, args.top_k, args.candidate_count, args.stop_sequences, args.saftey_categories, args.saftey_thresholds)
    else:
        print("Error: Please specify a mode to use. Use --help for more information.")
        exit()

if __name__ == "__main__":
    main()