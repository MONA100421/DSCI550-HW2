# 🕯️ TEAM03 - DSCI 550: Haunted Places – Large Scale Data Extraction & Analysis

## 1. 🧭 Overview

This project extends Homework 1 on Haunted Places by implementing **large-scale data enrichment and multimedia integration** using NLP, computer vision, geospatial services, and generative AI. Our objective was to transform raw descriptions of haunted places into a richly augmented dataset that includes:

- 🌍 **Geolocated coordinates** from text using Apache Tika's GeoTopicParser  
- 🧠 **Named Entity Recognition (NER)** from the story using SpaCy  
- 🎨 **AI-generated images** using Stable Diffusion v1.5 based on text prompts  
- 🖼️ **Image captioning** and 🏷️ **object recognition** using Tika's Im2Txt REST container  
- 📦 A final dataset integrating all features in a structured, tab-separated format  

The final dataset (`haunted_places_final_v2.tsv`) contains **10,974 rows** with multi-modal annotations.

## 2. 📁 Folder Structure

```bash
Data/
├── haunted_places_v1.tsv              # Original dataset
├── haunted_places_v2.tsv              # With AI image paths
├── haunted_places_v2_with_objects.tsv # With detected objects
├── haunted_places_geoparsed.csv       # With GeoTopicParser lat/lon
├── merged_data_v2_with_entities.tsv   # With NER entities
├── haunted_places_final_v2.tsv        # Final merged dataset

Source Code/
├── add_ai_image_paths.py              # Adds AI-generated image filenames
├── add_entities.py                    # Adds captions/objects using Tika REST
├── entity_extraction.ipynb            # SpaCy NER on descriptions
├── geolocation_extraction.ipynb       # GeoTopicParser-based lat/lon
├── image_captioning.ipynb             # Image captioning (Docker Tika)
├── image_captioning.py                # Batch version using Tika REST
├── image_generation.py                # Image generation with Stable Diffusion
├── named_entity_recognition.ipynb     # SpaCy pipeline + Named_Entities column
├── update_dataset.ipynb               # Final merge script

Others/
├── Requirements.txt
├── tika-config.xml
├── README.md                          
├── TEAM_03_EXTRACT.pdf                # Final report
```

## 3. 🛠 Tools & Libraries Used

### Core Technologies
- **Python 3.10+**
- **Apache Tika (Server + REST Docker)** – OCR, image captioning, object detection
- **SpaCy** – Named Entity Recognition (NER)
- **GeoTopicParser (Lucene Gazetteer)** – Geoparsing for latitude/longitude
- **Stable Diffusion v1.5 (via `diffusers`)** – Text-to-image generation

### Supporting Libraries
- `pandas`, `requests`, `tika`, `os`, `json`, `tqdm`, `subprocess`, `logging`
- All dependencies are listed in `Requirements.txt`

## 4. 🚀 How to Run the Project

### 🔧 Step 1: Install dependencies
```bash
pip install -r Requirements.txt
```

### 🌍 Step 2: Start GeoTopicParser (Lucene Gazetteer)
Follow setup instructions at:
> https://github.com/chrismattmann/lucene-geo-gazetteer  
Make sure the service runs at `http://localhost:8765/search`.

### 🎨 Step 3: Generate AI images (Stable Diffusion)
```bash
python image_generation.py
```
- Prompts are constructed using `city`, `state`, `description`, `apparition_type`.
- Output saved to `Data/images` and linked via `ai_image_path`.

### 🧠 Step 4: Perform NER using SpaCy
```bash
# Option 1: Notebook
named_entity_recognition.ipynb
# Option 2: Python script
python entity_extraction.py
```

### 📍 Step 5: Geocode using GeoTopicParser
```bash
python geolocation_extraction.ipynb
```

### 🖼️ Step 6: Caption + Detect Objects using Tika Docker
- Start Docker container (image captioning):
```bash
docker run -d -p 9998:9998 --name tika-caption uscdatascience/im2txt-rest-tika
```

- Run:
```bash
python image_captioning.py
```

### 🧩 Step 7: Merge All Results
```bash
python update_dataset.ipynb
```
Final file: `Data/haunted_places_final_v2.tsv`

## 5. 📌 Technical Notes

- All paths are relative and OS-compatible.
- Docker is **required** for image captioning (via Apache Tika).
- If using Stable Diffusion, ensure you have access to the model weights or HuggingFace account.
- You may need to skip failed records or adjust batch size for large-scale processing.

## 6. 👩‍💻 Team Members

**Team 03**
- 🧠 Colin Leahey ([cleahey@usc.edu](mailto:cleahey@usc.edu))  
- 🧠 Zili Yang ([ziliy@usc.edu](mailto:ziliy@usc.edu))  
- 🧠 Chen Yi Weng ([wengchen@usc.edu](mailto:wengchen@usc.edu))  
- 🧠 Aadarsh Sudhir Ghiya ([aadarshs@usc.edu](mailto:aadarshs@usc.edu))  
- 🧠 Niromikha Jayakumar ([njayakum@usc.edu](mailto:njayakum@usc.edu))  
- 🧠 Yung Yee Chia ([yungyeec@usc.edu](mailto:yungyeec@usc.edu))  