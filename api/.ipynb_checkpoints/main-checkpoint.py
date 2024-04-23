from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

# Initialize the FastAPI app
app = FastAPI()

# Define CORS origins (add or modify origins as needed)
origins = [
    "http://localhost:8001",
    "http://localhost:3000",
    "https://www.cs.drexel.edu",  
]

# Apply CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specify which origins are allowed to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# (the rest of your FastAPI code remains the same)


# Load the TensorFlow model
MODEL = tf.keras.models.load_model('../models')

# Define the class names for prediction
CLASS_NAMES = [
    'Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy',
    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
    'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight',
    'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus',
    'Tomato_healthy'
]

# Utility function to read uploaded file as an image
def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

# Define a route for a simple health check
@app.get("/ping")
async def ping():
    return {"message": "Hello, I'm alive"}

# Define a route to handle image uploads and predictions
@app.post('/predict')
async def predict(file: UploadFile = File(...)):
    bytes = await file.read()
    image = read_file_as_image(bytes)
    img_batch = np.expand_dims(image, 0)
    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions)]
    confidence = np.max(predictions[0]).item()  # Convert numpy.float32 to Python float
    return {"class": predicted_class, "confidence": confidence}

# Run the app with uvicorn
if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
