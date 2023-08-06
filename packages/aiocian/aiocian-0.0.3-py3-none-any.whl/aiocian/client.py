from __future__ import annotations
import asyncio
import datetime
import json
from time import sleep
from typing import Optional, Sequence

import aiohttp
from bs4 import BeautifulSoup
import requests

from .constants import (AREND_DAILY, AREND_MONTHLY, BED, BUILDING, BUSINESS, BUY, CAR_SERVICE,
                        COMMERCIAL_LAND, CURRENCIES, DOMESTIC_SERVICES, FLAT, FREE_SPACE, GARAGE,
                        HOMESTEAD, HOUSE, HOUSE_PART, MANUFACTURE, OFFICE, PART, PLACES,
                        PUBLIC_CATERING, REGIONS, ROOM, ROOMS, SPB, STOCK, TOWNHOUSE, TRADE_AREA,
                        USED)
from .exceptions import IncorrectPlaces


class Result:
    def __init__(self, id: int, user_id: int, url: str, deal: str, premium: bool, description: str,
                 added: datetime.datetime, address: str, latitude: float, longitude: float,
                 total_area: float, price: float):
        self.id = id
        self.user_id = user_id
        self.url = url
        self.deal = deal
        self.premium = premium
        self.description = description
        self.added = added
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.total_area = total_area
        self.price = price

    @classmethod
    def parse(cls, data: dict) -> Result:
        deal = None
        if data["dealType"] == "sale":
            deal = BUY

        return cls(
            id=data["id"],
            user_id=data["userId"],
            url=data["fullUrl"],
            deal=deal,
            premium=data["isPremium"],
            description=data["description"],
            added=datetime.datetime.utcfromtimestamp(data["addedTimestamp"]),
            address=None,
            latitude=data["geo"]["coordinates"]["lat"],
            longitude=data["geo"]["coordinates"]["lng"],
            total_area=float(data["totalArea"]),
            price=data["bargainTerms"]["price"],
        )

    def json(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, data: dict) -> Result:
        return cls(**json.loads(data))


