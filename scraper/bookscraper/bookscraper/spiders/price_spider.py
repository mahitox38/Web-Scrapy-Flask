import scrapy

class PriceSpider(scrapy.Spider):   
    name = 'price_spider' # name des Spiders
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html']

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            book_url = response.urljoin(book.css('h3 a::attr(href)').get()) # holt die Detailseite des Buches
            yield scrapy.Request(book_url, callback=self.parse_book) # wechselt zur Buchseite
        
            next_page = response.css('li.next a::attr(href)').get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                yield scrapy.Request(url=next_page_url, callback=self.parse)
    
    def parse_book(self, response):
        rows = response.css('table.table-striped tr')
        availability = 'Nicht Verfügbar'
        upc = ''
        for row in rows:
            header = row.css('th::text').get()
            if header and 'UPC' in header:
                upc = row.css('td::text').get()
            if header and 'Availability' in header:
                availability = row.css('td::text').get().strip()
        category = response.xpath('//ul[@class="breadcrumb"]/li[3]/a/text()').get()
           
            
        yield {
            'category': category,
            'title': response.css('h1::text').get(),
            'upc': upc,
            'price': response.css('.price_color::text').get(),
            'availability': availability,
            'image_url': response.urljoin(response.css('.item.active img::attr(src)').get()),
            'description': response.css('#product_description ~ p::text').get(),
            
        }
