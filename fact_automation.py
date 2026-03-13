import json
import os
import time
import requests

API_URL = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
FACT_FILE = "facts.json"
FETCH_INTERVAL = 30  # seconds


def load_facts():
    """Load facts from the JSON archive."""
    if not os.path.exists(FACT_FILE):
        return []

    try:
        with open(FACT_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_facts(facts):
    """Save facts to the JSON archive."""
    with open(FACT_FILE, "w", encoding="utf-8") as file:
        json.dump(facts, file, indent=2, ensure_ascii=False)


def fetch_fact():
    """Fetch one random fact from the API."""
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data.get("text")


def fact_exists(fact_text, facts):
    """Check whether the fact already exists in the archive."""
    normalized_fact = fact_text.strip().lower()
    for fact in facts:
        if fact.get("text", "").strip().lower() == normalized_fact:
            return True
    return False


def add_fact(fact_text, facts):
    """Add a unique fact to the archive."""
    if not fact_text:
        print("No fact returned from API.")
        return False

    if fact_exists(fact_text, facts):
        print("Duplicate fact detected. Not added.")
        return False

    facts.append({"text": fact_text})
    save_facts(facts)
    print("New fact added:")
    print(fact_text)
    return True


def run_fact_collector():
    """Continuously fetch and store unique facts."""
    print("Starting automated fact collector...")
    print(f"Fetching a new fact every {FETCH_INTERVAL} seconds.")
    print("Press Ctrl+C to stop.\n")

    while True:
        try:
            facts = load_facts()
            print(f"Currently stored facts: {len(facts)}")

            fact_text = fetch_fact()
            print("Fetched fact:")
            print(fact_text)

            added = add_fact(fact_text, facts)

            if added:
                print("Archive updated successfully.\n")
            else:
                print("Archive unchanged.\n")

        except requests.exceptions.RequestException as error:
            print(f"API error: {error}\n")
        except Exception as error:
            print(f"Unexpected error: {error}\n")

        time.sleep(FETCH_INTERVAL)


if __name__ == "__main__":
    run_fact_collector()
