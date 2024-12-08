import json


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        with open("outputs/great_offers.json", "w") as file:
            json.dump(self.items, file, default=str, indent=4)
