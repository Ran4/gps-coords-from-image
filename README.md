# Proof of concept, find GPS position based on one or more images

Given an input image, we find the closest image among a stored database of images.
We then look up some meta data about it, and show it as well.

In the default example (see [metadata.py](./metadata.py), we show the GPS coordinates for each image.

This would enable you to for example detect where you are in the world by taking a picture (
assuming that you have a dataset of images with their corresponding GPS positions).

A slightly more complicated algorithm that might increase the accuracy in the GPS example
would be something like:

* Take 5 different images of your surroundings.
* For each such image, find the top 10 nearest images.
* Find the GPS coordinates of all 50 images, then remove the 20 coordinates that are the furthest away from
  the rest.
* Take the average of the remaining 30 coordinates. This is where you are.

## Usage:

### Preparation

* Put image file you want to compare against in `images/`
* For each image file, set some metadata about them in `metadata.py` (update the `metadata_lookup_map`
  variable)
* Put the input image somewhere on disk.

## Running

* Assuming you have poetry and Python 3 installed, install dependencies with `poetry install`
* Run the program: `poetry run python imagesimilarity.py [path/to/your/input_image.jpg]`

## Example output

```bash
$ poetry run python imagesimilarity.py liberty2.jpg
Closest image is: images/liberty0.webp
Metadata: (40.6892, 74.0445) (gps coordinates)
similarity score: 0.9136244058609009
```
