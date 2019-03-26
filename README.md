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

## Step 1 (Setup)

### Python Environment

Using virtualenvwrapper, make a new virtual environment with the python dependecies using

`> mkvirtualenv ferriswheel -r requirements.txt`

### Download Data
To download the data simply run the `download_data.sh` script.

`> bash ./download_data.sh`.

This uses wget to get the json data from the github repository. It then creates an `images/` directory where all the downloaded images will be stored.

### Download Images

Run the `download_images.py` script to loop through the `product_data.json` file and download the required images into the `images/` directory.

## Step 2 (Explore Data)

To see the exploration please look the jupyter notebook `Explore_Data.ipynb`.

Without any gold standard labels to train a vision algorithm, there are two approaches I could have taken. I could started by manually labelling some data to train a statistical model with, or I could begin by exploring the text data. I began by exploring the text descriptions. First, I looked for an exact match of the product category within the description. I found only 21.4% of the descriptions had exact string matches with one of the product categories. 

214 examples wouldn't be enough to train a vision algorithm with. So I started to create a list of alias regexes that would help improve the recall from the exact match baseline. I iterated between adding regexes to the alias list and looking at the data for additional keywords to include.

Once I had increased the recall of my regex based model to 65.7% I decided it was time to begin training a statistical model. At this point, I could have backtracked and tried to hone in on the precision, which I assumed must have dropped after adding the heuristics. I did notice one gross precision issue, where the term 'dressy' was being captured by the 'dress' regex and added a negative regex to negate that case. I could have continued adding such negative regexes and tuning the heuristic model, but I decided that there were more performance gains to be made by training a statistical model from the noisy data I had acquired.

 After a cursory look at the unclassified data in the output csv file I identified that the regex heuristics had captured most of information in the description field. Therefore, I decided to use the image data to train a model.

 I trained a resnet34 model using the fastai library. The training and validation images were the ones I downloaded earlier using the `download_images.py` script. I resized them to 224px x 224px and trained the model over 4 epochs. There is a lot more that I could have done to improve this model. 

 - I could have unfrozen all the layers and fine tuned the entire resnet34 using tiered learning rates (Probably the easiest thing to do if I had access to a GPU machine).
 - I could have tuned the hyperparameters to get the most performant results using k-fold cross validation. 
 - I could have gone back and manually labeled (or used a labeling service like mturk) some examples from the data to get a less noisy dataset, which the model could have learned more from. (Another easy approach if I had more time) 

However, because of time and computational constraints I concluded the model training part of this project after only 4 epochs of training the last few layers and the softmax classification of the resnet34 model. On completion of the training, the resnet34 model achieved an error rate of 34.5%. Of course, this doesn't take into account the noisiness of the training and validation data. It is hard to evaluate how well the model is without gold standard labels. However, after examining the instances where the model did not agree with the first regex match in the description the performance seemed adequate enough to use.

Finally I combined the regex matches and the resnet34 scores to get the final label for the product. The final labels are provided in `final_predictions.json`.

## Special Cases

While working on this project there were a few cases where I was unable to download the image from the provided url. In those cases I had to rely exclusively on the description data.

Additionally, there was some data where the description was either in another language or completely absent. In those cases, the regex did not match anything and I had to rely exclusively on the predictions from the resnet34 model.

In cases where there was no image availale and no decipherable description I defaulted to the 'Others' class.