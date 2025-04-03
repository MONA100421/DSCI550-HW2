import os
import requests
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import time
import subprocess

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
IMAGE_DIR = PROJECT_ROOT / "Data" / "images"
OUTPUT_FILE = PROJECT_ROOT / "Data" / "haunted_places_v2.tsv"
TIKA_SERVER = "http://localhost:9998/tika"
TIMEOUT = 30
BATCH_SIZE = 50


def start_tika_container():
    """Start Tika Docker container with OCR support"""
    try:
        print("🚀 Starting Tika Docker container...")
        subprocess.run([
            "docker", "run", "-d",
            "-p", "9998:9998",
            "--name", "tika-caption",
            "apache/tika:latest-full"
        ], check=True)

        print(" Waiting 15 seconds for Tika to initialize...")
        time.sleep(15)
        return True
    except subprocess.CalledProcessError as e:
        print(f" Failed to start Tika container: {str(e)}")
        return False


def process_image(img_path):
    """Extract caption from a single image with retries"""
    for attempt in range(3):
        try:
            with open(img_path, 'rb') as f:
                response = requests.put(
                    TIKA_SERVER,
                    headers={
                        'Content-type': 'image/png',
                        'Accept': 'text/plain',
                        'X-Tika-OCRLanguage': 'eng'
                    },
                    data=f,
                    timeout=TIMEOUT
                )

            if response.status_code == 200:
                caption = response.text.strip()
                if caption and not caption.lower().startswith('<!doctype html'):
                    return caption

            time.sleep(2)  # Wait before retry
        except Exception as e:
            print(f"⚠️ Attempt {attempt + 1} failed for {img_path.name}: {str(e)}")
            time.sleep(5)

    return None


def main():
    # Setup directories
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Initialize DataFrame with required columns
    columns = ['image_file', 'image_caption', 'processed_at']

    # Load existing dataset or create new one
    if OUTPUT_FILE.exists():
        try:
            df = pd.read_csv(OUTPUT_FILE, sep='\t')
            # Ensure all required columns exist
            for col in columns:
                if col not in df.columns:
                    df[col] = None
        except Exception as e:
            print(f" Error loading existing dataset: {str(e)}")
            df = pd.DataFrame(columns=columns)
    else:
        df = pd.DataFrame(columns=columns)

    # Start Tika if not running
    try:
        requests.get("http://localhost:9998", timeout=5)
        print("✅ Tika server already running")
    except:
        if not start_tika_container():
            return

    # Process images
    image_files = list(IMAGE_DIR.glob("*.png"))
    if not image_files:
        print(f" No PNG images found in {IMAGE_DIR}")
        return

    print(f"\n🔍 Found {len(image_files)} images to process")

    processed_count = 0
    for img_path in tqdm(image_files, desc="Generating captions"):
        img_name = img_path.name

        # Skip if already processed
        if not df.empty and img_name in df['image_file'].values:
            continue

        caption = process_image(img_path)
        if caption:
            new_row = {
                'image_file': img_name,
                'image_caption': caption,
                'processed_at': pd.Timestamp.now()
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            processed_count += 1

            # Save progress periodically
            if processed_count % BATCH_SIZE == 0:
                df.to_csv(OUTPUT_FILE, sep='\t', index=False)

    # Final save
    df.to_csv(OUTPUT_FILE, sep='\t', index=False)
    print(f"\n✅ Completed! Processed {processed_count} new images")
    print(f"📄 Updated dataset saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()