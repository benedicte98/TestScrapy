# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import re
from tld import get_tld

class GatherDetailsSpider(scrapy.Spider):
    name = 'gather_details'

    greedy = True
    email_regex = re.compile(r"[-.a-z]+@[^@\s\.]+\.[.a-z]{2,3}")
    forbidden_keys = ['tel:', 'mailto:', '.jpg', '.pdf', '.png']

    def parse(self, response):
        try:
            html = response.body.decode('utf-8')
        except UnicodeDecodeError:
            return
        body_emails = self.email_regex.findall(html)
        emails = [email for email in body_emails if \
                  get_tld('https://' + email.split('@')[-1], fail_silently=True)]
        yield {
            'emails': list(set(emails)),
            'page': response.request.url
        }
        if self.greedy:
            links = response.xpath("//a/@href").getall()
            # If there are external links, scrapy will block them
            # because of the allowed_domains setting
            for link in links:
                skip = False
                for key in self.forbidden_keys:
                    if key in link:
                        skip = True
                        break
                if skip:
                    continue
                try:
                    yield scrapy.Request(link, callback=self.parse)
                except ValueError:
                    try:
                        yield response.follow(link, callback=self.parse)
                    except:
                        pass
                    skip = False
                    for key in self.forbidden_keys:
                        if key in link:
                            skip = True
                            break
                    if skip:
                        continue

