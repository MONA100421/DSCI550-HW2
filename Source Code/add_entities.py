import pandas as pd
import requests
import os
import time

# Endpoint for captioning
CAPTIONS_ENDPOINT = "http://localhost:8764/inception/v3/caption/image"
# Base URL for images (make sure your HTTP server is running and serving the images)
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
    # Load the dataset (adjust the file path if needed)
    df = pd.read_csv("Data/haunted_places_v2.tsv", sep="\t")
    # Create a subset for rows 5 through 10 (indices 5 to 10 inclusive)
    df_subset = df.iloc[10:100].copy()
    
    detected_entities = []
    
    for i, row in df_subset.iterrows():
        rel_path = row["ai_image_path"]  # e.g., "images/haunted_image_XXXX.png"
        filename = os.path.basename(rel_path)
        image_url = f"{BASE_URL}/{filename}"
        try:
            caption = get_caption_for_url(image_url)
            print(i)
            #print(f"Processed row index: {i} - Detected Entities: {caption}")
        except Exception as e:
            print(f"Error processing {image_url}: {e}")
            caption = ""
        detected_entities.append(caption)
        # Optional pause to see output
        #time.sleep(0.5)
    
    # Assign the new column "detected_objects" to these rows in the original dataframe
    df.loc[df_subset.index, "detected_objects"] = detected_entities
    
    output_filename = "Data/haunted_places_v2_with_objects.tsv"
    df.to_csv(output_filename, sep="\t", index=False)
    print(f"Updated dataset saved to {output_filename}")
    #print("Final detected objects for rows 5-10:")
    # Increase max column width for better readability if needed
    pd.set_option('display.max_colwidth', None)
    #print(df.loc[df_subset.index, ["ai_image_path", "detected_objects"]])

if __name__ == "__main__":
    main()