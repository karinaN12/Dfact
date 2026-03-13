import requests

API_URL = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"

def fetch_random_fact():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    return response.json()

def main():
    try:
        fact_data = fetch_random_fact()
        print("Here is a random fact:")
        print(fact_data["text"])
    except requests.exceptions.RequestException as error:
        print("Failed to fetch fact from API.")
        print(error)
    except KeyError:
        print("The API response did not contain the expected fact text.")

if __name__ == "__main__":
    main()
