from PIL import Image
from pathlib import Path
import shutil
import os

# исходная папка
input_folder = "data_src"

# новая папка
output_folder = "images_shortened"

# настройки сжатия
max_size = (128, 128)
quality = 10

for root, dirs, files in os.walk(input_folder):

    for file in files:

        input_path = os.path.join(root, file)

        # относительный путь
        relative_path = os.path.relpath(root, input_folder)

        # новая директория
        target_dir = os.path.join(output_folder, relative_path)

        os.makedirs(target_dir, exist_ok=True)

        output_path = os.path.join(target_dir, file)

        try:

            # =====================
            # картинки
            # =====================
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):

                img = Image.open(input_path).convert("RGB")

                # уменьшение размера
                img.thumbnail(max_size)

                # сохраняем
                img.save(
                    output_path,
                    format="JPEG",
                    quality=quality,
                    optimize=True
                )

                print("Compressed:", output_path)

            # =====================
            # текстовые/json файлы
            # =====================
            elif file.lower().endswith((".txt", ".json")):

                shutil.copy2(input_path, output_path)

                print("Copied:", output_path)

        except Exception as e:
            print("Error:", input_path, e)