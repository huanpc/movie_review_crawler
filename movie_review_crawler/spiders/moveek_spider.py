import scrapy
import hashlib
import time

from movie_review_crawler.items import MovieReviewCrawlerItem


class MoveekSpider(scrapy.Spider):
    name = "moveek"
    start_urls = ["https://moveek.com/danh-gia-phim/"]
    allowed_domains = ["moveek.com"]
    main_domain = "https://moveek.com"

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        list_views = response.xpath('//div[@class="panel panel-post panel-feed"]/a')
        for view in list_views:
            url = response.urljoin(view.xpath('@href').extract_first())
            item = MovieReviewCrawlerItem()
            item['url'] = url
            item['url_md5'] = hashlib.md5(str(url).encode("utf-8")).hexdigest()
            item['source'] = self.main_domain
            item['summary_image'] = view.xpath('img/@src').extract_first()
            request = scrapy.Request(url, callback=self.parse_page)
            request.meta['item'] = item
            yield request
        next_page = response.xpath('//a[@class="more"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse_list)

    def parse_page(self, response):
        try:
            item = MovieReviewCrawlerItem(response.meta['item'].copy())
            # title
            item['title'] = response.xpath('//div[@class="post"]/h1/text()').extract_first().strip()
            author_and_time = response.xpath('//div[@class="post"]/div[contains(concat(" ", @class, " "), "meta")]/text()').extract()
            author_and_time = "".join(author_and_time)
            author_and_time = author_and_time.strip()
            if len(author_and_time.split("·")) > 1:
                item['author'] = author_and_time.split("·")[0].strip()
                item['time'] = author_and_time.split("·")[1].strip()
            else:
                item['meta'] = author_and_time

            item['body'] = response.xpath('//div[@class="post"]/div[@class="post-content"]').extract_first().strip()
            item['created_at'] = int(time.time())
            return item
        except Exception as e:
            self.logger.error('Error in spider "<{0}>": {1}.'.format(self.name, e))
