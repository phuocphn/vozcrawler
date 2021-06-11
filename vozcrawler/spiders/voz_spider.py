import re
import os
import shutil
import scrapy

import random
import string

from vozcrawler.items import VozcrawlerItem
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings

class VozSpider(scrapy.Spider):
    name = "voz"

    def __init__(self, thread_url='', **kwargs):
        self.thread_url = thread_url
        super().__init__(**kwargs)  


    def start_requests(self):
        urls = [self.thread_url, ]
        settings = get_project_settings()
        shutil.rmtree(settings.get('IMAGES_STORE'))
        os.mkdir(settings.get('IMAGES_STORE'))
        if os.path.exists("errors.log"): os.remove("errors.log")
        if os.path.exists("meta.info"): os.remove("meta.info")

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        self.remove_space_fn = lambda x: ''.join(character for character in x if character not in '\r\t\n')


    def parse(self, response):

        # saving topic meta information to file, just too lazy to save it database :))
        if not os.path.exists("meta.info"):
            topic_title = response.xpath("//h1[contains(@class, 'p-title-value')]/text()").get()
            topic_author = response.xpath("//ul[contains(@class, 'listInline listInline--bullet')]/li/a/text()").get()
            topic_created_t = response.xpath("//ul[contains(@class, 'listInline listInline--bullet')]/li/a/time/text()").get()

            with open("meta.info", "w") as f:
                f.write(topic_title + "###" + topic_author + "###" + topic_created_t)

        for message in response.xpath('//article[contains(@class,"message--post")]').getall():
            m_message = self.remove_space_fn(message)
            for match in re.finditer(r"src=\"(/[^\"]*)\"",m_message):
                m_message = m_message.replace(match.group(1), "https://voz.vn" + match.group(1))

            comment_response = HtmlResponse(url="?", body=m_message, encoding='utf-8')
            comment_id = comment_response.xpath('//ul[contains(@class,"message-attribution-opposite")]/li/a/text()')[0].extract()
            comment_id = int(comment_id.strip("#"))

            comment = VozcrawlerItem()
            comment['comment_id'] = comment_id
            cleaned_message = m_message 

            images = []
            for img in comment_response.xpath("//img/@src").getall():
                cleaned_url = img.strip("/")
                file_name = cleaned_url[cleaned_url.rfind("/")+1:] 
                file_name = file_name[:file_name.find("?")]  

                if len(file_name) > 200:
                    file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
                    
                images.append({'url': img, 'name': file_name})
                cleaned_message = cleaned_message.replace(img, "http://127.0.0.1:5000/static/images/" + file_name)

            comment["image_urls"] = images
            comment['comment_content'] = cleaned_message
            yield comment
            # yield {
            #     'comment_id': comment_id,
            #     'comment_content': tidy.parseString(m_message, show_body_only=True,drop_empty_paras=False)
            # }

        next_page = response.xpath('//a[contains(@class,"pageNavSimple-el--next")]/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
