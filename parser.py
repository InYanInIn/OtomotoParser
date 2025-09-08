from bs4 import BeautifulSoup
import requests
import dateConverter

from VehicleAd import VehicleAd

# URL = "https://www.otomoto.pl/osobowe/bmw/seria-3/seg-coupe?search%5Bfilter_enum_generation%5D=gen-e90-2005-2012&search%5Border%5D=created_at_first%3Adesc&search%5Badvanced_search_expanded%5D=true"
URL = {}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; JanBot/1.0; +https://your-email.example.com)",
    "Accept-Language": "pl-PL,pl;q=0.9,en;q=0.8"
}


def get_soup(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html = response.text
        return BeautifulSoup(html, "html.parser")
    else:
        print(response.status_code)
        return


def get_num_pages(url: str, headers: dict) -> int:
    soup = get_soup(url, headers)

    num_items = soup.select("li.ooa-6ysn8b")
    num_pages = num_items[-1].get_text(strip=True) if num_items else 1

    return int(num_pages)


def get_urls(url: str, headers: dict) -> list:
    ads_urls = []

    num_pages = get_num_pages(url, headers)

    # for page in range(1, num_pages + 1):
    for page in range(1, 2):
        page_url = url + "&page=" + str(page)
        soup = get_soup(page_url, headers)

        ads = soup.select("article")

        for ad in ads:
            ad_tag = ad.select_one('h2')

            try:
                link = ad_tag.select_one('a')["href"]
                ads_urls.append(link)
            except:
                pass

    return ads_urls


def get_new_urls(old_urls: list, url: str, headers: dict) -> list:
    new_urls = []

    num_pages = get_num_pages(url, headers)

    for page in range(1, num_pages + 1):
        page_url = url + "&page=" + str(page)
        soup = get_soup(page_url, headers)

        ads = soup.select("article")

        for ad in ads:
            ad_tag = ad.select_one('h2')

            try:
                link = ad_tag.select_one('a')["href"]
                if link not in old_urls:
                    new_urls.append(link)
                else:
                    return new_urls
            except:
                pass

    return new_urls


def get_ad_data(url: str, headers: dict) -> VehicleAd:
    soup = get_soup(url, headers)

    data = {}

    data["title"] = soup.find('h1', class_="offer-title").text
    data["price"] = soup.find('span', class_="offer-price__number").text.replace(' ', '')
    data["currency"] = soup.find('span', class_="offer-price__currency").text
    data["publication_date"] = dateConverter.convert_date(soup.find('p', class_="e1s9vvdy6 ooa-116zxz0").text)

    details_section = soup.find('div', {"data-testid": "main-details-section"})
    basic_info = soup.find('div', {"data-testid": "basic_information"})

    if details_section:
        for detail in details_section.find_all("div", {"data-testid": "detail"}):
            labels = detail.find_all("p")
            if len(labels) >= 2:
                name = labels[0].get_text(strip=True)
                value = labels[1].get_text(strip=True)

                data[name] = value

        make_label = basic_info.find("div", {"data-testid": "make"}).find_all("p")
        if len(make_label) >= 2:
            data["Marka"] = make_label[1].get_text(strip=True)

        model_label = basic_info.find("div", {"data-testid": "model"}).find_all("p")
        if len(model_label) >= 2:
            data["Model"] = model_label[1].get_text(strip=True)

        year_label = basic_info.find("div", {"data-testid": "year"}).find_all("p")
        if len(year_label) >= 2:
            data["Rok produkcji"] = year_label[1].get_text(strip=True)

    result = VehicleAd(
        title=data.get("title"),
        publication_date=data.get("publication_date"),
        link=url,
        price=data.get("price"),
        currency=data.get("currency"),
        make=data.get("Marka"),
        model=data.get("Model"),
        year=data.get("Rok produkcji"),
        mileage=data.get("Przebieg"),
        fuel_type=data.get("Rodzaj paliwa"),
        gearbox=data.get("Skrzynia biegów"),
        vehicle_type=data.get("Typ nadwozia"),
        engine_capacity=data.get("Pojemność skokowa"),
    )

    return result
#
# urls = get_urls(URL, HEADERS)
# data = {}
# current = 1
# for url in urls:
#     print(f"Processing {current}/{len(urls)}: {url}")
#     data[url] = get_ad_data(url, HEADERS)
#     current += 1
# print(data)
# print(len(data))
