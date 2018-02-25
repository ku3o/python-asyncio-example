from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup


def scrape_route(departure, arrival, date):
    """Scrape all connections for a specific route and data."""
    print(f'Scraping route {departure} - {arrival} for {date}')
    with requests.Session() as session:
        session.get('https://jizdenky.regiojet.cz/m/')
        # Post data setup
        form_data = {}
        form_data['fromStation'] = departure
        form_data['toStation'] = arrival
        form_data['departure'] = date.strftime('%d.%m.%y')

        response = session.post('https://jizdenky.regiojet.cz/m/?0-1.IFormSubmitListener-searchForm-form', data=form_data)
        raw_body = response.text
        html_body = BeautifulSoup(raw_body, 'html.parser')
        routes = html_body.find_all(class_='select-line')  # Select bus connections only.
        for route in routes:
            connection = route.get_text().split()
            # Here is a place for further processing of results.

    print(f'Scraping COMPLETED {departure} - {arrival} for {date}')

def scrape_multiple_dates(departure, arrival, dates):
    """Scrape prices for a specifc route and multiple dates."""
    # Init ThreadPool without a limit for a thread. Number of threads can be limited by
    # `max_workers`.
    with ThreadPoolExecutor() as executor:
        [executor.submit(scrape_route, departure, arrival, date) for date in dates]


def main():
    next_hundred_days = [date.today() + timedelta(days=days) for days in range(100)]
    # Search for Praha Brno
    scrape_multiple_dates('ID10202003', 'ID10202002', next_hundred_days)


if __name__ == '__main__':
    main()
