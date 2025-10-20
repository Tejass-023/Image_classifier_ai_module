


# import numpy as np
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image

# # 1. Trained model load karo
# model = load_model("civic_eye_model.h5")

# # 2. Classes define karo
# classes = ["garbage", "pothole", "streetlight", "water_leakage"]

# # 3. Test image ka path
# img_path = "dataset\water_leakage\water_leakage_7.jpg"   # yaha ek image dalni hai test ke liye
# img = image.load_img(img_path, target_size=(224,224))
# img_array = np.expand_dims(image.img_to_array(img) / 255.0, axis=0)

# # 4. Prediction
# prediction = model.predict(img_array)
# predicted_class = np.argmax(prediction, axis=1)[0]

# print("Prediction:", classes[predicted_class])
# print("Confidence:", float(np.max(prediction)))


# confidence = float(np.max(prediction)) * 100
# print(f"Prediction: {classes[predicted_class]}")
# print(f"Confidence: {confidence:.2f}%")







import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import seaborn as sns
import random
import time

# 1️⃣ Load trained model
print("🔁 Loading your trained Civic Eye AI model...")
model = load_model("civic_eye_model.h5")
print("✅ Model loaded successfully!\n")

# 2️⃣ Define the categories
classes = ["garbage", "pothole", "streetlight", "water_leakage"]

# 3️⃣ Load image for testing
img_path = r"dataset\water_leakage\water_leakage_7.jpg"  # 👈 test image path here
img = image.load_img(img_path, target_size=(224, 224))
img_array = np.expand_dims(image.img_to_array(img) / 255.0, axis=0)

# 4️⃣ Predict
print("🧠 AI is analyzing the image...")
time.sleep(1)
prediction = model.predict(img_array)
predicted_class = np.argmax(prediction, axis=1)[0]
confidence = float(np.max(prediction)) * 100

# 5️⃣ Generate fun color for output
colors = ['🟩', '🟦', '🟨', '🟧', '🟥', '🟪']
chosen_color = random.choice(colors)

# 6️⃣ Display results
print("\n" + "="*45)
print(f"🤖 Prediction Summary ({chosen_color})")
print("="*45)
print(f"📂 Image Path     : {img_path}")
print(f"🔎 Predicted Class: {classes[predicted_class].upper()}")
print(f"📊 Confidence     : {confidence:.2f}%")
print("-"*45)

# 7️⃣ Probability Table
for i, cls in enumerate(classes):
    print(f"{cls.capitalize():<15} ➜ {prediction[0][i]*100:.2f}%")

print("="*45)
if confidence >= 90:
    print("✅ High confidence prediction — AI is sure about it!")
elif confidence >= 70:
    print("⚠️ Medium confidence — looks correct but verify once.")
else:
    print("❌ Low confidence — image might be unclear or poor quality.")
print("="*45)

# 8️⃣ Plot Bar Graph
plt.figure(figsize=(8, 5))
sns.barplot(x=classes, y=prediction[0], palette="coolwarm")
plt.title(f"Prediction Confidence Levels\n(Predicted: {classes[predicted_class]})", fontsize=12)
plt.ylabel("Probability")
plt.xlabel("Classes")
plt.show()

# 9️⃣ Plot Pie Chart (visual summary)
plt.figure(figsize=(6,6))
plt.pie(prediction[0], labels=classes, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("coolwarm", len(classes)))
plt.title("AI Confidence Distribution")
plt.show()

# 🔟 Show image with prediction overlay
plt.imshow(image.load_img(img_path))
plt.title(f"🧠 {classes[predicted_class].upper()} ({confidence:.2f}%)", fontsize=14, color='green')
plt.axis("off")
plt.show()

print("\n✨ Civic Eye AI Analysis Complete! ✨")
