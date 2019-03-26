# FerrisWheel

## Description

Takehome project from Ferriswheel using Python 3.7.2. Create classifier that takes as input an image url and a description of a product and outputs the which of the following classes the product belongs to. 

- Dresses
- Tops
- Jeans
- Skirts
- Rompers
- Shoes
- Bags
- Jewelry
- Swimwear
- Intimates
- Others

## Step 1

### Setup Environment

Using virtualenvwrapper, make a new virtual environment with the python dependecies using

`> mkvirtualenv ferriswheel -r requirements.txt`

### Download Data
To download the data simply run the `download_data.sh` script.

`> bash ./download_data.sh`.

This uses wget to get the json data from the github repository. It then creates an `images/` directory where all the downloaded images will be stored.

### Download Images

Run the `download_images.py` script to loop through the `product_data.json` file and download the required images into the `images/` directory.

## Step 2 (Explore data)

To see the exploration please look the jupyter notebook `Explore_Data.ipynb`.

## Project Files


