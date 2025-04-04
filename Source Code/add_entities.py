import pandas as pd
import requests
import os
import sys

# Endpoint for captioning
CAPTIONS_ENDPOINT = "http://localhost:8764/inception/v3/caption/image"
# Base URL for images, make sure the HTTP server is running
BASE_URL = "http://172.17.0.1:8000/images"

def get_caption_for_url(image_url):
    params = {
        "url": image_url,
        "beam_size": 1,
        "max_caption_length": 15
    }
    response = requests.get(CAPTIONS_ENDPOINT, params=params)
    response.raise_for_status()
    data = response.json()
    captions = data.get("captions", [])
    return "; ".join([f"{cap['sentence']} (confidence: {cap['confidence']:.5f})" for cap in captions])

def main():
    # Use the updated file if it exists, otherwise use the original dataset
    input_filename = "Data/haunted_places_v2_with_objects.tsv" if os.path.exists("Data/haunted_places_v2_with_objects.tsv") else "Data/haunted_places_v2.tsv"
    df = pd.read_csv(input_filename, sep="\t")
    
    # Ensure the "detected_objects" column exists; if not, create it with empty strings
    # This only matters for first time running the code
    if "detected_objects" not in df.columns:
        df["detected_objects"] = ""
    
    # Get start and end indices from command line arguments, defaulting to 0-10000 if not given
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    end = int(sys.argv[2]) if len(sys.argv) > 2 else 10000

    for i in range(start, min(end, len(df))):
        # Only process rows with empty detected_objects columns
        if pd.notna(df.loc[i, "detected_objects"]) and df.loc[i, "detected_objects"] != "":
            continue
        
        rel_path = df.loc[i, "ai_image_path"]  # "images/haunted_image_XXXX.png"
        filename = os.path.basename(rel_path)
        image_url = f"{BASE_URL}/{filename}"
        
        try:
            caption = get_caption_for_url(image_url)
            # Line below for debugging purposes
            #print(f"Processed row {i} - Detected Entities: {caption}")
            print(i)
        except Exception as e:
            print(f"Error processing {image_url} at row {i}: {e}")
            caption = ""
        
        df.loc[i, "detected_objects"] = caption
    
    output_filename = "Data/haunted_places_v2_with_objects.tsv"
    df.to_csv(output_filename, sep="\t", index=False)
    print(f"Updated dataset saved to {output_filename}")

if __name__ == "__main__":
    main()