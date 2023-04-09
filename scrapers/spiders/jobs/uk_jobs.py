import csv
import json
import scrapy


class Jobs(scrapy.Spider):
    name = 'jobs'
    # allowed_domains = ['rebag.com']
    base_url = ['https://www.civilservicejobs.service.gov.uk/csr/index.cgi']
    url = 'https://www.civilservicejobs.service.gov.uk/csr/index.cgi?SID=cGFnZWNsYXNzPVNlYXJjaCZvd25lcj01MDcwMDAwJm93bmVydHlwZT1mYWlyJnNvcnQ9Y2xvc2luZyZwYWdlYWN0aW9uPXNlYXJjaGNvbnRleHQmcGFnZT0xJmNvbnRleHRpZD0yMzU1OTQ3MCZyZXFzaWc9MTY3NDg4MTk5OS1mZGYxNjUxYTM3NTNkYWY5ZTQxMjg4ZThiNTAyOTJhYjgxNzU1YmU0'

    # start_urls = [url]
    counter = 0
    li=[]

    def start_requests(self):
        yield scrapy.Request(url=self.url)

    def parse(self, response):
        print(response)
        # titles = response.css('.search-results-job-box-title a::attr(title)').extract()
        links = response.css('.search-results-job-box-title a::attr(href)').extract()

        for link in links:
            yield scrapy.Request(link, callback=self.parse_job)

        next_link = response.css('.search-results-paging-menu li a::attr(href)').extract()
        if self.counter < 5:
            yield scrapy.Request(next_link[-1])
            self.counter += 1

    def parse_job(self, response):
        url = 'https://www.civilservicejobs.service.gov.uk/csr/jobs.cgi?jcode={}'
        print('job')
        link = response.css('[class="email"]::attr(href)').get('')

        item = dict(
            jobID=link.split('jcode%3D')[-1].split('.')[0],
            title=response.css('.csr-page-title h1::text').get('')
        )
        item['url'] = 'https://www.civilservicejobs.service.gov.uk/csr/jobs.cgi?jcode={}'.format(item['jobID'])
        print(item)
        self.li.append(item)
        if self.counter==5:
            headers=['jobID','title','url']
            with open('uk_jobs.csv', 'w') as f:  # You will need 'wb' mode in Python 2.x
                w = csv.DictWriter(f, fieldnames=headers)
                w.writeheader()
                w.writerows(self.li)
