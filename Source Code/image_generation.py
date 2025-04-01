from diffusers import StableDiffusionPipeline
import torch
import os
import pandas as pd
import time

# ---------------------------
# Configuration and Constants
# ---------------------------
INPUT_TSV = "Data/haunted_places_v1.tsv"       # Input dataset (TSV)
OUTPUT_TSV = "Data/haunted_places_v2.tsv"        # Updated dataset with image paths
IMAGES_DIR = "Data/images"                       # Directory to save generated images

# Create the images directory if it doesn't exist
os.makedirs(IMAGES_DIR, exist_ok=True)
print(f"Images will be saved to: {IMAGES_DIR}")

# Set device to GPU if available; else CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
# Use full precision on CPU; if GPU is available, you could use fp16 but here we keep it simple.
torch_dtype = torch.float32

# Model ID for Stable Diffusion 1.5 pruned-emaonly (lighter for CPU)
model_id = "runwayml/stable-diffusion-v1-5"

print("Loading model...")
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch_dtype,
    use_safetensors=True,
)
# Force full precision for CPU compatibility
pipe.unet = pipe.unet.float()
pipe = pipe.to(device)
print("Model loaded successfully.")

# ---------------------------
# Reduced Quality / Faster Generation Settings
# ---------------------------
# Lower resolution to reduce computation (e.g., 384x384 instead of 512x512)
HEIGHT = 384
WIDTH = 384
# Reduce the number of inference steps (default 30 -> 10)
NUM_INFERENCE_STEPS = 30
# Lower guidance scale
GUIDANCE_SCALE = 7

# ---------------------------
# Function Definitions
# ---------------------------
def create_prompt(record):
    """
    Build a text prompt using dataset fields without extra descriptive additions.
    Uses 'description', 'city', 'state', and 'apparition type'.
    """
    description = record.get("description", "")
    city = record.get("city", "")
    state = record.get("state", "")
    apparition = record.get("apparition type", "")
    
    prompt = f"Haunted scene in {city}, {state}. {description} Apparition: {apparition}."
    return prompt

def generate_and_save_image(prompt, idx):
    """
    Generate an image using the pipeline with reduced quality settings,
    save it to disk, and return the relative path.
    """
    try:
        image = pipe(
            prompt=prompt,
            num_inference_steps=NUM_INFERENCE_STEPS,
            guidance_scale=GUIDANCE_SCALE,
            height=HEIGHT,
            width=WIDTH
        ).images[0]
        filename = f"haunted_image_{idx}.png"
        image_path = os.path.join(IMAGES_DIR, filename)
        image.save(image_path)
        print(f"Saved image for record {idx} to {image_path}")
        return os.path.join("images", filename)
    except Exception as e:
        print(f"Error generating image for record {idx}: {e}")
        return None

def main():
    # Load the original dataset
    try:
        df = pd.read_csv(INPUT_TSV, sep="\t")
        print(f"Loaded {len(df)} records from {INPUT_TSV}")
    except Exception as e:
        print("Error loading dataset:", e)
        return

    # Add a new column for the image paths
    df["ai_image_path"] = ""

    # Process each record
    for idx, row in df.iterrows():
        if idx < 3000:
            continue
        if idx > 4000:
            continue
        prompt = create_prompt(row)
        print(f"Record {idx} prompt: {prompt[:80]}...")  # Display first 80 characters
        
        image_rel_path = generate_and_save_image(prompt, idx)
        if image_rel_path:
            df.at[idx, "ai_image_path"] = image_rel_path
        else:
            print(f"Skipping record {idx} due to generation failure.")
        
        # Pause briefly to mitigate any potential rate issues
        time.sleep(1)

    # Save the updated dataset
    try:
        df.to_csv(OUTPUT_TSV, sep="\t", index=False)
        print(f"Updated dataset saved to {OUTPUT_TSV}")
    except Exception as e:
        print("Error saving updated dataset:", e)

if __name__ == "__main__":
    main()
