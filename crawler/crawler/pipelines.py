# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
from crawler.items import UserItem, MovieItem, ReviewItem


class ExportPipeline:
    def open_spider(self, spider):
        self.exporters = {}
        self.seen = {}

    def close_spider(self, spider):
        for exporter in self.exporters.values():
            exporter.finish_exporting()
            exporter.file.close()

    def process_item(self, item, spider):
        if isinstance(item, UserItem):
            name = "user"
            columns = ["user_id", "name"]
            id = item["user_id"]
        elif isinstance(item, MovieItem):
            name = "movie"
            columns = ["movie_id", "title"]
            id = item["movie_id"]
        elif isinstance(item, ReviewItem):
            name = "review"
            columns = ["user_id", "movie_id", "point"]
            id = (item["user_id"], item["movie_id"])
        else:
            raise DropItem

        if name not in self.exporters:
            f = open(f"{name}.csv", "wb")
            exporter = CsvItemExporter(f, fields_to_export=columns)
            exporter.start_exporting()
            self.exporters[name] = exporter
            self.seen[name] = set()

        if id in self.seen[name]:
            raise DropItem

        self.seen[name].add(id)
        self.exporters[name].export_item(item)
        return item
