import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# Load the saved model
model_path = r'C:\Users\vkart\My Drive\mine\codes\python\learning\AI\tyre_classification_model.keras'
model = tf.keras.models.load_model(model_path)

# Recompile the model if needed (optional)
# You can modify the optimizer, learning rate, or any other settings here.
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), 
              loss='categorical_crossentropy', 
              metrics=['accuracy'])

# Define the path to the test images
test_image_dir = r'C:\Users\vkart\My Drive\mine\codes\python\learning\AI\dataset'  # Folder with test images

# Define class labels (must match the folder names used during training)
class_labels = ['new_tyre', 'old_tyre']

# Function to preprocess and predict on a single image
def predict_image(image_path):

    # Load the image with target size
    img = image.load_img(image_path, target_size=(224, 224))
    
    # Convert the image to array
    img_array = image.img_to_array(img)
        
    # Expand dimensions to match the input shape for the model
    img_array = np.expand_dims(img_array, axis=0)
        

    # Preprocess the image using ResNet50's preprocessing function
    img_array = tf.keras.applications.resnet50.preprocess_input(img_array)
        

    # Make prediction
    predictions = model.predict(img_array)
        

    # Get the predicted class label
    predicted_class = np.argmax(predictions, axis=1)[0]
        

    return class_labels[predicted_class], predictions
new, old = 0, 0
new_lis, old_lis = [], []
# Iterate over all images in the test image directory
for img_file in os.listdir(test_image_dir):
    if img_file.endswith(('.jpg', '.jpeg', '.png')):  # Check for image file extensions
        img_path = os.path.join(test_image_dir, img_file)
        predicted_class, prediction_probs = predict_image(img_path)
        
        if predicted_class == "new_tyre":
            new += 1
            new_lis += [predicted_class, img_file]
        elif predicted_class == "old_tyre":
            old += 1
            old_lis += [predicted_class, img_file]

        print(f"Image: {img_file}")
        print(f"Predicted Class: {predicted_class}")
        print(f"Prediction Probabilities: {prediction_probs}")
        print("\n\n")
print(f"new: {new}, old: {old}")
print(new_lis, "\n", old_lis)