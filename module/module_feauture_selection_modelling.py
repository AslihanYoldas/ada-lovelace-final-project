import matplotlib.pyplot as plt
import pandas as pd
from sklearn.calibration import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier

def encode_categorical_variable(categorical_data):
    """
    Encoding categorical data to numerical data

    :param categorical_data dataframe - dataframe that contains categorical one column 
    :return numpy array - Categorical data turn into numerical data
    """
    le = LabelEncoder()
    train = categorical_data.unique()
    return le.fit(train).transform(categorical_data)

def normalize_data(df, dropped_columns):
    """
    Normalizing the given dataframe except for dropped columns

    :param df dataframe - dataframe to be normalized
    :param dropped_columns list - column names that is not be normalized
    :return df_normalized dataframe - Normalized data frame 
    """

    scaler = StandardScaler()
    scaler.fit(df.drop(dropped_columns, axis=1))
    scaled_features = scaler.transform(df.drop(dropped_columns,axis=1))
    df_normalized= pd.DataFrame(scaled_features,columns=df.drop(dropped_columns,axis=1).columns)
    return df_normalized

def feauture_selection_select_k_best(df, k, X, y):
    """
    Select feautures with k_best and f_classif score function

    :param df dataframe - dataframe to select feautures
    :param k int - number of features to be selected
    :param X MatrixLike - data features
    :param y MatrixLike - data targets
    :return dataframe, dataframe df_feauture_k_best_score, df_feautures_k_best-
     Dataframe of features and their scores and for given df dataframe of selected features
    """

    k_best = SelectKBest(k=k, score_func=f_classif)
    k_best.fit_transform(X, y)
    # Get the indices of the selected features
    selected_features_indices = k_best.get_support(indices=True)
    # Get the scores associated with each feature
    feature_scores_k_best = k_best.scores_
    # Create a list of tuples containing feature names and scores
    feature_info = list(zip(X.columns, feature_scores_k_best))
    # Sort the feature info in descending order based on scores
    sorted_feature_info = sorted(feature_info, key=lambda x: x[1], reverse=True)
    # get feautre names and score
    feature_names, feature_scores = zip(*sorted_feature_info[:])
    # Turn into a dataframe 
    df_feauture_k_best_score = pd.DataFrame({'feature_name':feature_names,'feature_score':feature_scores})
    # Get the selected features data from the dataframe
    df_feautures_k_best =df.iloc[:, selected_features_indices]

    return df_feauture_k_best_score, df_feautures_k_best

def feature_selection_extra_trees_classifier(df, X, y):
    """
    Select feautures with ExtraTreesClassifier

    :param df dataframe - dataframe to select feautures
    :param X MatrixLike - data features
    :param y MatrixLike - data targets
    :return dataframe, dataframe df_extra_tree_class_feature_score, df_feautures_extra_tree_class -
     Dataframe of features and their scores and for given df dataframe of selected features
    """
    model = ExtraTreesClassifier()
    # fit the model
    model.fit(X, y)
    # summarize feature importance
    feature_info = list(zip(X.columns, model.feature_importances_))
    # sort the feature info in descending order based on scores
    sorted_feature_info = sorted(feature_info, key=lambda x: x[1], reverse=True)
    # get feautre names and score
    feature_names, feature_scores = zip(*sorted_feature_info[:])
    # turn into a dataframe
    df_extra_tree_class_feature_score = pd.DataFrame({'feature_name':feature_names,'feature_score':feature_scores})
    # select the feauters with high score
    extra_tree_class_selected_features = df_extra_tree_class_feature_score.query( 'feature_score > 0.05')['feature_name']
    # Get the selected features data from the dataframe
    df_feautures_extra_tree_class =df.loc[:, extra_tree_class_selected_features]
    return df_extra_tree_class_feature_score,df_feautures_extra_tree_class

