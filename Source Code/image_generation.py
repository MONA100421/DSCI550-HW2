from diffusers import StableDiffusionPipeline
import torch
import os
import pandas as pd
import time

# ---------------------------
# Configuration and Constants
# ---------------------------
INPUT_TSV = "Data/haunted_places_v1.tsv"       # Your input dataset (TSV)
OUTPUT_TSV = "Data/haunted_places_v2.tsv"        # Updated dataset with image paths
IMAGES_DIR = "Data/images"                       # Directory to save generated images

# Create the images directory if it doesn't exist
os.makedirs(IMAGES_DIR, exist_ok=True)
print(f"Images will be saved to: {IMAGES_DIR}")

# Set device to CPU (or "cuda" if GPU is available)
device = "cpu"  # Change to "cuda" if you are using a GPU
torch_dtype = torch.float32  # Use full precision on CPU

# Model ID for a lighter model: Stable Diffusion 1.5 pruned-emaonly
model_id = "runwayml/stable-diffusion-v1-5"

# Load the pipeline (weights will be downloaded automatically on first run)
print("Loading model...")
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch_dtype,
    use_safetensors=True,
)
# Convert UNet to full precision to ensure compatibility on CPU
pipe.unet = pipe.unet.float()
pipe = pipe.to(device)
print("Model loaded successfully.")

# ---------------------------
# Function Definitions
# ---------------------------
def create_prompt(record):
    """
    Construct a prompt using fields from the record.
    Uses 'description', 'city', 'state', and 'apparition type'.
    """
    description = record.get("description", "")
    city = record.get("city", "")
    state = record.get("state", "")
    apparition = record.get("apparition type", "")
    
    # Construct the prompt without any extra words.
    prompt = f"Haunted scene in {city}, {state}. {description} Apparition: {apparition}."
    return prompt

def generate_and_save_image(prompt, idx):
    """
    Generate an image for a given prompt and save it.
    Returns the relative path if successful.
    """
    try:
        # Generate the image using 30 inference steps and guidance scale of 7.
        image = pipe(prompt=prompt, num_inference_steps=30, guidance_scale=7).images[0]
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

    # Process each record to generate an image
    for idx, row in df.iterrows():
        prompt = create_prompt(row)
        print(f"Record {idx} prompt: {prompt[:80]}...")  # Show first 80 characters

        image_rel_path = generate_and_save_image(prompt, idx)
        if image_rel_path:
            df.at[idx, "ai_image_path"] = image_rel_path
        else:
            print(f"Skipping record {idx} due to generation failure.")

        # Pause briefly between requests (adjust as needed)
        time.sleep(1)

    # Save the updated dataset
    try:
        df.to_csv(OUTPUT_TSV, sep="\t", index=False)
        print(f"Updated dataset saved to {OUTPUT_TSV}")
    except Exception as e:
        print("Error saving updated dataset:", e)

if __name__ == "__main__":
    main()
