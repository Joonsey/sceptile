import os
import zmq
import model

module_dir = os.path.dirname(os.path.abspath(__file__))


class SceptileServer:
    def __init__(self) -> None:
        self.features = ['Strawberry___healthy', 'Apple___Apple_scab', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Apple___Cedar_apple_rust', 'Grape___Esca_(Black_Measles)', 'Tomato___Late_blight', 'Grape___healthy', 'Tomato___Leaf_Mold', 'Cherry_(including_sour)___Powdery_mildew', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Corn_(maize)___Northern_Leaf_Blight', 'Squash___Powdery_mildew', 'Tomato___Early_blight', 'Potato___healthy', 'Tomato___Tomato_mosaic_virus', 'Corn_(maize)___healthy', 'Tomato___healthy', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Peach___Bacterial_spot', 'Grape___Black_rot', 'Pepper,_bell___healthy', 'Pepper,_bell___Bacterial_spot', 'Tomato___Septoria_leaf_spot', 'Apple___healthy', 'Corn_(maize)___Common_rust_', 'Potato___Early_blight', 'Tomato___Target_Spot', 'Soybean___healthy', 'Cherry_(including_sour)___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Apple___Black_rot', 'Tomato___Bacterial_spot', 'Blueberry___healthy', 'Strawberry___Leaf_scorch', 'Peach___healthy', 'Raspberry___healthy', 'Potato___Late_blight', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)']
        self.model = model.SimpleCNN.load(module_dir + "/out/model.pth", len(self.features), model.SimpleCNN.device)

        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://*:5555")

    def run(self):
        while True:
            message = self.socket.recv()
            l = self.model.predict_image(message.decode(), model.PlantVillageDataset.transform)
            r = self.features[int(l)]
            self.socket.send(r.encode())

server = SceptileServer()
server.run()
