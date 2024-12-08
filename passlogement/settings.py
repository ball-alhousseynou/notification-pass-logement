# Scrapy settings for SourcingExtonScrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
BOT_NAME = "passlogement"

SPIDER_MODULES = ["passlogement.spiders"]
NEWSPIDER_MODULE = "passlogement.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "passlogement.pipelines.JsonWriterPipeline": 300,
}
