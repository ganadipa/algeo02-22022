import sys
# import downloader
from api.Web_Scraper import downloader
from pathlib import Path


def runScrape(query, limit):
    # output_dir = Path("../../public/dataset_images/")
    output_dir = Path("public/dataset_images/")
    timeout = 100
    print("[%] Downloading Images to {}".format(str(output_dir)))
    bing = downloader.Bing(query, limit, output_dir, timeout=timeout)
    bing.run()

# path = Path("../../../public/dataset_images/")
# runScrape("car",5,path,60)
