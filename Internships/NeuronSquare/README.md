**Requirement:** 
This project is written in order to scrape the data from a website mentioned below - 
URL:  https://www.midsouthshooterssupply.com/dept/reloading/primers

**Tools used:**
Scrapy Spider

**Attributes Scraped:**
1.	Title – Title of the product.
2.	Manufacturer – i.e. Remington, Winchester, etc.
3.	Price in dollars – Price of the product.
4.	Stock status – i.e. in-stock or out-stock. If in-stock then the value should be true and for out-stock value should be false.
5.	Description – Description of the product.
6.	Delivery Info – Delivery Information available of products details page.

This code scrapes data from all pages and all products. It also does minor formatting of the data that is scraped.

**Execution:**
A separate virtual environment was used for executing this project.

ProxyPoolMiddleware was configured in order to avoid getting blocked from the website during scraping.

Execute below command to scrape data and write output in a file.
> scrapy crawl ShooterSupplySpider -o output.json



