import scrapy


class ShooterSupplySpider(scrapy.Spider):
    name = "ShooterSupplySpider"
    start_urls = [
        'https://www.midsouthshooterssupply.com/dept/reloading/primers'
    ]

    def parse(self, response):

        all_products_data = response.css("div.product-container div#Div1")

        for idx, product in enumerate(all_products_data):
            product_title = product.css(".catalog-item-name::text").extract()
            product_manufacturer = product.css(".catalog-item-brand::text").extract()
            product_price = product.css(".price span::text").extract()
            product_in_stock_status = product.css("span.status span::text").extract()

            product_price = self.get_product_price_without_dollar_sign(product_price)
            product_in_stock_status = self.get_product_in_stock_status_boolean_value(product_in_stock_status)

            details_page = response.css("a.catalog-item-name::attr(href)").get()

            if details_page is not None:
                yield response.follow(details_page, callback=self.parse_details_page, dont_filter=True,
                                      meta={'title': product_title,
                                            'manufacturer': product_manufacturer,
                                            'price': product_price,
                                            'stock': product_in_stock_status})

        next_page = response.css("span#MainContent_dpProductsBottom a:nth-child(6)::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_details_page(self, response):
        product_title = response.meta['title']
        product_manufacturer = response.meta['manufacturer']
        product_price = response.meta['price']
        product_in_stock_status = response.meta['stock']

        product_description = response.css("section.page-content div#description::text").extract()
        product_description = self.get_clean_product_description(product_description)

        all_product_delivery_info = response.css("div#delivery-info ul")
        product_delivery_info = ""

        for del_info in all_product_delivery_info:
            temp_delivery_info = del_info.css("li::text").extract()
            for temp_del_info_element in temp_delivery_info:
                if product_delivery_info != "":
                    product_delivery_info = product_delivery_info + "_" + temp_del_info_element
                else:
                    product_delivery_info = temp_del_info_element

        yield {
            'title': product_title,
            'manufacturer': product_manufacturer,
            'price': product_price,
            'stock': product_in_stock_status,
            'description': product_description,
            'delivery_info': product_delivery_info
        }

    def get_product_price_without_dollar_sign(self, product_price):
        for idx in range(len(product_price)):
            product_price[idx] = float(product_price[idx].replace("$", ""))
        return product_price

    def get_product_in_stock_status_boolean_value(self, product_in_stock_status):
        for idx in range(len(product_in_stock_status)):
            if product_in_stock_status[idx] == "Out of Stock":
                product_in_stock_status[idx] = False
            else:
                product_in_stock_status[idx] = True
        return product_in_stock_status

    def get_clean_product_description(self, product_description):
        list_from_tuple = list(product_description)
        output_product_description = ""
        for idx in range(len(list_from_tuple)):
            list_from_tuple[idx] = list_from_tuple[idx].replace("\r\n", "")
            list_from_tuple[idx] = list_from_tuple[idx].strip()
            if len(list_from_tuple[idx]) > 0:
                if output_product_description == "":
                    output_product_description = list_from_tuple[idx]
                else:
                    output_product_description = output_product_description + "_" + list_from_tuple[idx]
        return output_product_description
