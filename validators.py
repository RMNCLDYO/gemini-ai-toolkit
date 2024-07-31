class SafetyValidator:
    def __init__(self):
        self.valid_categories = [
            'HARM_CATEGORY_HARASSMENT',
            'HARM_CATEGORY_HATE_SPEECH',
            'HARM_CATEGORY_SEXUALLY_EXPLICIT',
            'HARM_CATEGORY_DANGEROUS_CONTENT'
        ]

        self.valid_thresholds = [
            'BLOCK_LOW_AND_ABOVE',
            'BLOCK_MEDIUM_AND_ABOVE',
            'BLOCK_ONLY_HIGH',
            'BLOCK_NONE'
        ]

    def validate(self, category, threshold):
        if not self.validate_categories(category):
            print(f"[ ERROR ]: Invalid safety category: {category}. Valid categories are: {', '.join(self.valid_categories)}")
            return False
        if not self.validate_thresholds(threshold):
            print(f"[ ERROR ]: Invalid safety threshold: {threshold}. Valid thresholds are: {', '.join(self.valid_thresholds)}")
            return False
        return True

    def validate_categories(self, category):
        return category in self.valid_categories

    def validate_thresholds(self, threshold):
        return threshold in self.valid_thresholds

class InputValidator:
    def __init__(self):
        self.safety_validator = SafetyValidator()

    def validate_text_input(self, prompt, candidate_count, system_prompt, json, model, safety_categories, safety_thresholds):
        if not prompt:
            print("[ ERROR ]: Invalid input detected. Please enter a valid message.")
            return False
        return self.validate_common_params(candidate_count, system_prompt, json, model, safety_categories, safety_thresholds)

    def validate_chat_input(self, candidate_count, system_prompt, json, model, safety_categories, safety_thresholds):
        return self.validate_common_params(candidate_count, system_prompt, json, model, safety_categories, safety_thresholds)

    def validate_multimodal_input(self, candidate_count, system_prompt, json, model, safety_categories, safety_thresholds):
        return self.validate_common_params(candidate_count, system_prompt, json, model, safety_categories, safety_thresholds)

    def validate_common_params(self, candidate_count, system_prompt, json, model, safety_categories, safety_thresholds):
        if candidate_count is not None:
            if not isinstance(candidate_count, int) or candidate_count <= 0:
                print("[ ERROR ]: Candidate count must be a positive integer.")
                return False
            if candidate_count > 1:
                print("[ ERROR ]: Candidate count greater than 1 is not supported due to a bug in the API. Please use a candidate count of 1, or remove the parameter.")
                return False
        
        if system_prompt and "1.5" not in model:
            print(f"[ ERROR ]: System instructions are only supported in Gemini 1.5 and later. Current model: {model}")
            return False
        
        if json and "1.5" not in model:
            print(f"[ ERROR ]: JSON output is only supported in Gemini 1.5 and later. Current model: {model}")
            return False
        
        if safety_categories and safety_thresholds:
            if len(safety_categories) != len(safety_thresholds):
                print("[ ERROR ]: Mismatch in safety categories and thresholds. Ensure each category has a corresponding threshold.")
                return False
            for category, threshold in zip(safety_categories, safety_thresholds):
                if not self.safety_validator.validate(category, threshold):
                    return False

        return True