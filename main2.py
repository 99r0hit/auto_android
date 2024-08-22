import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_company_details(company_name):
    search_url = f"https://www.google.com/search?q={company_name.replace(' ', '+')}+website+contact+email+procurement"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract website URL
    website = ""
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('/url?q=') and not 'webcache' in href:
            website = href.split('/url?q=')[1].split('&')[0]
            break

    procurement_email = ""
    phone = ""

    if website:
        try:
            contact_response = requests.get(website, headers=headers)
            contact_soup = BeautifulSoup(contact_response.text, 'html.parser')

            # Extract email and phone using regular expressions
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            phone_pattern = r'\+?\d[\d -]{8,}\d'

            emails = re.findall(email_pattern, contact_soup.text)
            phones = re.findall(phone_pattern, contact_soup.text)

            procurement_email = emails[0] if emails else ""
            phone = phones[0] if phones else ""
        except Exception as e:
            print(f"Error fetching details from {website}: {e}")

    return {
        "Company Name": company_name,
        "Website": website,
        "Procurement Email": procurement_email,
        "Phone": phone
    }

companies = [
    "TOYOTA KIRLOSKAR MOTOR PVT LTD",
    "HANON AUTOMOTIVE SYSTEMS INDIA PVT LTD",
    # Add more companies as needed
]

company_details = []

for company in companies:
    details = get_company_details(company)
    company_details.append(details)

# Create DataFrame
df = pd.DataFrame(company_details)

# Save to Excel
df.to_excel('C:\\Users\\rohit\\Desktop\\EE\\Piano p\\company_details4.xlsx', index=False)
