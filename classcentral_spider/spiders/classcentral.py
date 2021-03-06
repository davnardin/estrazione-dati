from scrapy import Spider
from scrapy.http import Request


class ClasscentralSpider(Spider):
    name = 'classcentral'
    allowed_domains = ['classcentral.com']
    start_urls = ['https://www.classcentral.com/subjects']

    def __init__(self, subject=None):
        self.subject = subject

    def parse(self, response):
        if self.subject:
            subject_url = response.xpath('//a[contains(@title, "' + self.subject +'")]/@href').extract_first()
            absolute_subject_url = response.urljoin(subject_url)
            yield Request(absolute_subject_url, callback=self.parse_subject)
        else:
            self.log('Scraping all subjects.')
            subjects = response.xpath('//h3/a[1]/@href').extract()
            for subject in subjects:
                absolute_subject_url = response.urljoin(subject)
                yield Request(absolute_subject_url, callback=self.parse_subject)

    def parse_subject(self, response):
        subject_name = response.xpath('//h1/text()').extract_first()

        courses = response.xpath('//tr[@itemtype="http://schema.org/Event"]')
        for course in courses:
            course_name = course.xpath('.//*[@itemprop="name"]/text()').extract_first()

            course_url = course.xpath('.//a[@itemprop="url"]/@href').extract_first()   
            absolute_course_url = response.urljoin(course_url)

            yield {'subject_name': subject_name,
                   'course_name': course_name,
                   'course_url': course_url}    
