"""Helper function to download an image given an url and the save location.
Returns an error if fails to download. 1 otherwise."""

import urllib.request

__author__ = "partha das"
__version__ = "1.0.0"

def downloadImages(img_link, save_location):
    """Download the image linked.
    @Params:
        img_link: url of the image to be downloaded
        save_location: relative path to the save location for the file
    """

    try:
        urllib.request.urlretrieve(img_link, save_location)
        return 1
    except Exception as e:
        return e

if __name__ == "__main__":
    ret = downloadImages("https://pbs.twimg.com/profile_images/2767813753/c934648cb2a0ef186c678beaa240721a.gif",
                   "big.gif")
    print(ret)
    ret = downloadImages("http://hellow.world.jpg",
                   "world.gif")
    print(ret)

