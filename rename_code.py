import os

# Dataset ka root folder
dataset_dir = r"C:\Users\tejas\OneDrive\ドキュメント\2nd year\edi_2nd year\dataset"

# Har class folder ke liye loop
for folder in os.listdir(dataset_dir):
    folder_path = os.path.join(dataset_dir, folder)

    if os.path.isdir(folder_path):  # agar folder hai to
        for i, filename in enumerate(os.listdir(folder_path)):
            file_ext = os.path.splitext(filename)[1]  # extension (.jpg, .png)
            old_path = os.path.join(folder_path, filename)
            new_filename = f"{folder}_{i+1}{file_ext}"
            new_path = os.path.join(folder_path, new_filename)

            os.rename(old_path, new_path)

print("✅ All images renamed successfully!")
