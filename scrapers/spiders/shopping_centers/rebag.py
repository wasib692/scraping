import csv
import json
import scrapy


class RebagSpider(scrapy.Spider):
    name = 'rebag'
    allowed_domains = ['rebag.com']
    start_urls = ['https://www.rebag.com/']
    base_url = ['https://www.rebag.com/']
    url = 'https://services.mybcapps.com/bc-sf-filter/filter/?shop=trendlee.myshopify.com&page=1&limit=50&&build_filter_tree=true'

    def start_requests(self):
        yield scrapy.Request(url=self.url)

    def parse(self, response):
        data = json.loads(response.text).get('products')
        items = []
        for product in data:
            item = dict(
                productId=product.get('id'),
                title=product.get('title'),
                productType=product.get('product_type'),
                price=product.get('price_min'),
                skuId=product.get('skus')[0],
                url=f'{self.base_url[0]}{product.get("handle")}'
            )
            items.append(item)
            print(item)
        headers = ['productId', 'title', 'productType', 'price', 'skuId', 'url']
        with open('rebag.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(items)
