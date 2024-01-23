import matplotlib.pyplot as plt
import seaborn as sns


def df_turn_datatype_to_categorical(df,column_names):
    """
    In a dataframe turns the given columns' data types to categorical.

    :param df: dataframe 
    :param column_names: list- column names 
  
    :return df:dataframe -Returns the dataframe after changing data types to categorical for given column names
    """
    for column_name in column_names:
        df[column_name] = df[column_name].astype('category')
    return df 

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
    
def plot_hist(df, title, xlabel, column_name, bin_num, kde, color='maroon'):
    """
    Plots histogram for the given dataframe's column.

    :param df: dataframe
    :param title: str - Title of the plot
    :param xlabel: str - Label of the x-axis
    :param column_name: str - x axis data's column name
    :param bin-num: int - Number of the bins
    :param kde: bool - Drawing the line 

    :return : shows the plot"""
    plt.figure(figsize=(15,8))
    plt.title(title)
    plt.ylabel('Count')
    plt.xlabel(xlabel)
    sns.histplot(data = df, x = column_name, bins = bin_num,  kde = kde, color = color )
    plt.show()
    
    


def plot_scatter(x, y, title, xlabel, ylabel, hue=None, palette=None, color= None, marker='x'):
    """
    Scatter plot for the given dataframe's columns.

    :param df: dataframe
    :param column_name_x: str - x axis data's column name
    :param column_name_y: str - y axis data's column name
    :param title: str - Title of the plot
    :param xlabel: str - Label of the x-axis
    :param ylabel: str - Label of the y-axis

    :return : shows the plot
    """
    plt.figure(figsize=(15,8))
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.scatter(x = x,
                y = y,
                hue = hue,
                palette = palette,
                color = color,
                marker=marker
            
                )
    plt.show(sns)

def plot_bar(df, colmn_name_x, colmn_name_y, title, xlabel, ylabel, hue = None, palette=None, color= None, hue_order=None,order=None, orient='v'):

    plt.figure(figsize=(15,8))
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    sns.barplot(data=df,
                hue=hue,
                hue_order=hue_order,
                x=colmn_name_x,
                y=colmn_name_y,
                palette=palette,
                order=order,
                color=color,
                orient=orient
                )
    plt.show()
    
def plot_count(data, title, xlabel,color=None,order=None,hue=None,palette=None):
    plt.figure(figsize=(15,8))
    plt.title(title)
    plt.xlabel(xlabel)
    sns.countplot(x=data,color=color,hue=hue, palette=palette,orient='v',stat='percent',order=order)
    plt.show()
  



def corr_heatmap(df, column_names):
    """
    Calculates correllation between given dataframe's columns and shows it as a heatmap

    :param df: dataframe 
    :param column_names: list -column names 
  
    :return :shows the plot
    """
    
    matrix = df[column_names].corr()
    sns.heatmap(matrix, 
            xticklabels=matrix.columns.values,
            yticklabels=matrix.columns.values,
            cmap='RdYlBu',
            vmin=-1,
            vmax=1
            )
    plt.show()