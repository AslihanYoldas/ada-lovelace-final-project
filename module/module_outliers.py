import math
 

def outlier_thresholds(df, col_name, p1=0.1, p2=0.9):
    """
    In a dataframe finds the given column's thresholds for outliers with given percentiles.
    The low limit is the first percentile (p1)  minus 1.5 times the range. 
    The high limit is the second percentile (p2) sum 1.5 times the range. 

    :param df: dataframe 
    :param col_name: str- column name
    :param p1: float- first percentile (p1= 0.1)
    :param p2: float- second percentile (p2= 0.9)
  
    :return low_limit, up_limit:float,float -Returns the low threshold and high treshold for outliers
    """
    percentile1 = df[col_name].quantile(p1)
    percentile2 = df[col_name].quantile(p2)
    interpercentile_range = percentile2 - percentile1
    up_limit = percentile2 + 1.5 * interpercentile_range
    low_limit = percentile1 - 1.5 * interpercentile_range
    return low_limit, up_limit 


def check_outlier(df, col_name):
    """
    Checks if for given dataframe column has outlier using outlier_threshold() function

    :param df: dataframe 
    :param col_name: str- column name

    :return bool -Returns true if there is outliers otherwise it returns false
    """
    low_limit, up_limit = outlier_thresholds(df, col_name)
    if ((df[col_name] > up_limit) | (df[col_name] < low_limit)).any():
        return True
    else:
        return False # To check if variables have outliers.
    
# If outliers exists get the outliers
# Getting the outliers tresholds and finding the data exceeding thresholds
def get_outlier(df,col_name):
    """
    If outliers exists get the outliers using outlier_threshold() and check_outlier() functions.

    :param df: dataframe 
    :param col_name: str- column name

    :return dataframe or string -Returns the outliers' rows in the dataframe if outliers exist
      otherwise it returns "no outlier found" string
    """
    low_limit, up_limit = outlier_thresholds(df, col_name)
    if check_outlier(df,col_name):
        return df[(df[col_name] > up_limit) | (df[col_name] < low_limit)]
    else:
        return 'No outlier found'


## Replacing Outliers Functions
def replace_average_price_outlier_with_median_of_similar_rows(df,col_name='average_price'):
    """
    In average price column get the outliers and replace them. The new value found by getting
    similar rows to the outlier and calculating median of that rows' average prices.

    :param df: dataframe 
    :param col_name: str- column name =  average_price

    :return str - Returns confirmation text  """
    # Getting the upper limit
    threshold = outlier_thresholds(df, col_name)[1]
    try:
        # Getting the outliers indexes
        outlier_index = get_outlier(df, col_name).index
    except TypeError:
        # If outlier not exist
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
        # If not similar rows found
        if math.isnan(new_value):
            new_value =df.query('number_of_adults == @number_of_adults & \
                            number_of_week_nights == @number_of_week_nights & \
                            number_of_weekend_nights == @number_of_weekend_nights & \
                            type_of_meal == @type_of_meal  & \
                            average_price < @threshold')[col_name].median()
        # Replace the outlier
        df.loc[index,col_name]=new_value
    return 'Outliers filled with similar rows median value'

def replace_number_of_children_outlier_with_median_of_similar_rows(df, threshold, col_name='number_of_children'):
    """
    In number_of_children column get the outliers and replace them. The new value found by getting
    similar rows to the outlier and calculating median of that rows' number of children.

    :param df: dataframe 
    :param threshold: int - Outlier upper limit
    :param col_name: str- column name =  number_of_children

    :return str - Returns confirmation text  """
    try:
        # Getting the outliers indexes
        outlier_index = df[(df[col_name] > threshold)].index
    except TypeError:
        # If outlier not exist
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

        # Replace the outlier
        df.loc[index,col_name]=round(new_value)
    return 'Outliers filled with similar rows median value'

def replace_number_of_weekend_nights_outlier_with_median_of_similar_rows(df,col_name='number_of_weekend_nights'):
    """
    In number_of_weekend_nights column get the outliers and replace them. The new value found by getting
    similar rows to the outlier and calculating median of that rows' number of weekend nights.

    :param df: dataframe 
    :param col_name: str- column name =  number_of_weekend_nights

    :return str - Returns confirmation text  """
    # Getting the upper limit
    threshold = outlier_thresholds(df, col_name)[1]
    try:
        # Getting the outliers indexes
        outlier_index = get_outlier(df, col_name).index
    except TypeError:
        # If outlier not exist
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
        # Replace the outlier
        df.loc[index,col_name]=round(new_value)
    return 'Outliers filled with similar rows median value'

def replace_number_of_week_nights_outlier_with_median_of_similar_rows(df, threshold, col_name='number_of_week_nights'):

    """In number_of_week_nights column get the outliers and replace them. The new value found by getting
    similar rows to the outlier and calculating median of that rows' number of week nights.

    :param df: dataframe 
    :param threshold: int - Outlier upper limit
    :param col_name: str- column name =  number_of_week_nights

    :return str - Returns confirmation text  """
    try:
        # Getting the outliers indexes
        outlier_index = df[(df[col_name] > threshold)].index
    except TypeError:
        # If outlier not exist
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
        # Replace the outlier
        df.loc[index,col_name]=round(new_value)
    return 'Outliers filled with similar rows median value'

def replace_P_C_outlier_with_median_of_similar_rows(df, threshold, col_name='P_C'):
    """In P_C column get the outliers and replace them. The new value found by getting
    similar rows to the outlier and calculating median of that rows' P_C values.

    :param df: dataframe 
    :param threshold: int - Outlier upper limit
    :param col_name: str- column name = P_C

    :return str - Returns confirmation text  """
    
    try:
        # Getting the outliers indexes
        outlier_index = df[(df[col_name] > threshold)].index
    except TypeError:
        # If outlier not exist
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
        # Replace the outliers
        df.loc[index,col_name]=round(new_value)
    return 'Outliers filled with similar rows median value'

def replace_P_not_C_outlier_with_median_of_similar_rows(df, threshold, col_name='P_not_C'):
    """In P_not_C column get the outliers and replace them. The new value found by getting
    similar rows to the outlier and calculating median of that rows' P_not_C values.

    :param df: dataframe 
    :param threshold: int - Outlier upper limit
    :param col_name: str- column name = P_not_C

    :return str - Returns confirmation text  """
    try:
        # Getting the outliers indexes
        outlier_index = df[(df[col_name] > threshold)].index
    except TypeError:
        # If outlier not exist
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
        # Replace the outliers
        df.loc[index,col_name]=round(new_value)
    return 'Outliers filled with similar rows median value'