from google.cloud import storage
import tensorflow as tf
from PIL import Image
import numpy as np

model = None
interpreter = None
input_index = None
output_index = None

class_names = [
    'Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy',
    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
    'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight',
    'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus',
    'Tomato_healthy'
]

BUCKET_NAME = "main-model"

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")

def predict(request):
        global model
        if model is None :
         download_blob(
            BUCKET_NAME,
            'model_1/',
            '/tmp/model_1/',

        )
        model= tf.keras.models.load_model('/tmp/model_1/')
        image = request.files['file']
        image = np.array(
        Image.open(image).convert("RGB").resize((256, 256)))
        

        image = image/255 # normalize the image in 0 to 1 range

        img_array = tf.expand_dims(image, 0)
        predictions = model.predict(img_array)

        print("Predictions:",predictions)

        predicted_class = class_names[np.argmax(predictions[0])]
        confidence = round(100 * (np.max(predictions[0])), 2)
from google.cloud import storage
import tensorflow as tf
from PIL import Image
import numpy as np
import os

model = None
class_names = [
    'Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy',
    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
    'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight',
    'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus',
    'Tomato_healthy'
]

BUCKET_NAME = "main-model"

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # Initializes a client
    storage_client = storage.Client()
    # Retrieve an existing bucket
    bucket = storage_client.bucket(bucket_name)
    # Construct a blob
    blob = bucket.blob(source_blob_name)
    # Download the blob to a temporary file
    os.makedirs(os.path.dirname(destination_file_name), exist_ok=True)
    blob.download_to_filename(destination_file_name)
    print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")

def load_model(model_path='/tmp/model_1/'):
    global model
    if model is None:
        if not os.path.exists(model_path):
            # Assuming 'model_1' is a directory containing the model files
            download_blob(BUCKET_NAME, 'model_1/', model_path)
        model = tf.keras.models.load_model(model_path)

def predict(request):
    try:
        # Load the model on first request
        load_model()
        
        # Check if an image file was uploaded
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return 'No selected file', 400
        
        image = np.array(Image.open(file).convert("RGB").resize((256, 256)))
        image = image / 255.0  # Normalize the image to 0-1 range
        
        img_array = tf.expand_dims(image, 0)  # Create a batch
        predictions = model.predict(img_array)
        
        predicted_class = class_names[np.argmax(predictions[0])]
        confidence = round(100 * np.max(predictions[0]), 2)
        
        return {"class": predicted_class, "confidence": confidence}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}, 500

        return {"class": predicted_class, "confidence": confidence}
        