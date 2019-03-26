#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Downloads the images in order from the product_data.json file,
and adds indexes to the product_data.json file"""
import json
import os
import sys
from urllib import request
from urllib.error import HTTPError

from PIL import Image
from tqdm import tqdm


def clean_image_url(image_url):
  """Clean the image url to retrieve"""
  if image_url.startswith("//"):
    image_url = 'http:' + image_url
  return image_url


def main():
  """Main Function"""
  with open('product_data.json') as fh:
    data = json.load(fh)
    
  for index in tqdm(range(len(data))):
    if 'id' not in data[index]:
      # If id is not already in the datum add it
      data[index]['id'] = index
    if 'image_path' not in data[index]:
      # if image path is not in the datum
      image_url = clean_image_url(data[index]['images_url'])
      image_path = f'images/{index}.jpg'


      if os.path.isfile(image_path):
        # If image path already exists, add it to the datum and continue
        data[index]['image_path'] = image_path
        continue

      try:
        request.urlretrieve(image_url, image_path)
        Image.open(image_path)
        data[index]['image_path'] = image_path
      except (ValueError, HTTPError):
        data[index]['image_path'] = None
        print(f"Couldn't resolve url for index {index} url {image_url}",
              file=sys.stderr)
      except OSError:
        os.remove(image_path)
        data[index]['image_path'] = None
        print(f"Couldn't download image for index {index} url {image_url}",
              file=sys.stderr)
  
  with open('product_data.json', 'w') as fh:
    json.dump(data, fh)


if __name__ == '__main__':
  main()
