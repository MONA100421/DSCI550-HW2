import pandas as pd, requests, os

# Endpoint from your test that worked
CAPTIONS_ENDPOINT = "http://localhost:8764/inception/v3/captions"
# Base URL for images served via HTTP server
BASE_URL = "http://localhost:8000/images"

def get_caption_for_url(image_url):
    params = {
        "url": image_url,
        "beam_size": 3,
        "max_caption_length": 15
    }
    r = requests.get(CAPTIONS_ENDPOINT, params=params)
    r.raise_for_status()
    data = r.json()
    captions = data.get("captions", [])
    return "; ".join([f"{cap['sentence']} (confidence: {cap['confidence']:.5f})" for cap in captions])

# Since we're in the Data folder, read the file directly.
df = pd.read_csv("haunted_places_v2.tsv", sep="\t")
print("Original dataset preview:")
print(df.head())

# Process only the first 100 rows.
df_subset = df.head(100).copy()
captions_list = []

for _, row in df_subset.iterrows():
    # "ai_image_path" is something like "images/haunted_image_0.png"
    rel_path = row["ai_image_path"]
    # Construct full URL using just the basename (e.g., "haunted_image_0.png")
    filename = os.path.basename(rel_path)
    image_url = f"{BASE_URL}/{filename}"
    try:
        caption = get_caption_for_url(image_url)
    except Exception as e:
        print(f"Error processing {image_url}: {e}")
        caption = ""
    captions_list.append(caption)

df_subset["detected_objects"] = captions_list
df.update(df_subset)

# Save updated dataset in the current folder (Data)
output_filename = "haunted_places_v2_with_objects.tsv"
df.to_csv(output_filename, sep="\t", index=False)
print(f"Updated dataset saved to {output_filename}")