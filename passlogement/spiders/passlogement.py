import json

import scrapy

from passlogement.items import Offers


class PassLogementSpider(scrapy.Spider):
    name = "passlogement"
    start_urls = ["https://offres.passlogement.com/account/auth/login"]

    def __init__(self, username, password, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
        self.password = password
        self.auth_cookie = None

    def start_requests(self):
        login_url = "https://offres.passlogement.com/account/auth/login"
        yield scrapy.FormRequest(
            url=login_url,
            formdata={"username": self.username, "password": self.password},
            callback=self.after_login,
        )

    def after_login(self, response):
        self.auth_cookie = response.headers.get("Set-Cookie", "").decode()
        if "PHPSESSID" in self.auth_cookie:
            self.log("Authentication successful!")
            offers_url = "https://offres.passlogement.com/account/offer/listing/json"
            yield scrapy.Request(
                url=offers_url,
                headers={"Cookie": self.auth_cookie},
                callback=self.parse_offers,
            )
        else:
            self.log("Authentication failed. Check credentials.")

    def parse_offers(self, response):
        data = json.loads(response.text)
        offers = data.get("offer", [])
        for offer_data in offers:
            offer = Offers(**offer_data)
            if offer.is_great_offer():
                yield offer
