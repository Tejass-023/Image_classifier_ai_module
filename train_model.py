import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt

# 1. Data Augmentation (ye model ko robust banayega)
train_datagen = ImageDataGenerator(
    rescale=1.0/255, 
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2  # 80% train, 20% validation
)

# 2. Dataset load karo
train_data = train_datagen.flow_from_directory(
    "dataset/",
    target_size=(224, 224),
    batch_size=32,
    class_mode="categorical",
    subset="training"
)

val_data = train_datagen.flow_from_directory(
    "dataset/",
    target_size=(224, 224),
    batch_size=32,
    class_mode="categorical",
    subset="validation"
)

# 3. Pretrained MobileNetV2 (transfer learning)
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224,224,3))
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation="relu")(x)
predictions = Dense(len(train_data.class_indices), activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=predictions)

# Freeze base_model layers
for layer in base_model.layers:
    layer.trainable = False

# 4. Compile model
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# 5. Train model
history = model.fit(train_data, validation_data=val_data, epochs=10)

# 6. Save model
model.save("civic_eye_model.h5")

# 7. Plot accuracy/loss
plt.plot(history.history["accuracy"], label="train_acc")
plt.plot(history.history["val_accuracy"], label="val_acc")
plt.legend()
plt.show()
