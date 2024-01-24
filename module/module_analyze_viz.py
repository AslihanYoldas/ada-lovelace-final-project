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

    
def plot_hist(df, title, xlabel, column_name, bin_num, kde, hue=None):
    """
    Plots histogram for the given dataframe's column.

    :param df: dataframe
    :param title: str - Title of the plot
    :param xlabel: str - Label of the x-axis
    :param column_name: str - x axis data's column name
    :param bin-num: int - Number of the bins
    :param kde: bool - Drawing the line 
    :param hue: str - Grouping variable column name
    
    :return : shows the plot"""
    
    plt.figure(figsize=(15,8))
    plt.title(title)
    plt.ylabel('Count')
    plt.xlabel(xlabel)
    sns.histplot(data = df, x = column_name, bins = bin_num,  kde = kde, hue=hue,
                 multiple="stack",
                palette="deep",
                edgecolor=".3",
                linewidth=.5,
     )
    plt.show()
    
    
    
def plot_count(data, title, xlabel,color=None,hue=None,palette=None):
    """Plots count plot for the given dataframe's column.

    :param data: dataframe that contains one column
    :param title: str - title of the plot
    :param xlabel: str - label of the x-axis
    :param hue: str - grouping variable column name
    :param color: string - color of the plot 
    :param palette: string - palette of the plot when using hue

    :return : shows the plot"""
    plt.figure(figsize=(15,8))
    plt.title(title)
    plt.xlabel(xlabel)
    sns.countplot(x=data,color=color,hue=hue, palette=palette,orient='v',stat='percent')
    plt.show()
  

def plot_bar(df, colmn_name_x, colmn_name_y, title, xlabel, ylabel, color, orient='v'):
    """
    Plots bar plot for the given data.

    :param df: dataframe
    :param column_name_x: str - x axis data's column name
    :param column_name_y: str - y axis data's column name
    :param title: str - Title of the plot
    :param xlabel: str - Label of the x-axis
    :param ylabel: str - Label of the y-axis
    :param color: string - color of the plot 
    :param orien: string - Orientation of the plot (orient ='v')

    :return : shows the plot"""
    plt.figure(figsize=(15,8))
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    sns.barplot(data=df,
                x=colmn_name_x,
                y=colmn_name_y,
                color=color,
                orient = orient
                )
    plt.show()

def corr_heatmap(df):
    """
    Calculates correllation for given dataframe and plot it as a heatmap

    :param df: dataframe 
  
    :return :shows the plot
    """
    
    matrix = df.corr()
    plt.figure(figsize=(15,8))
    sns.heatmap(matrix, 
            xticklabels=matrix.columns.values,
            yticklabels=matrix.columns.values,
            cmap=sns.diverging_palette(20, 220, n=200),
            vmin=-1,
            vmax=1,
            square=True
    )
    plt.show()
