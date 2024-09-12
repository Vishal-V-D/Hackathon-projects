import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D

# Load the prebuilt CIFAR-10 dataset
(train_images, train_labels), (validation_images, validation_labels) = tf.keras.datasets.cifar10.load_data()

# Normalize the images
train_images = train_images / 255.0
validation_images = validation_images / 255.0

# Convert labels to one-hot encoding (since you're using categorical crossentropy)
train_labels = tf.keras.utils.to_categorical(train_labels, 10)
validation_labels = tf.keras.utils.to_categorical(validation_labels, 10)

# Load the base model with pretrained ResNet50 weights
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(32, 32, 3))

# Freeze the base model layers
for layer in base_model.layers:
    layer.trainable = False

# Add custom classification layers
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
x = Dense(512, activation='relu')(x)
predictions = Dense(10, activation='softmax')(x)  # CIFAR-10 has 10 classes

# Create the model
model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model using the CIFAR-10 dataset
model.fit(
    train_images, train_labels,
    epochs=2,  # Number of epochs
    batch_size=32,
    validation_data=(validation_images, validation_labels)
)

# Save the model
model.save(r'C:\Users\vkart\New volume H\defaults\MyDrive\mine\codes\python\learning\AI\cifar10_classification_model.keras')
