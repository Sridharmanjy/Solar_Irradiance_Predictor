# Solar Energy Output Prediction

Project Structure Project Overview
This project aims to predict solar energy output based on solar irradiance, temperature, and other environmental factors across different geographical locations and seasons. By utilizing data from the **NASA POWER API**, the project builds a **linear regression model** to forecast solar irradiance and visualize seasonal energy trends.

### Key Features
- **Data Collection**: Automated data scraping from **NASA POWER API** for solar irradiance and temperature over one year (hourly data).
- **Data Processing**: Cleaned and transformed the data, handling missing values and feature engineering to include **solar zenith angle**, **temperature**, and **seasonality**.
- **Predictive Modeling**: Built a linear regression model to predict solar irradiance, evaluated with metrics such as **R²**, **MAE**, and **MSE** using **Scikit-learn**.
- **Data Visualization**: Created visualizations of actual vs predicted solar irradiance, seasonal averages, and geographical heat maps using **Matplotlib**

### Technologies Used
- **Pandas**: Data cleaning, transformation, and analysis.
- **Scikit-learn**: Machine learning model development and performance evaluation.
- **Matplotlib**: Data visualization for actual vs predicted values and seasonal trends.
- **NASA POWER API**: Data source for solar irradiance and environmental factors.

### Project Structure
solar-energy-prediction <br/>
│<br/>
├── data/                     # Folder to store raw and processed data<br/>
├── python_scripts/           # Folder for Python scripts<br/>
│   ├── data_scraper_nasa.py  # Script for scraping solar data from NASA POWER API<br/>
│   ├── model.py              # Script for model training and evaluation <br/>
│   ├── visualization.py      # Script for visualization <br/>
├── tests/                    # Folder for unit tests<br/>
├── requirements.txt          # List of project dependencies<br/>
└── README.md                 # Project documentation<br/>

### Results
The project provides insights into solar energy output trends across seasons, helping identify potential regions for solar energy optimization. Performance metrics such as R², MAE, and MSE are printed and visualized to evaluate the model's accuracy.

### Contributing
If you'd like to contribute to this project, please feel free to open a pull request or issue. All contributions are welcome!
