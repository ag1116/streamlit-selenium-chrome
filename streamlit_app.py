import streamlit as st
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd

async def scrape(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        # Wait for the table to be rendered
        await page.wait_for_selector('#_threedayforecastlist_WAR_isoneportlet_INSTANCE_942ZZ7qiGL8q_table tbody tr')

        # Wait until there are at least 3 rows
        await page.wait_for_function(
            "document.querySelector('#_threedayforecastlist_WAR_isoneportlet_INSTANCE_942ZZ7qiGL8q_table tbody').children.length > 3"
        )

        content = await page.content()
        await browser.close()
        return content

def extract_table(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': '_threedayforecastlist_WAR_isoneportlet_INSTANCE_942ZZ7qiGL8q_table'})
    
    if table is None:
        st.error("Table not found in the HTML content.")
        return pd.DataFrame()
    
    # Extract table rows
    rows = []
    for tr in table.find('tbody').find_all('tr'):
        cells = [td.text.strip() for td in tr.find_all('td')]
        rows.append(cells)
    
    if not rows:
        st.error("No rows found in the table.")
        return pd.DataFrame()

    # Create a DataFrame without headers
    df = pd.DataFrame(rows)
    return df

def run_scrape(url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    html = loop.run_until_complete(scrape(url))
    return extract_table(html)

def main():
    st.title("Dynamic Web Scraping with Playwright and Streamlit")
    
    url = "https://www.iso-ne.com/isoexpress/web/charts/guest-hub?p_p_id=threedayforecastlist_WAR_isoneportlet_INSTANCE_942ZZ7qiGL8q&p_p_lifecycle=0&p_p_state=pop_up&p_p_mode=view&p_p_col_id=column-2&p_p_col_pos=5&p_p_col_count=6"
    if st.button("Scrape Data Table"):
        with st.spinner("Scraping the website..."):
            data_table = run_scrape(url)
            if not data_table.empty:
                st.write("Scraped Data Table:")
                st.dataframe(data_table)
            else:
                st.write("No data found in the table.")

if __name__ == "__main__":
    main()
