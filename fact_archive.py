import json
import os
import requests
import hashlib

API_URL = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
FACTS_FILE = "facts.json"


def load_facts():
    """Load facts from the local JSON archive."""
    if not os.path.exists(FACTS_FILE):
        return []

    try:
        with open(FACTS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []


def save_facts(facts):
    """Save the full list of facts to the local JSON archive."""
    with open(FACTS_FILE, "w", encoding="utf-8") as file:
        json.dump(facts, file, indent=2, ensure_ascii=False)


def fetch_fact():
    """Fetch one random fact from the API."""
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data.get("text")


def generate_fact_id(fact_text):
    """Generate a stable short ID from the fact text."""
    return hashlib.md5(fact_text.encode("utf-8")).hexdigest()[:8]


def fact_exists(fact_text, facts):
    """Check whether a fact already exists in the archive."""
    normalized_new_fact = fact_text.strip().lower()
    for fact in facts:
        existing_text = fact.get("text", "").strip().lower()
        if existing_text == normalized_new_fact:
            return True
    return False


def add_fact(fact_text, facts):
    """Add a new fact only if it does not already exist."""
    if fact_exists(fact_text, facts):
        print("Duplicate fact found. Not adding to archive.")
        return False

    new_fact = {
        "id": generate_fact_id(fact_text),
        "text": fact_text
    }
    facts.append(new_fact)
    save_facts(facts)
    print("New fact added to archive:")
    print(fact_text)
    return True


def main():
    try:
        facts = load_facts()
        print(f"Loaded {len(facts)} fact(s) from archive.")

        fact_text = fetch_fact()
        if not fact_text:
            print("No fact returned from API.")
            return

        print("\nFetched fact:")
        print(fact_text)
        print()

        add_fact(fact_text, facts)

    except requests.exceptions.RequestException as error:
        print(f"Error fetching fact from API: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
