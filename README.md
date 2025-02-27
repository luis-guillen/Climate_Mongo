 🌎 Climate_Mongo
Overview
Climate_Mongo is a project focused on analyzing and visualizing climate data using MongoDB as the primary database. This project leverages Python for data processing and analysis, along with HTML for visualization.

Features
📥 Data Ingestion: Efficiently ingest large climate datasets into MongoDB.
📊 Data Processing: Perform complex data transformations and analysis using Python.
📈 Data Visualization: Visualize climate data trends and patterns using HTML-based dashboards.
Installation
To set up this project locally, follow these steps:

Clone the repository

bash
git clone https://github.com/luis-guillen/Climate_Mongo.git
cd Climate_Mongo
Create a virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies

bash
pip install -r requirements.txt
Usage
Data Ingestion

Ensure MongoDB is running on your machine.
Use the provided scripts to ingest data into MongoDB.
bash
python ingest_data.py
Data Processing

Process the ingested data using the process_data.py script.
bash
python process_data.py
Data Visualization

Generate visualizations using the visualize_data.py script.
bash
python visualize_data.py
Requirements
Python 3.8 or higher
MongoDB 4.4 or higher
See requirements.txt for Python dependencies.
Contributing
Contributions are welcome! Please fork this repository and submit pull requests.

License
This project is licensed under the MIT License.

Acknowledgments
Thanks to all contributors and users for their support.
