import time 
import pandas as pd
import numpy as np

# loading files
CITY_DATA = {
    'chicago':'chicago.csv',
    'new york city':'new_york_city.csv',
    'washington':'washington.csv'
}

def user_input():
    '''
    This function starts the user interface by introduction and
    asking the user with the city he/she wants to analyze

    '''

    print('Hay! Let\'s see some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
   
    city = input('Choose the city you want to analyze: \n 1-Chicago \n 2-New York \n 3-Washington\n Enter the city: ').lower()
    
         
    if city == 'chicago':
        print("\n Chicago City! Okay Let's go further \n")
        return 'chicago'
    elif city == 'new york':
        print("\n New York City! Okay let's go further \n")
        return 'new york city'
    elif city == 'washington':
        print("\n Washington! Okay let's go further \n")
        return 'washington'        
    return city

def get_time():
    '''
    the code below asks the user to choose between month and day of month,
    day of the week or no filters

    '''
    period = input('\n filter the data by month and day of the month, day of the week or do not want to filter? Type "no" for no filter. \n').lower()

    while True: 
        if period == "month":
            while True:
                day_month = input("\n Do you want to filter the data by day of the month too? Type 'yes' or 'no' \n").lower()
                if day_month == "no":
                    print('\n The data is now being filtered by month...\n')
                    return 'month'
                elif day_month == "yes":
                   print ('\n The data is now being filtered by month and day of the month... \n')
                   return 'day_of_month'
                
        if period == "day":
            print('\n The data is now being filtered by the day of the week...\n')
            return 'day_of_week'
        elif period == "no":
            print('\n No period filter is being applied to the data\n')
            return "none"
        period = input("\n Please choose a period filter option between 'month', 'day' of the week, or (no) \n").lower()
# get user input for month (all, january, february, ... , june)
def month_info(m):      
    if m == 'month':
        month = input('\nChoose month! January, February, March, April, May, or June? Please type the full month name.\n').lower()
        while month not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input('\nPlease choose between January, February, March, April, May, or June? Please type the full month name.\n').lower()
        return month
    else:
        return 'none'

def month_day_info(df, day_of_month):     # Asks the user for a month and a day of month,
    month_day = []
    if day_of_month == "day_of_month":
        month = month_info("month")
        month_day.append(month)
        maximum_day_month = max_day_month(df, month)

        while (True):
            a = """ \n Which day of the month? \n
            Please type your response as an integer between 1 and """                 
            b  = a + str(maximum_day_month) + "\n" 
            day_of_month = input(b)

            try: 
                day_of_month = int(day_of_month)
                if 1 <= day_of_month <= maximum_day_month:
                    month_day.append(day_of_month)
                    return month_day
            except ValueError:
                print("That's not a numeric value")
    else:
        return 'none'
# Asks the user for a day and returns the specified day
def day_info(d):       
    if d == 'day_of_week':
        day = input('\n Which day? Please type a day Mon, Tus, Wen, Thi, Fri, Sat, Sun. \n').lower().strip()
        while day not in ['mon', 'tus', 'wen', 'thi', 'fri', 'sat', 'sun']:
            day = input('\nPlease type a day as a choice from Mon, Tus, Wen, Thi, Fri, Sat, Sun. \n').lower()
        return day
    else:
        return 'none'

def load_data(city):
    # Loads data for the specified city
    print('\nLoading the data... .. .. ..\n')
    df = pd.read_csv(CITY_DATA[city])

    #extracting from Start Time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")
    df['month'] = df['Start Time'].dt.month
    df["day_of_month"] = df["Start Time"].dt.day
    return df

def time_filters(df, time, month, week_day, md):
    '''
    Filters the data according to the criteria specified by the user.
    Local Variables:
    df         - city dataframe 
    time       - indicates the specified time (either "month", "day_of_month", or "day_of_week")
    month      - indicates the month used to filter the data
    week_day   - indicates the week day used to filter the data
    md         - list that indicates the month (at index [0]) used to filter the data
                    and the day number (at index [1])
    Result:
    df - dataframe to be used for final calculation
    '''
    print('\nData loaded!!! \n')

    #Filter by Month
    if time == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #Filter by day of week
    if time == 'day_of_week':
        days = ['Monday', 'Tuesday', 
        'Wednesday', 'Thursday', 
        'Friday', 'Saturday', 'Sunday']
        for d in days:
            if week_day.capitalize() in d:
                day_of_week = d
        df = df[df['day_of_week'] == day_of_week]

    if time == "day_of_month":
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = md[0]
        month = months.index(month) + 1
        df = df[df['month']==month]
        day = md[1]
        df = df[df['day_of_month'] == day]

    return df

def max_day_month(df, month):
    ''' Gets the max day of the month '''

    months = {"january": 1, "february": 2, "march": 3, "april":4, "may": 5, "june":6}
    df = df[df["month"] == months[month]]
    max_day = max(df["day_of_month"])
    return max_day

def month_freq(df):
    '''What is the most popular month for start time?
    '''
    # df - dataframe returned from time_filters
    print('\n -- What is the most popular month for bike traveling?')
    m = df.month.mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[m - 1].capitalize()
    return popular_month

def day_freq(df):
    '''What is the most popular day of week for start time?
    '''
    # df - dataframe returned from time_filters
    print('\n -- What is the most popular day of the week for bike rides?')
    return df['day_of_week'].value_counts().reset_index()['index'][0]

def hour_freq(df):
    '''What is the most popular hour of day for start time?
    '''
    # df - dataframe returned from time_filters
    print('\n -- What is the most popular hour of the day for bike rides?')
    df['hour'] = df['Start Time'].dt.hour
    return df.hour.mode()[0]

def ride_duration(df):
    '''
    What is the total ride duration and average ride duration?
    Result:
        tuple = total ride duration, average ride durations
    '''
    # df - dataframe returned from time_filters
    print('\n -- What was the total traveling done for 2017 through June, and what was the average time spent on each trip?')
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    #sum for total trip time, mean for avg trip time
    total_ride_time = np.sum(df['Travel Time'])
    total_days = str(total_ride_time).split()[0]

    print ("\n Total travel time on 2017 through June was " + total_days + " days \n")
    avg_ride_time = np.mean(df['Travel Time'])
    avg_days = str(avg_ride_time).split()[0]
    print("\n Average travel time on 2017 through June was " + avg_days + " days \n")

    return total_ride_time, avg_ride_time

def stations_stats(df):
    '''
    What is the most popular start station and most popular end station?
    '''
    # df - dataframe returned from time_filters
    print("\n -- What is the most popular start station?\n")
    start_station = df['Start Station'].value_counts().reset_index()['index'][0]
    print (start_station)
    print("\n -- What is the most popular end station?\n")
    end_station = df['End Station'].value_counts().reset_index()['index'][0]
    print(end_station)
    return start_station, end_station

def popular_trip(df):
    '''
    What is the most popular trip?

    '''
    # df - dataframe returned from time_filters
    result = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\n -- What was the most popular trip from start to end?')
    return result

def counts_of_users_type(df):
    '''
    What are the counts of each user type?

    '''
     # df - dataframe returned from time_filters
    print('\n -- Types of users: 1-subscribers\n2-customers\n3-others\n')
    return df['User Type'].value_counts()

def gender_count(df):
    '''
    What are the counts of gender?
    '''
    # df - dataframe returned from time_filters
    print('\n -- What is the breakdown of gender among users?\n')
    return df['Gender'].value_counts()
    
    
def birth_years(df):
    '''What is the earliest, latest, and most frequent birth year?'''
    # df - dataframe returned from time_filters
    try:
        print('\n -- What is the earliest, latest, and most frequent year of birth, respectively?')
        earliest = np.min(df['Birth Year'])
        print ("\nThe earliest year of birth is " + str(earliest) + "\n")
        latest = np.max(df['Birth Year'])
        print ("The latest year of birth is " + str(latest) + "\n")
        most_frequent= df['Birth Year'].mode()[0]
        print ("The most frequent year of birth is " + str(most_frequent) + "\n")
        return earliest, latest, most_frequent
    except:
        print('No available birth date data for this period.')

def process(f, df):
    '''Calculates the time it takes to commpute a statistic
    '''
    start_time = time.time()
    statToCompute = f(df)
    print(statToCompute)
    print("Computing this stat took %s seconds." % (time.time() - start_time))

def disp_data(df):
    '''
    Displays the data used to compute the stats
    Input:
        the df with all the bikeshare data
    Returns: 
       none
    '''
    #omit irrelevant columns from visualization
    df = df.drop(['month', 'day_of_month'], axis = 1)
    row = 0

    data = input("\nYou like to see rows of the data? write 'yes' or 'no' \n").lower()
    while True:
        if data == 'no':
            return
        if data == 'yes':
            print(df[row: row + 5])
            row = row + 5
        data = input("\n Would you like to see five more rows? write 'yes' or 'no' \n").lower()

def main():
    '''The main function calculates and prints out the 
    descriptive statistics about a requested city
    '''
    # calling all the functions step by step
    city = user_input()
    df = load_data(city)
    period = get_time()
    month = month_info(period)
    day = day_info(period)
    month_day = month_day_info(df, period)

    df = time_filters(df, period, month, day, month_day)
    disp_data(df)
    
    # all the conclusions
    stats_funcs_list = [month_freq,
     day_freq, hour_freq, 
     ride_duration, popular_trip, 
     stations_stats, counts_of_users_type, birth_years, gender_count]
	
    # displays processing time for each function block
    for x in stats_funcs_list:	
        process(x, df)

    # Restarting option
    restart = input("\n * Would you like to do it again and perform another analysis? Type \'yes\' or \'no\'.\n").lower()
    if restart == 'yes':
        main()

if __name__ == '__main__':
    main()