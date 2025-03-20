import pandas as pd

def clean_numeric_value(value):
    """Removes special characters like '*' and converts to float."""
    return float(value.replace('*', '')) if '*' in value else float(value)

def load_and_clean_data(file_path):
    """Loads data from a file, handles missing/invalid values, and returns a cleaned DataFrame."""
    with open(file_path, "r") as file:
        lines = file.readlines()

    data = []
    for line in lines:
        columns = line.split()
        if len(columns) >= 3:
            try:
                day = int(columns[0])
                max_temp = clean_numeric_value(columns[1])  # Clean * from max temp
                min_temp = clean_numeric_value(columns[2])  # Clean * from min temp
                if max_temp >= min_temp:
                    data.append([day, max_temp, min_temp])
            except ValueError:
                continue

    return pd.DataFrame(data, columns=["Day", "MaxTemp", "MinTemp"])

def calculate_temp_spread(df):
    """Computes temperature spread and returns the day with the smallest spread and its spread value."""
    df["TempSpread"] = df["MaxTemp"] - df["MinTemp"]
    min_spread_row = df.loc[df["TempSpread"].idxmin()]
    return min_spread_row["Day"], min_spread_row["TempSpread"]

def calculate_avg_temp(df):
    """Computes daily average temperature and returns the day with the highest average and its value."""
    df["AvgTemp"] = (df["MaxTemp"] + df["MinTemp"]) / 2
    max_avg_row = df.loc[df["AvgTemp"].idxmax()]
    return max_avg_row["Day"], max_avg_row["AvgTemp"]

def find_extremes(df):
    """Finds the days with the highest max temperature and lowest min temperature along with their values."""
    highest_max_row = df.loc[df["MaxTemp"].idxmax()]
    lowest_min_row = df.loc[df["MinTemp"].idxmin()]
    return (highest_max_row["Day"], highest_max_row["MaxTemp"]), (lowest_min_row["Day"], lowest_min_row["MinTemp"])

if __name__ == "__main__":
    file_path = "/Users/Matthew/Documents/Jobs/Potential/weather.dat"  # Update this path if needed
    df_cleaned = load_and_clean_data(file_path)

    if df_cleaned.empty:
        print("Error: No valid weather data found in the file.")
    else:
        min_spread_day, min_spread_value = calculate_temp_spread(df_cleaned)
        highest_avg_day, highest_avg_value = calculate_avg_temp(df_cleaned)
        (highest_max_day, highest_max_temp), (lowest_min_day, lowest_min_temp) = find_extremes(df_cleaned)

        results = {
            "Day with Smallest Temperature Spread": (min_spread_day, min_spread_value),
            "Day with Highest Average Temperature": (highest_avg_day, highest_avg_value),
            "Day with Highest Maximum Temperature": (highest_max_day, highest_max_temp),
            "Day with Lowest Minimum Temperature": (lowest_min_day, lowest_min_temp),
        }

        print("\nWeather Analysis Results:")
        for key, (day, value) in results.items():
            print(f"{key}: Day {int(day)}, Value: {value:.2f}°")