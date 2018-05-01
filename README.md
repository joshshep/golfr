# README #

# Current pipeline
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
* prep resultant square for NN
    * remove border (partial square)
    * reduce noise (similar above)
    * crop
    * downsample
* run NN on sample