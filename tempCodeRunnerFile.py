
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
# import numpy as np

# # Model load
# model = load_model("complaint_classifier.h5")

# # Labels
# classes = ["garbage", "pothole", "streetlight", "water_leakage"]

# # Test image load
# img = image.load_img("dataset/test_sample.jpg", target_size=(128, 128))
# x = image.img_to_array(img)
# x = np.expand_dims(x, axis=0) / 255.0

# # Predict
# pred = model.predict(x)
# class_index = np.argmax(pred)
# confidence = np.max(pred)

# print(f"Prediction: {classes[class_index]} ({confidence*100:.2f}%)")
