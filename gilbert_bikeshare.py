import time
from os import path

import pandas as pd
import numpy as np

DATA_DIR = "bikeshare_data"
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = ['January', 'February', 'March', 'April', 'June', 'May', 'None']
cities = ['chicago', 'new york city', 'washington']


def get_filters():
    """
    Asks user to specify a city, month, and day in order to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\n Which city would you like to analyse? (Chicago, New york city, Washington) \n").lower()
        if city in cities:
            break
        else:
            print("\n Please enter a valid city name")

            # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nWhich month would you like to consider? (January, February, March, April, May, June)? Type "
                      "'None' for no month filter\n").title()
        if month in months:
            break
        else:
            print("\n Please enter a valid month")

            # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'None']
        day = input("\nWhich day of the week would you like to consider? (Monday, Tuesday, Wednesday, Thursday, "
                    "Friday, Saturday, Sunday)? Type 'None' for no day filter \n").title()
        if day in days:
            break
        else:
            print("\n Please enter a valid day")

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to be analyzed
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    date_cols = ['Start Time', 'End Time']
    try:
        df = pd.read_csv(path.join(DATA_DIR, CITY_DATA[city]), parse_dates=date_cols)

        # convert the Start Time column to datetime
        # df['Start Time'] = pd.to_datetime(df['Start Time'])

        # extract month and day of week from Start Time to create new columns
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.day_name()
        df['hour'] = df['Start Time'].dt.hour

        # filter by month if applicable
        if month != 'None':
            # use the index of the months list to get the corresponding int
            month = months.index(month) + 1

            # filter by month to create the new dataframe
            df = df[df['month'] == month]

            # filter by day of week if applicable
        if day != 'None':
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day]
        return df
    except:
        print("\nData files not found. Please check file location (%s)" % DATA_DIR)
        return None


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    try:
        # display the most common month
        if month == 'None':
            pop_month = df['month'].mode()[0]
            pop_month = months[pop_month - 1]
            print("The most Popular month is", pop_month)

        # display the most common day of week
        if day == 'None':
            pop_day = df['day_of_week'].mode()[0]
            print("The most Popular day is", pop_day)

        # display the most common start hour
        pop_hour = df['hour'].mode()[0]
        print("The popular Start Hour is {}:00 hrs".format(pop_hour))
    except:
        print(
            "A data error occurred. Please check that the right data is present in the expected location (%s)" % DATA_DIR)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    try:
        pop_start_station = df['Start Station'].mode()[0]
        print("The most commonly used Start Station is {}".format(pop_start_station))

        # display most commonly used end station
        pop_end_station = df['End Station'].mode()[0]
        print("The most commonly used End Station is {}".format(pop_end_station))

        # display most frequent combination of start station and end station trip
        df['combination'] = df['Start Station'] + " " + "to" + " " + df['End Station']
        pop_com = df['combination'].mode()[0]
        print("The most frequent combination of Start and End Station is {} ".format(pop_com))
    except:
        print(
            "A data error occurred. Please check that the right data is present in the expected location (%s)" % DATA_DIR)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    try:
        # display total travel time
        total_duration = df['Trip Duration'].sum()
        minute, second = divmod(total_duration, 60)
        hour, minute = divmod(minute, 60)
        print("The total trip duration: {} hour(s) {} minute(s) {} second(s)".format(hour, minute, second))

        # display mean travel time
        average_duration = round(df['Trip Duration'].mean())
        m, sec = divmod(average_duration, 60)
        if m > 60:
            h, m = divmod(m, 60)
            print("The average trip duration: {} hour(s) {} minute(s) {} second(s)".format(h, m, sec))
        else:
            print("The average trip duration: {} minute(s) {} second(s)".format(m, sec))

    except:
        print(
            "A data error occurred. Please check that the right data is present in the expected location (%s)" % DATA_DIR)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        # Display counts of user types
        user_counts = df['User Type'].value_counts()
        print("The user types are:\n", user_counts)

        # Display counts of gender
        if city.title() == 'Chicago' or city.title() == 'New York City':
            gender_counts = df['Gender'].value_counts()
            print("\nThe counts of each gender are:\n", gender_counts)

            # Display earliest, most recent, and most common year of birth
            earliest = int(df['Birth Year'].min())
            print("\nThe oldest user is born in the year", earliest)
            most_recent = int(df['Birth Year'].max())
            print("The youngest user is born in the year", most_recent)
            common = int(df['Birth Year'].mode()[0])
            print("Most users are born in the year", common)
    except:
        print(
            "A data error occurred. Please check that the right data is present in the expected location (%s)" % DATA_DIR)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def print_raw_data(iterator):
    """Displays 5 rows from the iterator passed in"""

    # Show 5 rows
    for x in range(0, 5):
        try:
            row = next(iterator)
            print(row)
        # If we come to the end of the iterator
        except StopIteration:
            print("\nNo more data")
            return False
    return True


def prompt_raw_data_display(df, columns):
    """Prompt the user if they want to see the raw data"""

    # filter by supplied columns
    df_tmp = df[columns]
    while True:
        rd = input("\nWould you like to see raw data?\n").lower()
        if rd not in ("yes", "no"):
            print("\nPlease enter 'yes' or 'no'")
        else:
            break
    if rd == 'yes':
        # get an iterator to walk through the raw data
        iterator = df_tmp.itertuples()
        show_next_rows = None

        # Check if the user has not entered "no" and that we are not at the end of the iterator
        while show_next_rows != "no" and print_raw_data(iterator):
            while True:
                show_next_rows = input("\nWould you like to see more data?\n").lower()
                if show_next_rows not in ("yes", "no"):
                    print("\nPlease enter 'yes' or 'no'")
                else:
                    break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # If data load failed, exit
        if df is None:
            exit()

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        # Filter the columns to return in the raw data
        if city in ['chicago', 'new york city']:
            columns = ["Start Time", "End Time", "Trip Duration", "Start Station", "End Station", "User Type", "Gender",
                       "Birth Year"]
        else:
            columns = ["Start Time", "End Time", "Trip Duration", "Start Station", "End Station", "User Type"]

        # Ask user if they want to see raw data
        prompt_raw_data_display(df, columns)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
