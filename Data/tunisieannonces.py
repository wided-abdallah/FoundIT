import pandas as pd
import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup

async def scrape_page(url):
    browser = await launch(executablePath="path\\to\\chrome.exe", headless=True)
    page = await browser.newPage()
    await page.goto(url)
    content = await page.content()
    await browser.close()
    return content

async def scrape_tunisie_annonces(base_url, total_pages, output_file):
    # Initialize lists to store data
    regions = []
    natures = []
    types = []
    texts = []
    prices = []
    modified_dates = []

    # Loop through each page
    for page_number in range(1, total_pages + 1):
        url = base_url.format(page_number)
        content = await scrape_page(url)
        soup = BeautifulSoup(content, 'html.parser')
        rows = soup.find_all('tr', class_='Tableau1')
        
        # Extract data from each row
        for row in rows:
            columns = row.find_all('td')
            regions.append(columns[1].get_text(strip=True))
            natures.append(columns[3].get_text(strip=True))
            types.append(columns[5].get_text(strip=True))
            texts.append(columns[7].get_text(strip=True))
            prices.append(columns[9].get_text(strip=True))
            modified_dates.append(columns[11].get_text(strip=True))

    # Create DataFrame
    data = {
        'Region': regions,
        'Nature': natures,
        'Type': types,
        'Text': texts,
        'Price': prices,
        'Modified Date': modified_dates
    }
    df = pd.DataFrame(data)

    # Save DataFrame to CSV
    df.to_csv(output_file, index=False)

def run_scraper():
    base_url = 'http://www.tunisie-annonce.com/AnnoncesImmobilier.asp?rech_cod_cat=1&rech_page_num={}'
    total_pages = 700
    output_file = 'tunisie-annonces.csv'
    asyncio.run(scrape_tunisie_annonces(base_url, total_pages, output_file))
