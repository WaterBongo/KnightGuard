import torchvision.transforms as T
from PIL import Image
import functools
import random
import torch
import io

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
    prediction = prediction[0]
    try:
      return round(prediction['scores'][0].item(), 3)
    except:
      num = random.random()
      if num > 0.1:
        num *= 0.1
      return round(num, 3)

analyze = functools.partial(predict, model=model)