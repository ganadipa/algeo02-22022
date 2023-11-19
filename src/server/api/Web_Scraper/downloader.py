import os, sys
import shutil
from pathlib import Path

try:
    from bing import Bing
except ImportError: 
    from .bing import Bing


def download(query,limit,output_dir,timeout):
    
    
    print("[%] Downloading Images to {}".format(str(output_dir)))
    bing = Bing(query, limit, output_dir,timeout=timeout)
    bing.run()

