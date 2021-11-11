
import numpy as np
from tf_bodypix.api import download_model, load_model, BodyPixModelPaths

from libs import timer

class BodyPix:

    def __init__(
        self, 
        model: BodyPixModelPaths = BodyPixModelPaths.MOBILENET_FLOAT_50_STRIDE_16,
        threshold: float = 0.8
        ):
        """Wrapper for bodypix
        
        Keyword arguments:
        model -- The bodypix model to use (default = MOBILENET_FLOAT_50_STRIDE_16; see tf_bodypix.api.BodyPixModelPaths)
        threshold -- The decision boundary (default = 0.8, range = [0, 1])
        """
        self.bodypix_model = load_model(download_model(model))
        self.threshold = threshold
    
    @timer.time_func
    def get_mask(self, capture: np.array) -> np.array:
        """Get the mask of a person in the provided photo
        
        Keyword arguments:
        capture -- The photo to analyse
        """
        result = self.bodypix_model.predict_single(capture)
        return np.array(result.get_mask(threshold=0.8))
