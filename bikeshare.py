import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv' }
cities = ['chicago', 'new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Enter City name (Chicago, New york city, Washington): ").lower()
        if city not in cities:
            print("Sorry the city entered isn't in the list! Try again")
            continue
        else:
            break
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("Select a month (all, january, february, ... , june): ").lower()
        if month not in months:
            print("You made a typo! Try again")
            continue
        else:
            break
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter day of week (all, monday, tuesday, ... sunday): ").lower()
        if day not in days:
            print("You made a typo! Try again")
            continue
        else:
            break


    print('-'*40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month
    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most Common month:', common_month)
    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most Common day:', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    # extract hour from the Start Time column to create an hour column
    common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Start_Station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station is: {}".format(Start_Station))

    # display most commonly used end station
    End_Station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station is: {}".format(End_Station))

    # display most frequent combination of start station and end station trip
    Combination_Station = df.groupby(['Start Station', 'End Station']).count()
    print("The most commonly used end station is: {} & {}".format(Start_Station, End_Station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_drive_time = sum(df["Trip Duration"])
    print("The total travel time = {} hours".format(total_drive_time/3600))
    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print("The mean travel time = {} hours".format(mean_travel_time/3600))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types, '\n')

    # Display counts of gender
    try:
        user_gender = df['Gender'].value_counts()
        print(user_gender, '\n')
    except KeyError:
        print("Sorry The washington City files don't have the Gender column to display counts of gender.\n")

    # Display earliest, most recent, and most common year of birth
    try:
        Earliest_Year = df['Birth Year'].min()
        print("\n The earliest year of birth is: {}".format(Earliest_Year))
    except KeyError:
        print("Sorry The washington City files don't have the Birth Year column to calculate the earliest year of birth.\n")

    try:
        Most_Recent = df['Birth Year'].max()
        print("\n The most recent year of birth is: {}".format(Most_Recent))
    except KeyError:
        print("Sorry The washington City files don't have the Birth Year column to calculate the most recent year of birth.\n")

    try:
        Most_Common = df['Birth Year'].value_counts().idxmax()
        print("\n The most common year of birth is: {}".format(Most_Common))
    except KeyError:
        print("Sorry The washington City files don't have the Birth Year column to calculate the most common year of birth.\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Display 5 rows of raw data."""
    
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no: ').lower()
    start_loc = 0
    # Display 5 rows of raw data
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()
        if view_data != 'yes':
            break
    
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
