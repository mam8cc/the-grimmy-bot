from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from pprint import pprint
import csv

driver = webdriver.Firefox()

BASE_URL = "https://wiki.bloodontheclocktower.com"

links = []

for edition in ["Trouble_Brewing", "Sects_%26_Violets", "Bad_Moon_Rising"]:
    driver.get(f"{BASE_URL}/{edition}")
    table = driver.find_element(By.ID, "edition-details-characters")

    for link in table.find_elements(By.TAG_NAME, "a"):
        links.append(link.get_attribute("href"))

for special in ["Experimental", "Fabled", "Travellers"]:
    driver.get(f"{BASE_URL}/{special}")
    elements = driver.find_element(By.XPATH, "/html/body/div[1]/div/section/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div/div")
    link_elements = elements.find_elements(By.TAG_NAME, "a")

    # This sucks but it filters some links and dead space.
    link_elements = filter(lambda x: x.text and not x.text[0].isdigit(), link_elements)
    links = links + list(set([f'{BASE_URL}/{x.text}' for x in link_elements]))

with open('characters.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'rule', 'flavor', 'type', 'link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for link in links:
        print(f'Navigating to {link}')
        driver.get(link)
        character = driver.find_element(By.CLASS_NAME, "mw-page-title-main").text
        rule = driver.find_element(By.XPATH, "/html/body/div[1]/div/section/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div[1]/p[1]").text

        flavor = 'N/A'
        try:
            flavor = driver.find_element(By.CLASS_NAME, "flavour").text
        except NoSuchElementException:
            pass

        character_details = driver.find_element(By.ID, "character-details")
        character_type = character_details.find_element(By.XPATH, "/html/body/div[1]/div/section/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div/div[1]/div/table/tbody/tr[1]/td[2]/a").text

        writer.writerow({'name': character, 'rule': rule, 'flavor': flavor, 'type': character_type, 'link': link})

driver.close()