import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    distance_matrix = pd.pivot_table(df, values='distance', index='id_start', columns='id_end', fill_value=0)
    distance_matrix = distance_matrix + distance_matrix.T  
    # Ensure symmetry


    return df


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    unrolled_df = df.melt(id_vars='id_start', var_name='id_end', value_name='distance')
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]  
    # Exclude same id_start to id_end


    return df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()
    threshold = 0.1 * reference_avg_distance
    selected_ids = df.groupby('id_start')['distance'].mean().abs() - reference_avg_distance <= threshold


    return df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    for vehicle in rate_coefficients:
        df[vehicle] = df['distance'] * rate_coefficients[vehicle]


    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    weekday_discounts = {0: 0.8, 1: 1.2, 2: 1.2, 3: 1.2, 4: 1.2}  # Monday to Friday
    weekend_discount = 0.7  # Saturday and Sunday

    df['start_day'] = df['start_time'].apply(lambda x: x.weekday()).map({0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday'})
    df['end_day'] = df['end_time'].apply(lambda x: x.weekday()).map({0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday'})

    df['start_time'] = df.apply(lambda row: apply_discount(row['start_time'], weekday_discounts) if row['start_day'] in weekday_discounts else apply_discount(row['start_time'], weekend_discount), axis=1)
    df['end_time'] = df.apply(lambda row: apply_discount(row['end_time'], weekday_discounts) if row['end_day'] in weekday_discounts else apply_discount(row['end_time'], weekend_discount), axis=1)

    return df

def apply_discount(time, discounts):
    if time < pd.to_datetime('10:00:00').time():
        return time.replace(hour=0, minute=0, second=0)  # 00:00:00
    elif time < pd.to_datetime('18:00:00').time():
        return time.replace(hour=10, minute=0, second=0)  # 10:00:00
    else:
        return time.replace(hour=18, minute=0, second=0)  # 18:00:00
    
