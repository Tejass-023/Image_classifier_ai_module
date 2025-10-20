# from icrawler.builtin import GoogleImageCrawler

# # Streetlight
# google_crawler = GoogleImageCrawler(storage={"root_dir": "dataset/streetlight"})
# google_crawler.crawl(keyword="broken streetlight", max_num=200)

# # Water Leakage
# google_crawler = GoogleImageCrawler(storage={"root_dir": "dataset/water_leakage"})
# google_crawler.crawl(keyword="water leakage", max_num=200)



from icrawler.builtin import GoogleImageCrawler

# Garbage
google_crawler = GoogleImageCrawler(storage={"root_dir": "dataset/garbage"})
google_crawler.crawl(keyword="garbage dump", max_num=500)

# aur agar road ke upar garbage chahiye
google_crawler = GoogleImageCrawler(storage={"root_dir": "dataset/garbage"})
google_crawler.crawl(keyword="garbage on road", max_num=500)
