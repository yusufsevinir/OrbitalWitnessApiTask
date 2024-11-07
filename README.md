Orbital Witness API Task

Overview

The Orbital Witness API Task is a Python-based solution developed to calculate usage credits for an AI-powered assistant, Orbital Copilot. The system processes user messages, applies configurable credit calculation rules, and determines the total credits consumed during a billing period. Built with FastAPI, it provides a robust and extensible API for usage data retrieval and credit computations.

Features

	•	Credit Calculation:
	•	Base cost per message.
	•	Character count costs.
	•	Word-length multipliers.
	•	Advanced rules for:
	•	Third vowels.
	•	Length penalties.
	•	Unique word bonuses.
	•	Palindromes.
	•	Fallback Mechanism:
	•	Graceful handling of unavailable external data (e.g., missing report details).
	•	API Endpoints:
	•	/usage: Returns detailed usage data for the current billing period.
	•	Extensible Design:
	•	Modular architecture supports easy addition of new rules or adjustment of existing logic.

Project Structure

OrbitalWitnessApiTask/
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app entry point
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── external_api_client.py  # External API client for fetching messages/reports
│   ├── services/
│   │   ├── __init__.py
│   │   ├── usage_service.py        # Core logic for usage and credits
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── credit_calculator.py    # Implements credit calculation logic
│   ├── config.py                   # Configuration settings
│   └── requirements.txt            # App dependencies
├── tests/
│   ├── __init__.py
│   ├── test_main.py                # Tests for FastAPI endpoints
│   ├── test_usage_service.py       # Unit tests for usage service
│   ├── test_external_api_client.py # Unit tests for API client
│   ├── test_credit_calculator.py   # Unit tests for credit calculator
│   └── requirements_test.txt       # Dependencies for testing
├── README.md                       # Project documentation
└── pytest.ini                      # Pytest configuration

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


	3.	Install dependencies:

pip install -r src/requirements.txt


	4.	Install testing dependencies:

pip install -r tests/requirements_test.txt


	5.	Run the FastAPI application:

uvicorn src.app.main:app --reload


	6.	Access the API documentation:
Open http://127.0.0.1:8000/docs in your browser.

Usage

API Endpoints

1. /usage

	•	Method: GET
	•	Description: Returns usage data for the current billing period.
	•	Example Response:

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

pytest tests/

Test Coverage

	•	Tested Components:
	•	FastAPI routes.
	•	Usage service logic.
	•	External API client.
	•	Credit calculation rules.

Configuration

External Endpoints

	•	src/clients/external_api_client.py fetches data from:
	•	Messages: https://owpublic.blob.core.windows.net/tech-task/messages/current-period
	•	Report Details: https://owpublic.blob.core.windows.net/tech-task/reports/:id

Editable Settings

	•	Configure base URLs and endpoints in src/config.py.

Credit Calculation Rules

	1.	Base Cost:
	•	Every message starts with 1 credit.
	2.	Character Count:
	•	Add 0.05 credits per character in the message.
	3.	Word Length Multipliers:
	•	1-3 characters: +0.1 credits per word.
	•	4-7 characters: +0.2 credits per word.
	•	8+ characters: +0.3 credits per word.
	4.	Third Vowels:
	•	Add 0.3 credits for each third vowel in the message.
	5.	Length Penalty:
	•	Add 5 credits if the message exceeds 100 characters.
	6.	Unique Word Bonus:
	•	Subtract 2 credits if all words are unique (minimum 1 credit).
	7.	Palindrome Check:
	•	Double the total credits if the message is a multi-character palindrome.

Example Scenarios

Scenario 1: Single Word

	•	Input: “hello”
	•	Output: Base + char count + word multiplier = 1 + 0.25 + 0.2 = 1.45 credits

Scenario 2: Palindrome

	•	Input: “madam”
	•	Output: Base + char count + word multiplier (doubled) = 1.45 * 2 = 2.9 credits

Scenario 3: Long Text

	•	Input: 101 characters (“A” * 101)
	•	Output: Base + char count + length penalty = 1 + 5.05 + 5 = 11.05 credits

Design Decisions

	1.	Separation of Concerns:
	•	Each module has a distinct responsibility (e.g., credit_calculator.py for rule logic).
	2.	Extensibility:
	•	Easily add new credit rules or API endpoints.
	3.	Error Handling:
	•	Fallbacks ensure continued functionality even when external data is unavailable.
	4.	Testing:
	•	Comprehensive unit tests cover all critical components and edge cases.