class Search:
    API_HOST = "https://api.cian.ru"
    SEARCH_URL = "/search-offers/v2/search-offers-desktop/"

    def __init__(self, client: CianClient, region: str, action: str, places: Sequence[str],
                 offer_owner: Optional[str]=None, rooms: Sequence[str]=(),
                 min_bedrooms: Optional[int]=None, max_bedrooms: Optional[int]=None,
                 building_status: Optional[str]=None, min_price: Optional[float]=None,
                 max_price: Optional[float]=None, currency: Optional[str]=None,
                 square_meter_price: bool=False, min_square: Optional[float]=None,
                 max_square: Optional[float]=None, by_homeowner: bool=False, start_page: int=1,
                 end_page: Optional[int]=None, limit: Optional[int]=None, delay: Optional[float]=0):
        self.client = client
        self.region = region
        self.action = action
        self.places = places
        self.offer_owner = offer_owner
        self.rooms = rooms
        self.min_bedrooms = min_bedrooms
        self.max_bedrooms = max_bedrooms
        self.building_status = building_status
        self.min_price = min_price
        self.max_price = max_price
        self.currency = currency
        self.square_meter_price = square_meter_price
        self.min_square = min_square
        self.max_square = max_square
        self.by_homeowner = by_homeowner
        self.start_page = start_page
        self.end_page = end_page
        self.limit = limit
        self.delay = delay
        self._count = 0
        self._page = start_page - 1
        self._results_count = 0 
        self._cache_results = []

    def __len__(self) -> int:
        return self._count

    def __iter__(self) -> Search:
        return self

    def __aiter__(self) -> Search:
        return self

    def __next__(self) -> Result:
        if self.limit is not None and self.limit < self._results_count:
            raise StopIteration
        self._results_count += 1

        if self._cache_results:
            return self._cache_results.pop(0)
        sleep(self.delay)

        self._page += 1
        if self.end_page is not None and self._page == self.end_page:
            raise StopIteration

        request_data = {
            "url": self.API_HOST + self.SEARCH_URL,
            "json": {"jsonQuery": self._search_data()},
        }
        response = self.client.session.post(**request_data)
        data = response.json()

        self._count = data["offerCount"]
        self._cache_results = [Result.parse(x) for x in data["offersSerialized"]]

        if not self._cache_results:
            raise StopIteration
        return self._cache_results.pop(0)

    async def __anext__(self) -> Result:
        if self.limit is not None and self.limit < self._results_count:
            raise StopAsyncIteration
        self._results_count += 1

        if self._cache_results:
            return self._cache_results.pop(0)
        await asyncio.sleep(self.delay)

        self._page += 1
        if self.end_page is not None and self._page == self.end_page:
            raise StopAsyncIteration

        request_data = {
            "url": self.API_HOST + self.SEARCH_URL,
            "json": {"jsonQuery": self._search_data()},
        }
        async with self.client.asession.post(**request_data) as response:
            data = (await response.json())["data"]

        self._count = data["offerCount"]
        self._cache_results = [Result.parse(x) for x in data["offersSerialized"]]

        if not self._cache_results:
            raise StopAsyncIteration
        return self._cache_results.pop(0)

    def json(self) -> str:
        return json.dumps({
            "region": self.region,
            "action": self.action,
            "places": self.places,
            "offer_owner": self.offer_owner,
            "rooms": self.rooms,
            "min_bedrooms": self.min_bedrooms,
            "max_bedrooms": self.max_bedrooms,
            "building_status": self.building_status,
            "min_price": self.min_price,
            "max_price": self.max_price,
            "currency": self.currency,
            "square_meter_price": self.square_meter_price,
            "min_square": self.min_square,
            "max_square": self.max_square,
            "by_homeowner": self.by_homeowner,
            "start_page": self.start_page,
            "end_page": self.end_page,
            "limit": self.limit,
            "delay": self.delay,
            "count": self._count,
            "page": self._page,
            "results_count": self._results_count,
            "cache_results": [result.json() for result in self._cache_results],
        })

    @classmethod
    def from_json(cls, data: str, client: CianClient) -> Search:
        data = json.loads(data)
        search = cls(
            client=client,
            region=data["region"],
            action=data["action"],
            places=data["places"],
            offer_owner=data["offer_owner"],
            rooms=data["rooms"],
            min_bedrooms=data["min_bedrooms"],
            max_bedrooms=data["max_bedrooms"],
            building_status=data["building_status"],
            min_price=data["min_price"],
            max_price=data["max_price"],
            currency=data["currency"],
            square_meter_price=data["square_meter_price"],
            min_square=data["min_square"],
            max_square=data["max_square"],
            by_homeowner=data["by_homeowner"],
            start_page=data["start_page"],
            end_page=data["end_page"],
            limit=data["limit"],
            delay=data["delay"],
        )
        search._count = data["count"]
        search._page = data["page"]
        search._results_count = data["results_count"],
        search._cache_results = [Result.from_json()]

    def _search_data(self) -> dict:
        places_set = set(self.places)
        
        data = {
            "region": {"type": "terms", "value": [REGIONS[self.region]]},
            "engine_version": {"type": "term", "value": 2},
        }

        if self.action == BUY and places_set <= {FLAT}:
            data["_type"] = "flatsale"
            if self.building_status is not None:
                data["building_status"] = {"type": "terms", "value": USED[self.building_status]}
            if self.square_meter_price:
                data["price_sm"] = {"type": "term", "value": True}
            if self.by_homeowner:
                data["is_by_homeowner"] = {"type": "term", "value": True}
            # IT IS NOT ALL
        elif self.action == BUY and places_set <= {ROOM, PART}:
            data["_type"] = "flatsale"
            data["room"] = {"type": "terms", "value": []}
            while places_set:
                data["room"]["value"].append(PLACES[places_set.pop()])
            if self.square_meter_price:
                data["price_sm"] = {"type": "term", "value": True}
            if self.by_homeowner:
                data["is_by_homeowner"] = {"type": "term", "value": True}
            # IT IS NOT ALL
        elif self.action == BUY and places_set <= {HOUSE, HOUSE_PART, HOMESTEAD, TOWNHOUSE}:
            data["_type"] = "suburbansale"
            data["object_type"] = {"type": "terms", "value": []}
            while places_set:
                data["object_type"]["value"].append(PLACES[places_set.pop()])
            if self.offer_owner is not None:
                data["suburban_offer_filter"] = {"type": "term", "value": self.offer_owner}
            if self.min_square is not None and self.max_square is not None:
                data["total_area"] = {"type": "range", "value": {}}
            if self.min_square is not None:
                data["total_area"]["value"]["gte"] = self.min_square
            if self.max_square is not None:
                data["total_area"]["value"]["lte"] = self.max_square
            if self.by_homeowner:
                data["is_by_homeowner"] = {"type": "term", "value": True}
            # IT IS NOT ALL
        elif self.action == BUY and places_set <= {OFFICE, TRADE_AREA, STOCK, PUBLIC_CATERING,
                                                   FREE_SPACE, GARAGE, MANUFACTURE, CAR_SERVICE,
                                                   BUSINESS, BUILDING, DOMESTIC_SERVICES}:
            data["_type"] = "commercialsale"
            data["office_type"] = {"type": "terms", "value": []}
            while places_set:
                data["office_type"]["value"].append(PLACES[places_set.pop()])
            if self.currency is not None:
                data["currency"] = {"type": "term", "value": CURRENCIES[self.currency]}
            if self.square_meter_price:
                data["price_sm"] = {"type": "term", "value": True}
            if self.min_square is not None and self.max_square is not None:
                data["total_area"] = {"type": "range", "value": {}}
            if self.min_square is not None:
                data["total_area"]["value"]["gte"] = self.min_square
            if self.max_square is not None:
                data["total_area"]["value"]["lte"] = self.max_square
            if self.by_homeowner:
                data["from_offrep"] = {"type": "term", "value": True}
            # IT IS NOT ALL
        elif self.action == BUY and places_set <= {COMMERCIAL_LAND}:
            data["_type"] = "commercialsale"
            data["category"] = {"type": "terms", "value": ["commercialLandSale"]}
            if self.currency is not None:
                data["currency"] = {"type": "term", "value": CURRENCIES[self.currency]}
            if self.square_meter_price:
                data["price_sm"] = {"type": "term", "value": True}
            if self.min_square is not None:
                data["site"]["value"]["gte"] = self.min_square
            if self.max_square is not None:
                data["site"]["value"]["lte"] = self.max_square
            # IT IS NOT ALL
        elif self.action == AREND_MONTHLY and places_set <= {FLAT}:
            data["_type"] = "flatrent"
            if self.by_homeowner:
                data["is_by_homeowner"] = {"type": "term", "value": True}
            # IT IS NOT ALL
        elif self.action == AREND_MONTHLY and places_set <= {ROOM, BED}:
            data["_type"] = "flatrent"
            data["room"] = {"type": "terms", "value": []}
            while places_set:
                data["room"]["value"].append(PLACES[places_set.pop()])
            if self.min_price is not None or self.max_price is not None:
                data["price"] = {"type": "range", "value": {}}
            if self.min_price is not None:
                data["price"]["value"]["gte"] = self.min_price
            if self.max_price is not None:
                data["price"]["value"]["lte"] = self.max_price
            if self.by_homeowner:
                data["is_by_homeowner"] = {"type": "term", "value": True}
            # IT IS NOT ALL
        elif self.action == AREND_MONTHLY and places_set <= {HOUSE, HOUSE_PART, TOWNHOUSE}:
            data["_type"] = "suburbanrent"
            data["object_type"] = {"type": "terms", "value": []}
            while places_set:
                data["object_type"]["value"].append(PLACES[places_set.pop()])
            if self.min_square is not None and self.max_square is not None:
                data["total_area"] = {"type": "range", "value": {}}
            if self.min_square is not None:
                data["total_area"]["value"]["gte"] = self.min_square
            if self.max_square is not None:
                data["total_area"]["value"]["lte"] = self.max_square
            if self.by_homeowner:
                data["is_by_homeowner"] = {"type": "term", "value": True}
            # IT IS NOT ALL
        elif self.action == AREND_MONTHLY and places_set <= {OFFICE, TRADE_AREA, STOCK,
                                                             PUBLIC_CATERING, FREE_SPACE, GARAGE,
                                                             MANUFACTURE, CAR_SERVICE, BUSINESS,
                                                             BUILDING, DOMESTIC_SERVICES}:
            data["_type"] = "commercialrent"
            data["office_type"] = {"type": "terms", "value": []}
            while places_set:
                data["office_type"]["value"].append(PLACES[places_set.pop()])
            if self.currency is not None:
                data["currency"] = {"type": "term", "value": CURRENCIES[self.currency]}
            if self.square_meter_price:
                data["price_sm"] = {"type": "term", "value": True}
            if self.min_square is not None and self.max_square is not None:
                data["total_area"] = {"type": "range", "value": {}}
            if self.min_square is not None:
                data["total_area"]["value"]["gte"] = self.min_square
            if self.max_square is not None:
                data["total_area"]["value"]["lte"] = self.max_square
            if self.by_homeowner:
                data["from_offrep"] = {"type": "term", "value": True}
        elif self.action == AREND_MONTHLY and places_set <= {COMMERCIAL_LAND}:
            data["_type"] = "commercialrent"
            data["category"] = {"type": "terms", "value": ["commercialLandSale"]}
            if self.currency is not None:
                data["currency"] = {"type": "term", "value": CURRENCIES[self.currency]}
            if self.square_meter_price:
                data["price_sm"] = {"type": "term", "value": True}
            if self.min_square is not None:
                data["site"]["value"]["gte"] = self.min_square
            if self.max_square is not None:
                data["site"]["value"]["lte"] = self.max_square
            # IT IS NOT ALL
        elif self.action == AREND_DAILY and places_set <= {FLAT}:
            data["_type"] = "flatrent"
            if self.rooms:
                data["room"] = {"type": "terms", "value": [ROOMS[room] for room in self.rooms]}
            if self.by_homeowner:
                data["is_by_homeowner"] = {"type": "term", "value": True}
            # IT IS NOT ALL
        elif self.action == AREND_DAILY and places_set <= {ROOM, BED}:
            data["_type"] = "flatrent"
            while places_set:
                data["room"]["value"].append(PLACES[places_set.pop()])
            if self.by_homeowner:
                data["is_by_homeowner"] = {"type": "term", "value": True}
            # IT IS NOT ALL
        elif self.action == AREND_DAILY and places_set <= {HOUSE}:
            data["_type"] = "suburbanrent"
            data["object_type"] = {"type": "terms", "value": PLACES[HOUSE]}
            if self.min_bedrooms is not None and self.max_bedrooms is not None:
                data["bedroom_total"] = {"type": "range", "value": {}}
            if self.min_bedrooms is not None:
                data["bedroom_total"]["value"]["gte"] = self.min_bedrooms
            if self.max_bedrooms is not None:
                data["bedroom_total"]["value"]["lte"] = self.max_bedrooms
            if self.min_square is not None and self.max_square is not None:
                data["total_area"] = {"type": "range", "value": {}}
            if self.min_square is not None:
                data["total_area"]["value"]["gte"] = self.min_square
            if self.max_square is not None:
                data["total_area"]["value"]["lte"] = self.max_square
            if self.by_homeowner:
                data["is_by_homeowner"] = {"type": "term", "value": True}
            # IT IS NOT ALL
        else:
            raise IncorrectPlaces(action=self.action, places=self.places)

        if self._page > 1:
            data["page"] = {"type": "term", "value": self._page}
        if self.action == AREND_MONTHLY:
            data["for_day"] = {"type": "term", "value": "!1"}
        elif self.action == AREND_DAILY:
            data["for_day"] = {"type": "term", "value": "1"}
        if self.min_price is not None or self.max_price is not None:
            data["price"] = {"type": "range", "value": {}}
        if self.min_price is not None:
            data["price"]["value"]["gte"] = self.min_price
        if self.max_price is not None:
            data["price"]["value"]["lte"] = self.max_price
        if places_set <= {FLAT} and self.rooms:
            data["room"] = {"type": "terms", "value": [ROOMS[room] for room in self.rooms]}

        return data


