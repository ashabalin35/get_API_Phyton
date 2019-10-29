# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=113&st=searchVacancy&text=Project+Manager']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page,callback=self.parse)
        vacancy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()
        for link in vacancy:
            yield response.follow(link,self.vacancy_parse)

    def vacancy_parse (self, response: HtmlResponse):
        vacancy = response.css('div.vacancy-title h1.header::text').extract_first()
        salary_min = response.xpath("//meta[@itemprop='minValue']/@content").get()
        salary_max = response.xpath("//meta[@itemprop='maxValue']/@content").get()
        salary_type = response.xpath("//meta[@itemprop='currency']/@content").get()
        salary = {'min': salary_min, 'max': salary_max, 'type': salary_type}
        company = response.xpath("//meta[@itemprop='name']/@content").get()
        link = response.xpath("//meta[@itemprop='url']/@content").get()

        yield JobparserItem(vacancy_from = self.allowed_domains[0], vacancy=vacancy, salary=salary, company=company, link = link)
