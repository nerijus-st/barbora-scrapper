import bs4
import matplotlib.pyplot as plt
import requests


class BarboraScrapper():

    def __init__(self):
        self.category_url = self.get_category()
        self.chosen_nutrition = self.get_nutrition()
        self.reversed = self.get_order()
        self.scrap_page()

    BASE_URL = 'https://www.barbora.lt'

    CATEGORY_URLS = [
        ['fish', 'https://www.barbora.lt/mesa-zuvys-ir-kulinarija/zuvu-gaminiai'],
        ['cheese', 'https://www.barbora.lt/pieno-gaminiai-ir-kiausiniai/suris'],
        ['curd-products', 'https://www.barbora.lt/pieno-gaminiai-ir-kiausiniai/varskes-produktai'],
        ['yogurt', 'https://www.barbora.lt/pieno-gaminiai-ir-kiausiniai/jogurtai-ir-desertai'],
        ['bread', 'https://www.barbora.lt/duonos-gaminiai-ir-konditerija/duona'],
        ['flakes', 'https://www.barbora.lt/bakaleja/grudu-dribsniai-koses-ir-batoneliai'],
        ['ice-cream', 'https://www.barbora.lt/saldytas-maistas/ledai-ir-ledo-kubeliai'],
        ['frozen-confectionery',
         'https://www.barbora.lt/saldytas-maistas/saldyti-kulinarijos-ir-konditerijos-gaminiai'],
        ['soft-drinks', 'https://www.barbora.lt/nealkoholiniai-gerimai/vaisvandeniai'],
        ['juice', 'https://www.barbora.lt/nealkoholiniai-gerimai/sultys-nektarai-ir-sulciu-gerimai']
    ]

    NUTRITION = [
        ['fat', 'Riebalai'],
        ['saturated-fat', 'Sočiosios riebalų rūgštys', ],
        ['carbs', 'Angliavandeniai'],
        ['sugar', 'Cukrūs'],
        ['protein', 'Baltymai'],
        ['salt', 'Druska']
    ]

    def get_category(self):

        print('Hello. Please choose category:')
        for _category in self.CATEGORY_URLS:
            print(self.CATEGORY_URLS.index(_category), _category[0])

        self.chosen_category_number = int(input('Select category number: '))
        category_url = self.CATEGORY_URLS[self.chosen_category_number][1]
        return category_url

    def get_nutrition(self):

        print('Please chose nutrition')
        for _nutrition in self.NUTRITION:
            print(self.NUTRITION.index(_nutrition), _nutrition[0])

        self.chosen_nutrition_number = int(input('Select nutrition number: '))
        chosen_nutrition = self.NUTRITION[self.chosen_nutrition_number][1]
        return chosen_nutrition

    def get_order(self):

        print('You can choose ascending or descending order')
        print('0. Ascending')
        print('1. Descending')

        chosen_order = int(input('Enter number (0 or 1): '))
        return chosen_order

    def scrap_page(self):

        category_request = requests.get(self.category_url)

        soup = bs4.BeautifulSoup(category_request.text, "html5lib")

        elements = soup.find_all("a", {"class": "b-product--imagelink b-link--product-info"})
        pagination = soup.find('ul', {"class": "pagination"})
        pagination_numbers = [num.getText() for num in pagination.find_all("a") if
                              num.getText().isdigit() and int(num.getText()) > 1]

        if len(pagination_numbers) > 0:
            print('INFO: Patience! There are {} pages to parse.'.format(len(pagination_numbers)))
            for pagination_number in pagination_numbers:
                next_url = '{0}?page={1}'.format(self.category_url, pagination_number)
                category_request = requests.get(next_url)
                soup = bs4.BeautifulSoup(category_request.text, "html5lib")
                elements.extend(soup.find_all("a", {"class": "b-product--imagelink b-link--product-info"}))

        product_urls = [self.BASE_URL + element['href'] for element in elements]

        print('INFO: Total {0} products will be parsed'.format(len(product_urls)))
        print('')

        if product_urls:
            self.parse_products(product_urls)
        else:
            return ('Sorry, no products found...')

    def parse_products(self, product_urls):

        parsed_products = {}
        for product_url in product_urls:
            product = requests.get(product_url)
            soup_product = bs4.BeautifulSoup(product.text, 'html5lib')
            product_price = soup_product.find("span", {"class": "b-product-price-current-number"}).getText().strip()
            product_title = soup_product.find("h1", {"class": "b-product-info--title"}).getText(), product_price
            nutrition_table = soup_product.find("table", {"class": "table table-striped table-condensed"})
            print('Parsing {0}'.format(product_title))

            parsed_nutrition = self.get_nutrition_table(nutrition_table, product_title)

            parsed_products[product_title] = parsed_nutrition
        print('INFO: Done parsing!')

        self.get_final_list(parsed_products)

    def get_nutrition_table(self, nutrition_table, product_title):
        if nutrition_table:
            parsed_nutrition = {}
            for row in nutrition_table.find_all('tr'):
                nutrition_name = row.find('td').getText()
                nutrition_value = row.find('td', {'class': 'b-text-right'}).getText()
                parsed_nutrition[nutrition_name] = nutrition_value
            return parsed_nutrition
        else:
            print('INFO: ', product_title, ' does not have nutrition table')

    def get_final_list(self, parsed_products):
        final_list = {}
        for name, nutrition in parsed_products.items():
            if nutrition and self.chosen_nutrition in nutrition:
                final_list[name] = float(nutrition[self.chosen_nutrition][:-1].strip().replace(",", "."))

        sorted_final_list = [(k, v) for v, k in sorted([(v, k) for k, v in final_list.items()], reverse=self.reversed)]
        print('Info: Total {} products retrieved'.format(len(sorted_final_list)))
        print(sorted_final_list)

        self.draw_top_ten_graph(sorted_final_list[:10])

    def draw_top_ten_graph(self, top_ten_list):
        y = [val[1] for val in top_ten_list]
        x = [key[0][0].rsplit(',')[0] for key in top_ten_list]

        plt.rcParams.update({'font.size': 6, 'figure.figsize': (20, 20)})

        if self.reversed:
            order_text = 'highest'
        else:
            order_text = 'lowest'
        nutrition_text = self.NUTRITION[self.chosen_nutrition_number][0]
        category_text = self.CATEGORY_URLS[int(self.chosen_category_number)][0]
        plt.title('Top 10 {0} {1} products in {2} category'.format(order_text, nutrition_text, category_text))

        plt.xticks(rotation=90)
        plt.scatter(x, y)
        plt.show()


if __name__ == '__main__':
    barbora = BarboraScrapper()