class CianClient:
    def __init__(self):
        self.asession = aiohttp.ClientSession()
        self.session = requests.Session()

    async def __aenter__(self) -> CianClient:
        return self

    async def __aexit__(self, *args):
        await self.asession.close()

    def search(self, region: str, action: str, places: Sequence[str],
               offer_owner: Optional[str]=None, rooms: Sequence[str]=(),
               min_bedrooms: Optional[int]=None, max_bedrooms: Optional[int]=None,
               building_status: Optional[str]=None, min_price: Optional[float]=None,
               max_price: Optional[float]=None, currency: Optional[str]=None,
               square_meter_price: bool=False, min_square: Optional[float]=None,
               max_square: Optional[float]=None, by_homeowner: bool=False, start_page: int=1,
               end_page: Optional[int]=None, limit: Optional[int]=None, delay: float=0) -> Search:
        return Search(
            session=self.session,
            asession=self.asession,
            region=region,
            action=action,
            places=places,
            offer_owner=offer_owner,
            rooms=rooms,
            min_bedrooms=min_bedrooms,
            max_bedrooms=max_bedrooms,
            building_status=building_status,
            min_price=min_price,
            max_price=max_price,
            currency=currency,
            square_meter_price=square_meter_price,
            min_square=min_square,
            max_square=max_square,
            by_homeowner=by_homeowner,
            start_page=start_page,
            end_page=end_page,
            limit=limit,
            delay=delay,
        )

    async def aclose(self):
        await self.asession.close()
