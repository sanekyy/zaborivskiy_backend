import imageio
import numpy as np
from keras.models import load_model


class FigureRecognizer:

    def __init__(self):
        self.model = load_model("model.h5")

    def predict_figure(self, path):
        img = imageio.imread(path)
        img = (img - np.min(img)) / (np.max(img) - np.min(img))
        img = img[np.newaxis, ..., np.newaxis]
        pred_res = self.model.predict(img)
        type = np.argmax(pred_res)

        if type == 0:
            return 3
        elif type == 1:
            return 2
        elif type == 2:
            return 1