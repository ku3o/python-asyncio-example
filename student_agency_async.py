import asyncio
from datetime import date, timedelta

import aiohttp
from bs4 import BeautifulSoup


async def scrape_route(departure, arrival, date):
    """Scrape all connections for a specific route and data."""
    print(f'Scraping route {departure} - {arrival} for {date}')
    async with aiohttp.ClientSession() as session:
        await session.get('https://jizdenky.regiojet.cz/m/')
        form_data = aiohttp.FormData()
        form_data.add_field('fromStation', departure)
        form_data.add_field('toStation', arrival)
        form_data.add_field('departure', date.strftime('%d.%m.%y'))

        response = await session.post('https://jizdenky.regiojet.cz/m/?0-1.IFormSubmitListener-searchForm-form', data=form_data)
        raw_body = await response.text()
        html_body = BeautifulSoup(raw_body, 'html.parser')
        routes = html_body.find_all(class_='select-line')  # Select bus connections only.
        for route in routes:
            bus_connection = route.get_text().split()
            # Here is a place for further processing of results.

    print(f'Scraping COMPLETED {departure} - {arrival} for {date}')

async def scrape_multiple_dates(departure, arrival, dates):
    """Scrape prices for a specifc route and multiple dates."""
    await asyncio.gather(*[scrape_route(departure, arrival, date) for date in dates])


def main():
    loop = asyncio.get_event_loop()
    next_hundred_days = [date.today() + timedelta(days=days) for days in range(100)]
    # Search for Praha Brno
    loop.run_until_complete(scrape_multiple_dates('ID10202003', 'ID10202002', next_hundred_days))


if __name__ == '__main__':
    main()
