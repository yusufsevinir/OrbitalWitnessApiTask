Orbital Witness API Task

Overview

The Orbital Witness API Task is a Python-based solution designed to calculate usage credits for an AI-powered assistant called Orbital Copilot. The system processes user messages, calculates credits based on configurable rules, and determines the total credits consumed during a billing period. The project uses FastAPI for the API layer, and several Python utilities for core logic.

Features

	•	Credit Calculation:
		    Base cost per message.
		    Character count costs.
		    Word-length multipliers.
	    	Special rules for third vowels, length penalties, unique word bonuses, and palindromes.
	•	Fallback Mechanism:
		    Handles scenarios where external data (e.g., report details) is unavailable.
	•	API Endpoints:
	    	/usage: Returns usage data for the current billing period.
	•	Extensible Design:
	        Modularity allows easy addition of new rules and adjustments to the existing logic.

Installation

Requirements

	•	Python 3.10 or higher
	•	pip (Python package manager)

Steps

	1.	Clone the repository:

        git clone https://github.com/yusufsevinir/OrbitalWitnessApiTask.git
        cd OrbitalWitnessApiTask


	2.	Create a virtual environment:

        python3 -m venv venv
        source venv/bin/activate   # On Windows: venv\Scripts\activate


	3.	Install dependencies for the app:

        pip install -r src/requirements.txt


	4.	Install dependencies for testing:

        pip install -r tests/requirements_test.txt


	5.	Run the FastAPI application:

        uvicorn src.main:app --reload


	6.	Access the API documentation:
		Open your browser and navigate to http://127.0.0.1:8000/docs.

Usage

API Endpoints

1. /usage

	•	Method: GET
	•	Description: Returns usage data for the current billing period.
	•	Response Format:

{
  "usage": [
    {
      "message_id": 123,
      "timestamp": "2024-11-07T10:00:00Z",
      "report_name": "Short Lease Report",
      "credits_used": 15.0
    },
    {
      "message_id": 124,
      "timestamp": "2024-11-07T10:05:00Z",
      "credits_used": 8.45
    }
  ]
}

Testing

Run Tests

To run the tests, use the following command:

    pytest tests/

Test Coverage

	•	Tested Components:
	•	FastAPI routes.
	•	Usage service logic.
	•	External API client.
	•	Credit calculation logic (all rules covered).

Configuration

External Endpoints

	•	src/clients/external_api_client.py is configured to fetch data from the following endpoints:
	    https://owpublic.blob.core.windows.net/tech-task/messages/current-period: Fetches messages for the current billing period.
	    https://owpublic.blob.core.windows.net/tech-task/reports/:id: Fetches details for a specific report.

Editable Settings

	•	Update the base URL or endpoints in src/config.py.

Design Decisions

	1.	Separation of Concerns:
	    •	Each module handles a specific responsibility (e.g., credit_calculator.py handles only credit calculations).
	2.	Extensibility:
	    •	The design allows for new rules or calculation methods to be added easily.
	3.	Error Handling:
	    •	Handles API failures gracefully, using fallbacks when report details are unavailable.
	4.	Testing:
	    •	Comprehensive test coverage for individual components and overall system behavior.

Credit Calculation Rules

The following rules are applied to determine credits for each message:
	1.	Base Cost:
	    •	Every message starts with a base cost of 1 credit.
	2.	Character Count:
	    •	Add 0.05 credits for each character in the message.
	3.	Word Length Multipliers:
	    •	Words of 1-3 characters: +0.1 credits per word.
	    •	Words of 4-7 characters: +0.2 credits per word.
	    •	Words of 8+ characters: +0.3 credits per word.
	4.	Third Vowels:
	    •	Add 0.3 credits for each third character that is a vowel.
	5.	Length Penalty:
	    •	Add 5 credits if the message exceeds 100 characters.
	6.	Unique Word Bonus:
	    •	Subtract 2 credits if all words are unique and there are more than one word(minimum credit is still 1).
	7.	Palindrome Check:
	    •	Double the total credits if the message is a multi-character palindrome.

Example Scenarios

Scenario 1: Single Word

	•	Input: "hello"
	•	Output: Base + char count + word multiplier = 1 + 0.25 + 0.2 = 1.45 credits.

Scenario 2: Palindrome

	•	Input: "madam"
	•	Output: Base + char count + word multiplier (doubled) = 1.45 * 2 = 2.9 credits.

Scenario 3: Long Text

	•	Input: "A" * 101 (101 characters of A).
	•	Output: Base + char count + length penalty = 1 + 5.05 + 5 = 11.05 credits.
