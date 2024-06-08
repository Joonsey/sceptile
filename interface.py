import os
import model


module_dir = os.path.dirname(os.path.abspath(__file__))

class SceptileInterface:
    """
    This interface is supposed to be used by external programs

    all features intended to be public to other programs should go through this interface
    """
    def __init__(self):
        self.features = model.PlantVillageDataset(
            root_dir=module_dir + '/data',
            transform=model.PlantVillageDataset.transform
        ).classes
        self.model = model.SimpleCNN.load(module_dir + "/out/model.pth", len(self.features), model.SimpleCNN.device)

    def predict(self, image: str):
        return self.features[int(self.model.predict_image(image, model.PlantVillageDataset.transform))]
