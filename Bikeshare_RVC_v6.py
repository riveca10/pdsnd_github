import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Data just have six months

val_months = ['january', 'february', 'march', 'april', 'may', 'june','all']
val_days = ['monday','tuesday','wednesday','thursday','friday',
        'saturday','sunday','all']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_input = input('Please select between these three cities: new york city, chicago or washington:\n').lower().strip()
    #print(city_input)
    while city_input not in CITY_DATA.keys():
        city_input = input('Please choose one of these 3 options: new york city, chicago or washington:\n').lower().strip()
    print('Thank you for choosing this city:',city_input)

    # TO DO: get user input for month (all, january, february, ... , june)
    month_input = input('Select a month between january and june:\n').lower()
    while month_input not in val_months:
        month_input = input('Please choose a month between January and June:\n').lower().strip()
    print('Thanks for choosing this month:',month_input)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_input = input('Select a day:\n').lower().strip()
    while day_input not in val_days:
        day_input = input('Please choose a valid day:\n').lower().strip()

    return city_input, month_input, day_input

def load_data(city, month, day):
#     print(city + month + day)
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])
#     print(df.head())
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["months"] = df["Start Time"].dt.month
    df["day"] = df["Start Time"].dt.day_name()
    df["start_hour"] = df["Start Time"].dt.hour
    if month != 'all':
        month = val_months.index(month) + 1
        df = df[df['months'] == month]
    if day != 'all':
        df = df[df["day"] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print('the most common month was: {}\n'.format(val_months[df['months'].value_counts().idxmax()-1]))
    #
    # # TO DO: display the most common day of week
    print('the most common month was: {}\n'.format(df['day'].value_counts().idxmax()))
    #
    # # TO DO: display the most common start hour
    print('the most common hour to start a ride was: {}\n'.format(df['start_hour'].value_counts().idxmax()))
    #
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    most_popular_start_station = df["Start Station"].mode()[0]
    print ("most popular start station: {}".format(most_popular_start_station))
    # display most commonly used end station
    most_popular_end_station = df["End Station"].mode()[0]
    print ("most popular end station: {}".format(most_popular_end_station))
    # display most frequent combination of start station and end station trip
    most_popular_combinations = (df["Start Station"] + " --> " + df["End Station"]).value_counts().head(1)
    print ("most frequent trip: {}".format(most_popular_combinations))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # TO DO: display total travel time
    print('total travel time was: {}\n'.format(df['Trip Duration'].sum()))
    # TO DO: display mean travel time
    print('Mean travel time was: {}\n'.format(df['Trip Duration'].mean()))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # TO DO: Display counts of user types
    print('counts of user types:\n{}\n'.format(df['User Type'].value_counts()))
    # TO DO: Display counts of gender
    if city in ['new york city', 'chicago']:
        print('counts of Gender:\n{}\n'.format(df['Gender'].value_counts()))

    # TO DO: Display earliest, most recent, and most common year of birth
    if city in ['new york city', 'chicago']:
        print('youngest year of birth: {}\n'.format(df['Birth Year'].max()))
        print('oldest year of birth: {}\n'.format(df['Birth Year'].min()))
        print('popular year of birth: {}\n'.format(df['Birth Year'].value_counts().idxmax()))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def individual_trip_data(df):
    """Prompt the user if they want to see 5 lines of raw data, display the data if the answer is yes and continue these prompts and displays until the user say no"""

    raw_data_answer = input("Do you want to look for details of the first 5 trips? yes or no: ")
    while str(raw_data_answer).strip().lower() not in ("yes","no"):
            rd_answer = input("Please type yes or no: ")
            if str(rd_answer).strip().lower() in ("yes","no"):
                raw_data_answer = str(rd_answer).strip().lower()
                break
    start_time = time.time()
    start = 0
    end = 4

    while str(raw_data_answer).strip().lower() == "yes":
        print('\nLooking for individual trip data...\n')
        df = df.sort_values(by=["Start Time"])
        for i in range(start,end):
            print("\n","-"*40,"\n",df.rename(columns={"Unnamed: 0": "Trip Reference"}).iloc[i])

        extra_question=input("\n\nDo you want to loof for additional individual trip data related to your data selection? Type yes or no: ")
        raw_data_answer = str(extra_question).strip().lower()

        while str(extra_question).strip().lower() not in ("yes","no"):
            rd_answer = input("Please type yes or no: ")
            if str(rd_answer).strip().lower() in ("yes","no"):
                raw_data_answer = str(rd_answer).strip().lower()
                break

        if raw_data_answer == "no":
            break

        start += 5
        end += 5

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print(df.head())
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        more_info=input("\n\nDo you want to view more individual information on trip data? type yes or no: ")

        while str(more_info).lower() not in ("yes","no"):
            new_answer = input("Please type yes or no: ")
            if str(new_answer).lower() in ("yes","no"):
                more_info = str(new_answer).lower()
                break

        answer = more_info
        if str(more_info).lower() == "yes":
        #if str(more_info).lower() == "yes":
            individual_trip_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
