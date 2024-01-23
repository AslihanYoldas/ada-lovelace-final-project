# Hotel Booking Cancellation Prediction

Data Science project for analyzing and visualizing hotel booking dataset and predicting booking status.

## Installation
Make sure you have Python installed. Clone the repository and install the required dependencies.


``` 
git clone https://github.com/AslihanYoldas/ada-lovelace-final-project.git

cd ada-lovelace-final-project.git

pip install -r requirements.txt 
```

## Data
[Dataset link](https://www.kaggle.com/datasets/youssefaboelwafa/hotel-booking-cancellation-prediction) 

- Dataset contains 36k rows and 27 columns.
- Original Columns:
    - Booking_ID  *string - ID of the booking (unique)*
    - number_of_adults *int - number of adults*
    - number_of_children *int - number of children*
    - number_of_weekend_nights *int - number of weekend nights*
    - number_of_week_nights *int - number of week nights*
    - type_of_meal *category - meal type (Meal type 1, Meal Type 2, Meal Type 3, Not Selected)*
    - car_parking_space *int- car parking space (0,1)*
    - room_type *category - room type (Room Type 1, Room Type 2, Room Type 3, Room Type 4)*
    - lead_time *int - number of days between the booking date and the arrival date*
    - market_segment_type *category - market segment type (Offline, Online, Corporate, Aviation, Complementary)*
    - repeated *int - Indicates whether the booking is a repeat booking (0,1)*
    - P_C *int - number of previous bookings that were canceled by the customer prior to the current booking*
    - P_not_C *int - number of previous bookings not canceled by the customer prior to the current booking*
    - average_price *float - average price of the booking*
    - special_requests *int - number of the special request*
    - date_of_reservation *datetime - Date of the booking*
    - booking_status *str- booking status (Canceled, Not Canceled)*
- New columns : This columns created by using existing columns 
    - reservation_day *int - day of the reservation (1-31)*
    - reservation_month *int - month of the reservation (1-12)*
    - reservation_year *int - year of the reservation (2016-2019)*
    - date_of_arrival *datetime - date of the arrival* 
    - arrival_day *int - day of the arrival (1-31)*
    - arrival_month *int - month of the arrival (1-12)*
    - arrival_year *int - year of the arrival (2018-2020)*
    - lead_month *int - number of months between the booking date and the arrival date*
    - number_of_total_nights *int - sum of week and weekend nights*
    - number_of_total_people *int - sum of adult and children*

## Data Preprocessing
[Preprocessing-notebook]('data_analyze.ipynb')
- Dataset doesn't have null values.

### Handling Outliers
#### How it detected ?
For each column thresholds determined. The low limit is the 10th percentile minus 1.5 times the range. The high limit is the 90th percentile sum 1.5 times the range. Also scatter plots created for each column. Sometimes looking to the scatter plots new thresholds determined and sometimes outliers that calculated doesn't determined as outliers. For example with the case of number of adults the algorithm detected 4 adults as outliers. Because 4 adults doesn't seem to be extreme situation detected outliers left in the dataset.

#### How it handled ?
For each outlier some other columns values compared to other data. The rows that contain some values as the outliers found. In that rows calculated the median of the that outliers' column and replace outlier with it.

Outliers detected and replaced in:
- Average Price
- Number of childeren
- Number of week nights
- Number of weekend nights
- P-C
- P-not-C
<br><br/>

 Also because there is only one row has the arrival date of 2016 and three rows has the arrival date of 2020 that rows dropped.


## Data Visualazation

## Feauture Selection 

### Logistic Regression
###

## Model Training
## Model Evaluation

## Results

## Contributing
Feel free to contribute by opening issues or submitting pull requests. 

## Contact
For questions or feedback, contact aslihanyoldas24@gmail.com