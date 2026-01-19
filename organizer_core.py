import os
import json
import time
import shutil

CATEGORY_FILE = "categories.json"
def load_categories(path=CATEGORY_FILE):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_category_by_ext(ext):
    ext = ext.lower()
    for category, extensions in categories.items():
        if ext in extensions:
            return category
    return "Others"

def move_tofolder(src, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    base = os.path.basename(src)
    dest = os.path.join(dest_dir, base)
    name, ext = os.path.splitext(base)
    counter = 1
    while os.path.exists(dest):
        dest = os.path.join(dest_dir, f"{name} ({counter}){ext}")
        counter += 1
    shutil.move(src, dest)
    return dest

def remove_ansii(text):
    ansii_colors = ["\u001b[31m", "\u001b[32m", "\u001b[33m", "\u001b[34m", "\u001b[0m"]
    for ascii_color in ansii_colors:
        text = text.replace(ascii_color, "")
    return text

def organize_folder(folder_path, logger_callback):
    info = None
    if not os.path.isdir(folder_path):
        info = "\u001b[31m[ \u001b[32m* \u001b[31m] The given folder does not exist..."
        print(info)
        logger_callback(info)
        return
    moved = 0

    info = f"\u001b[33m[ \u001b[32m* \u001b[33m] \u001b[0mStarting file organization process on folder {folder_path}\u001b[0m...\n"
    print(info)
    logger_callback(info)
    time.sleep(2)

    info = "\u001b[32m[ \u001b[34m* \u001b[32m] \u001b[0mEnumerating files in folder..."
    print(info)
    logger_callback(info)
    time.sleep(2)

    try:
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isdir(file_path):
                continue
            _, ext = os.path.splitext(file_path)
            category = get_category_by_ext(ext)
            dest_dir = os.path.join(folder_path, category)
            info = f"\u001b[32m[ \u001b[34m* \u001b[32m] \u001b[0mFound file \u001b[32m{file}\u001b[0m of category {category}\u001b[0m..."
            print(info)
            logger_callback(info)

            info = f"\u001b[33m[ \u001b[32m* \u001b[33m] \u001b[0mMoving file {file} into folder category \u001b[32m{category}\u001b[0m...\n"
            print(info)
            logger_callback(info)
            try:
                new_path = move_tofolder(file_path, dest_dir)
                moved += 1
            except Exception as e:
                info = f"[ \u001b[31m* \u001b[0m] Failed to move file {file}: {e}...\n"
                print(info)
                logger_callback(info)
    except Exception as e:
        info = f"[ \u001b[31m* \u001b[0m] Failed to read folder {folder_path}: {e}...\n"
        print(info)
        logger_callback(info)

    if moved > 0:
        info = f"\u001b[32m[ \u001b[0m* \u001b[32m] Successfully moved {moved} files into different categories...\u001b[0m"
    else:
        info = f"\u001b[32m[ \u001b[0m* \u001b[32m] No files were found to move into categories...\u001b[0m"
    print(info)
    logger_callback(info)
categories = load_categories()
