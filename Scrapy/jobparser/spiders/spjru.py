# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
import json


class SpjruSpider(scrapy.Spider):
    name = 'spjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Project%20Manager']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            "//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-dalshe']/@href").get()
        next_page_full = 'https://www.superjob.ru' + next_page
        yield response.follow(next_page_full, callback=self.parse)
        vacancy_link = response.xpath("//a[contains(@class,'icMQ_ _1QIBo')]/@href").getall()
        for link in vacancy_link:
            link_full = 'https://www.superjob.ru' + link
            yield response.follow(link_full, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        # vacancy = response.css("div._3MVeX h1._3mfro::text").extract_first()
        link = response.xpath("//link[@rel='canonical']/@href").get()

        # Остальное вытаскиваем из Json-скрипта
        script = response.xpath("//div[@class = '_1Tjoc _3C60a Ghoh2 UGN79 _1XYex']/script/text()").getall()
        script_json = json.loads(script[0])
        vacancy = script_json['title']
        if 'identifier' in script_json:
            company = script_json['identifier']['name']
        else:
            company = None
        if 'baseSalary' in script_json:
            if 'minValue' in script_json['baseSalary']['value']:
                salary_min = script_json['baseSalary']['value']['minValue']
            else:
                salary_min = None
            if 'currency' in script_json['baseSalary']:
                salary_type = script_json['baseSalary']['currency']
            else:
                salary_type = None
            if 'maxValue' in script_json['baseSalary']['value']:
                salary_max = script_json['baseSalary']['value']['maxValue']
            else:
                salary_max = None
        else:
            salary_min = None
            salary_type = None
            salary_max = None

        salary = {'min': salary_min, 'max': salary_max, 'type': salary_type}

        yield JobparserItem(vacancy_from=self.allowed_domains[0], vacancy=vacancy, salary=salary, company=company,
                            link=link)
