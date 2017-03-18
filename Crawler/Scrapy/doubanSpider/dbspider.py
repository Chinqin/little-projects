import scrapy
from dbMovie.items import DbmovieItem
from scrapy.http import Request


class DBbadmovies(scrapy.Spider):
    name = 'dbBadMovies'
    start_urls = ["https://movie.douban.com/tag/%E7%83%82%E7%89%87?start=0&type=T"]
    #url = "https://movie.douban.com/tag/%E7%83%82%E7%89%87?start=0&type=T"

    def parse(self, response):
        item = DbmovieItem()
        tree = scrapy.Selector(response)

        Movies = tree.xpath('//div[@class="article"]')
        for Movie in Movies:
            movieName = Movie.xpath('/div[@class=""]/a/text()').extract()[0]
            movieInfo = Movie.xpath('/div[@class=""]/p/text()').extract()[0]

            Performer, Nation, Director, movieTime, Category, Playwright, Language = movieInfo.split('/')[]

            Rating = Movie.xpath('/div[@class="star clearfix"]/span[2]/text()').extract()[0]

            item['movieName'] = movieName
            item['movieInfo'] = movieInfo
            item['Rating'] = Rating
            yield item

    def modify_realtime_request(self, request):
        request.meta["dont_redirect"] = True
        return request

        test for two pages
        next_link = tree.xpath('//div[@class="article"]/div[2]/a[1]/@href').extract()[0]
        print next_link
        yield Request(next_link, callback=self.parseDB)

            next_link = tree.xpath('//span[@class="next"]/link/@href').extract()
            if next_link:
                next_link = next_link[0]
                print next_link
                yield Request(self.url + next_link, callback=self.parseDB)