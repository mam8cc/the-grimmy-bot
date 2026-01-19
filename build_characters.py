"""
Scrapes character data from the Blood on the Clocktower wiki using the MediaWiki API.
Outputs a CSV file with character names, rules, flavor text, types, and links.
"""

import csv
import time
from typing import TypedDict

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://wiki.bloodontheclocktower.com"
API_URL = f"{BASE_URL}/api.php"

# Rate limiting: seconds between requests
REQUEST_DELAY = 0.25


class Character(TypedDict):
    name: str
    rule: str
    flavor: str
    type: str
    link: str


def get_characters_in_category(category: str) -> list[str]:
    """Fetch all character page titles from a wiki category."""
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmlimit": "500",
        "format": "json",
    }

    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    return [
        member["title"] for member in data.get("query", {}).get("categorymembers", [])
    ]


def get_page_html(title: str) -> str:
    """Fetch parsed HTML content for a wiki page."""
    params = {
        "action": "parse",
        "page": title,
        "format": "json",
        "prop": "text",
    }

    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    return data.get("parse", {}).get("text", {}).get("*", "")


def extract_character_data(title: str, html: str) -> Character:
    """Extract character information from parsed HTML."""
    soup = BeautifulSoup(html, "html.parser")

    # Extract rule text - first paragraph in the summary section
    rule = "N/A"
    summary_div = soup.find("div", class_="summary")
    if summary_div:
        first_p = summary_div.find("p")
        if first_p:
            rule = first_p.get_text(strip=True)

    # Fallback: try finding the first substantial paragraph
    if rule == "N/A":
        for p in soup.find_all("p"):
            text = p.get_text(strip=True)
            if text and len(text) > 20 and not text.startswith("Category"):
                rule = text
                break

    # Extract flavor text
    flavor = "N/A"
    flavor_div = soup.find("div", class_="flavour")
    if flavor_div:
        flavor = flavor_div.get_text(strip=True)

    # Extract character type from the character details table
    char_type = "Unknown"
    details_div = soup.find("div", id="character-details")
    if details_div:
        # Look for the type link in the table
        type_link = details_div.find("a", href=lambda x: x and "Character_Types" in x)
        if type_link:
            char_type = type_link.get_text(strip=True)

    # Fallback: check for type in any table cell with a link
    if char_type == "Unknown":
        for td in soup.find_all("td"):
            link = td.find("a", href=lambda x: x and "Character_Types" in x)
            if link:
                char_type = link.get_text(strip=True)
                break

    # Fallback: check for type as plain text in table rows (e.g., Loric characters)
    if char_type == "Unknown":
        for tr in soup.find_all("tr"):
            cells = tr.find_all("td")
            if len(cells) >= 2:
                label = cells[0].get_text(strip=True).lower()
                if label == "type":
                    char_type = cells[1].get_text(strip=True)
                    break

    # Build the character link
    link = f"{BASE_URL}/{title.replace(' ', '_')}"

    return Character(
        name=title,
        rule=rule,
        flavor=flavor,
        type=char_type,
        link=link,
    )


def main() -> None:
    # All character type categories to scrape
    categories = [
        "Townsfolk",
        "Outsiders",
        "Minions",
        "Demons",
        "Travellers",
        "Fabled",
        "Loric",
    ]

    # Collect all unique character titles
    all_titles: set[str] = set()

    print("Fetching character lists from categories...")
    for category in categories:
        print(f"  - {category}")
        titles = get_characters_in_category(category)
        all_titles.update(titles)
        time.sleep(REQUEST_DELAY)

    print(f"\nFound {len(all_titles)} unique characters")

    # Fetch and parse each character page
    characters: list[Character] = []
    total = len(all_titles)

    for i, title in enumerate(sorted(all_titles), 1):
        print(f"[{i}/{total}] Fetching: {title}")
        try:
            html = get_page_html(title)
            character = extract_character_data(title, html)
            characters.append(character)
        except requests.RequestException as e:
            print(f"  Error fetching {title}: {e}")
        except Exception as e:
            print(f"  Error parsing {title}: {e}")

        time.sleep(REQUEST_DELAY)

    # Write to CSV
    output_file = "characters.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["name", "rule", "flavor", "type", "link"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(characters)

    print(f"\nWrote {len(characters)} characters to {output_file}")


if __name__ == "__main__":
    main()
