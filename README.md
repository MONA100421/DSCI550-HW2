# TEAM03-DSCI 550: Large Scale Data Extraction & Analysis for Haunted Places

------------------------------------------------------------
## 1. Overview
------------------------------------------------------------
This assignment extends the first homework on Haunted Places by incorporating advanced large-scale data extraction techniques, including geolocation parsing, named entity recognition (NER), generative AI image creation, image captioning, and object recognition.

We created a new version of our dataset (v2), which includes the following newly extracted features:
- Geolocated place names with latitude and longitude (via GeoTopicParser)
- Named entities from the description text (via SpaCy)
- AI-generated image paths for each Haunted Place
- Automatically generated image captions (via Tika’s Show & Tell)
- Detected objects in each image (via Tika Vision)

------------------------------------------------------------
## 2. Folder Structure
------------------------------------------------------------
```bash
Data/
  ├── dataset1/                 # Empty folder as instructed
Source Code/
  ├── geolocation_extraction.py
  ├── entity_extraction.py
  ├── image_generation.py
  ├── image_captioning.py
  ├── update_dataset.py
  ├── notebook/                # Contains any Jupyter Notebooks used
TEAM_03_EXTRACT.pdf          # Final report (4 pages)
v2_dataset.tsv               # Updated dataset with new features
Readme.txt                   # This file
Requirements.txt             # All required libraries with version info
```
------------------------------------------------------------
## 3. Tools and Libraries Used
------------------------------------------------------------

- **Python 3.10+**
- **Tika Python**: for content extraction
    - https://github.com/chrismattmann/tika-python
- **Apache Tika + GeoTopicParser**:
    - https://cwiki.apache.org/confluence/display/tika/GeoTopicParser
    - https://github.com/chrismattmann/lucene-geo-gazetteer
- **SpaCy**: for Named Entity Recognition (NER)
    - https://spacy.io
- **Generative AI Tools**: (Choose one)
    - Stable Diffusion / DALL·E 3 / Imagine from Meta / Midjourney
- **Tika Docker (Image Captioning & Object Recognition)**:
    - https://github.com/USCDataScience/tika-dockers
    - https://hub.docker.com/r/uscdatascience/im2txt-rest-tika

Other Python libraries used:
- pandas
- requests
- os, json, re
- tqdm (for progress bars)

All libraries and versions are listed in `Requirements.txt`.

------------------------------------------------------------
## 4. How to Run
------------------------------------------------------------

### **Step 1: Install all Python dependencies:**
```bash
pip install -r Requirements.txt
```

### **Step 2: Start the GeoTopicParser Lucene GeoGazetteer server**
```bash
# Follow setup instructions from:
# https://github.com/chrismattmann/lucene-geo-gazetteer
```

### **Step 3: Generate images using your chosen AI service**
- Run `image_generation.py` to generate images using descriptions from the dataset.
- Make sure generated images are saved to a folder and paths are referenced in the dataset.

### **Step 4: Run image captioning & object detection**
- Ensure Tika Docker containers are running (`im2txt-rest-tika`)
- Use `image_captioning.py` to add captions and detected objects to each row in the dataset.

### **Step 5: Run geolocation and NER extraction**
```bash
python geolocation_extraction.py
python entity_extraction.py
```

### **Step 6: Combine everything into the final dataset**
```bash
python update_dataset.py
```

------------------------------------------------------------
## 5. Notes
------------------------------------------------------------

- All scripts use **relative paths**.
- We generated images using: [Insert Tool Name Here]
- Make sure Docker is running before executing image captioning.
- If you use API keys or tokens (e.g. OpenAI), store them securely as environment variables.

------------------------------------------------------------
## 6. Team Members
------------------------------------------------------------

Team 3:
- **Zili Yang** ([ziliy@usc.edu](mailto:ziliy@usc.edu))
- **Chen Yi Weng** ([wengchen@usc.edu](mailto:wengchen@usc.edu))
- **Aadarsh Sudhir Ghiya** ([aadarshs@usc.edu](mailto:aadarshs@usc.edu))
- **Niromikha Jayakumar** ([njayakum@usc.edu](mailto:njayakum@usc.edu))
- **Yung Yee Chia** ([yungyeec@usc.edu](mailto:yungyeec@usc.edu))
- **Colin Leahey** ([cleahey@usc.edu](mailto:cleahey@usc.edu))

