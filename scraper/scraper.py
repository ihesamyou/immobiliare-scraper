import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import json
import csv
import pandas as pd


class Immobiliare:
    def __init__(self, url, get_data_of_following_pages=False) -> None:
        self.url = url
        self.last_scraped_url = self.url
        self.get_data_of_following_pages = get_data_of_following_pages
        self.response = requests.get(self.url)
        self.last_response = self.response
        self.real_estates = []
        self.gather_real_estate_data()
        self.data_frame = pd.DataFrame(self.real_estates)

    def __str__(self) -> str:
        return f"Immobiliare scraper - url='{self.url}'"

    def _check_url(self) -> None:
        if not "https://www.immobiliare.it" in self.url:
            raise ValueError(f"Given url must include 'https://www.immobiliare.it'.")

        if "mapCenter" in self.url:
            raise ValueError(f"Given url must not include 'mapCenter' as it uses another api to retrieve data.")

        if "search-list" in self.url:
            raise ValueError(f"Given url must not include 'search-list' as it uses another api to retrieve data.")

        if self.response.status_code != 200:
            self.response.raise_for_status()

    def gather_real_estate_data(self) -> None:
        self._check_url()
        if self.get_data_of_following_pages:
            parsed_url = urlparse(self.url)
            query_params = parse_qs(parsed_url.query)
            pag_value = int(query_params.get("pag", ["1"])[0])
            self.last_scraped_url = urlunparse((parsed_url.scheme, parsed_url.netloc,
                parsed_url.path, parsed_url.params, urlencode(query_params, doseq=True),
                parsed_url.fragment))
            self.last_response = requests.get(self.last_scraped_url)

            while self.last_response.status_code == 200:
                print(f"Getting real estate data of {self.last_scraped_url}")
                self.real_estates += self.filter_json_data(self.last_response)
                pag_value += 1
                query_params['pag'] = [str(pag_value)]
                self.last_scraped_url = urlunparse((parsed_url.scheme, parsed_url.netloc,
                    parsed_url.path, parsed_url.params, urlencode(query_params, doseq=True),
                    parsed_url.fragment))
                if self.last_response.status_code == 200:
                    self.last_response = requests.get(self.last_scraped_url)
        else:
            print(f"Getting real estate data of {self.url}")
            self.real_estates += self.filter_json_data(self.response)

    def filter_json_data(self, response) -> list:
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            json_data = json.loads(soup.find("script", {"id": "__NEXT_DATA__"}).text)
            json_data = json_data["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["pages"][0]["results"]
        except KeyError:
            json_data = []

        real_estates = []
        if json_data:
            for record in json_data:
                real_estate = {}
                real_estate["id"] = record["realEstate"]["id"]
                real_estate["url"] = record["seo"]["url"]
                real_estate["contract"] = record["realEstate"]["contract"]
                real_estate["agency_id"], real_estate["agency_url"], real_estate["agency_name"] =  None, None, None
                real_estate["is_private_ad"] = 1 if record["realEstate"]["advertiser"].get("agency", None) == None else 0
                if not real_estate["is_private_ad"]:
                    real_estate["agency_id"] =  record["realEstate"]["advertiser"]["agency"]["label"]
                    real_estate["agency_url"] = record["realEstate"]["advertiser"]["agency"]["agencyUrl"]
                    real_estate["agency_name"] = record["realEstate"]["advertiser"]["agency"]["displayName"]
                real_estate["is_new"] = 1 if record["realEstate"]["isNew"] else 0
                real_estate["is_luxury"] = 1 if record["realEstate"]["luxury"] else 0
                real_estate["formatted_price"] = record["realEstate"]["price"]["formattedValue"]
                real_estate["price"] = record["realEstate"]["price"].get("value", None)
                if (not real_estate["price"]):
                    price_match = re.search(r'\d+\.?\d*', real_estate["formatted_price"])
                    if price_match:
                        real_estate["price"] = price_match.group(0).replace('.', '')
                real_estate["bathrooms"] = record["realEstate"]["properties"][0].get("bathrooms", None)
                real_estate["bedrooms"] = record["realEstate"]["properties"][0].get("bedRoomsNumber", None)
                real_estate["floor"], real_estate["formatted_floor"] = None, None
                floor_data = record["realEstate"]["properties"][0].get("floor", None)
                if floor_data:
                    real_estate["floor"] = floor_data["abbreviation"]
                    real_estate["formatted_floor"] = floor_data["value"]
                real_estate["total_floors"] = record["realEstate"]["properties"][0].get("floors", None)
                real_estate["condition"] = record["realEstate"]["properties"][0].get("condition", None)
                real_estate["rooms"] = record["realEstate"]["properties"][0].get("rooms", None)
                real_estate["has_elevators"] = 1 if record["realEstate"]["properties"][0]["hasElevators"] else 0
                real_estate["surface"] = None
                real_estate["surface_formatted"] = record["realEstate"]["properties"][0].get("surface", None)
                if real_estate["surface_formatted"]:
                    real_estate["surface"] = re.search(r'(\d+\.?\d*)', real_estate["surface_formatted"]).group(1) or None
                real_estate["type"] = record["realEstate"]["properties"][0]["typologyGA4Translation"]
                real_estate["caption"] = record["realEstate"]["properties"][0].get("caption", None)
                real_estate["category"] = record["realEstate"]["properties"][0]["category"]["name"]
                real_estate["description"] = record["realEstate"]["properties"][0].get("description", None)
                energy_data = record["realEstate"]["properties"][0].get("energy", None)
                real_estate["heating_type"], real_estate["air_conditioning"] = None, None
                if energy_data:
                    real_estate["heating_type"] = energy_data.get("heatingType", None)
                    real_estate["air_conditioning"] = energy_data.get("airConditioning", None)
                real_estate["latitude"] = record["realEstate"]["properties"][0]["location"]["latitude"]
                real_estate["longitude"] = record["realEstate"]["properties"][0]["location"]["longitude"]
                real_estate["region"] = record["realEstate"]["properties"][0]["location"]["region"]
                real_estate["province"] = record["realEstate"]["properties"][0]["location"]["province"]
                real_estate["macrozone"] = record["realEstate"]["properties"][0]["location"]["macrozone"]
                real_estate["microzone"] = record["realEstate"]["properties"][0]["location"]["microzone"]
                real_estate["city"] = record["realEstate"]["properties"][0]["location"]["city"]
                real_estate["country"] = record["realEstate"]["properties"][0]["location"]["nation"]["id"]
                real_estates.append(real_estate)
        else:
            self.last_response.status_code = 404
        return real_estates

    def save_data_json(self, filename="immobiliare.json") -> None:
        with open(filename, "w") as file:
            json.dump(self.real_estates, file, indent=4)

    def save_data_csv(self, filename="immobiliare.csv") -> None:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = self.real_estates[0].keys() if self.real_estates else []
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for real_estate in self.real_estates:
                writer.writerow(real_estate)


immo = Immobiliare(url="https://www.immobiliare.it/affitto-case/milano/?criterio=rilevanza&pag=75", get_data_of_following_pages=True)
immo.save_data_json()
immo.save_data_csv()
data = immo.data_frame