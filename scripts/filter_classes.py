import os

# 1. Define your original 120 classes EXACTLY as they were ordered
ORIGINAL_CLASSES = [
    'Akabare Khursani', 'Apple', 'Artichoke', 'Ash Gourd -Kubhindo-', 'Asparagus -Kurilo-', 'Avocado', 'Bacon', 'Bamboo Shoots -Tama-', 'Banana', 'Beans', 'Beaten Rice -Chiura-', 'Beef', 'Beetroot', 'Bethu ko Saag', 'Bitter Gourd', 'Black Lentils', 'Black beans', 'Bottle Gourd -Lauka-', 'Bread', 'Brinjal', 'Broad Beans -Bakullo-', 'Broccoli', 'Buff Meat', 'Butter', 'Cabbage', 'Capsicum', 'Carrot', 'Cassava -Ghar Tarul-', 'Cauliflower', 'Chayote-iskus-', 'Cheese', 'Chicken', 'Chicken Gizzards', 'Chickpeas', 'Chili Pepper -Khursani-', 'Chili Powder', 'Chowmein Noodles', 'Cinnamon', 'Coriander -Dhaniya-', 'Corn', 'Cornflakec', 'Crab Meat', 'Cucumber', 'Egg', 'Farsi ko Munta', 'Fiddlehead Ferns -Niguro-', 'Fish', 'Garden Peas', 'Garden cress-Chamsur ko saag-', 'Garlic', 'Ginger', 'Green Brinjal', 'Green Lentils', 'Green Mint -Pudina-', 'Green Peas', 'Green Soyabean -Hariyo Bhatmas-', 'Gundruk', 'Ham', 'Ice', 'Jack Fruit', 'Ketchup', 'Lapsi -Nepali Hog Plum-', 'Lemon -Nimbu-', 'Lime -Kagati-', 'Long Beans -Bodi-', 'Masyaura', 'Milk', 'Minced Meat', 'Moringa Leaves -Sajyun ko Munta-', 'Mushroom', 'Mutton', 'Nutrela -Soya Chunks-', 'Okra -Bhindi-', 'Olive Oil', 'Onion', 'Onion Leaves', 'Orange', 'Palak -Indian Spinach-', 'Palungo -Nepali Spinach-', 'Paneer', 'Papaya', 'Pea', 'Pear', 'Pointed Gourd -Chuche Karela-', 'Pork', 'Potato', 'Pumpkin -Farsi-', 'Radish', 'Rahar ko Daal', 'Rayo ko Saag', 'Red Beans', 'Red Lentils', 'Rice -Chamal-', 'Sajjyun -Moringa Drumsticks-', 'Salt', 'Sausage', 'Snake Gourd -Chichindo-', 'Soy Sauce', 'Soyabean -Bhatmas-', 'Sponge Gourd -Ghiraula-', 'Stinging Nettle -Sisnu-', 'Strawberry', 'Sugar', 'Sweet Potato -Suthuni-', 'Taro Leaves -Karkalo-', 'Taro Root-Pidalu-', 'Thukpa Noodles', 'Tofu', 'Tomato', 'Tori ko Saag', 'Tree Tomato -Rukh Tamatar-', 'Turnip', 'Wallnut', 'Water Melon', 'Wheat', 'Yellow Lentils', 'kimchi', 'mayonnaise', 'noodle', 'seaweed'
]

# 2. Define the 33 common classes you decided to keep
KEPT_CLASSES = [
    'Beef', 'Chicken', 'Egg', 'Fish', 'Mutton', 'Pork', 'Tofu',
    'Bread', 'noodle', 'Potato', 'Rice -Chamal-',
    'Garlic', 'Ginger', 'Onion', 'Tomato',
    'Apple', 'Banana', 'Broccoli', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Cucumber', 'Lemon -Nimbu-', 'Mushroom', 'Orange',
    'Butter', 'Cheese', 'Milk', 'Olive Oil', 'Paneer', 'Salt', 'Soy Sauce'
]

# 3. Create a translation dictionary mapping: { Old_ID: New_ID }
class_remap = {}
for new_idx, class_name in enumerate(KEPT_CLASSES):
    old_idx = ORIGINAL_CLASSES.index(class_name)
    class_remap[old_idx] = new_idx

def filter_label_file(file_path):
    """Reads a YOLO text file, filters out dropped classes, and remaps kept ones."""
    if not os.path.exists(file_path):
        return

    new_lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split()
        if not parts:
            continue
        
        old_class_id = int(parts[0])
        
        # If the class is in our kept list, convert its ID and save the line
        if old_class_id in class_remap:
            new_class_id = class_remap[old_class_id]
            parts[0] = str(new_class_id)
            new_lines.append(" ".join(parts) + "\n")
            
    # Overwrite the file with the cleaned annotations
    with open(file_path, 'w') as f:
        f.writelines(new_lines)

def process_dataset(labels_dir):
    """Iterates through a specific labels directory."""
    print(f"Filtering annotations in: {labels_dir}")
    count = 0
    for filename in os.listdir(labels_dir):
        if filename.endswith('.txt'):
            filter_label_file(os.path.join(labels_dir, filename))
            count += 1
    print(f"Successfully updated {count} annotation files.")

# Execute the pipeline on both train and validation label folders
# Adjust these paths to match your actual folder setup!
process_dataset("./data/train/labels")
process_dataset("./data/valid/labels")

print("\nDataset filtering complete! Your new data.yaml should list these classes in order:")
for idx, name in enumerate(KEPT_CLASSES):
    print(f"  {idx}: {name}")