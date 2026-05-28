import os
import time

import requests

from bs4 import BeautifulSoup
import re
from playwright.sync_api import sync_playwright
import logging
import json
seen = set()
duplicates_count = 0

def get_with_retry(url, retries=3, delay=2, timeout=10):
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=timeout)

            if response.status_code == 200:
                return response

            logging.debug(f"Попытка {attempt}: статус {response.status_code}")

        except requests.exceptions.RequestException as e:
            logging.debug(f"Попытка {attempt}: ошибка {e}")

        time.sleep(delay)

    return None

def get_post_urls_for_page(html:str) -> list:

    soup = BeautifulSoup(html, "html.parser")
    container = soup.find("div", class_="styles_list__pfMHf styles_list__photo__ogPFb")

    links = []

    if container:
        a_tags = container.find_all("a", href=True)

        for a in a_tags:
            href = a["href"]
            links.append(href)
    normlink = []
    for link in links:
        match = re.search(r"/ro/\d+", link)
        if match is not None:
            normlink.append(f"https://999.md{match.group()}")
    return normlink

def get_all_posts_links(browser, from_file = False):
    all_posts_links = []

    if from_file:
        with open("links.txt", "r", encoding="utf-8") as f:
            all_posts_links = [line.strip() for line in f]
        pass
    else:
        page = browser.new_page()
        for i in range(1, 279):
            page.goto(f"https://999.md/ro/list/real-estate/apartments-and-rooms?page={i}&o_16_1=776")
            time.sleep(1)

            page.wait_for_load_state("networkidle")


            html = page.content()
            all_posts_links.extend(get_post_urls_for_page(html))

        with open("links.txt", "w", encoding="utf-8") as f:
            for item in all_posts_links:
                f.write(item + "\n")

    return all_posts_links

def parse_post(link):

    logging.debug(f"Retrieving post: {link}")
    content = get_with_retry(link)

    if content is None:
        return
    html = content.content
    logging.debug(f"Parsing...")

    with open("debug_html.html", "wb") as f:
        f.write(html)

    soup = BeautifulSoup(html, "html.parser")


    block = soup.find("div", attrs={"data-testid": "Caracteristici"})

    label = soup.find(string=lambda s: s and "Caracteristici" in s)

    block = label.find_parent("div") if label else None

    post_data = {}

    if block is None:
        return
    for li in block.find_all("li"):
        key = li.find("span", class_=lambda x: x and "styles_group__key" in x)

        # значение может быть либо в <a>, либо в <span>
        value = li.find("a") or li.find("span", class_=lambda x: x and "value" in x)

        if key and value:
            post_data[key.text.strip()] = value.text.strip()

    block = soup.find("div", attrs={"data-testid": "Condiții de utilizare"})

    label = soup.find(string=lambda s: s and "Condiții de utilizare" in s)
    block = label.find_parent("div") if label else None
    if block is not None:
        # перебираем все li (каждая характеристика)
        for li in block.find_all("ul"):
            key = li.find("span", class_=lambda x: x and "styles_group__key" in x)

            # значение может быть либо в <a>, либо в <span>
            value = li.find("a") or li.find("span", class_=lambda x: x and "value" in x)

            if key and value:
                post_data[key.text.strip()] = value.text.strip()

    block = soup.find("div", attrs={"data-testid": "Adăugător"})

    label = soup.find(string=lambda s: s and "Adăugător" in s)
    block = label.find_parent("div") if label else None
    if block:
        values = [
            el.get_text(" ", strip=True)
            for el in block.find_all(["span", "a"])
            if el.get_text(strip=True)
        ]

        for value in values:
            post_data[value.strip()] = 1

    meta = soup.find("meta", attrs={"property": "product:price:amount"})

    price = meta.get("content") if meta else None
    post_data['price'] = price

    urls = re.findall(r'https://i\.simpalsmedia\.com/999\.md/BoardImages/900x900/[a-f0-9]+\.jpg', str(html))
    urls = list(set(urls))


    for url in urls:
        logging.debug(url)



    with open("file_debug.txt", "w", encoding="utf-8") as f:
        f.write(str(html))

    coords = re.findall(r'\\\\\"lat\\\\\":([0-9.]+),\\\\\"lon\\\\\":([0-9.]+)', str(html))
    logging.debug(coords)
    if coords:
        lat, long = coords[0]
        post_data['lat'] = lat
        post_data['long'] = long

    descriptions = soup.find_all("meta", attrs={"property": "og:description"})
    if len(descriptions) > 0:
        text = descriptions[-1].get("content")
        post_data['description'] = text

    for k, v in post_data.items():
        logging.debug(f"{k}: {v}")

    number = link.split("/")[-1]

    key = str(post_data)

    if key not in seen:
        seen.add(key)
    else:
        global duplicates_count
        duplicates_count += 1
        logging.info(f"Duplicate post: {key} Total duplicate posts count: {duplicates_count}")
        return

    os.makedirs(f"data/{number}", exist_ok=True)
    with open(f"data/{number}/data.json", "w", encoding="utf-8") as f:
        json.dump(post_data, f, indent=2, ensure_ascii=False)


    folder = f"data/{number}"
    os.makedirs(folder, exist_ok=True)

    for i, url in enumerate(urls):
        response = get_with_retry(url)
        if response is not None:
            filename = os.path.join(folder, f"image_{number}_{i}.jpg")

            with open(filename, "wb") as f:
                f.write(response.content)

            # print(f"Сохранено: {filename}")
        else:
            logging.debug(f"Ошибка загрузки: {url}")


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        links = get_all_posts_links(browser, from_file=False)
        print(links)

        single_page = False

        if not single_page:
            for i in range(len(links)):
                logging.debug(f"{i}/{len(links)}")
                parse_post(links[i])
        else:
            parse_post("https://999.md/ro/104092842")

        browser.close()
    logging.info(f"Total duplicate posts: {duplicates_count}")

if __name__ == "__main__":
    main()