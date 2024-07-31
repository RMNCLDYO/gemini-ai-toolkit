from gemini import Multimodal

Multimodal().run(
    prompt="Analyze both of these files and provide a summary of each, one by one. Don't overlook any details.",
    files=[
        "https://storage.googleapis.com/cloud-samples-data/generative-ai/audio/pixel.mp3",
        "https://storage.googleapis.com/cloud-samples-data/generative-ai/image/scones.jpg"
    ]
)