import tensorflow as tf
from tensorflow.keras import models, layers
import matplotlib.pyplot as plt

# Constants
IMAGE_SIZE = 256
BATCH_SIZE = 32
DATASET_PATH = "PlantVillage"
EPOCHS = 50


def load_dataset(path, image_size, batch_size):
    """Load and preprocess the image dataset."""
    dataset = tf.keras.preprocessing.image_dataset_from_directory(path, shuffle=True, image_size=(image_size, image_size), batch_size=batch_size)
    return dataset


def display_classes(dataset):
    """Print the classes in the dataset."""
    class_names = dataset.class_names
    print(f"Our all {len(class_names)} classes:\n{class_names}")
    print(f"\nTotal number of datasets:\n{len(dataset)}")


def display_image_details(dataset):
    """Print the details of the first batch of images in the dataset."""
    for image_batch, label_batch in dataset.take(1):
        print(f"\nImage details(batch size, pixel, pixel, channel=RGB):\n{image_batch.shape}")
        print(f"\nLabel number:\n{label_batch.numpy()}")


def visualize_images(dataset, class_names):
    """Visualize the first batch of images in the dataset."""
    plt.figure(figsize=(60, 40))
    for image_batch, label_batch in dataset.take(1):
        for i in range(15):
            plt.subplot(3, 5, i + 1)
            plt.imshow(image_batch[i].numpy().astype("uint8"))
            plt.title(class_names[label_batch[i]])
            plt.axis("off")
        plt.show()


"""TO DO: Data Visualization"""
# Load and preprocess the dataset
dataset = load_dataset(DATASET_PATH, IMAGE_SIZE, BATCH_SIZE)

# Display the classes in the dataset
display_classes(dataset)

# Display the details of the first batch of images
display_image_details(dataset)

# Visualize the first batch of images
visualize_images(dataset, dataset.class_names)
