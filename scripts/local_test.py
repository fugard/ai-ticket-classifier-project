import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "lambda" / "src"))

from ai_classifier import classify_ticket  # noqa: E402

sample_file = ROOT / "data" / "sample_tickets.json"
tickets = json.loads(sample_file.read_text())

for index, ticket in enumerate(tickets, start=1):
    result = classify_ticket(ticket["message"]).to_dict()
    print(f"\nTicket {index}")
    print("-" * 50)
    print("Message:", ticket["message"])
    print("Result:", json.dumps(result, indent=2))
