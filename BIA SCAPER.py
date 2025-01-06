import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.toronto.ca/business-economy/business-operation-growth/business-improvement-areas/bia-list/bia-list-a-e/"
output_path = "C:/Users/elvin/Documents/BIA_scrape.csv"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

bia_names = []
locations = []
phone_numbers = []
emails = []

# Find all the main accordion sections
accordion_sections = soup.find_all('div', id=lambda x: x and x.startswith('accordion-'))

for section in accordion_sections:
    # Extract BIA Name from the preceding sibling <div>
    bia_name_element = section.find_previous_sibling('div', attrs={'data-type': 'toggle'})
    if bia_name_element:
        bia_name = bia_name_element.text.strip()
        bia_names.append(bia_name)
    else:
        bia_names.append("NA")

    location_element = section.find('p')
    if location_element:
        location = location_element.text.strip()
        locations.append(location)
    else:
        locations.append("NA")

    contact_heading = section.find('h3', string='BIA Contact')

    if contact_heading:
        contact_paragraph = contact_heading.find_next_sibling('p')
        if contact_paragraph:
            phone_element = contact_paragraph.contents[0] # Get first element, which is usually the phone number
            if isinstance(phone_element, str): #Check if it's a string
                phone_number = phone_element.strip()
            else:
                phone_number="NA"
            phone_numbers.append(phone_number)
            email_element = contact_paragraph.find('a', href=lambda href: href and "mailto:" in href)
            if email_element:
                email = email_element['href'].replace('mailto:', '')
                emails.append(email)
            else:
                emails.append("NA")
        else:
            phone_numbers.append("NA")
            emails.append("NA")
    else:
        phone_numbers.append("NA")
        emails.append("NA")

with open(output_path, "w", newline="", encoding="utf-8") as csvfile:  # Added encoding
    writer = csv.writer(csvfile)
    writer.writerow(["BIA Name", "Location", "Phone Number", "Email"])
    for i in range(len(bia_names)):
        writer.writerow([bia_names[i], locations[i], phone_numbers[i], emails[i]])

print("Data scraped successfully! Check C:/Users/elvin/Documents/BIA_scrape.csv")
