import pandas as pd
import os

# ---------------------------
# Configuration and Constants
# ---------------------------
INPUT_TSV = "Data/haunted_places_v1.tsv"   # Original dataset
OUTPUT_TSV = "Data/haunted_places_v2.tsv"    # Updated dataset with image paths
IMAGES_DIR = "Data/images"                   # Directory where images are stored

# ---------------------------
# Load the Dataset
# ---------------------------
try:
    df = pd.read_csv(INPUT_TSV, sep="\t")
    print(f"Loaded {len(df)} records from {INPUT_TSV}")
except Exception as e:
    print("Error loading dataset:", e)
    exit(1)

# ---------------------------
# Update Dataset with Image Paths
# ---------------------------
def image_path_for_index(idx):
    """
    Build the relative image path for a given row index.
    """
    filename = f"haunted_image_{idx}.png"
    relative_path = os.path.join("images", filename)
    return relative_path

# Optionally, check if the image exists before assigning the path
def verify_and_get_image_path(idx):
    expected_path = os.path.join(IMAGES_DIR, f"haunted_image_{idx}.png")
    if os.path.exists(expected_path):
        return os.path.join("images", f"haunted_image_{idx}.png")
    else:
        print(f"Warning: Image file for index {idx} not found at {expected_path}")
        return ""

# Update the ai_image_path column for each record
df["ai_image_path"] = df.index.map(lambda idx: verify_and_get_image_path(idx))

# ---------------------------
# Save the Updated Dataset
# ---------------------------
try:
    df.to_csv(OUTPUT_TSV, sep="\t", index=False)
    print(f"Updated dataset saved to {OUTPUT_TSV}")
except Exception as e:
    print("Error saving updated dataset:", e)
