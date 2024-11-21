from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, HttpUrl

app = FastAPI()


# Request Model
class ScrapeRequest(BaseModel):
    url: HttpUrl
    max_pages: Optional[int] = Query(1, ge=1, description="Maximum number of pages to scrape")
    proxy: Optional[str] = Query(None, description="Proxy in the format http://user:password@proxyserver:port")


# Response Model
class ScrapeResponse(BaseModel):
    page: int
    data: List[dict]


@app.post("/scrape", response_model=List[ScrapeResponse])
async def scrape_website(request: ScrapeRequest):
    """
    Scrape the given website with optional proxy settings and pagination.
    """
    url = request.url
    max_pages = request.max_pages
    proxy = {"http": request.proxy, "https": request.proxy} if request.proxy else None
    all_data = []

    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}...")
        try:
            # Construct URL with pagination (assumes ?page= pattern)
            paginated_url = f"{url}/page/{page}"
            response = requests.get(paginated_url, proxies=proxy, timeout=10)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.text, "html.parser")
            data = extract_data(soup)
            all_data.append(ScrapeResponse(page=page, data=data))

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error scraping page {page}: {e}")

    return all_data


def extract_data(soup: BeautifulSoup) -> List[dict]:
    """
    Extract data from the BeautifulSoup object.
    Customize this method for different websites.
    """
    data = []
    for item in soup.select(".mf-product-details"):  # Adjust selector as needed
        name = item.select_one(".woo-loop-product__title").text.strip() if item.select_one(".woo-loop-product__title") else "N/A"
        prices = item.select(".woocommerce-Price-amount bdi")
        #img_url = item.select_one(".mf-product-thumbnail img").get('src')
        if len(prices) == 2:
            original_price = prices[0].text.strip()
            discounted_price = prices[1].text.strip()
        data.append({"name": name, "original_price": original_price, "discounted_price": discounted_price, "img_url": img_url})
    return data
