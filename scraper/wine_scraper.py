import requests
import html
from bs4 import BeautifulSoup
import logging
import re
import json
import pprint


class WineScapper:
    BASE_URL = "https://www.wine.com.br/vinhos/cVINHOS"
    
    def __init__(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filename='wine_scraper.log',
                            filemode='w')
        self.logger = logging.getLogger(__name__)
    
    def scraper(self, start_page=1, end_page=None):
        wine_products = []
        page = start_page
        while end_page is None or page <= end_page:
            html_content = self._get_page(page)
            page_products = self._parse_page(html_content)
            if not page_products:  # Verifica se a página não contém produtos
                break  # Sai do loop se não houver produtos
            wine_products.extend(page_products)
            page += 1
        return wine_products
    
    def _get_page(self, page_number):
        url = f"{self.BASE_URL}-p{page_number}.html"
        print (url)
        response = requests.get(url)
        response.raise_for_status() # Lança uma exceção para respostas não bem-sucedidas
        return response.text
    
    def _parse_page(self, html_content):
        """analisa o html de uma pagina e extrai os dados dos vinhos
        """
        all_products = []
        soup = BeautifulSoup(html_content, 'html.parser')
        produtos = soup.find_all("article", class_="ProductDisplay ProductDisplay--vertical")
        dados_dos_produtos = []
        for produto in produtos:
            # Extrair título
            titulo_div = produto.find("div", class_="ProductDisplay-name")
            titulo = titulo_div.find("h2").text if titulo_div else ""
            # Encontrar o elemento <price-box>
            price_box = produto.find("price-box")
            if price_box:
                product_data_str = price_box.get(':product', '{}')
                # Limpar e converter a string para formato JSON
                # Remover caracteres inválidos e substituir aspas simples por aspas duplas
                product_data_str = re.sub(r"(\w+):", r'"\1":', product_data_str)  # Adicionar aspas em chaves
                product_data_str = product_data_str.replace("'", '"')  # Substituir aspas simples por duplas
                try:
                    product_data = json.loads(product_data_str)
                    dados_dos_produtos.append({
                        "productSku": product_data.get('productSku', ''),
                        "clubPrice": product_data.get('clubPrice', ''),
                        "listPrice": product_data.get('listPrice', ''),
                        "salePrice": product_data.get('salePrice', ''),
                        "productType": product_data.get('productType', ''),
                        "title": titulo
                    })
                except json.JSONDecodeError:
                    print("Erro ao decodificar JSON para produto:", titulo)
        pprint.pprint(dados_dos_produtos)
        return "data"


scraper = WineScapper()
scraper.scraper
        
        


    
