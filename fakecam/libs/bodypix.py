
import numpy as np
from tf_bodypix.api import download_model, load_model, BodyPixModelPaths

class BodyPix:
    # BodyPixModelPaths.MOBILENET_FLOAT_50_STRIDE_16 # Not omega mode : 0.030881166458129883
    # BodyPixModelPaths.RESNET50_FLOAT_STRIDE_16 # Omega mode : 2 powerful
    def __init__(
        self, 
        model: BodyPixModelPaths = BodyPixModelPaths.MOBILENET_FLOAT_50_STRIDE_16,
        ):
        # load model (once)
        self.bodypix_model = load_model(download_model(model))
    
    def get_mask(self, capture) -> np.array:
        result = self.bodypix_model.predict_single(capture)
        return np.array(result.get_mask(threshold=0.75))
