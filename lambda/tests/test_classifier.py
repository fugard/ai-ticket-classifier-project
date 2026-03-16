from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from ai_classifier import classify_ticket


def test_billing_ticket():
    result = classify_ticket("I was charged twice and need a refund")
    assert result.category == "Billing"
    assert result.priority == "High"


def test_account_access_ticket():
    result = classify_ticket("I cannot log in and password reset is not working")
    assert result.category == "Account Access"
    assert result.team == "Security"


def test_feature_request_ticket():
    result = classify_ticket("Please add dark mode and dashboard export templates")
    assert result.category == "Feature Request"
    assert result.priority == "Low"
