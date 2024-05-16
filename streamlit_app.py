import streamlit as st

"""
## Web scraping on Streamlit Cloud with Selenium

[![Source](https://img.shields.io/badge/View-Source-<COLOR>.svg)](https://github.com/snehankekre/streamlit-selenium-chrome/)

This is a minimal, reproducible example of how to scrape the web with Selenium and Chrome on Streamlit's Community Cloud.

Fork this repo, and edit `/streamlit_app.py` to customize this app to your heart's desire. :heart:
"""

with st.echo():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.core.os_manager import ChromeType

    @st.cache_resource
    def get_driver():
        return webdriver.Chrome(
            service=Service(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            ),
            options=options,
        )

    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = get_driver()
    driver.get("https://www.iso-ne.com/isoexpress/web/charts/guest-hub?p_p_id=threedayforecastlist_WAR_isoneportlet_INSTANCE_942ZZ7qiGL8q&p_p_lifecycle=0&p_p_state=pop_up&p_p_mode=view&p_p_col_id=column-2&p_p_col_pos=5&p_p_col_count=6")

    # Wait for the table to load
    driver.implicitly_wait(2)

    # Find the table by its tag name
    table = driver.find_element_by_tag_name('table')
    
    if table:
        # Find all rows in the table
        rows = table.find_elements_by_tag_name('tr')
        table_data = []

        for row in rows:
            # Find all columns in each row
            cols = row.find_elements_by_tag_name('td')
            cols = [col.text.strip() for col in cols]
            table_data.append(cols)
        
        # Display the table data in Streamlit
        st.write("Table Data:")
        st.table(table_data)
    
    driver.quit()