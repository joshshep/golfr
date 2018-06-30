#constants are defined here

from os.path import dirname, abspath, join

ROOT_DIR = dirname(abspath(__file__))

DFLT_MODEL_PATH = join(ROOT_DIR, 'models/digit_classifier_cnn.model')

DEBUG_OUTPUT_DIR = 'debug/pipeline_imgs'
