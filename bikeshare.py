import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


print('Hello! Let\'s explore some US bikeshare data!')


# below I've created the get_filters function that takes the user selection of city, month and day .. and return the 3 values in a usable format

def get_filters():

    # creating the lists of valid options and setting the default value for month and day filters to "all"

    month, day = "all", "all"
    
    cities = ["chicago" , "washington" , "new york city"]
    
    months = ["january", "february", "march", "april", "may", "june"]
    
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    
    # now it's time to take the user's choice of the city
    
    city = input("Please enter one of the following 3 city names: chicago, new york city and washington: ").lower()
    
    # a while loop to make sure the user enters a valid city name
    
    while city not in cities:
        city = input("Incorrect city name, Please enter one of the following 3 city names: 'chicago', 'new york city' or 'washington': ").lower()
        
        
    # now let's see if the user would like to filter the stats or not, and if so by month ? or day ? or both ?
    
    filter = input("would you like to filter the stats by month, day or both ?  (enter 'no' to skip): ").lower()
    
    # making sure the user enters a valid filter through a while loop that rejects invalid inputs
    
    while filter not in ["month", "day", "both", "no"]:
        filter = input("Incorrect input, Please enter 'month' to filter the stats by month or 'day' to filter the stats by day or 'both' to filter the stats by both month and day, you can skip filter selection by entering 'no': ").lower()

    # now let's take the user's choices of filters and prevent invalid inputs through while loops similar to the previous one

    if filter != "no":
        
        if filter == "month":
            month = input("which month would you like to see the stats for ? (january, february, march, april, may or june) : ").lower()
            while month not in months:
                month = input("Incorrect month entered, Please enter the name of the month you'd like to filter the stats by (january, february, march, april, may or june): ").lower()
        
        if filter == "day":
            day = input("which day you like to see the stats for ? ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' or 'sunday') : ").lower()
            while day not in days:
                day = input("Incorrect day entered, Please enter the day you'd like to filter the stats by ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' or 'sunday'): ").lower()
        
        if filter == "both":
            month = input("which month would you like to see the stats for ? (january, february, march, april, may or june) : ").lower()
            while month not in months:
                month = input("Incorrect month entered, Please enter the name of the month you'd like to filter the stats by (january, february, march, april, may or june): ").lower()
            day = input("which day you like to see the stats for ? (monday, tuesday, wednesday, thursday, friday, saturday or sunday) : ").lower()
            while day not in days:
                day = input("Incorrect day entered, Please enter the day you'd like to filter the stats by ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' or 'sunday'): ").lower()
    
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # first we convert the city's data set csv to a pandas data frame using the dictionary "CITY_DATA" and the user's choice of city from the get_filters() function as the key
    
    df = pd.read_csv(CITY_DATA[city])

    # converting the start time and end time columns to "date time" objects that we can work with
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # now that we have a datetime formatted coloumns, let's create a separate coloumn for the month
    
    df['month'] = df['Start Time'].dt.month

    
    # creating a new dataframe that only includes the month and day the user chose in the get_filters() function (only if the user chose a specific month)

    if month != 'all':
    
        # creating a variable that hold the month's index in the calender, +1 is to offset the zero based indexing of python lists
        
        months_list = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months_list.index(month) + 1

        # overwriting the data frame with a new one where the month's column = the month's index
        df = df[df['month'] == month]

    # creating a column for the week day
    
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # last step: filter by day
    
    if day != 'all':
        
        #overwriting the data frame with a new one where there's only stats for the week day chosen
        
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    
    # here I've used the mode method to get the most frequent month
    most_common_month = df['month'].mode()[0]

    # here I'm converting month calendar indices back into month names, primitive way to do it :) but I've got no time left to think about a better way lol

    if most_common_month == 1:
        most_common_month = "January"
    if most_common_month == 2:
        most_common_month = "February"
    if most_common_month == 3:
        most_common_month = "March"
    if most_common_month == 4:
        most_common_month = "April"
    if most_common_month == 5:
        most_common_month = "May"
    if most_common_month == 6:
        most_common_month = "June"

    print("The most common month is: {}".format(most_common_month))

    # using a different method to get the most common for the day of the week since the mode method is not working this time for some reason
    print("The most common day is: ", df['day_of_week'].value_counts().idxmax())

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    
    # similar to what I did with the months, but much longer and dumb xD

    if most_common_hour > 12:
        if most_common_hour == 13:
            most_common_hour = "1 PM"
        if most_common_hour == 14:
            most_common_hour = "2 PM"
        if most_common_hour == 15:
            most_common_hour = "3 PM"
        if most_common_hour == 16:
            most_common_hour = "4 PM"
        if most_common_hour == 17:
            most_common_hour = "5 PM"
        if most_common_hour == 18:
            most_common_hour = "6 PM"
        if most_common_hour == 19:
            most_common_hour = "7 PM"
        if most_common_hour == 20:
            most_common_hour = "8 PM"
        if most_common_hour == 21:
            most_common_hour = "9 PM"
        if most_common_hour == 22:
            most_common_hour = "10 PM"
        if most_common_hour == 23:
            most_common_hour = "11 PM"
        print("The most common hour is: {}".format(most_common_hour))
    else:
        print("The most common hour is: {} AM".format(most_common_hour))
            
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common start station is: ", df ['Start Station'].mode()[0])

    # display most commonly used end station
    print("The most common end station is: ", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    
    # below I'm using groupby to group the start and end stations together and get the most common pair
    
    print("The most frequent combination of start station and end station trip: {}".format(df.groupby(['Start Station','End Station']).size().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() / 3600.0  # converting seconds to hours 
    print("total travel time: ", total_travel_time, "Hours")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 3600.0  # converting seconds to hours 
    print("mean travel time: ", mean_travel_time, "Hours")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types, I'm using .string to get rid of the annoying "dtype" that gets printed 
    user_types = df['User Type'].value_counts()
    print(user_types.to_string())
    
    # Display counts of gender, I've used try except to avoid keyerror because washington does not keep track of user genders
    try:
        user_genders = df['Gender'].value_counts()
        print(user_genders.to_string())
    except KeyError:
        print("No gender data for Washington")


    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year_of_birth = int(df['Birth Year'].min())
        most_recent_year_of_birth = int(df['Birth Year'].max())
        most_common_year_of_birth = int(df['Birth Year'].mode()[0])
        print("earliest year of birth: " , earliest_year_of_birth)
        print("most recent year of birth: " , most_recent_year_of_birth)
        print("most common year of birth: " , most_common_year_of_birth)

    except KeyError:
        print("No date of birth data for Washington users")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def data_rows(df):
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no").lower()
    start_loc = 0
    while (view_data != "no"):
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: yes or no  ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_rows(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()