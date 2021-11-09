"""
Template for the COMP1730/6730 project assignment, S2 2021.
The assignment specification is available on the course web
site, at https://cs.anu.edu.au/courses/comp1730/assessment/project/


The assignment is due 25/10/2021 at 9:00 am, Canberra time

Collaborators: <list the UIDs of ALL members of your project group here>
Bowen Hu: u7152919(33%)
Fengqing Wu: u7166770(33%)
Kexiang Wang: u7394240(33%)
"""
import os
import numpy as np
import pandas as pd
import time

def analyse(path_to_files):
    # only read the .csv file in the folder
    file = os.listdir(path_to_files)
    files = []
    for f in file:
        if f[-3:] == "csv":
            files.append(f)
    # read every .csv files and store the DataFrame files in a dictionary
    date = {}
    for f in files:
        data = pd.read_csv(path_to_files + "/" + f)
        date[f] = data

    latest_all_data = 0
    latest_file = 0

    # Q1(a)(Kexiang Wang completed this function)
    for f in files:
        # 1.use time.strptime method to parse the time string in the m-d-Y format
        # 2.use time.mktime method to that time in seconds
        seconds = time.mktime(time.strptime(f[:-4], "%m-%d-%Y"))
        # get the file with the maximum time
        if seconds > latest_all_data:
            latest_file = f
    latest_all_data = date[latest_file].values

    mk_time = []
    # traverse line by line in the latest file and get all last_update time in seconds
    for line in latest_all_data:
        mk_time.append(time.mktime(time.strptime(line[4], "%Y-%m-%d %H:%M:%S")))
    # get the row of the maximum last_update time in seconds and find it
    max_seconds_index = np.argmax(np.array(mk_time))
    latest_time = latest_all_data[max_seconds_index][4]

    print("Analysing data from folder ...\n")
    print("Question 1:")
    print("Most recent data is in file '", latest_file, "'")
    print("Last updated at ", latest_time)

    # Q1(b)(Kexiang Wang completed this function)
    # use the sum method in numpy to solve it
    total_world_case = np.sum(latest_all_data[:, 7])
    total_world_death = np.sum(latest_all_data[:, 8])
    print("Total worldwide cases:", total_world_case, ", Total worldwide deaths:", total_world_death, "\n")

    # Q2(Fengqing Wu and Bowen Hu completed this function)
    latest_confirmed_death_data = date[latest_file]
    # use groupby in pandas to Divide these data according to Country_Region and add Confirmed and Deaths data
    latest_data_by_country = latest_confirmed_death_data[["Country_Region", "Confirmed", "Deaths"]].groupby(["Country_Region"]).sum()
    # use the nlargest in pandas to sort the countries in descending order of number of Confirmed
    confirmed_top10 = latest_data_by_country.nlargest(10, "Confirmed")
    print("Question 2:")
    # get the day before the last update file
    before_latest_data = time.mktime(time.strptime(latest_file[: -4], "%m-%d-%Y")) - 86400
    before_local_time = time.localtime(before_latest_data)
    before_latest_file = time.strftime("%m-%d-%Y", before_local_time) + ".csv"
    before_latest_data = date[before_latest_file]

    # get the sum of Confirmed and Deaths data in the day before the last update file
    before_latest_two_data = before_latest_data[["Country_Region", "Confirmed", "Deaths"]].groupby(["Country_Region"]).sum()
    short_recovery_days = 15
    long_recovery_days = 30
    for index, row in confirmed_top10.iterrows():
        new = row["Confirmed"] - before_latest_two_data.loc[index]["Confirmed"]
        # According to the number of new Confirmed every day, the average cure period (15-30 days)
        # of the new coronavirus and the death rate to estimate range of active people
        print("%s - total cases: %d deaths: %d new: %d active: %d ~ %d"
              % (index, row["Confirmed"], row["Deaths"], new,
                new * short_recovery_days - new * row["Deaths"] / row["Confirmed"],
                 new * long_recovery_days - new * row["Deaths"] / row["Confirmed"]))
    print("\n")

    # Q3(Bowen Hu completed this function)
    print("Question 3:")
    case_death = []
    while (1):
        last_two_date = time.mktime(time.strptime(latest_file[: -4], "%m-%d-%Y")) - 86400
        last_two_local_time = time.localtime(last_two_date)
        last_two_file = time.strftime("%m-%d-%Y", last_two_local_time) + ".csv"
        # if that date file is not in the folder, break the loop
        if last_two_file not in date:
            break
        # get the data of the latest day and the last two day
        latest_case_death_data = date[latest_file].values
        last_two_data = date[last_two_file].values
        new_cases = np.sum(latest_case_death_data[:, 7]) - np.sum(last_two_data[:, 7])
        new_deaths = np.sum(latest_case_death_data[:, 8]) - np.sum(last_two_data[:, 8])
        # use this to get the date format like 2021-08-17
        print("%s-%s-%s : new cases: %d  new deaths: %d" % (
        latest_file[-8: -4], latest_file[-14: -12], latest_file[-11: -9], new_cases, new_deaths))
        # use two-dimensional list to store all files and their new Confirmed and new Death
        case_death.append([latest_file[: -4], new_cases, new_deaths])
        latest_file = last_two_file

    # get the current week
    cur_week = time.mktime(time.strptime(case_death[0][0], "%m-%d-%Y"))
    cur_local_time = time.localtime(cur_week)
    cur_week = time.strftime("%W-%Y", cur_local_time)
    # case_death[0][0] is last day because append this two-dimensional list
    last_day = case_death[0][0]
    week_total_case = 0
    week_total_death = 0
    for i in range(len(case_death)):
        # traverse this list and add the new Confirmed and new Death if traversed to the current week
        now_week = time.mktime(time.strptime(case_death[i][0], "%m-%d-%Y"))
        now_local_time = time.localtime(now_week)
        now_week = time.strftime("%W-%Y", now_local_time)
        if now_week == cur_week:
            week_total_case += case_death[i][1]
            week_total_death += case_death[i][2]
        # by judging whether the next day is in this week, if not, the data for this week will be settled
        if i + 1 < len(case_death):
            next_week = time.mktime(time.strptime(case_death[i + 1][0], "%m-%d-%Y"))
            next_local_time = time.localtime(next_week)
            next_week = time.strftime("%W-%Y", next_local_time)
            if(next_week != cur_week):
                # use this to get the date format like 2021-08-17
                last_exact_date = last_day.split('-', 3)
                exact_date = case_death[i][0].split('-', 3)
                print("Week %s-%s-%s to %s-%s-%s : new cases: %d  new deaths: %d" %
                      (exact_date[2], exact_date[0], exact_date[1],
                       last_exact_date[2], last_exact_date[0], last_exact_date[1],
                       week_total_case, week_total_death))
                # move to the next week
                cur_week = next_week
                last_day = case_death[i + 1][0]
                week_total_case = 0
                week_total_death = 0
        else:
            last_exact_date = last_day.split('-', 3)
            exact_date = case_death[i][0].split('-', 3)
            print("Week %s-%s-%s to %s-%s-%s : new cases: %d  new deaths: %d" %
                  (exact_date[2], exact_date[0], exact_date[1],
                   last_exact_date[2], last_exact_date[0], last_exact_date[1],
                   week_total_case, week_total_death))
    print("\n")

    # Q4(Bowen Hu completed this function)
    print("Question 4:")
    latest_ir_data = date[case_death[0][0] + ".csv"]
    # Get the average of Incident_Rate and then sort it in descending order
    ir_country = latest_ir_data[["Country_Region", "Incident_Rate"]].groupby(["Country_Region"]).mean()
    ir_top10 = ir_country.nlargest(10, "Incident_Rate")
    # Get the average of Case_Fatality_Ratio
    cfr = latest_ir_data[["Country_Region", "Case_Fatality_Ratio"]].groupby(["Country_Region"]).mean()
    for index, row in ir_top10.iterrows():
        print("%s : %.4f cases per 100,000 people and case_fatality_ratio: %.4f" %
              (index, row["Incident_Rate"], cfr.loc[index]["Case_Fatality_Ratio"]), "%")

# The section below will be executed when you run this file.
# Use it to run tests of your analysis function on the data
# files provided.

if __name__ == '__main__':
    # test on folder contain all CSV files
    analyse('./covid-data')
