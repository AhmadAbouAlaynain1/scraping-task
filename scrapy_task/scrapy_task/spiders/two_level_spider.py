import scrapy

'''
Spider that accesses the two level VC website
Extracts name, description, sectors, and headquarters of each company by accessing nested links in initial page
Then writes them to JSON file
'''


class TwoLevel(scrapy.Spider):
    name = "twoLevel"

    start_urls = ["https://www.anthemis.com/invest/"]

    # Goes through link for each company passing it to the parseSubPage function
    def parse(self, response):
        for company in response.css(".team-member h4"):
            url = company.css("a::attr(href)").get()
            if url is not None:
                yield response.follow(url, self.parseSubPage)

    # returns dictionary of related fields from nested url to be parsed as a list of dictionaries
    def parseSubPage(self, response):
        description = response.css(".wpb_text_column h4 i::text").getall()
        name = response.css("title::text").get().split("|")[0].strip()
        details = response.css(".row_col_wrap_12_inner.col.span_12.left")
        if (description):
            yield {
                "name": name,
                "description": description,
                "sectors": details.css("p::text")[0].get().strip(),
                "headquarters": details.css("p::text")[1].get().strip()
            }
        yield {
            "name": name,
            "description": response.css(".wpb_text_column h4::text").get(),
            "sectors": details.css("p::text")[0].get().strip(),
            "headquarters": details.css("p::text")[1].get().strip()
        }
