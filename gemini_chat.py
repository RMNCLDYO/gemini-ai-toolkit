from loading import Loading
from base_api import BaseAPI

class ChatAPI(BaseAPI):
    def chat(self):
        chat_history = []
        print("Start chatting with the model (type 'exit' or 'quit' to end the chat)")
        while True:
            user_input = input("[User]: ").strip()

            if user_input.lower() in ['exit', 'quit']:
                print("Exiting chat.")
                break

            if not user_input:
                print("Invalid input detected. Please enter a valid message.")
                continue

            chat_history.append({"role": "user", "parts": [{"text": user_input}]})
            response = self.response(chat_history)

            if response:
                print(f"[AI]: {response}")
                chat_history.append({"role": "model", "parts": [{"text": response}]})
            else:
                error_message = "An error occurred after your input. Attempting to continue."
                print(error_message)
                chat_history.append({"role": "model", "parts": [{"text": error_message}]})

    def response(self, chat_history):
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.0-pro-latest:generateContent?key={self.api_key}"
        payload = {"contents": chat_history}
        
        loading = Loading()
        loading.start()

        try:
            response = self.post(url, payload)
        except ValueError as e:
            print(f"Error communicating with Chat API: {e}")
            return None
        finally:
            loading.stop()

        if "candidates" in response and response["candidates"]:
            return response["candidates"][0]["content"]["parts"][0]["text"]
        return None