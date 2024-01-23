from module.module_analyze_viz import *
from module.module_feauture_selection_modelling import *
from module.module_outliers import *
import numpy as np

# Load Dataset
df = pd.read_csv('data/booking.csv')

#Change column names
df.columns = [name.replace(' ','_') for name in df.columns]
df = df.rename(columns={'P-C': 'P_C', 'P-not-C': 'P_not_C'})

# Change datatypes 
#categorical
df = df_turn_datatype_to_categorical(df,['type_of_meal', 'room_type', 'market_segment_type', 'booking_status' ])
#datetime
# In 2018 Feb doesn't have 29 days
# Moving the data that have booking date 2/29/2018 to the previous day and changing the format
df.date_of_reservation = df.date_of_reservation.str.replace('2018-2-29', '2/28/2018')
df['date_of_reservation'] = pd.to_datetime(df['date_of_reservation'], format='%m/%d/%Y') 

# Handle Outliers
replace_average_price_outlier_with_median_of_similar_rows(df,'average_price')
replace_number_of_children_outlier_with_median_of_similar_rows(df, 8)
replace_number_of_weekend_nights_outlier_with_median_of_similar_rows(df)
replace_number_of_week_nights_outlier_with_median_of_similar_rows(df,11)
replace_P_C_outlier_with_median_of_similar_rows(df,10)
replace_P_not_C_outlier_with_median_of_similar_rows(df,30)
df = df.drop(df.query('arrival_year == 2016 | arrival_year == 2020 | reservation_year == 2016' ).index)

# Creating New Feautures
# Reservation date day/month/year
df["reservation_day"] = df["date_of_reservation"].dt.day
df["reservation_month"] = df["date_of_reservation"].dt.month
df["reservation_year"] = df["date_of_reservation"].dt.year
# Arrival day to hotel
# Sum of date of reservation and lead time(day between reservation and arrival)
df['date_of_arrival'] = df['date_of_reservation'].combine(df['lead_time'], lambda x,y: x + pd.DateOffset(days=y))
# Arrival date day/month/year
df["arrival_day"] = df["date_of_arrival"].dt.day
df["arrival_month"] = df["date_of_arrival"].dt.month
df["arrival_year"] = df["date_of_arrival"].dt.year
# how many months between reservation and arrival
df["lead_month"] = np.floor(df["lead_time"]/30).astype('int')
#total staying nights
df["number_of_total_nights"] = df["number_of_weekend_nights"]+df['number_of_week_nights']
#total number of people that staying
df["number_of_total_people"] = df["number_of_children"]+df['number_of_adults']

# Normalize the data
df_normalized = normalize_data(df,['Booking_ID','date_of_reservation','date_of_arrival','booking_status'])
X = df_normalized
y = df['booking_status']

# Feauture Selection
df_feauture_k_best_score, df_feautures_k_best = feauture_selection_select_k_best(8,X,y)
plot_bar(df_feauture_k_best_score,'feature_score', 'feature_name','K-Best Feature Importance Scores', 'Feauture Score', 'Feature Name',color='salmon',orient='h')
print("k-best features:", df_feautures_k_best.columns)
df_extra_tree_class_feature_score,df_feautures_extra_tree_class = feature_selection_extra_trees_classifier(X,y)
plot_bar(df_extra_tree_class_feature_score,'feature_score', 'feature_name','Extra Tree Class Feature Importance Scores', 'Feauture Score', 'Feature Name',color='salmon',orient='h')
print("Extra Tree classifier features:", df_feautures_extra_tree_class.columns)
df_logistic_feature_score, df_feautures_logistic = feauture_selection_logistic_regression(X,y)
plot_bar(df_logistic_feature_score,'feature_score', 'feature_name','Logistic Regression Feature Importance Scores', 'Feauture Score', 'Feature Name',color='salmon',orient='h')
print("Logistic Regression features:", df_feautures_logistic.columns)
df_dt_feature_score,df_feautures_dt = feature_selection_dt(X,y)
plot_bar(df_dt_feature_score,'feature_score', 'feature_name','Decision Tree Feature Importance Scores', 'Feauture Score', 'Feature Name',color='salmon',orient='h')
print("Decision Tree features:", df_feautures_dt.columns)

# Training and Evulating the models
# Logistic Regression
X_train, X_test, y_train, y_test = train_test_split( df_feautures_logistic, df['booking_status'], test_size=0.2, random_state=10)
logreg = LogisticRegression()
y_pred = train_model_and_predict(logreg,X_train,y_train,X_test)
evaluate_model(logreg,X_test,y_test, y_pred,'Logistic Regression Model')
#KNN
X_train, X_test, y_train, y_test = train_test_split( df_feautures_extra_tree_class, df['booking_status'], test_size=0.2, random_state=10)
knn = KNeighborsClassifier(n_neighbors=3)
y_pred = train_model_and_predict(knn,X_train,y_train,X_test)
evaluate_model(knn,X_test,y_test, y_pred, 'K Nearest Neighbour Classifier')
# Decision Tree
X_train, X_test, y_train, y_test = train_test_split( df_feautures_dt, df['booking_status'], test_size=0.2, random_state=10)
classifier = DecisionTreeClassifier()
y_pred = train_model_and_predict(classifier,X_train,y_train,X_test)
evaluate_model(classifier,X_test,y_test, y_pred, 'Decision Tree Classifier')
#SVM
X_train, X_test, y_train, y_test = train_test_split( df_feautures_extra_tree_class, df['booking_status'], test_size=0.2, random_state=10)
model = svm.SVC(kernel='linear')            
y_pred = train_model_and_predict(model,X_train,y_train,X_test)
evaluate_model(model,X_test,y_test, y_pred, 'Support Vector Classifier(SVC)')