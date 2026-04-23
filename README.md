# Image Edge to CAD

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

An automated pipeline designed to extract edges from images and convert them into editable CAD formats (DXF/SVG). This tool is ideal for converting hand-drawn sketches, architectural diagrams, or mechanical parts into vector-based engineering files.

---

## 🚀 Key Features
* **Precision Edge Detection:** Utilizes Canny edge detection and morphological operations to find clean boundaries.
* **Vectorization:** Converts raster pixel data into smooth geometric paths (Polylines).
* **CAD Compatibility:** Exports directly to `.dxf` format, compatible with AutoCAD, SolidWorks, and Fusion 360.
* **Batch Processing:** Support for processing multiple images in a single directory.

## 🛠 Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/kang851216/image-edge-to-cad.git](https://github.com/kang851216/image-edge-to-cad.git)
   cd image-edge-to-cad

2. **Install dependencies:**
   ```bash
    pip install -r requirements.txt

## 💻 Usage
* Place your images in the input/ folder and run the conversion script:
  ```bash
    python image_to_cad.py --input ./input/drawing.png --output ./output/result.dxf
