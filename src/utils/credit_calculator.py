import re


class CreditCalculator:
    @staticmethod
    def calculate_message_credits(text: str) -> float:
        """
        Calculate the number of credits used based on the given text.

        Rules:
        - Base cost: Every message has a base cost of 1 credit.
        - Character count: Add 0.05 credits for each character in the message.
        - Word length multipliers:
            - For words of 1-3 characters: Add 0.1 credits per word.
            - For words of 4-7 characters: Add 0.2 credits per word.
            - For words of 8+ characters: Add 0.3 credits per word.
        - Third vowels: Add 0.3 credits for each third (3rd, 6th, 9th, ...) character
          that is a vowel (a, e, i, o, u).
        - Length penalty: If the message length exceeds 100 characters, add a penalty of 5 credits.
        - Unique word bonus: If all words in the message are unique (case-sensitive),
          subtract 2 credits (minimum cost should still be 1 credit).
        - Palindromes: If the entire message is a palindrome, double the total cost.
        
        :param text: The input text for which credits are calculated.
        :return: The total number of credits for the message.
        """
         # Base cost
        total_credits = 1.0

        # Character count cost
        char_count_cost = len(text) * 0.05
        total_credits += char_count_cost

        # Split the text into words
        words = re.findall(r"[a-zA-Z'-]+", text)

        # Calculate word length multipliers
        word_cost = 0
        for word in words:
            if len(word) <= 3:
                word_cost += 0.1
            elif len(word) <= 7:
                word_cost += 0.2
            else:
                word_cost += 0.3
        total_credits += word_cost

        # Calculate third vowels
        vowels = set("aeiouAEIOU")
        third_chars = text[2::3]  # Get every third character (0-indexed)
        third_vowel_cost = sum(0.3 for char in third_chars if char in vowels)
        total_credits += third_vowel_cost

        # Length penalty
        length_penalty = 5 if len(text) > 100 else 0
        total_credits += length_penalty

        # Unique word bonus (applies only if there are >1 words, and all are unique)
        unique_bonus = -2 if len(words) > 1 and len(set(words)) == len(words) else 0
        total_credits = max(1, total_credits + unique_bonus)

        # Palindrome check
        cleaned_text = ''.join(char.lower() for char in text if char.isalnum())
        is_palindrome = len(cleaned_text) > 1 and cleaned_text == cleaned_text[::-1]
        if is_palindrome:  # Exclude single-char palindromes
            total_credits *= 2

        # Ensure the minimum cost is 1 credit and round to two decimal places
        final_credits = round(max(1, total_credits), 2)
        return final_credits