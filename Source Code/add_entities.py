import pandas as pd
import requests
import os

# Endpoint for captioning
CAPTIONS_ENDPOINT = "http://localhost:8764/inception/v3/caption/image"
# Base URL for images (using host IP so the container can access them)
BASE_URL = "http://172.17.0.1:8000/images"

def get_caption_for_url(image_url):
    params = {
        "url": image_url,
        "beam_size": 5,
        "max_caption_length": 20
    }
    r = requests.get(CAPTIONS_ENDPOINT, params=params)
    r.raise_for_status()
    data = r.json()
    captions = data.get("captions", [])
    return "; ".join([f"{cap['sentence']} (confidence: {cap['confidence']:.5f})" for cap in captions])

def main():
    # Load the TSV dataset from the Data folder
    df = pd.read_csv("Data/haunted_places_v2.tsv", sep="\t")
    #print("Original dataset preview (rows 100-110):")
    #print(df.iloc[100:110])
    
    # Create a subset for rows 100 to 999 (i.e. 100-1000)
    df_subset = df.iloc[6500:7000].copy()
    detected_entities = []
    
    for i, row in df_subset.iterrows():
        rel_path = row["ai_image_path"]  # e.g., "images/haunted_image_0.png"
        filename = os.path.basename(rel_path)
        image_url = f"{BASE_URL}/{filename}"
        try:
            caption = get_caption_for_url(image_url)
        except Exception as e:
            print(f"Error processing {image_url}: {e}")
            caption = ""
        detected_entities.append(caption)
        # Print progress every 10 rows processed
        if (i + 1) % 10 == 0:
            print(f"Processed row index: {i}")
    
    # Add the new column "detected_objects" to the subset and update the original dataframe
    df.loc[df_subset.index, "detected_objects"] = detected_entities
    
    # Save the updated dataset to a new TSV file
    output_filename = "Data/haunted_places_v2_with_objects.tsv"
    df.to_csv(output_filename, sep="\t", index=False)
    print(f"Updated dataset saved to {output_filename}")

if __name__ == "__main__":
    main()
