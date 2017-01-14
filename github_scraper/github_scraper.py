"""
File: github_scraper

Description:
Primary Author(s): Michael Clawar
Secondary Author(s):

Notes:

January 14, 2017
StratoDem Analytics, LLC
"""

from typing import List

import requests
from bs4 import BeautifulSoup, Tag


PERIOD_STRING_TO_QUERY_TEXT = {
    'this week': 'weekly',
    'this month': 'monthly',
    'today': 'daily',
}


def get_top_repositories(language: str, period: str) -> List[dict]:
    url = _trending_url(language, period)

    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    top_repo_li = soup.find_all('li', {'class': 'col-12 d-block width-full py-4 border-bottom'})

    return [_parse_div_to_dict(x) for x in top_repo_li]


def _parse_div_to_dict(li: Tag) -> dict:
    if not isinstance(li, Tag):
        raise TypeError('div should be a Tag instance')

    user, repository = li.find('div', {'class': 'd-inline-block col-9 mb-1'}).text.split(' / ')
    user = user.strip()
    repository = repository.strip()
    description = li.find('p', {'class': 'col-9 d-inline-block text-gray m-0 pr-4'}).text.strip()
    language = li.find('span', {'class': 'mr-3'}).text.strip()
    stars, forks = li.find_all('a', {'class': 'muted-link tooltipped tooltipped-s mr-3'})
    stars = stars.text.strip()
    forks = forks.text.strip()

    stars_this_period = li.find('span', {'class': 'float-right'})
    if stars_this_period is not None:
        stars_this_period = stars_this_period.text.strip()
    else:
        stars_this_period = 'an unknown number of stars this period'

    return dict(
        user=user.strip(),
        repository=repository.strip(),
        description=description,
        language=language,
        stars=stars,
        forks=forks,
        stars_this_period=stars_this_period)


def _trending_url(language: str, period: str) -> str:
    if not isinstance(language, str):
        raise TypeError('language should be a string')
    if not isinstance(period, str):
        raise TypeError('period should be a string')
    period = period.lower()
    if period not in PERIOD_STRING_TO_QUERY_TEXT:
        raise ValueError('period not allowed')

    if language.lower() == 'all languages':
        url_formatter = 'https://github.com/trending?since={period}'
    else:
        url_formatter = 'https://github.com/trending?l={language}'.format(language=language.lower())
        url_formatter += '&since={period}'

    period_query_text = PERIOD_STRING_TO_QUERY_TEXT[period]

    return url_formatter.format(period=period_query_text)


if __name__ == '__main__':
    print(get_top_repositories('python', 'this week'))
