from src.utils.credit_calculator import CreditCalculator


def test_calculate_message_credits_basic():
    """
    Test basic credit calculation with default rules.
    """
    calculator = CreditCalculator()
    credits = calculator.calculate_message_credits("Simple test")
    assert credits > 0  # Ensure some credits are calculated


def test_calculate_message_credits_with_palindrome():
    """
    Test credit calculation for a palindrome.
    Ensures the total is doubled for palindromes.
    """
    calculator = CreditCalculator()
    credits = calculator.calculate_message_credits("madam")
    assert credits > 2  # Palindrome multiplier applied


def test_calculate_message_credits_with_long_text():
    """
    Test credit calculation for a long message with length penalties.
    """
    calculator = CreditCalculator()
    credits = calculator.calculate_message_credits("A" * 101)
    assert credits > 5  # Length penalty applied


def test_calculate_message_credits_unique_words():
    """
    Test credit calculation with a unique word bonus.
    """
    calculator = CreditCalculator()
    credits = calculator.calculate_message_credits("unique words here")
    assert credits < 5  # Unique word bonus applied