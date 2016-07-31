#coding:utf-8	
import scrapy
from toutiao_spider.items import ToutiaoSpiderItem
site="http://www.tooopen.com"

class ToutiaoSpider(scrapy.Spider):
	name = "toutiao"
	allowed_domains = ["toutiao.com"]
	start_urls = [
	'http://toutiao.com/articles_news_photography/p1'
	]
	base_class_url = 'http://toutiao.com/articles_news_photography'
	base_url = 'http://toutiao.com'
	maxpage = 500;#允许爬的最大的页数
	category = ['articles_news_photography']

#请求每一个分类,按页数来
	def parse(self,response):
		for ctg in self.category:
			for page in range(0,self.maxpage):
				url = self.base_url+'/'+ctg+'/p'+str(page)
				yield scrapy.Request(url,self.parseNewsHref)

#解析每页新闻列表的地址
	def parseNewsHref(self,response):
		urls = response.xpath("//div[@class='info']//a/@href").extract()
		for url in urls:
			news_url = self.base_url+url
			yield scrapy.Request(news_url,self.parseNews)

#解析具体新闻内容 
	def parseNews(self,response):
		image_urls = resonse.xpath("//div[@class='img-wrap']/@data-src").extract()
		for image_url in image_urls:
			item = ToutiaoSpiderItem()
			item['image_urls'] = image_url
			yield item

		# articles = response.xpath("//div[@id='pagelet-article']")
		# item = NewsSpiderItem()
		# title = articles.xpath("//div[@class='article-header']/h1/text()").extract()[0]
		# tm = articles.xpath("//div[@id='pagelet-article']//span[@class='time']/text()").extract()[0]
		# content = articles.xpath("//div[@class='article-content']//p/text()").extract()

		# if(len(title)!=0 and len(tm)!=0 and len(content)!=0):
		# 	item['title'] = title
		# 	item['time'] = int(time.mktime(time.strptime(tm,'%Y-%m-%d %H:%M')))
		# 	item['url'] = response.url
		# 	cc=''
		# 	if(len(content) != 0):
		# 		for c in content:
		# 			cc = cc+c+'\n'
		# 		item['content'] = cc
		# 		yield item
	# def parse(self, response):
	# 	global site
	# 	imageclassurls=response.xpath('//div[contains(@class,"cell type-list")]/ul/li/a[(contains(@href,"img/97"))]/@href').extract()
	# 	for imageclassurl in imageclassurls:
	# 		print "imageclassurls=",imageclassurl
	# 		yield scrapy.Request(site+imageclassurl.encode("utf-8"),callback=self.parse_dir_contents)
	# 	#yield scrapy.Request(site+imageclassurls[0].encode("utf-8"),callback=self.parse_dir_contents)

	# def	parse_dir_contents(self, response):
	# 	imageurls=response.xpath('//a[@target="_blank" and contains(@href,"http://www.tooopen.com/v")]/@href').extract()
	# 	for imageurl in imageurls:
	# 		print "imageurl=",imageurl
	# 		yield scrapy.Request(imageurl.encode("utf-8"),callback=self.parse_image)		
	# 	nextpage=response.xpath('//span[contains(@class,"page-nav")]/a/@href').extract()
	# 	print "nextpage[-1]=",type(nextpage[-1])
	# 	yield scrapy.Request(site+nextpage[-1].encode("utf-8"),callback=self.parse_dir_contents)
	
	# def	parse_image(self,response):
	# 	image=response.xpath('//div[contains(@class,"pic-box")]/img[contains(@id,"imgView")]/@src').extract()
	# 	print "image=",image
	# 	item = TooopenItem()
	# 	item['image_urls']=image
	# 	yield item
		
#response.xpath('//a[@target="_blank" and contains(@href,"http://www.tooopen.com/v")]/@href').extract() //页面图片

#response.xpath('//div[contains(@class,"cell type-list")]/ul/li/a[contains(@href,"img/88")]/@href').extract()
#response.xpath('//div[contains(@class,"cell type-list")]/ul/li/a[not(contains(@href,"img/88"))]/@href').extract())／／页面地址
#response.xpath('//span[contains(@class,"page-nav")]/a/@href')[-1].extract()／／下一页
