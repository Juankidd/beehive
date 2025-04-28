# 🐝 Beehive With Small Language Models

**Smart Beehive** is an integrated platform combining datasets, sensor networks, and AI algorithms for intelligent beekeeping, enhanced by Edge GenAIoT technology.  
This repository supports the associated scientific article by providing full datasets, analytical code, and hardware integration examples.

## 📖 Overview

Beehive consolidates diverse modules to analyze the beekeeping process:
- Datasets representing honey production records.
- Edge IoT hardware integration with ESP32 and Raspberry Pi devices.
- AI-driven predictive modeling using bio-inspired algorithms and deep learning.

It is designed for reproducibility, scalability, and ease of deployment across research and industrial environments.

## ✨ Key Features

- Centralized datasets (.csv files) for different beekeeping elements.
- ESP32 and Raspberry Pi hardware communication modules.
- Predictive modeling using LSTM neural networks.
- Bio-inspired optimization algorithms.
- Exploratory Data Analysis (EDA) of production metrics.
- Full Edge GenAIoT pipeline example for smart beehive management.

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/Juankidd/beehive.git
cd beehive

Install required dependencies:
pip install -r requirements.txt

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate    # On Linux/Mac
venv\Scripts\activate.bat   # On Windows
🚀 Usage
The project is structured in modules:

EDA_Beehives.ipynb provides an exploratory data analysis of honey production.

lstm_prediccion_miel.py trains and evaluates an LSTM model for yield prediction.

bioinspired_algorithms.py contains optimization routines.

*.ino files are firmware sketches for ESP32 devices (sensor nodes and gateways).

Datasets are provided in CSV format, located in the repository root:

Honey_Production_Dataset_2023.csv

Honey_Production_Dataset_for_2024.csv

etc.

Important:
Each CSV file represents a dataset associated with different production periods or conditions for honey generation.

Project Structure
beehive/
├── EDA_Beehives.ipynb            # Exploratory Data Analysis notebook
├── Honey_Production_Dataset_*.csv # Datasets (various elements)
├── lstm_prediccion_miel.py       # LSTM-based yield prediction
├── bioinspired_algorithms.py     # Bio-inspired algorithms
├── nodo_sensor_colmena_esp32.ino # ESP32 sensor node firmware
├── gateway_ES32_espnow_to_serial.ino # ESP32 gateway firmware
├── raspberry_serial_gateway.py   # Raspberry Pi serial gateway
├── hive_scheduler_rpi_5.py       # Raspberry Pi task scheduler
└── README.md
📚 Dependencies
The main Python dependencies are:

pandas

numpy

matplotlib

seaborn

scikit-learn

tensorflow

keras

statsmodels

scipy

(See requirements.txt for the full list.)

📈 Results / Examples

jupyter notebook EDA_Beehives.ipynb

👥 Authors
Juan Manuel Núñez Velasco (@Juankidd)

📄 License
This project is licensed under the MIT License – see the LICENSE file for details.


