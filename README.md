<div align="center">

# OtomotoParser

A Telegram bot that watches an [Otomoto.pl](https://www.otomoto.pl) search and messages you when new car listings appear.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-pyTelegramBotAPI-26A5E4?logo=telegram&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-PyMongo-47A248?logo=mongodb&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/Scraping-BeautifulSoup4-4B8BBE)

</div>

## What it does

- Takes an Otomoto search URL (with your filters applied) sent to the bot in Telegram.
- Scrapes the listings on the first results page and stores each one in MongoDB.
- Re-checks the search every 60 seconds and sends every new listing to your chat.
- Extracts title, publication date, price, make, model, year, mileage, fuel type, gearbox, body type and engine capacity.

## Quick start

### Prerequisites

- Python 3
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- A MongoDB instance (local or [Atlas](https://www.mongodb.com/atlas)) and its connection string

### Install

```bash
git clone https://github.com/InYanInIn/OtomotoParser.git
cd OtomotoParser
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt python-dotenv
```

`python-dotenv` is imported by the code but is not listed in `requirements.txt`, so it is installed explicitly.

### Configure

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=123456:your-bot-token
MONGO_URI=mongodb://localhost:27017
```

### Run

```bash
python botController.py
```

The bot starts polling Telegram immediately.

### Use

1. Open your bot in Telegram and send `/start`.
2. On Otomoto.pl, set your filters, sort by newest, and copy the URL.
3. Send that URL to the bot. It scrapes the current listings and replies `Done!`.
4. Tap **Start checking** (or send `/check`) to begin watching for new listings.
5. Tap **Stop checking** (or send `/stop`) to stop.

Example notification:

```text
https://www.otomoto.pl/osobowe/oferta/...
 BMW 320d - 2026-11-10 18:42:00 - 28900 PLN - 2009 - 213 000 km - Diesel - Manualna - Coupe - 1 995 cm3
```

## Configuration

| Variable             | Required | Description                                  |
|----------------------|----------|----------------------------------------------|
| `TELEGRAM_BOT_TOKEN` | yes      | Token of your Telegram bot                   |
| `MONGO_URI`          | yes      | MongoDB connection string                    |

Listings are saved to database `OtomotoParserDB`, collection `Advertisement`, one document per listing link (existing links are not overwritten).

## Project structure

```text
botController.py     Telegram bot, commands and menu (entry point)
checkerService.py    60-second polling loop per chat
parser.py            Fetches and parses Otomoto pages
VehicleAd.py         Listing model
databaseService.py   MongoDB storage
dateConverter.py     Polish date strings to datetime
menu_filters.py      Unused, fully commented-out filter menu
requirements.txt     Pinned dependencies
```

## Limitations

- The built-in filter menu is not implemented; use the link option.
- The first scrape reads only page 1 of the results.
- Parsing relies on Otomoto's current HTML, so it can break when the site changes.

## Responsible use

Respect Otomoto's terms of service and `robots.txt`. Keep the polling interval modest, do not run many watchers against the site, and set a real contact address in the `User-Agent` in `parser.py` (`HEADERS`). Use the data for personal purposes only.
