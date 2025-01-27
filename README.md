# sentiment-analysis-pipeline

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
2. Set up the database:
    ```bash
    python data_ingestion.py
3. Train the Model
    ```bash
    python model_training.py
4. Run the Flask API:
    ```bash 
    python app.py
 ## API Endpoint
- **POST /predict**: Predict sentiment for a given review.
