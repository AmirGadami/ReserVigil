# ReserVigil (MLOPS): Hotel Reservation Outcome Predictor

ReserVigil is a machine learning-powered system that predicts whether a hotel reservation will be honored or canceled. The main purpose of this project is to **showcase MLOps best practices** through a complete end-to-end deployment pipeline, including experiment tracking, version control, CI/CD with Jenkins, and a user-facing Streamlit app.

## Project Objective

To build a binary classification model that helps hotel operators forecast reservation cancellations in advance, enabling smarter inventory management and revenue optimization.

## Project Structure

```
.
├── data/                   # Raw and processed datasets
├── notebooks/              # Jupyter notebooks for EDA & experiments
├── src/                    # Source code (data ingestion, processing, training, etc.)
├── models/                 # Trained model artifacts
├── config/                 # YAML configuration files
├── app/                    # Streamlit app for interactive predictions
├── Dockerfile              # Container setup for Jenkins CI/CD
└── README.md               # Project documentation
```

## Features

- Cleaned and preprocessed hotel booking data
- Exploratory Data Analysis (EDA)
- Model training using ensemble techniques (e.g., Random Forest, LightGBM)
- Data and model versioning (DVC or Git)
- Experiment tracking (MLflow or Weights & Biases)
- CI/CD pipeline with Jenkins
- Interactive user interface built with Streamlit

## Machine Learning Pipeline

1. Data Ingestion  
2. Preprocessing and Feature Engineering  
3. Model Training and Evaluation  
4. Experiment Tracking  
5. Model Registry and Versioning  
6. CI/CD for Deployment using Jenkins  
7. Streamlit App for Real-Time Predictions

## Dataset

Public dataset containing hotel reservation records. Each row represents a booking with features such as:
- Lead time
- Room type
- Special requests
- Average price per room
- Meal plan
- Booking status (target)

## Tech Stack

- Python, Pandas, NumPy, Scikit-learn
- Matplotlib, Seaborn
- MLflow / Weights & Biases
- DVC / Git
- Jenkins, Docker
- Streamlit

## Results

The trained model achieves high accuracy in predicting cancellations, enabling real-time alerts or dashboard integrations for hotel operators. The Streamlit app allows users to interactively test booking scenarios and view predictions instantly.

## Future Improvements

- Hyperparameter tuning and model ensembling
- Integration with a live booking system
- Deeper analysis of customer behavior and cancellation reasons

## Author

Amirhossein Ghadami  
LinkedIn: https://www.linkedin.com/in/amirhosseinghadami/  
GitHub: https://github.com/amirgadami

## License

This project is licensed under the MIT License.