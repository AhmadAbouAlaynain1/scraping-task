import scrapy

'''
Spider that accesses the one level VC website
Extracts site, name, first investment, and description of each company and writes them to JSON file and TXT file
'''


class OneLevel(scrapy.Spider):
    name = "oneLevel"

    start_urls = ["https://www.usv.com/companies/?status-cat=current"]

    # returns dictionary of related fields to be parsed as a list of dictionaries
    def parse(self, response):
        for company in response.css('div.companies-list div.m__list-row'):
            if (company.css('div.m__list-row__excerpt::text').get() is not None):
                site = self.removeWebPrefix(company.css(
                    'div.m__list-row__col a::attr(href)').get().strip())
                companyName = company.css(
                    'div.m__list-row__col a::text').get().strip()
                firstInvestment = company.css(
                    "div.m__list-row__col:nth-child(3) ::text").get().strip()
                description = company.css(
                    'div.m__list-row__excerpt::text').get().strip()
                yield {
                    'site': site,
                    'companyName': companyName,
                    'firstInvestment': firstInvestment,
                    'description': description,
                }

    def removeWebPrefix(self, x):
        x = x.replace("www.", "")
        x = x.replace("https://", "")
        return x
