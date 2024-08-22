import numpy as np
import json
from tqdm import tqdm
import pandas as pd


try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve
from bs4 import *
import requests

data = {
    "Name": [],
    "Url of Property": [],
    "Description 1": [],
    "Description 2": [],
    "Price": [],
    "Time": [],
    "Img": [],
}
idx = 0
for page_num in tqdm(range(1, 10)):
    url = f"https://ikman.lk/en/ads/sri-lanka/property?sort=date&order=desc&buy_now=0&urgent=0&page={page_num}"
    properties = BeautifulSoup(requests.get(url).text, "html.parser").find_all(
        "li", class_="normal--2QYVk gtm-normal-ad"
    )
    for property in properties:
        try:
            name = "null"
            url_of_property = "null"
            bed_and_bathroom = "null"
            description = "null"
            price = "null"
            time = "null"
            img = "null"
            name = property.find("a", class_="card-link--3ssYv gtm-ad-item").attrs["title"]
            url_of_property = (
                "https://ikman.lk"
                + property.find("a", class_="card-link--3ssYv gtm-ad-item").attrs["href"]
            )
            bed_and_bathroom = (
                property.find("div", class_="content--3JNQz").find("div").find("div").text
            )
            description = (
                property.find("div", class_="content--3JNQz")
                .find("div")
                .find("div", class_="description--2-ez3")
            ).text
            price = (
                "$"
                + str(
                    int(
                        (
                            property.find("div", class_="content--3JNQz")
                            .find("div")
                            .find("div", class_="price--3SnqI color--t0tGX")
                        )
                        .text.split(" ")[1]
                        .replace(",", "")
                    )
                    / 355.0
                )
                + " "
                + (
                    property.find("div", class_="content--3JNQz")
                    .find("div")
                    .find("div", class_="price--3SnqI color--t0tGX")
                ).text.split(" ")[2]
                + " "
                + (
                    property.find("div", class_="content--3JNQz")
                    .find("div")
                    .find("div", class_="price--3SnqI color--t0tGX")
                ).text.split(" ")[3]
            )
            time = (
                property.find("div", class_="content--3JNQz").find(
                    "div", class_="updated-time--1DbCk"
                )
            ).text
            img = property.find("img", class_="normal-ad--1TyjD").attrs["src"]
            # print(name)
            data["Name"].append(name)
            data["Url of Property"].append(url_of_property)
            data["Description 1"].append(bed_and_bathroom)
            data["Description 2"].append(description)
            data["Price"].append(price)
            data["Time"].append(time)
            data["Img"].append(img)
        except:
            # print(name)
            data["Name"].append(name)
            data["Url of Property"].append(url_of_property)
            data["Description 1"].append(bed_and_bathroom)
            data["Description 2"].append(description)
            data["Price"].append(price)
            data["Time"].append(time)
            data["Img"].append(img)

data = pd.DataFrame(data)
data.to_csv("./data.csv", index=False)
data.to_json("./data.json")
