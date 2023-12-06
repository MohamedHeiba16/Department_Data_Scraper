import scrapy


class DepartSpider(scrapy.Spider):
    name = "depart"
    allowed_domains = ["www.argenprop.com"]
    start_urls = ["https://www.argenprop.com/"]

    def parse(self, response):

        urls = response.xpath("//div[@class='suggested__search-content']/div//a/@href")[8:106]          
        for url in urls:
            relative_url = url.get()           
            yield response.follow(relative_url,callback=self.parse_urls)

    def parse_urls(self,response):

        urls = response.xpath("//div[@class='main__content']/div[2]/div/div/a/@href")
        for url in urls:
            relative_url = url.get()
            yield response.follow(relative_url,callback=self.parse_results)

        next_page_url = response.xpath("//a[@aria-label='Siguiente']/@href").get()
        if next_page_url is not None:
            yield response.follow(next_page_url,self.parse_urls)

    def parse_results(self,response):
        
        title = response.xpath("//div[@class='titlebar']/h3/text()").get()
        price = response.xpath("//div[@class='titlebar']/p/text()").get().strip()
        
        yield {
            "title":title,
            "price":price
               }


            

        
