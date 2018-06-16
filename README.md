# golfr (working title) #
  golfr is a golf scorecard parser developed in Python.

  The end goal is to be able to upload an image and then extract the handwritten scores for each hole. Eventually, this could be encapsulated by a larger application for developing an online golf profile.
## Getting started ##
  * Clone the repo
    ```bash
    git clone https://github.com/joshshep/golfr.git
    ```
  * Install golfr
    ```bash
    cd golfr
    sudo -H pip install -r requirements
    python setup.py develop
    ```
  * Run a test
    ```bash
    python tests/test_classify_cells.py
    ```

## Current pipeline ##
* find grid points
    * adaptive threshold
    * erode
    * dilate
    * vertical lines
    * horizontal lines
    * intersection
    * dilate
    * centroid
* sort grid points into square corners
* prep resultant square for CNN
    * remove border (partial square)
    * reduce noise (similar above)
    * crop
    * downsample
* run CNN on samples
