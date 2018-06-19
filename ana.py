"""
This script fetches ANA-specific information from 空飛ぶ株優.com
http://soratobu-kabuyu.com/ana/index.html
"""


import ast
import bs4
import requests


def print_average_price(soup):
    """
    ANA株主優待券（新券）の平均買取価格を表示
    """
    priceElements = soup.select(r'#main > div.section.emphasis > table:nth-of-type(1) > tr > td > span')
    print('ANA株主優待券の平均買取価格（新券）：' + priceElements[0].getText() + '円')


def print_price_table(soup):
    """
    Print the price table for "ANA株主優待券（新券）"

    Note that original_price_table[0] is ['週', '価格', '初日の平均価格', '最終日の平均価格', '価格']
    original_price_table[0][0]: 週の始まりの日（日曜日）
    original_price_table[0][1]: 週全体の安値／高値
    original_price_table[0][2]: 初日の平均価格
    original_price_table[0][3]: 最終日の平均価格
    original_price_table[0][4]: 週全体の安値／高値

    See this page for details.
    https://developers.google.com/chart/interactive/docs/gallery/candlestickchart
    """

    chart_all0_script_element = soup.select(r'#pageSection > script:nth-of-type(2)')
    chart_all0_script_text = chart_all0_script_element[0].getText()
    price_table_text = chart_all0_script_text               \
        .split('google.visualization.arrayToDataTable(')[1] \
        .split(')')[0]
    original_price_table = ast.literal_eval(price_table_text)

    def extract_value(item):
        """Extract values from original item in original_price_table"""
        average_price = (item[1] + item[4]) / 2.0     # Take average of the row price and the high price
        return [item[0], average_price]

    price_table = list(map(extract_value, original_price_table[1:]))
    print(price_table)


def get_BeautifulSoup():
    response = requests.get('http://soratobu-kabuyu.com/ana/index.html')
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    return soup


def main():
    soup = get_BeautifulSoup()
    print_average_price(soup)
    print_price_table(soup)


if __name__ == '__main__':
    main()
