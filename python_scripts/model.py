import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import os
import numpy as np
pd.set_option('display.max_columns', None)
season_mapping = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}

def assign_season(df):
    """
    Assigns a season based on the month in the DateTime column and encodes the season into a numerical label.
    Seasons for London
    - Winter: December, January, February (12, 1, 2) -> 1
    - Spring: March, April, May (3, 4, 5) -> 2
    - Summer: June, July, August (6, 7, 8) -> 3
    - Fall: September, October, November (9, 10, 11) -> 4
    """

    # Define function to map months to seasons
    def get_season(month):
        if month in [12, 1, 2]:
            return 1  # Winter
        elif month in [3, 4, 5]:
            return 2  # Spring
        elif month in [6, 7, 8]:
            return 3  # Summer
        elif month in [9, 10, 11]:
            return 4  # Fall

    # Extract month from DateTime and assign seasons
    df['Month'] = df['DateTime'].dt.month
    df['Season_Encoded'] = df['Month'].apply(get_season)

    return df


def feature_engineering(df):
    """
    Extracts useful features such as hour of the day, month, temperature, and solar zenith angle
    from the cleaned solar data.
    :param df: Cleaned pandas DataFrame.
    :return: DataFrame with new features for modeling.
    """

    df_clean = df.dropna(subset=['Solar_Irradiance', 'Solar_zenith_angle', 'Temperature', 'Season_Encoded'])
    df_clean = df_clean[df_clean['Solar_Irradiance'] != 0.00]
    # Keep relevant features (including the target)
    features = df_clean[['Solar_Irradiance', 'Solar_zenith_angle', 'Temperature', 'Season_Encoded','DateTime']]

    return features


def split_data(df):
    """
    Splits the dataset into training and testing sets.
    :param df: DataFrame with features.
    :return: X_train, X_test, y_train, y_test
    """
    # Define target variable and features
    x = df[['Temperature','Solar_zenith_angle']]
    y = df['Solar_Irradiance']

    # Split the data into 80% training and 20% testing sets
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=4)

    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    """
    Trains a linear regression model on the training data.
    :param X_train: Training features.
    :param y_train: Training target variable (solar irradiance).
    :return: Trained model.
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    r_sq = model.score(X_train, y_train)
    print(f'The R squared value for the test model is {r_sq:.4f}')

    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluates the model on the test set and prints performance metrics.
    :param model: Trained model.
    :param X_test: Test features.
    :param y_test: True values for the test set.
    """
    # Predict on the test set
    y_pred = model.predict(X_test)

    # Calculate Mean Absolute Error (MAE)
    mae = mean_absolute_error(y_test, y_pred)

    # Calculate Mean Squared Error (MSE)
    mse = mean_squared_error(y_test, y_pred)

    # Calculate R-squared (R²)
    r2 = r2_score(y_test, y_pred)

    print(f'The R squared value for the training model is {r2:.4f}')
    print(f"Mean Absolute Error (MAE): {mae:.4f}")
    print(f"Mean Squared Error (MSE): {mse:.4f}")

    return y_pred

def train_and_evaluate_by_season(df):
    """
    Trains and evaluates separate models for each season.
    :param df: DataFrame with season-encoded data.
    """
    results = {}
    seasons = df['Season_Encoded'].unique()

    for season in seasons:

        print(f"Training and Evaluating Model for Season {season_mapping.get(season, 'Unknown Season')}")

        # Filter the data for the current season
        df_season = df[df['Season_Encoded'] == season]

        pd.set_option('display.max_columns', None)

        features = feature_engineering(df_season)
        # Split the data for the current season
        X_train, X_test, y_train, y_test = split_data(features)

        # Train the model
        model = train_model(X_train, y_train)

        # Predict the test set
        y_pred = model.predict(X_test)

        # Evaluate the model
        evaluate_model(model, X_test, y_test)

        results[season] = (model, y_pred, X_train, X_test, y_train, y_test)

    return results

# 5. Main Function to Execute the Model Training and Evaluation
if __name__ == "__main__":
    try:
        # Load the cleaned solar data
        start_date , end_date = '20230101', '20240101'
        data_folder = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'data')
        filename = f"cleaned_solar_data_{start_date}_to_{end_date}.json"
        file_path = os.path.join(data_folder, filename)
        cleaned_data = pd.read_json(file_path)

        # Assign seasons
        cleaned_data = assign_season(cleaned_data)

        # Perform feature engineering
        features = feature_engineering(cleaned_data)

        # Group and analyze by season and zenith angle bins
        train_and_evaluate_by_season(features)
    except Exception as e:
        print(f"An error occurred: {str(e)}")