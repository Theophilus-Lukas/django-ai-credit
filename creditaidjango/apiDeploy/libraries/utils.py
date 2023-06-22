# =============================================================================
# file: libraries/utils.py
# this file contains the function to do data preprocessing
# =============================================================================

from .config import *


# * Jarak dari dua titik
def calculate_distance(lat1, lon1, lat2, lon2):
    d = distance.distance((lat1, lon1), (lat2, lon2))
    meter = d.m
    return meter


# * Jarak Rata-rata
def average_distance(row):
    now_distance = calculate_distance(
        row["now_lat"], row["now_lon"], row["domicile_lat"], row["domicile_lon"]
    )
    last_1_week_distance = calculate_distance(
        row["last_1_week_lat"],
        row["last_1_week_lon"],
        row["domicile_lat"],
        row["domicile_lon"],
    )
    last_2_week_distance = calculate_distance(
        row["last_2_week_lat"],
        row["last_2_week_lon"],
        row["domicile_lat"],
        row["domicile_lon"],
    )
    last_3_week_distance = calculate_distance(
        row["last_3_week_lat"],
        row["last_3_week_lon"],
        row["domicile_lat"],
        row["domicile_lon"],
    )
    last_4_week_distance = calculate_distance(
        row["last_4_week_lat"],
        row["last_4_week_lon"],
        row["domicile_lat"],
        row["domicile_lon"],
    )

    average_distance = (
        now_distance
        + last_1_week_distance
        + last_2_week_distance
        + last_3_week_distance
        + last_4_week_distance
    ) / 5

    return now_distance, average_distance


# * Stabilitas Alamat
def calculate_address_stability(row):
    stability_score = 0
    total_population = row["total_population"]
    income_rate = row["income_rate"]
    unemployment_rate = row["unemployment_rate"]
    education_rate = row["education_rate"]
    crime_rate = row["crime_rate"]
    poverty_rate = row["poverty_rate"]
    average_distance = row["average_distance"]
    length_of_stay = row["length_of_stay"]

    if total_population == "Sangat Rendah":
        stability_score += random.randint(3, 5)
    elif total_population == "Rendah":
        stability_score += random.randint(2, 4)
    elif total_population == "Sedang":
        stability_score += random.randint(2, 3)
    elif total_population == "Tinggi":
        stability_score += random.randint(1, 2)
    elif total_population == "Sangat Tinggi":
        stability_score += 1

    if income_rate == "Sangat Rendah":
        stability_score += random.randint(1, 2)
    elif income_rate == "Rendah":
        stability_score += random.randint(2, 3)
    elif income_rate == "Sedang":
        stability_score += random.randint(3, 4)
    elif income_rate == "Tinggi":
        stability_score += random.randint(4, 5)
    elif income_rate == "Sangat Tinggi":
        stability_score += 5

    if unemployment_rate == "Rendah":
        stability_score += 5
    elif unemployment_rate == "Sedang":
        stability_score += 3
    elif unemployment_rate == "Tinggi":
        stability_score += 2
    elif unemployment_rate == "Sangat Tinggi":
        stability_score += 1

    if education_rate == "Sangat Rendah":
        stability_score += 1
    elif education_rate == "Rendah":
        stability_score += random.randint(2, 3)
    elif education_rate == "Sedang":
        stability_score += random.randint(3, 4)
    elif education_rate == "Tinggi":
        stability_score += random.randint(3, 5)
    elif education_rate == "Sangat Tinggi":
        stability_score += random.randint(4, 5)

    if crime_rate == "Sangat Rendah":
        stability_score += 5
    elif crime_rate == "Rendah":
        stability_score += random.randint(3, 4)
    elif crime_rate == "Sedang":
        stability_score += random.randint(2, 3)
    elif crime_rate == "Tinggi":
        stability_score += random.randint(1, 2)
    elif crime_rate == "Sangat Tinggi":
        stability_score += 1

    if poverty_rate == "Rendah":
        stability_score += 5
    elif poverty_rate == "Sedang":
        stability_score += 3
    elif poverty_rate == "Tinggi":
        stability_score += 2
    elif poverty_rate == "Sangat Tinggi":
        stability_score += 1

    if average_distance <= 1000:
        stability_score += 5
    elif average_distance <= 4000:
        stability_score += 3
    elif average_distance <= 10000:
        stability_score += 2
    elif average_distance > 10000:
        stability_score += 1

    if length_of_stay == "< 1 Tahun":
        stability_score += 1
    elif length_of_stay == "1 - 2 Tahun":
        stability_score += 2
    elif length_of_stay == "3 - 4 Tahun":
        stability_score += 3
    elif length_of_stay == "> 5 Tahun":
        stability_score += 5

    # calculate address stability
    if stability_score <= 10:
        address_stability = "Sangat tidak stabil"
    elif stability_score <= 20:
        address_stability = "Tidak stabil"
    elif stability_score <= 30:
        address_stability = "Stabil"
    else:
        address_stability = "Sangat stabil"

    return address_stability


# * Kesesuaian Alamat
def calculate_address_suitability(row):
    now_distance = row["now_distance"]

    if now_distance > 100:
        suitability_score = 0
        address_suitability = "Tidak Sesuai"
    elif now_distance <= 100 and now_distance > 5:
        suitability_score = 1
        address_suitability = "Sesuai"
    else:
        suitability_score = 2
        address_suitability = "Sangat Sesuai"

    return address_suitability


# * Function to calculate input variable to output variable
def data_preprocessing(data):
    # do some calculation to output variable
    data[["now_distance", "average_distance"]] = data.apply(
        lambda row: average_distance(row), axis=1, result_type="expand"
    )
    data["address_stability"] = data.apply(
        lambda row: calculate_address_stability(row), axis=1
    )
    data["address_suitability"] = data.apply(
        lambda row: calculate_address_suitability(row), axis=1
    )

    # selecting feature
    data = data[["average_distance", "address_stability", "address_suitability"]]

    # do preprocessing transformation in pipeline
    preprocessed_data = preprocessing_pipeline(data)

    return preprocessed_data


# * Function to transform data in pipeline
def preprocessing_pipeline(data):
    preprocessed_data = pipeline[1].fit_transform(data)
    feature_names = numerical_feature + ordinal_feature
    df_preprocessed = pd.DataFrame(
        preprocessed_data,
        columns=["average_distance",
                 "address_stability",
                 "address_suitability"],
    )
    return df_preprocessed
