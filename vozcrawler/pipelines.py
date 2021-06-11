# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import os
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
import shutil
from io import BytesIO

class CustomImageNamePipeline(ImagesPipeline): 

    def get_media_requests(self, item, info):
        for image in item.get('image_urls', []):
            yield scrapy.Request(image["url"], meta={'image_name': image["name"]})

    def file_path(self, request, response=None, info=None):
        return request.meta['image_name']

    def convert_image(self, image, size=None):
        ORIGINAL_FORMAT = image.format
        # if image.format == 'PNG' and image.mode == 'RGBA':
        #     #background = self._Image.new('RGBA', image.size, (255, 255, 255))
        #     #background.paste(image, image)
        #     #image = background.convert('RGB')
        #     pass
        # elif image.mode == 'P':
        #     image = image.convert("RGBA")
        #     background = self._Image.new('RGBA', image.size, (255, 255, 255))
        #     background.paste(image, image)
        #     image = background.convert('RGB')
        # elif image.mode != 'RGB':
        #     image = image.convert('RGB')

        # if size:
        #     image = image.copy()
        #     image.thumbnail(size, self._Image.ANTIALIAS)

        buf = BytesIO()
        image.save(buf, ORIGINAL_FORMAT)
        return image, buf


class SQLitePipeline:

    def __init__(self):
        self.db_name = 'database.db'

    def open_spider(self, spider):
        if os.path.exists(self.db_name): os.remove(self.db_name)
        if os.path.exists("errors.log"): os.remove("errors.log")

        self.client = sqlite3.connect(self.db_name)
        self.client.execute("CREATE TABLE COMMENT (ID INT PRIMARY KEY NOT NULL, CONTENT LONGTEXT NOT NULL);")
        self.client.commit()

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            self.client.execute("INSERT INTO COMMENT (ID, CONTENT) \
                            VALUES ({}, '{}' )".format(item['comment_id'], item['comment_content']));
            self.client.commit()
        except:
            with open('errors.log', 'w') as f:
                f.write("#" + str(item['comment_id']))
                f.write("\n")

        return item