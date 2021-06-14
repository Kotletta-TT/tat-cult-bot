import asyncio
import re
from models import Event
import aiohttp
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from config import SOURCE


class Culture:

    def __init__(self):
        self.events = []
        self.events_urls = []

    async def __get_event_urls(self, url: str):
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10, )) as session:
            async with session.get(url, ssl=False, timeout=aiohttp.ClientTimeout(total=10)) as response:
                content = await response.text()
                soup = BeautifulSoup(content, 'lxml')
                get_url = soup.find_all("div", class_="entity-cards_item col")
                for i in get_url:
                    url = SOURCE + i.div["data-entity-url"][1:]
                    self.events_urls.append(url)

    async def __run_get_urls(self):
        pagination_urls = self.calc_pagination("https://www.culture.ru/afisha/kazan")
        await asyncio.gather(*[self.__get_event_urls(url) for url in pagination_urls])

    def get_times(self, json_obj):
        datetime_start = datetime.fromisoformat(json_obj['startDate'])
        time_start = datetime.fromisoformat(json_obj['startDate']).time()
        time_end = datetime.fromisoformat(json_obj['endDate']).time()

        date_start = datetime.fromisoformat(json_obj['startDate']).date()
        date_end = datetime.fromisoformat(json_obj['endDate']).date()
        if date_end > date_start + timedelta(days=30):
            date_end = date_start + timedelta(days=30)

        delta = date_end - date_start
        delta_h = time_end.hour - time_start.hour
        date_list = []

        for i in range(delta.days + 1):
            start = datetime_start + timedelta(days=i)
            end = datetime_start + timedelta(days=i, hours=delta_h)
            date_list.append({"startDate": f"{start.date().year}-{start.date().month}-{start.date().day} {start.time().hour}:{start.time().minute}", "endDate": f"{end.date().year}-{end.date().month}-{end.date().day} {end.time().hour}:{end.time().minute}"})
        return str(date_list)

    def calc_pagination(self, url: str) -> list:
        urls = []
        nums = []

        pag_example = "/afisha/kazan?page={}&limit=20"
        request = requests.get(url)
        soup = BeautifulSoup(request.content, 'lxml')
        pagination = soup.find_all("a", class_="pagination_item")

        for i in pagination:
            num_page = re.search(r'page=(\d+)', i["href"])
            if num_page and num_page.group(1) not in nums:
                nums.append(int(num_page.group(1)))
        if len(nums):
            for k in (range(1, max(nums) + 1)):
                urls.append(SOURCE[:-1] + pag_example.format(str(k)))
        return urls

    async def __get_event(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                try:
                    content = await response.text()
                except Exception as e:
                    print(e)
                    return None
                soup = BeautifulSoup(content, 'lxml')
                title = str(soup.h1.text).replace(u'\xa0', u' ')
                json_obj = eval(soup.find("body", class_="js-body").find_all("script")[1].string)
                site_id = json_obj["@id"].split("/")[4]
                event_type = soup.find("div", class_="entity-heading_subtitle").text.split(",")[0]
                img = json_obj['image']['url']
                agent_address = json_obj['location']['address']
                desc = json_obj['description'].replace(u'\xa0', u' ')
                # try:
                #     img = soup.find("div", class_="cover_entity-heading").find_all("a")[1]["href"]
                # except IndexError:
                #     img = soup.find("div", class_="cover_entity-heading").find_all("a")[0]["href"]
                try:
                    price = json_obj['offers']['priceSpecification']['price']
                    currency = json_obj['offers']['priceSpecification']['priceCurrency']
                except KeyError:
                    price = json_obj['offers']['price']
                    currency = "RUB"
                try:
                    agent_url = json_obj['offers']['url']
                except KeyError:
                    agent_url = None
                try:
                    agent_name = json_obj['location']['name']
                except KeyError:
                    agent_name = None
                try:
                    gps_latitude = float(json_obj['location']['geo']['latitude'])
                    gps_longitude = float(json_obj['location']['geo']['longitude'])
                except KeyError:
                    gps_latitude = 0.0
                    gps_longitude = 0.0
                try:
                    event_date = self.get_times(json_obj)
                except Exception:
                    event_date = []
                event = {"site_id": site_id, "title": title, "url": url, "image": img, "event_date": event_date, "price": price, "currency": currency, "agent_name": agent_name, "agent_address": agent_address, "agent_url": agent_url, "event_type": event_type, "event_description": desc, "gps_latitude": gps_latitude, "gps_longitude": gps_longitude}
                event = Event(**event)
                print(event)
                self.events.append(event)


    async def __run_get_events(self):
        await asyncio.gather(*[self.__get_event(url) for url in self.events_urls])

    def get_event_urls(self):
        asyncio.run(self.__run_get_urls())

    def get_events(self):
        self.get_event_urls()
        asyncio.run(self.__run_get_events())
