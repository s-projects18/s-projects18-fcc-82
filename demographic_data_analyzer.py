import pandas as pd
import numpy as np

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv("adult.data.csv", header=0)
    
    # 32561 entries, no NaN, 15 columns, no dates
    # fnlwgt: final weight; People with similar demographic characteristics should have similar weights
    #print(df.info())

    # NaN-check/-correction
    # age:ok, workclass:?, fnlwgt:ok, education:ok, education-num:ok
    # marital-status:ok, occupation:?,relationship:ok, race:ok,sex:ok
    # capital-gain:ok, capital-loss:ok, hours-per-week:ok
    # native-country:?, salary:ok
    #print(df['salary'].unique())
    df['workclass'] = df['workclass'].replace('?', np.NaN)
    df['occupation'] = df['occupation'].replace('?', np.NaN)
    df['native-country'] = df['native-country'].replace('?', np.NaN)


    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    # (1) long-way:
    #all_races = df['race'].unique()
    #l=i=[]
    #for race in all_races:
    #  l.append( df['race'][df['race']==race].count() )
    #  i.append(race)
    #race_count = pd.Series(l, index=i)

    # (2) aggregate way
    #race_count = df.groupby('race').agg({'race':'count'})['race']

    # (3) simplest way. (Input = Output = Series-Object)
    race_count = df['race'].value_counts()


    # What is the average age of men?
    #average_age_men = df['age'][df['sex']=='Male'].mean()
    # why does this work???
    #average_age_men = df.groupby(['sex'])['age'].mean()['Male']
    average_age_men = df.groupby(['sex']).get_group('Male').mean()['age'] # Series
    average_age_men = round(average_age_men, 1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round(df['education'].value_counts(normalize=True)["Bachelors"]*100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    adv_edu = ['Bachelors', 'Masters', 'Doctorate']
    f1 = df['education'].isin(adv_edu)
    f2 = (df['salary']=='>50K')
    total = df['education'].count()
    high = df[f1]['education'].count()
    low  = df[~f1]['education'].count()

    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate` 
    # ???
    higher_education = round(high/total*100,1) # 23
    lower_education = round(low/total*100,1)   # 77
    #print(total, high, low, higher_education, lower_education)

    # percentage with salary >50K
    total_high = df[f1]['education'].count()
    total_low = df[~f1]['education'].count()
    high = df[f1 & f2]['education'].count()
    low  = df[~f1 & f2]['education'].count()
    higher_education_rich = round(high/total_high*100,1)
    lower_education_rich = round(low/total_low*100,1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    f3 = (df['hours-per-week']==min_work_hours)
    num_min_workers_total = df[f3]['hours-per-week'].count()
    num_min_workers = df[f2 & f3]['hours-per-week'].count()

    rich_percentage = round(num_min_workers/num_min_workers_total*100,1)


    # What country has the highest percentage of people that earn >50K?
    all_persons = df['native-country'].value_counts()
    rich_perc = df['native-country'][f2].value_counts() / all_persons
    rich_perc.sort_values(ascending =False, inplace=True)

    highest_earning_country = rich_perc.keys()[0]
    highest_earning_country_percentage = round(rich_perc[0]*100,1)

    # Identify the most popular occupation for those who earn >50K in India.
    r = df['occupation'][df['native-country']=='India'].value_counts()
    top_IN_occupation = r.keys()[0]


    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