def feauture_selection_logistic_regression(df, X, y):
  """
    Select feautures with Logistic Regression coefficents

    :param df dataframe - dataframe to select feautures
    :param X MatrixLike - data features
    :param y MatrixLike - data targets
    :return dataframe, dataframe df_logistic_feature_score,df_feautures_logistic -
     Dataframe of features and their scores and for given df dataframe of selected features
    """
  model = LogisticRegression()
  # fit the model
  model.fit(X, y)
  # get coefficents
  feature_scores_logistic = model.coef_[0]
  # summarize feature importance
  feature_info = list(zip(X.columns, feature_scores_logistic))
  # sort the feature info in descending order based on scores
  sorted_feature_info = sorted(feature_info, key=lambda x: x[1], reverse=True)
  # get feautre names and score
  feature_names, feature_scores = zip(*sorted_feature_info[:])
  # turn into a dataframe 
  df_logistic_feature_score = pd.DataFrame({'feature_name':feature_names,'feature_score':feature_scores})
  # select the feauters with high score
  logistic_regression_selected_features = df_logistic_feature_score.query( 'feature_score > 0.50 | feature_score < -0.50')['feature_name']
  # get the selected features data from the dataframe
  df_feautures_logistic =df.loc[:, logistic_regression_selected_features]

  return df_logistic_feature_score,df_feautures_logistic

# decision tree for feature importance on a classifier problem
def feature_selection_dt(df, X, y):
    """
    Select feautures with Decision Tree feature importance scores

    :param df dataframe - dataframe to select feautures
    :param X MatrixLike - data features
    :param y MatrixLike - data targets
    :return dataframe, dataframe df_dt_feature_score, df_feautures_dt -
     Dataframe of features and their scores and for given df dataframe of selected features
"""
    model = DecisionTreeClassifier()
    # fit the model
    model.fit(X, y)
    # get importance
    feature_scores_dt = model.feature_importances_
    # summarize feature importance
    feature_info = list(zip(X.columns, feature_scores_dt))
    # sort the feature info in descending order based on scores
    sorted_feature_info = sorted(feature_info, key=lambda x: x[1], reverse=True)
    # get feautre names and score
    feature_names, feature_scores = zip(*sorted_feature_info[:])
    # turn into a dataframe
    df_dt_feature_score = pd.DataFrame({'feature_name':feature_names,'feature_score':feature_scores})
    # select the feauters with high score
    dt_selected_features = df_dt_feature_score.query( 'feature_score > 0.05 | feature_score < -0.05')['feature_name']
    # get the selected features data from the dataframe
    df_feautures_dt =df.loc[:, dt_selected_features]

    return df_dt_feature_score,df_feautures_dt

def train_model_and_predict(model,X_train,y_train,X_test):
    """
    Training the given model with given train data and predicting test data returning the predictions

    :param model Any - The model (Logistic regression , knn classifiier etc.)
    :param X_train numpy array - Train data features
    :param y_train numpy array - Train data targets
    :param X_test numpy array - Test data features
    :return y_pred numpy array - Test data predictions
    """

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return y_pred

def evaluate_model(model, X_test, y_test, y_pred, title, display_labels=['Canceled','Not Canceled']):
    """
    Getting the normalize and not normalized confusion matrix  and printing the classification report for given model and data

    :param model Any - The model (Logistic regression , knn classifiier etc.)
    :param X_train numpy array - Train data features
    :param y_train numpy array - Train data targets
    :param y_test numpy array - Test data targets
    :param y_pred numpy array - Test data predictions
    :param display_labels list - The labels of the targets

    :return - shows the plot and print classification report

    """
    titles_options = [
    (title+" confusion matrix, without normalization", None),
    (title+" normalized confusion matrix", "true"),]
    for title, normalize in titles_options:
        disp = ConfusionMatrixDisplay.from_estimator(
            model,
            X_test,
            y_test,
            display_labels=display_labels,
            cmap=plt.cm.Greens,
            normalize=normalize,
        )
        disp.ax_.set_title(title)

        print(title)
        print(disp.confusion_matrix)

    plt.show()
    print(title + '\n' + classification_report(y_test,y_pred,labels=[0,1]))