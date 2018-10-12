商务网站爬虫  
cd tuto  
scrapy crawl mofcom

百度搜索爬虫   
cd tuto  
scrapy crawl baidu

山东质监局网站爬虫  
需要安装scrapy-splash  
pip install scrapy-splash

另外还需要docker运行  
docker run -p 8050:8050 scrapinghub/splash  

cd zhijian  
scrapy crawl zhijian
