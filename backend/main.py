from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Sign Language API is running"}

@app.get("/model")
def get_models():
    return {
        "models": ["resnet50", "mobilenetv3", "efficientnet", "yolov8", "mediahand_mlp"]
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    features = preprocess(image_bytes)
    pred = model.predict(features)
    return {"prediction": pred}
