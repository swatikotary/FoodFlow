\# FoodFlow — Large-Scale Grocery Demand Analytics



FoodFlow is an end-to-end Big Data Analytics and Machine Learning project built using the Instacart Market Basket Analysis dataset.



The project analyses historical grocery purchasing behaviour, predicts products customers are likely to reorder, and presents actionable insights through interactive dashboards and a Streamlit application.



\## Project Objectives



\- Analyse large-scale grocery transaction data.

\- Identify product, department and customer purchasing patterns.

\- Build a machine learning model to predict customer-product reorder likelihood.

\- Generate personalised Top-10 product recommendations.

\- Present analytical results through interactive dashboards.

\- Explore data-driven business recommendations for grocery retail.



\## Project Architecture



FoodFlow is organised into three major stages:



\### Stage 1 — Historical Data Analytics

\- PySpark-based data processing and analysis.

\- Data integration, cleaning and feature exploration.

\- Product, customer, basket and reorder analysis.

\- Aggregated datasets exported for visualisation.



\### Stage 2 — Predictive Analytics

\- Candidate generation using historical purchases and popular products.

\- Customer-product feature engineering.

\- Class imbalance handling.

\- Logistic Regression classification.

\- Model evaluation using Precision, Recall, F1-score and PR-AUC.

\- Personalised Top-10 product recommendations.

\- Coefficient-based model interpretation.



\### Stage 3 — Visualisation and Decision Support

\- Power BI dashboards for historical and predictive analytics.

\- Streamlit application for interactive customer recommendations, product intelligence, department insights and model performance.



\## Technology Stack



\- Python

\- PySpark

\- Apache Spark

\- Pandas

\- Scikit-learn concepts and Spark MLlib

\- Logistic Regression

\- Power BI

\- Streamlit

\- Google Colab



\## Repository Structure



```text

FoodFlow/

├── notebooks/

│   └── FoodFlow\_BigData\_Analytics.ipynb

├── powerbi/

│   └── FoodFlow\_Dashboard.pbix

├── streamlit/

│   ├── app.py

│   ├── requirements.txt

│   ├── data/

│   └── .streamlit/

└── README.md

```



\## Running the Streamlit Application



1\. Clone this repository.

2\. Open the project folder.

3\. Install the dependencies:



```bash

pip install -r requirements.txt

```



4\. Run the application:



```bash

streamlit run app.py

```



Run the command from inside the `streamlit` directory.



\## Dataset



The project uses the Instacart Market Basket Analysis dataset.



The dataset contains historical grocery orders, product information, departments, aisles and reorder behaviour.



\## Important Limitations



\- The dataset does not contain product prices or revenue.

\- The dataset does not provide actual calendar dates for transactions.

\- The analysis uses historical static data and does not implement live streaming.

\- Recommendations represent predicted reorder likelihood, not guaranteed purchases.

\- Business recommendations are indicative and should not be interpreted as proven causal outcomes.



\## Project Scope



FoodFlow demonstrates an end-to-end workflow combining Big Data processing, predictive modelling, recommendation generation, visual analytics and an interactive decision-support application.





