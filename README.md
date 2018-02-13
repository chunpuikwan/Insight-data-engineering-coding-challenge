Summary:
This project is to build a program (using python 3.6) that can help political consultants to identify the followings for each recipient from each zip code from x to y year (y > x):
1. Total dollars received from repeated donations.
2. Total number of contributions received from repeated donators.
3. Donation amount in given percentile.

Approach:
This program do not take repeated donors’ very first donation into account as one donation does not make them ‘repeated’ donors. In other words, their second donation is counted as the first repeated contribution. It is divided into multiple parts to achieve the goal:

1. Initially, it is inputting a person (a line of data) at a time. The information of this single person is stored in new_list list so that each line in ‘itcont.txt’ will pass through a filter such that requirements 1, 5, 6 in ‘Input files considerations’ in the Insight README are satisfied. 
2. In ‘Identfying and filtering repeated contributors by same name and zip code’ in the program, after initial screening, the person (new_list) will be recorded on a list (Full_contributor_list). Each new incoming person will be compared to this list to see if they are repeated. If that is the case, they will be sent to another lists (filter_repeated_donors and sorted_bydate_filtered_repeated_donors) and requirement 2 will be completed. However, these new lists consist of repeated donors’ first time donation.
3.  The ‘filter through first time donation’ part in the program is to sweep away repeated donors’ first time non repeated contribution. This part also takes care of the case that an early record comes in late as data in ‘itcont.txt’ are not in chronological order. For example, by 50th line, we thought repeated donor X’s first repeated donation was in 2016; however, by 51st line, we realized his first repeated donation was in 2014. Therefore, we keep looping the sorted_bydate_filtered_repeated_donors list (which was sorted by date) to recalculate the earliest contribution from repeated donors and filter it out. Here, we fulfill requirements 3 and 4 in ‘Input files considerations’.
4. At this stage, the ‘Grouping by receipient ID, zip code, year and calculations’, we already have a list of repeated donors. This part simply check where the repeated donation was heading to and where it came from. Final output is sent to ‘repeat_donors.txt’ and keeps updating it as the data are streaming in. 
As entries in filter_repeated_donors and sorted_bydate_filter_repeated_donors are dynamically changing in a sense that index of each entry keep changing in a unpredictable manner, it is therefore refreshed and organized everytime a new entry comes in (through no_first_time_donation).  

Dependencies:
Couple modules are used:  fileinput, datetime, math, copy, and sys.
