import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of companies for which you want procurement information
companies = [
    "TOYOTA KIRLOSKAR MOTOR PVT LTD",
    "HANON AUTOMOTIVE SYSTEMS INDIA PVT LTD",
    "TEXSPIN BEARINGS LTD",
    
    # Add more companies as needed
]

# Function to scrape contact, website, and email
def scrape_company_info(company_name):
    url = f"https://www.google.com/search?q={company_name}+procurement+contact"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Example: Scraping contact information from Google search results
        contact_info = soup.find('div', {'class': 'BNeawe s3v9rd AP7Wnd'}).text.strip()

        # Example: Extracting website and email from Google search results
        # Replace with specific parsing logic for each company's website
        website = "www.example.com"
        email = "info@example.com"

        return {
            "Company": company_name,
            "Contact": contact_info,
            "Website": website,
            "Email": email
        }

    except requests.exceptions.RequestException as e:
        print(f"Error scraping data for {company_name}: {e}")
        return None

# Scraping information for each company
company_info_list = []
for company in companies:
    company_info = scrape_company_info(company)
    if company_info:
        company_info_list.append(company_info)

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(company_info_list)

# Export to Excel
excel_file = "C:\\Users\\rohit\\Desktop\\EE\\Piano p\\company_information1.xlsx"
df.to_excel(excel_file, index=False)

print(f"Company information exported to {excel_file}")
