import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    cities = ['Chicago', 'New York', 'Washington']
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'all']
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday','all']

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("From which city would you like to have information (Chicago, New York or Washington): ").title()
        if city not in cities:
            print('Ups...the selected city is not available. Try again!')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Would you like to have information for a specific month (January, February, March, April, May, June) or would you like to see all (all)? ')
        if month not in months:
            print('Ups... the select month is not available. Try again')
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_of_week = input('Would you like to have information for a specific day of the week (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) or would you like to see all (all)? ')
        if day_of_week not in days_of_week:
            print('Ups... the select day of the week is not available. Try again')
            continue
        else:
            break

    print('-'*40)
    return city, month, day_of_week

def load_data(city, month, day_of_week):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':

        # use the index of the month list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day_of_week != 'all':

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day_of_week]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if df['month'].to_string != 'all':
        print(' ')
    else:
        most_popular_month = df['month'].mode()[0]
        print('Most popular month: %s' % most_popular_month)


    # display the most common day of week
    most_popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most popular day of the week: {}'.format(most_popular_day_of_week))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_popular_hour = df['hour'].mode()[0]
    print('Most popular hour: {}'.format(most_popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_popular_start_station = df['Start Station'].mode()[0]
    print('Most popular Start Station: {}'.format(most_popular_start_station))

    # display most commonly used end station
    most_popular_end_station = df['End Station'].mode()[0]
    print('Most popular End Station: {}'.format(most_popular_end_station))

    # display most frequent combination of start station and end station trip
    most_popular_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most popular Combination of Stations: {}'.format(most_popular_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time was {} seconds'.format(total_travel_time))

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('The average travel time was {} seconds'.format(avg_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Distribution of user types:')
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_distribution = df['Gender'].value_counts()
        print('The gender split is the following:')
        print(gender_distribution)
    else:
        print('Gender information unavailable')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        print('The oldest user was born in {}'.format(earliest_birth_year))

        latest_birth_year = int(df['Birth Year'].max())
        print('The youngest user was born in {}'.format(latest_birth_year))

        most_common_birth_year = int(df['Birth Year'].mode())
        print('The most common birth year is {}'.format(most_common_birth_year))
    else:
        print('Birth year information unavailable')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def data_display(df):
    """Logic that will make the user interaction effective printing 5 rows of raw data at a time and waiting for user input."""



    view_data = input('\nWould you like to see the first 5 lines of raw data? (yes/no)\n')
    row = 0
    while True:
        if view_data.lower() == 'yes':
            print(df.iloc[row:row+5])
            row += 5
            view_data = input("Would you like to see more data? (yes/no)").lower()
        else:
            break



def main():
    while True:
        city, month, day_of_week = get_filters()
        df = load_data(city, month, day_of_week)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_display(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
        main()
