from pathlib import Path
import urllib.request
import urllib
import imghdr
import posixpath
import re


class Bing:
    def __init__(self, query, limit, output_dir,seen,timeout):
        self.query = query
        self.limit = limit
        self.output_dir = output_dir
        self.seen = set()
        self.timeout = timeout
        
    # def save_image(self,link,file_path):
        