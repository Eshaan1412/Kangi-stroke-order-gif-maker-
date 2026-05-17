# Kanji-Motion: Programmatic Vector Stroke-Order Animator

An open-source graphics utility that converts vector Kanji stroke-order data into smooth, optimized, alpha-transparent animated GIFs. 

Instead of relying on pre-rendered raster sets, this engine dynamically interfaces with raw vector repositories, extracts coordinate path matrices, parameterizes the curves, and simulates a continuous physical pen-tip trajectory using a custom alpha-channel blending layer.

## 🚀 Key Architectural Features

* **Dynamic Unicode Extraction:** Maps input characters directly to their exact hexadecimal representation to fetch standard vector schemas (`KanjiVG`) over remote endpoints.
* **Vector Path Parameterization:** Utilizes `svgpathtools` and `numpy` to interpolate quadratic and cubic Bézier segments, translating geometric functions into explicit discrete canvas coordinates ($x, y$).
* **Artifact-Free Alpha Blending:** Solves the classic GIF binary transparency problem (jagged white edge pixelation) by isolating the image alpha channel and processing it through an adaptive 255-color palette mask.
* **Synchronized Dynamic Guidance:** Features a real-time tracking element ("pen tip") that calculates instantaneous velocity points along the active stroke array before executing a deterministic final rendering pause.

## 🛠️ Tech Stack & Dependencies

* **Language:** Python 3.x
* **Vector Parsing:** `svgpathtools`, `xml.dom.minidom`
* **Numerical Mathematics:** `numpy`
* **Image Processing Engine:** `Pillow` (PIL)
* **Networking:** `requests`

## 📦 Installation & Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/kanji-motion.git](https://github.com/yourusername/kanji-motion.git)
   cd kanji-motion
