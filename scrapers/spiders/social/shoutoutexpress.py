import csv
import json
import scrapy


class RebagSpider(scrapy.Spider):
    name = 'shoutout'
    start_urls = ['https://shoutoutexpress.com/']
    base_url = ['https://shoutoutexpress.com/']
    lis = []
    url = 'https://shoutoutexpress.com/listing?type%5B0%5D=model&category%5B0%5D=6&gender=female&platforms%5B0%5D=3&page=2'

    def stat_requests(self):
        yield scrapy.Request(url=self.url)

    def parse(self, response):
        print(response)
        for i in response.css('.job-listing'):
            item = dict(
                url=i.css('::attr(href)').get(),
                name=i.css('.job-listing-company::text').get('').strip(),
                userName=i.css('.job-listing-title::text').get('').strip())
            keys = [e for e in i.css('.job-listing-footer li i::attr(class)').extract() if e.strip()]
            values = [e.strip() for e in i.css('.job-listing-footer li::text').extract() if e.strip()]
            info = dict(zip(keys, values))
            item['twitterFollowers'] = info.get('icon-brand-twitter')
            item['instagramFollowers'] = info.get('icon-brand-instagram')
            item['facebookFollowers'] = info.get('icon-brand-facebook')
            yield scrapy.Request(i.css('::attr(href)').get(), callback=self.parse_profile, meta=dict(item=item))

    def parse_profile(self, response):
        print("profile")
        item = response.meta['item']
        item.update(
            facebookStory=response.xpath(
                '//h3[contains(text(),"Facebook Story")]/parent::div/parent::div/following::div/strong/text()').get(
                '').strip(),
            facebookFeedPost=response.xpath(
                '//h3[contains(text(),"Facebook Feed Post")]/parent::div/parent::div/following::div/strong/text()').get(
                '').strip(),
            twitterPost=response.xpath(
                '//h3[contains(text(),"Twitter Post")]/parent::div/parent::div/following::div/strong/text()').get(
                '').strip(),
            twitterRetweet=response.xpath(
                '//h3[contains(text(),"Twitter Retweet")]/parent::div/parent::div/following::div/strong/text()').get(
                '').strip()
        )
        print(item)
        self.lis.append(item)
        print(len(self.lis))
        if len(self.lis)==15:
            headers = ['url', 'name', 'userName', 'twitterFollowers', 'instagramFollowers', 'facebookFollowers',
                       'facebookStory', 'facebookFeedPost', 'twitterPost', 'twitterRetweet']
            print(len(self.lis))
            with open('shoutout.csv', 'w',encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(self.lis)

