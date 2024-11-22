import asyncio
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup

from ..dependencies import (get_request_service, get_scrap_service,
                            get_setting_service)
from ..persistance.abstract import IPersistanceOperation
from ..router.model.request import Request, ScrapMetaInformation, Status
from ..router.model.scrap import ScrapCreate
from ..router.model.setting import Setting


async def process_records():
    """
    Background task to process unprocessed records every 5 minutes.
    This function uses the persistence layer for fetching and updating records.
    """
    request_service = get_request_service()
    setting_service = get_setting_service()
    scrap_service = get_scrap_service()
    while True:
        print(f"Processing requests at {datetime.utcnow()}...")

        unprocessed_records: List[Request] = await request_service.get_all_unprocessed()

        print(f"Found {len(unprocessed_records)} requests in unprocessed state")

        for record in unprocessed_records:
            print(f"Processing request: {record.id}")
            setting_detail = await setting_service.get_setting(record.setting_id)
            if setting_detail:
                records = scrap_data(setting_detail, record)
                if records and len(records) > 0:
                    print(f'Total records: {len(records)}')
                    scrap_records: List[ScrapCreate] = [
                        ScrapCreate(request_id=record.id, data=scrap_record)
                        for scrap_record in records
                    ]

                    await scrap_service.create_scrap(record.id, scrap_records)

            record.status = Status.PROCESSED
            await request_service.update_request(record.id, record)
            print(f"Processed request: {record.id}")

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
    data_records = []    
    for page_number in range(limit):
        page_number = page_number + 1
        paginated_url += str(page_number)
        response = requests.get(paginated_url, proxies=setting.proxy, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        data = extract_data(soup, request.meta)
        print(f"Found {len(data)} records")
        data_records.extend(data)

    return data_records


def extract_data(
    soup: BeautifulSoup, scrap_meta_information: ScrapMetaInformation
) -> List[dict]:
    """
    Extract data based on the root selector and conditional logic for single or multiple items.
    """
    data = []

    if scrap_meta_information.is_multiple_items:
        items = soup.select(scrap_meta_information.root_selector)
    else:
        items = [soup]

    for item in items:
        extracted_item = {}
        for field_mapping in scrap_meta_information.field_mappings:
            element = item.select_one(field_mapping.mapped_to)

            if element:
                extracted_item[field_mapping.field_name] = element.text.strip()
                if field_mapping.requires_fetch:
                    print('Further download and save file')
                    #extracted_item[field_mapping.field_name] = element.text.strip()
            else:
                extracted_item[field_mapping.field_name] = "N/A"

        data.append(extracted_item)

    return data
