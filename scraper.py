from urllib.error import HTTPError

from bs4 import BeautifulSoup
from urllib.request import urlopen

LAST_STATEMENT_URL = 'http://www.tdcj.state.tx.us/death_row/{0}'

_page = urlopen('http://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html')
_soup = BeautifulSoup(_page, "lxml")

_table_rows = _soup.findAll('tr')


def get_relevant_row_data(row):
    # todo: parse out row data to pull only relevant information out.
    # information includes:
        # First Name
        # Last Name
        # Execution Number
        # Execution Date
        # Race
        # Age
        # County
        # Last Words
    row_strings = row.text.split('\n')
    statement_link = LAST_STATEMENT_URL.format(row.find('a').find_next('a').get('href'))
    return [row_strings[1].strip(), get_last_words(statement_link).strip(), row_strings[4].strip(),
            row_strings[5].strip(), row_strings[6].strip(), row_strings[7].strip(), row_strings[8].strip(),
            row_strings[9].strip()]


def write_to_file(file_path, data):
    with open(file_path, 'a+') as f:
        f.write(' | '.join(data))
        f.write('\n')


def get_last_words(url):
    
    try:
        soup = BeautifulSoup(urlopen(url), "lxml")
        statement = soup.findAll('p')[-1].text
        if statement.isspace():
            statement = soup.findAll('p')[-2].text
        return statement.replace('\n', ' ')
    except HTTPError:
        return "N/A: " + url

# script begin
for row in _table_rows[1:]:
    row_data = get_relevant_row_data(row)
    write_to_file('data.txt', row_data)
