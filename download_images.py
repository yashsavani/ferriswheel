#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Downloads the images in order from the product_data.json file,
and adds indexes to the product_data.json file"""
import json
import sys
from urllib import request
from urllib.error import HTTPError

from tqdm import tqdm


def main():
  """Main Function"""
  with open('product_data.json') as fh:
    data = json.load(fh)
    
  for index in tqdm(range(len(data))):
    if 'id' not in data[index]:
      data[index]['id'] = index
    if 'image' not in data[index]:
      image_url = data[index]['images_url']
      if image_url.startswith("//"):
        image_url = 'http:' + image_url
      image_path = f'images/{index}.jpg'

      try:
        request.urlretrieve(image_url, image_path)
        data[index]['image'] = image_path
      except (ValueError, HTTPError):
        data[index]['image'] = None
        print(f"Couldn't resolve url for index {index} url {image_url}",
              file=sys.stderr)
  
  with open('product_data.json', 'w') as fh:
    json.dump(data, fh)


if __name__ == '__main__':
  main()
