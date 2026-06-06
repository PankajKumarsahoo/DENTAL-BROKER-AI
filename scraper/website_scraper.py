import json
import time
from collections import deque
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = "https://dentalbrokerflorida.com/"

MAX_PAGES = 100


driver = webdriver.Chrome(
    service=Service(
        ChromeDriverManager().install()
    )
)

visited = set()
queue = deque([BASE_URL])

pages = []

while queue and len(visited) < MAX_PAGES:

    url = queue.popleft()

    if url in visited:
        continue

    try:

        print(f"Scraping: {url}")

        driver.get(url)

        time.sleep(3)

        soup = BeautifulSoup(
            driver.page_source,
            "html.parser"
        )

        visited.add(url)

        title = ""

        if soup.title:
            title = soup.title.get_text(strip=True)

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        pages.append({
            "url": url,
            "title": title,
            "content": text
        })

        for a in soup.find_all("a", href=True):

            link = urljoin(url, a["href"])

            parsed = urlparse(link)

            if (
                parsed.netloc ==
                urlparse(BASE_URL).netloc
            ):

                clean_link = (
                    parsed.scheme +
                    "://" +
                    parsed.netloc +
                    parsed.path
                )

                if clean_link not in visited:
                    queue.append(clean_link)

    except Exception as e:

        print("Error:", url)
        print(e)

driver.quit()

with open(
    "data/website_pages.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        pages,
        f,
        indent=4,
        ensure_ascii=False
    )

print(f"Saved {len(pages)} pages")
