import asyncio
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup

from ..dependencies import get_request_service, get_setting_service
from ..persistance.abstract import IPersistanceOperation
from ..router.model.request import Request
from ..router.model.setting import Setting


async def process_records():
    """
    Background task to process unprocessed records every 5 minutes.
    This function uses the persistence layer for fetching and updating records.
    """
    request_service = get_request_service()
    setting_service = get_setting_service()
    while True:
        print(f"Processing records at {datetime.utcnow()}...")

        # Fetch unprocessed records using the persistence layer
        unprocessed_records: List[Request] = await request_service.get_all_unprocessed()

        print(f"Found {len(unprocessed_records)} records in unprocessed state")

        # Process each record
        for record in unprocessed_records:
            print(f"Processing record: {record.id}")
            setting_detail = await setting_service.get_setting(record.setting_id)
            if setting_detail:
                print(f"Processed record:")
                scrap_data(setting_detail, record)
            # Simulate processing the record, update its status
            # updated_record = await persistence.update(
            #     record.id, {"processed": True}
            # )
            # if updated_record:
            #print(f"Processed record:")

        # Wait for 5 minutes before running again
        await asyncio.sleep(30)

def scrap_data(setting: Setting, request: Request):
    paginated_url = setting.base_url
    limit = 1
    if setting.is_scrapping_paginated:
        if setting.is_page_query_parameter:
            paginated_url += "?page="
        else:
            paginated_url += "/page/"

        if request.override_page_limit > 0:
            limit = request.override_page_limit
        else:
            limit = setting.max_pages_limit    
    for page_number in range(limit):
        page_number = page_number + 1
        paginated_url += str(page_number)
        response = requests.get(paginated_url, proxies=setting.proxy, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        data = extract_data(soup)
        print(f"Found {len(data)} records")

    # Parse HTML
    # soup = BeautifulSoup(response.text, "html.parser")
    # data = extract_data(soup)
    #all_data.append(ScrapeResponse(page=page, data=data))


def extract_data(soup: BeautifulSoup) -> List[dict]:
    """
    Extract data from the BeautifulSoup object.
    Customize this method for different websites.
    """
    data = []
    for item in soup.select(".product-inner"):
        name = item.select_one(".woo-loop-product__title").text.strip() if item.select_one(".woo-loop-product__title") else "N/A"
        img_url = item.select_one(".mf-product-thumbnail img").get('data-lazy-src')
        original_price = item.select_one(".woocommerce-Price-amount bdi:nth-of-type(1)").text.strip()
        discounted_price = "" #item.select_one(".woocommerce-Price-amount bdi:nth-of-type(2)").text.strip()
        data.append({"name": name, "original_price": original_price, "discounted_price": discounted_price, "image": img_url})
    return data
