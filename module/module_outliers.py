import math


# Find the thresold of outliers with IQR
# IQR normally between first quartile(25) and third quartile(75) 
# But here we define range as between 10th 90th percentile
# If data higher than sum of 90th percentile and range times 1.5 count as a outlier
# If data lower than difference of 10th percentile and range times 1.5 count as a outlier
def outlier_thresholds(df, col_name, p1=0.1, p2=0.9):
    percentile1 = df[col_name].quantile(p1)
    percentile2 = df[col_name].quantile(p2)
    interpercentile_range = percentile2 - percentile1
    up_limit = percentile2 + 1.5 * interpercentile_range
    low_limit = percentile1 - 1.5 * interpercentile_range
    return low_limit, up_limit # To find low and up thresholds


def check_outlier(df, col_name):
    low_limit, up_limit = outlier_thresholds(df, col_name)
    if ((df[col_name] > up_limit) | (df[col_name] < low_limit)).any():
        return True
    else:
        return False # To check if variables have outliers.
    
# If outliers exists get the outliers
# Getting the outliers tresholds and finding the data exceeding thresholds
def get_outlier(df,col_name):
    low_limit, up_limit = outlier_thresholds(df, col_name)
    if check_outlier(df,col_name):
        return df[(df[col_name] > up_limit) | (df[col_name] < low_limit)]
    else:
        return 'No outlier found'



def replace_average_price_outlier_with_median_of_similar_rows(df,col_name='average_price'):
    threshold = outlier_thresholds(df, col_name)[1]
    try:
        outlier_index = get_outlier(df, col_name).index
    except TypeError:
        return 'No outlier found'
    for index in outlier_index:
        # Getting the outlier's data
        number_of_adults=df.loc[index,'number_of_adults']
        number_of_children=df.loc[index,'number_of_children']
        number_of_weekend_nights=df.loc[index,'number_of_weekend_nights']
        number_of_week_nights=df.loc[index,'number_of_week_nights']
        type_of_meal=df.loc[index,'type_of_meal']
        room_type=df.loc[index,'room_type']
        # Getting the median of outlier's similar rows 
        new_value =df.query('number_of_adults == @number_of_adults & \
                            number_of_week_nights == @number_of_week_nights & \
                            number_of_children == @number_of_children & \
                            number_of_weekend_nights == @number_of_weekend_nights & \
                            type_of_meal == @type_of_meal  & \
                            room_type ==@room_type  & \
                            average_price < @threshold')[col_name].median()
        if math.isnan(new_value):
            new_value =df.query('number_of_adults == @number_of_adults & \
                            number_of_week_nights == @number_of_week_nights & \
                            number_of_weekend_nights == @number_of_weekend_nights & \
                            type_of_meal == @type_of_meal  & \
                            average_price < @threshold')[col_name].median()
        df.loc[index,col_name]=new_value
    return 'Outliers filled with similar rows median value'

def replace_number_of_children_outlier_with_median_of_similar_rows(df, threshold, col_name='number_of_children'):
    try:
        outlier_index = df[(df[col_name] > threshold)].index
    except TypeError:
        return 'No outlier found'
    for index in outlier_index:
        # Getting the outlier's data
        number_of_adults=df.loc[index,'number_of_adults']
        average_price=df.loc[index,'average_price']
        type_of_meal=df.loc[index,'type_of_meal']
        room_type=df.loc[index,'room_type']
        # Getting the median of outlier's similar rows 
        new_value =df.query('number_of_adults == @number_of_adults & \
                             type_of_meal == @type_of_meal  & \
                            room_type ==@room_type  & \
                            average_price ==@average_price  & \
                            number_of_children < @threshold')[col_name].median()
        df.loc[index,col_name]=round(new_value)
    return 'Outliers filled with similar rows median value'
