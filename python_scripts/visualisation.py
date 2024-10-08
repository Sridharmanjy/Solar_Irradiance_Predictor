import matplotlib.pyplot as plt
import os
import pandas as pd
from model import assign_season, feature_engineering, train_and_evaluate_by_season
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

pd.set_option('display.max_columns', None)
season_mapping = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}

def plot_actual_by_season(df, results):
    """
       Plots the actual vs predicted solar irradiance values over time, grouped by season.
       Skips invalid results.
    """

    seasons = df['Season_Encoded'].unique()

    for season in seasons:
        season_df = df[df['Season_Encoded'] == season]

        if not season_df.empty:
            # Retrieve the model, y_pred, X_train, X_test, y_train, y_test for the specific season
            model_result = results.get(season, None)

            # Skip this season if the result is invalid
            if model_result is None:
                print(f"Skipping Season {season_mapping.get(season)}: No valid data available.")
                continue

            model, y_pred, X_train, X_test, y_train, y_test = model_result

            if y_test is None or y_pred is None or len(y_test) == 0 or len(y_pred) == 0:
                print(f"Skipping Season {season_mapping.get(season)}: Insufficient test data.")
                continue

            r2 = r2_score(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            intercept = model.intercept_
            coefficients = model.coef_

            # Plot the actual vs predicted values
            plt.figure(figsize=(12, 6))
            # Scatter plot for actual solar irradiance (y_test) vs Temperature from X_test
            plt.scatter(season_df['Temperature'], season_df['Solar_Irradiance'], alpha=0.5, label = "Data Points")

            plt.xlabel('Temperature')
            plt.ylabel('Solar Irradiance (kW-hr/m^2)')
            plt.title(f'Actual Solar Irradiance ({season_mapping.get(season)}) with the predicted linear regression equation')
            plt.xticks(rotation=45)
            plt.legend()
            plt.grid(True)

            textstr = f"R² = {r2:.4f}\nMAE = {mae:.4f}\nMSE = {mse:.4f} \ny = {coefficients[0]:.4f} * Temperature + {coefficients[1]:.4f} * Solar Zenith Angle + {intercept:.4f}"
            plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

            # Set y-axis (solar irradiance) to start at 0
            plt.ylim(bottom=0)

            plt.show()

def plot_avg_irradiance_by_season(df):
    """
    Plots a bar chart of average solar irradiance for each season.
    """
    # Group by season and calculate average solar irradiance
    # to note that this is only for times when there is solar irradiance and not total energy which could be misleading
    avg_irradiance = df.groupby('Season_Encoded')['Solar_Irradiance'].mean()

    plt.figure(figsize=(10, 6))
    avg_irradiance.plot(kind='bar', color='skyblue')
    plt.title('Average Solar Irradiance by Season')
    plt.xlabel('Season')
    plt.xticks(rotation=45)
    plt.ylabel('Average Solar Irradiance (kW-hr/m^2)')
    plt.xticks(ticks=range(4), labels=['Winter', 'Spring', 'Summer', 'Fall'])
    plt.grid(True)
    plt.legend()
    # Set y-axis to start at 0
    plt.ylim(bottom=0)

    plt.show()

if __name__ == "__main__":

    try:
        # Scatter plot of solar irradiance vs temperature

        start_date , end_date = '20230101', '20240101'
        data_folder = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'data')
        filename = f"cleaned_solar_data_{start_date}_to_{end_date}.json"
        file_path = os.path.join(data_folder, filename)
        cleaned_data = pd.read_json(file_path)

        df_1 = assign_season(cleaned_data)
        cleaned_df = feature_engineering(df_1)
        results = train_and_evaluate_by_season(cleaned_data)

        plot_actual_by_season(cleaned_df, results)

        plot_avg_irradiance_by_season(cleaned_df)
    except Exception as e:
        print(f"An error occurred: {str(e)}")