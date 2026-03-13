import json
import os
import time
import requests

API_URL = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
FACT_FILE = "facts.json"
FETCH_INTERVAL = 30  # fetch every 30 seconds


def load_facts():
    if not os.path.exists(FACT_FILE):
        return []

    try:
        with open(FACT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_facts(facts):
    with open(FACT_FILE, "w", encoding="utf-8") as f:
        json.dump(facts, f, indent=2, ensure_ascii=False)


def fetch_fact():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data.get("text")


def fact_exists(fact_text, facts):
    normalized_new_fact = fact_text.strip().lower()
    for fact in facts:
        existing_text = fact.get("text", "").strip().lower()
        if existing_text == normalized_new_fact:
            return True
    return False


def add_fact(fact_text, facts):
    if not fact_text:
        print("No fact returned from API.")
        return False

    if fact_exists(fact_text, facts):
        print("Duplicate fact found. Not adding to archive.")
        return False

    facts.append({"text": fact_text})
    save_facts(facts)
    print("New fact added to archive.")
    return True


def main():
    print("Starting automated fact collector...")
    print(f"Fetching a fact every {FETCH_INTERVAL} seconds.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            facts = load_facts()
            print(f"Currently stored facts: {len(facts)}")

            fact_text = fetch_fact()
            print("Fetched fact:")
            print(fact_text)

            if add_fact(fact_text, facts):
                print("Archive updated.\n")
            else:
                print("Archive unchanged.\n")

            time.sleep(FETCH_INTERVAL)

    except KeyboardInterrupt:
        print("\nAutomation stopped by user.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching fact: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