def replace_number_of_weekend_nights_outlier_with_median_of_similar_rows(df,col_name='number_of_weekend_nights'):
    threshold = outlier_thresholds(df, col_name)[1]
    try:
        outlier_index = get_outlier(df, col_name).index
    except TypeError:
        return 'No outlier found'
    for index in outlier_index:
        # Getting the outlier's data
        number_of_adults=df.loc[index,'number_of_adults']
        number_of_children=df.loc[index,'number_of_children']
        number_of_weekend_nights=df.loc[index,'number_of_weekend_nights']
        type_of_meal=df.loc[index,'type_of_meal']
        room_type=df.loc[index,'room_type']
        # Getting the median of outlier's similar rows 
        new_value =df.query('number_of_adults == @number_of_adults & \
                            number_of_children == @number_of_children & \
                            type_of_meal == @type_of_meal  & \
                            room_type ==@room_type  & \
                            number_of_weekend_nights < @threshold')[col_name].median()
        
        df.loc[index,col_name]=round(new_value)
    return 'Outliers filled with similar rows median value'
def replace_number_of_week_nights_outlier_with_median_of_similar_rows(df, threshold, col_name='number_of_week_nights'):
    try:
        outlier_index = df[(df[col_name] > threshold)].index
    except TypeError:
        return 'No outlier found'
    for index in outlier_index:
        # Getting the outlier's data
        number_of_adults=df.loc[index,'number_of_adults']
        number_of_children=df.loc[index,'number_of_children']
        number_of_weekend_nights=df.loc[index,'number_of_weekend_nights']
        type_of_meal=df.loc[index,'type_of_meal']
        room_type=df.loc[index,'room_type']
        average_price=df.loc[index,'average_price']
        # Getting the median of outlier's similar rows 
        new_value =df.query('number_of_adults == @number_of_adults & \
                            number_of_children == @number_of_children & \
                            type_of_meal == @type_of_meal  & \
                            room_type ==@room_type  & \
                            number_of_weekend_nights < @threshold')[col_name].median()
        
        df.loc[index,col_name]=round(new_value)
    return 'Outliers filled with similar rows median value'

def replace_P_C_outlier_with_median_of_similar_rows(df, threshold, col_name='P_C'):
    try:
        outlier_index = df[(df[col_name] > threshold)].index
    except TypeError:
        return 'No outlier found'
    for index in outlier_index:
        # Getting the outlier's data
        number_of_adults=df.loc[index,'number_of_adults']
        number_of_children=df.loc[index,'number_of_children']
        number_of_weekend_nights=df.loc[index,'number_of_weekend_nights']
        number_of_week_nights=df.loc[index,'number_of_week_nights']
        type_of_meal=df.loc[index,'type_of_meal']
        room_type=df.loc[index,'room_type']
        average_price=df.loc[index,'average_price']
        # Getting the median of outlier's similar rows 
        new_value =df.query('number_of_adults == @number_of_adults & \
                            number_of_children == @number_of_children & \
                            type_of_meal == @type_of_meal  & \
                            room_type ==@room_type  & \
                            P_C < @threshold')[col_name].median()
        df.loc[index,col_name]=round(new_value)
    return 'Outliers filled with similar rows median value'

def replace_P_not_C_outlier_with_median_of_similar_rows(df, threshold, col_name='P_not_C'):
    try:
        outlier_index = df[(df[col_name] > threshold)].index
    except TypeError:
        return 'No outlier found'
    for index in outlier_index:
        # Getting the outlier's data
        number_of_adults=df.loc[index,'number_of_adults']
        number_of_children=df.loc[index,'number_of_children']
        number_of_weekend_nights=df.loc[index,'number_of_weekend_nights']
        number_of_week_nights=df.loc[index,'number_of_week_nights']
        type_of_meal=df.loc[index,'type_of_meal']
        room_type=df.loc[index,'room_type']
        average_price=df.loc[index,'average_price']
        # Getting the median of outlier's similar rows 
        new_value =df.query('number_of_adults == @number_of_adults & \
                            number_of_children == @number_of_children & \
                            type_of_meal == @type_of_meal  & \
                            room_type ==@room_type  & \
                            average_price ==@average_price  & \
                            P_C < @threshold')[col_name].median()
        
        df.loc[index,col_name]=round(new_value)
    return 'Outliers filled with similar rows median value'