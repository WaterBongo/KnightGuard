import io
import torch
from PIL import Image
import torchvision.transforms as T

# Load the model
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
LOAD_MODEL_VERSION = "1.0a"
LOAD_MODEL_FILENAME = "weapon_trained_model-"+LOAD_MODEL_VERSION+".pt"
LOAD_DIR = './'
model = torch.load(LOAD_DIR+LOAD_MODEL_FILENAME, map_location=device)
model.eval()

def predict(image_byte, model):
    image = Image.open(io.BytesIO(image_byte)).convert("RGB")
    transform = T.Compose([T.ToTensor()])
    image = transform(image).to(device)
    image = image.unsqueeze(0)

    model = model.to(device)
    model.eval()
    with torch.no_grad():
        prediction = model(image)
    return prediction[0]

# Ask for an input image
if __name__ == "__main__":
    image_path = input("Please enter your image path: ")
    #open and get the bytes
    with open (image_path,"rb")as f :
        imgbytes =f.read()
    # Perform the prediction and print the result
    prediction = predict(imgbytes, model)
    safety = round(prediction['scores'][0].item(),3)
    print(safety)