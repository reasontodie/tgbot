import requests
import asyncio

from datetime import datetime as dt
from concurrent.futures import ThreadPoolExecutor

from source import Database


class Parser:
    def __init__(self, database: Database):
        self.db = database

    @staticmethod
    async def async_request(method, url, **kwargs) -> requests.Response:
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            response = await loop.run_in_executor(
                pool,
                lambda: requests.request(method, url, **kwargs)
            )
            return response

    async def get_published_vacancies_list(self, keyword: str) -> int:
        url = "https://dracula.robota.ua/"
        querystring = {"q": "getPublishedVacanciesList"}
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "user-agent": "Mustage"
        }
        payload = {
            "operationName": "getPublishedVacanciesList",
            "variables": {
                "pagination": {
                    "count": 40,
                    "page": 0
                },
                "filter": {
                    "keywords": keyword,
                    "clusterKeywords": [],
                    "salary": 0,
                    "districtIds": [],
                    "scheduleIds": [],
                    "rubrics": [],
                    "metroBranches": [],
                    "showAgencies": True,
                    "showOnlyNoCvApplyVacancies": False,
                    "showOnlySpecialNeeds": False,
                    "showOnlyWithoutExperience": False,
                    "showOnlyNotViewed": False,
                    "showWithoutSalary": True,
                    "showMilitary": True
                },
                "sort": "BY_VIEWED",
                "isBrowser": True
            },
            "query": "query getPublishedVacanciesList($filter: PublishedVacanciesFilterInput!, $pagination: PublishedVacanciesPaginationInput!, $sort: PublishedVacanciesSortType!, $isBrowser: Boolean!) {\n  publishedVacancies(filter: $filter, pagination: $pagination, sort: $sort) {\n    totalCount\n    items {\n      ...PublishedVacanciesItem\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment PublishedVacanciesItem on Vacancy {\n  id\n  schedules {\n    id\n    __typename\n  }\n  title\n  description\n  sortDateText\n  hot\n  designBannerUrl\n  isPublicationInAllCities\n  badges {\n    name\n    __typename\n  }\n  salary {\n    amount\n    comment\n    amountFrom\n    amountTo\n    __typename\n  }\n  company {\n    id\n    logoUrl\n    name\n    honors {\n      badge {\n        iconUrl\n        tooltipDescription\n        locations\n        isFavorite\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  city {\n    id\n    name\n    __typename\n  }\n  showProfile\n  seekerFavorite @include(if: $isBrowser) {\n    isFavorite\n    __typename\n  }\n  seekerDisliked @include(if: $isBrowser) {\n    isDisliked\n    __typename\n  }\n  formApplyCustomUrl\n  anonymous\n  isActive\n  publicationType\n  __typename\n}\n"
        }
        response = await self.async_request(method='POST', url=url, headers=headers, params=querystring, json=payload)
        if response.status_code == 200:
            response_dict = response.json()
            if response_dict['data'] and response_dict['data']['publishedVacancies']:
                return response_dict['data']['publishedVacancies']['totalCount']

    async def parse_and_save(self, keyword: str, datetime: dt) -> None:
        total_count = await self.get_published_vacancies_list(keyword)
        if total_count is not None:
            self.db.insert_data_to_db(total_count, datetime)
        else:
            await self.parse_and_save(keyword, datetime)
