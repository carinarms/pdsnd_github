import time
import pandas as pd
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input('You can choose between Chicago, New York City, and Washington. Enter the name below:\n').lower()
        if city in ('chicago', 'new york city', 'washington'):
            break
        else:
            print('\nCity name not found. Please try again. :)')

    # TO DO: get user input for month (all, january, february, ... , june)

    while True:
        month = input('Enter any of the year\'s first six months or type "all" to filter by month. (January, February, March, April, May, June, all)\n').lower()
        if month in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            break
        else:
            print('\nMonth not found. Please try again. ')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input('Enter any day of the week or type: "all" to filter by day. (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, all)\n').lower()
        if day in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            break
        else:
            print('\nDay not found. Please try again. ')

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
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
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

    # TO DO: display the most common month
    popular_month = calendar.month_name[df['month'].mode()[0]]
    print('Most popular month: ', popular_month)

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most popular day of the week: ', popular_day)

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular start hour: ', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Most popular start station: ', popular_start)

    # TO DO: display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('Most popular end station: ', popular_end)

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' --> ' + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    print('Most popular start to end route: ', popular_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    def hr_min_sec(t):
        """Divides seconds into hours, minutes, and seconds."""

        m, s = divmod(t, 60)
        h, m = divmod(m, 60)
        t = '%d hr %02d min %02d sec' % (h, m, s)
        return t

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total travel time: ', hr_min_sec(total_time))

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Total mean time:', hr_min_sec(mean_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Types of users:\n', user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_types = df['Gender'].value_counts()
        print('\nGender stats:\n', gender_types)
    else:
        print('\nThere is no recorded gender data in this city. ')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nBirth year stats: ')

        early_year = int(df['Birth Year'].min())
        print('Earliest year of birth: ', early_year)

        recent_year = int(df['Birth Year'].max())
        print('Most recent year of birth: ', recent_year)

        common_year = int(df['Birth Year'].mode()[0])
        print('Most common year of birth: ', common_year)

    else:
        print('\nThere is no recorded birth data in this city. ')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # TO DO: Offer option of displaying raw data
        i= 5
        raw = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n').lower()

        while True:
            if raw == 'no':
                break
            if raw == 'yes':
                print(df.head(i))
                i += 5
                raw = input('\nHow about 5 more lines of raw data? Enter yes or no.\n').lower()
            else:
                raw = input('\nI am not sure what you meant. Please type yes or no.\n').lower()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
