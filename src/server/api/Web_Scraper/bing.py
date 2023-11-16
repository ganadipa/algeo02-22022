from pathlib import Path
import urllib.request
import urllib
import imghdr
import posixpath
import re


class Bing:
    def __init__(self, query, limit, output_dir,timeout):
        self.download_count = 0
        self.query = query
        self.limit = limit
        self.output_dir = output_dir
        self.seen = set()
        self.timeout = timeout
        
        self.page_counter = 0
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'
        }
        
    def save_image(self,link,file_path):
        request = urllib.request.Request(link, None, self.headers)
        image = urllib.request.urlopen(request, timeout=self.timeout).read()
        if not imghdr.what(None, image):
            print('[Error]Invalid image, not saving {}\n'.format(link))
            raise ValueError('Invalid image, not saving {}\n'.format(link))
        with open(str(file_path), 'wb') as f:
            f.write(image)


    def download_image(self,link):
        self.download_count += 1
        
        try:
            path = urllib.parse.urlsplit(link).path
            filename = posixpath.basename(path).split('?')[0]
            file_type = filename.split(".")[-1]
            if file_type.lower() not in [ "jpeg", "png", "jpg"]:
                file_type = "jpg"
                
            print("[%] Downloading Image #{} from {}".format(self.download_count, link))
                
            self.save_image(link, self.output_dir.joinpath("Image_{}.{}".format(
                str(self.download_count), file_type)))
            
            print("[%] File Downloaded !\n")
            
        except Exception as e:
            self.download_count -= 1
            print("[!] Issue getting: {}\n[!] Error:: {}".format(link, e))
            
            
    def run(self):
        while self.download_count < self.limit:
            print('\n\n[!!]Indexing page: {}\n'.format(self.page_counter + 1))
            request_url = 'https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(self.query) \
                          + '&first=' + str(self.page_counter) + '&count=' + str(self.limit) \
                          + '&adlt='  + '&qft='
                          
            #CHECK KEMUNGKINAN EROR
            request = urllib.request.Request(request_url, None, headers=self.headers)
            response = urllib.request.urlopen(request)
            html = response.read().decode('utf8')
            if html ==  "":
                print("[%] No more images are available")
                break
            links = re.findall('murl&quot;:&quot;(.*?)&quot;', html)
            
         
            print("[%] Indexed {} Images on Page {}.".format(len(links), self.page_counter + 1))
            print("\n===============================================\n")

            for link in links:
                if self.download_count < self.limit and link not in self.seen:
                    self.seen.add(link)
                    self.download_image(link)

            self.page_counter += 1
        print("\n\n[%] Done. Downloaded {} images.".format(self.download_count))
         