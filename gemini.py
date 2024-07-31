from gemini_base import GeminiBase

print("------------------------------------------------------------------\n")
print("                         Gemini AI Toolkit                        \n")
print("               API Wrapper & Command-line Interface               \n")
print("                        [v1.3] by @rmncldyo                       \n")
print("------------------------------------------------------------------\n")

class Text(GeminiBase):
    def run(self, api_key=None, model=None, prompt=None, stream=None, json=None, system_prompt=None, max_tokens=None, temperature=None, top_p=None, top_k=None, candidate_count=None, stop_sequences=None, safety_categories=None, safety_thresholds=None):
        mode = "text"
        try:
            self.initialize_client(api_key, model)

            if not self.input_validator.validate_text_input(prompt, candidate_count, system_prompt, json, self.model, safety_categories, safety_thresholds):
                return

            command, _, user_text = self.handle_user_input(prompt, mode)
            if command == "exit":
                return

            conversation_data = self.prepare_conversation_data([{"role": "user", "parts": [{"text": user_text}]}], system_prompt, json, max_tokens, temperature, top_p, top_k, candidate_count, stop_sequences, safety_categories, safety_thresholds)
            
            if conversation_data is None:
                print("[ ERROR ]: Failed to prepare conversation data")
                return

            print("User: " + user_text)
            response = self.client.send_message(conversation_data, stream)
            if response:
                if not stream:
                    print(f"Assistant: {response.strip()}")
            else:
                print("[ ERROR ]: No response received from the assistant.")

        except Exception as e:
            print(f"[ ERROR ]: An unexpected error occurred: {str(e)}")
        finally:
            print("\nThank you for using the Gemini AI toolkit. Have a great day!")

class Chat(GeminiBase):
    def run(self, api_key=None, model=None, prompt=None, stream=None, json=None, system_prompt=None, max_tokens=None, temperature=None, top_p=None, top_k=None, candidate_count=None, stop_sequences=None, safety_categories=None, safety_thresholds=None):
        mode = "chat"
        try:
            self.initialize_client(api_key, model)
            
            if not self.input_validator.validate_chat_input(candidate_count, system_prompt, json, self.model, safety_categories, safety_thresholds):
                return

            conversation_history = []
            
            print("\nEnter '/clear' at any time to clear the conversation history (saving you on API credits).")
            print("Enter '/exit' or '/quit' at any time to end the conversation.\n")
            
            print("Assistant: Hello! How can I assist you today?")
            while True:
                try:
                    if prompt:
                        user_input = prompt.strip()
                        print(f"User: {user_input}")
                        prompt = None
                    else:
                        user_input = input("User: ").strip()

                    command, _, user_text = self.handle_user_input(user_input, mode)
                    if command == "exit":
                        break
                    elif command == "clear":
                        conversation_history = []
                        print("Assistant: Conversation history has been cleared.")
                        continue

                    if not user_text:
                        print("[ ERROR ]: Invalid input detected. Please enter a valid message.")
                        continue

                    conversation_history.append({"role": "user", "parts": [{"text": user_text}]})

                    conversation_data = self.prepare_conversation_data(conversation_history, system_prompt, json, max_tokens, temperature, top_p, top_k, candidate_count, stop_sequences, safety_categories, safety_thresholds)

                    if conversation_data is None:
                        print("[ ERROR ]: Failed to prepare conversation data")
                        continue

                    response = self.client.send_message(conversation_data, stream)
                    
                    if response:
                        conversation_history.append({"role": "model", "parts": [{"text": response.strip()}]})
                        if not stream:
                            print(f"Assistant: {response.strip()}")
                    else:
                        print("[ ERROR ]: No response received from the assistant.")
                
                except Exception as e:
                    print(f"[ ERROR ]: An unexpected error occurred: {str(e)}")
                    
        except Exception as e:
            print(f"[ ERROR ]: An unexpected error occurred: {str(e)}")
        finally:
            print("\nThank you for using the Gemini AI toolkit. Have a great day!")

class Multimodal(GeminiBase):
    def run(self, api_key=None, model=None, prompt=None, files=None, stream=None, json=None, system_prompt=None, max_tokens=None, temperature=None, top_p=None, top_k=None, candidate_count=None, stop_sequences=None, safety_categories=None, safety_thresholds=None):
        mode = "multimodal"
        first_message = True

        try:
            self.initialize_client(api_key, model)
            
            if not self.input_validator.validate_multimodal_input(candidate_count, system_prompt, json, self.model, safety_categories, safety_thresholds):
                print("[ ERROR ]: Multimodal input validation failed. Please check your parameters and try again.")
                return
            
            conversation_history = []

            print("Enter '/upload' at any time followed by the file path or url (separated by a space) and an optional prompt.")
            print("- Example: /upload https://example.com/image.jpg /path/to/file2.pdf What do you think about these files?")
            print("\nEnter '/clear' at any time to clear the conversation history (saving you on API credits).")
            print("Enter '/exit' or '/quit' at any time to end the conversation.\n")
            
            if files or prompt:
                conversation_history.append({"role": "user", "parts": []})
            
            if files:
                processed_files = self.file_handler.process_files(files)
                if processed_files:
                    conversation_history[0]["parts"].extend(processed_files)
                else:
                    print("[ WARNING ]: Failed to process some or all files. Continuing without them.")

            if prompt:
                conversation_history[0]["parts"].append({"text": prompt})
            
            if not files and not prompt:
                print("Assistant: Hello! I'm ready to assist you with any questions you may have.")
                first_message = False

            while True:
                try:
                    if conversation_history and conversation_history[-1]["role"] == "user" and conversation_history[-1]["parts"]:
                        conversation_data = self.prepare_conversation_data(conversation_history, system_prompt, json, max_tokens, temperature, top_p, top_k, candidate_count, stop_sequences, safety_categories, safety_thresholds)

                        if conversation_data is None:
                            print("[ ERROR ]: Failed to prepare conversation data")
                            continue

                        response = self.client.send_message(conversation_data, stream)

                        if response:
                            conversation_history.append({"role": "model", "parts": [{"text": response.strip() if not stream else response}]})
                            if not stream:
                                print(f"Assistant: {response.strip()}")
                            if not first_message and not stream:
                                print()
                        else:
                            print("[ ERROR ]: No response received from the assistant.")
                        first_message = False

                    user_input = input("User: ").strip()
                    
                    command, processed_files, user_text = self.handle_user_input(user_input, mode)
                    
                    if command == "exit":
                        break
                    elif command == "clear":
                        conversation_history = []
                        print("Assistant: Conversation history has been cleared.")
                        first_message = True
                        continue
                    elif command == "upload":
                        if not processed_files:
                            continue
                    
                    if processed_files or user_text:
                        if not conversation_history or conversation_history[-1]["role"] != "user":
                            conversation_history.append({"role": "user", "parts": []})

                        if processed_files:
                            conversation_history[-1]["parts"].extend(processed_files)
                        
                        if user_text:
                            conversation_history[-1]["parts"].append({"text": user_text})
                    else:
                        print("[ ERROR ]: Invalid input detected. Please enter a valid message or use the /upload command.")
                        continue

                except Exception as e:
                    print(f"[ ERROR ]: An unexpected error occurred: {str(e)}")

        except Exception as e:
            print(f"[ ERROR ]: An unexpected error occurred: {str(e)}")
        finally:
            if self.file_handler:
                self.file_handler.cleanup_cache()
            print("\nThank you for using the Gemini AI toolkit. Have a great day!")