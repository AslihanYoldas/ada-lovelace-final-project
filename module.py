import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors


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
    
    


def plot_scatter(df, colmn_name_x, colmn_name_y, hue, palette, title, xlabel, ylabel):
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
    sns.scatterplot(data=df,
                x=colmn_name_x,
                y=colmn_name_y,
                hue=hue,
                palette=palette
                )
    plt.show()

def plot_bar(df, colmn_name_x, colmn_name_y, title, xlabel, ylabel, hue, palette='pastel'):

    plt.figure(figsize=(15,8))
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    sns.barplot(data=df,
                hue=hue,
                x=colmn_name_x,
                y=colmn_name_y,
                palette=palette
                )
    plt.show()
    
def plot_count(data, title, xlabel,color):
    plt.figure(figsize=(15,8))
    plt.title(title)
    plt.xlabel(xlabel)
    sns.countplot(x=data,color=color,orient='v',stat='percent')
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
            vmin=-1)
    plt.show()