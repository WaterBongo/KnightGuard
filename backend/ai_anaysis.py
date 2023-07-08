import cv2
import tensorflow as tf
import numpy as np
import os

# Load the image
# image_folder = 'data'
# image_filename = 'image.jpg'
# image_path = os.path.join(image_folder, image_filename)
# image = cv2.imread(image_path)

def check_danger(image_bytes):
    # Convert image bytes to NumPy array
    nparr = np.frombuffer(image_bytes, np.uint8)

    # Load the image 
    # Decodes an ecoded image data from a buffer
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Tensorflow Keras Model
    model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
    
    # Define the class labels
    class_labels = ['Not Dangerous', 'Dangerous']

    # Preprocess the image
    image = cv2.resize(image, (244, 244))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)

    # Make predictions
    predictions = model.predict(image)
    probability = predictions[0][0]
    class_index = np.argmax(predictions)

    # Get the predicted class label
    predicted_label = class_labels[class_index]

    # Determine the danger status based on the probability threshold
    threshold = 0.5
    if probability >= threshold:
        danger_status = 'Dangerous'
    else:
        danger_status = 'Not Dangerous'

    # Return the result
    return {
        'probability': probability,
        'danger_status': danger_status,
        'predicted_label': predicted_label
    }