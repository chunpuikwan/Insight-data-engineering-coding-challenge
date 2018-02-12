import fileinput                                                                #Fileinput is used for datastreaming from a source file.
import datetime                                                                 #Library that provides current year for later use in the program.
import math
import sys
'''
START --- Extract current year
'''
today = datetime.datetime.today()                                               #Extract current year for later use. 
current_year = str(today.year)
'''
FINISH --- Extract current year
'''

'''
START --- Import percentile file
'''
f = open(sys.argv[2], 'r')                                                      #Import percentile file as requested
percentile = int(f.readline())
f.close
'''
FINSIH --- Import percentile file
'''
'''
Start --- INITIALIZATION
'''
Full_contributor_list = []                                                      #Used in IDENTIFYING AND FILTERING REPEATED CONTRIBUTORS BY SAME NAME AND ZIP CODE.
unorganized_repeated_donors = []                                                #Used in IDENTIFYING AND FILTERING REPEATED CONTRIBUTORS BY SAME NAME AND ZIP CODE.
line_count = int(0)                                                             #Used in PROGRAM to help inputing donors.
y = int(0)                                                                      #Used in GROUPING BY RECIPIENT ID, ZIP CODE and CALCULATIONS for calculation purpose.
seen_1 = []                                                                     #Used in IDENTIFYING AND FILTERING REPEATED CONTRIBUTORS BY SAME NAME AND ZIP CODE to filter repeated unorganized_repeated_donors list.
seen_2 = []                                                                     #Used in FILTERING THROUGH YEAR to get repeated donors in current year.
seen_index = []                                                                 #Used in GROUP BY RECIPIENT ID, ZIP CODE and CALCULATIONS to assign ID to repeated donors since name is absent there.
calculated_last_output = []                                                     #Used in GROUP BY RECIPIENT ID, ZIP CODE and CALCULATIONS to ensure those in last_output are not repeated.
filtered_repeated_donors = []                                                   #Used in IDENTIFYING AND FILTERING REPEATED CONTRIBUTORS BY SAME NAME AND ZIP CODE to hold a list of repeated donors in mixed years.
current_year_repeated_donors = []                                               #Used in FILTERING THROUGH YEAR to get a clean list of repeated donors who donoated this year.
last_output =[]                                                                 #Used in GROUP BY RECIPIENT ID, ZIP CODE and CALCULATIONS to hold all temp_output together.
temp_output = []                                                                #Used in GROUP BY RECIPIENT ID, ZIP CODE and CALCULATIONS to temporarily hold details of each person who donoated in current year.
real_output = []                                                                #Used in GROUP BY RECIPIENT ID, ZIP CODE and CALCULATIONS for outputting last_output to text file.
dict_percentile = {}                                                            #Used in GROUP BY RECIPIENT ID, ZIP CODE and CALCULATIONS to keep track which recipient received how much from a zip code.
'''
Finish --- INITIALIZATION
'''
'''
Start --- Program
'''                                                       
for line in fileinput.FileInput(files=(sys.argv[1])):                           #Data comes in line by line through fileinput
    input_data = line.split('|')                                                #Delimit '|' and each line of data becomes a list.                                                                                 
    '''
    Now we extract position 0, 7, 10, 13, 14, 15 from original list into a 
    new_list
    original list[0] = new_list[0] = recipient ID
    original list[7] = new_list[1] = contributor's name
    original list[10] = new_list[2] = zip code
    original list[13] = new_list[3] = transaction year
    original list[14] = new_list[4] = transaction amount
    original list[15] = new_list[5] = Other_ID 
    '''
    new_list = [input_data[0], input_data[7], input_data[10][0:5],              
                input_data[13], input_data[14], input_data[15]]
    
    if all(new_list) or len(new_list[2])<5:                                     #Filtering data according to "6.other considerations" in "Input file considerations".
        pass                                                                    
    else:
       del new_list[-1]                                                         #Delete new_list[5] since data here passed filter("Input file considerations") already.
       '''
       Start --- Identifying  and filtering repeated contributors by same name 
       and zip code
       '''
       for p in range(line_count):
           if new_list[1] == Full_contributor_list[p][1] and new_list[2] == Full_contributor_list[p][2]:
               unorganized_repeated_donors.append(Full_contributor_list[p])
               unorganized_repeated_donors.append(new_list)                                    #Identifying repeated donors is HERE. It is messy that multiple repeated donors are repeated.
       Full_contributor_list.append(new_list)                                                  #Forming a list of contributors with their details/ fields.
       for item in unorganized_repeated_donors:                                                #This is to filter repeated repeated donors from unorganized_donor_repeated donors.
           if item not in seen_1:
               seen_1.append(item)                                         
               filtered_repeated_donors.append([x for i, x in enumerate(item) if i!=1])        #Filtered results HERE in filtered_repeated_donors with no names.      
       '''
       Finish --- Identifying repeated contributors by same name and zip code
       '''
       '''
       Start --- Filtering through year
       '''
       x = int(0)                                                               #INITIALIZE x for loop counting HERE.
       for item in filtered_repeated_donors:                                    #Filter through year
           if filtered_repeated_donors[x][2][-4:] == current_year:              #A tiny bug here that output two entris in a row if a person donates twice when no one is between the two consecutive times. It is fixed in the output next stage. 
               if item not in seen_2:
                   seen_2.append(item)
                   current_year_repeated_donors.append(filtered_repeated_donors[x])
           x += 1
       '''
       Finish --- Filtering through year
       '''
       '''
       Start --- Grouping by receipient ID, zip code and calculations
       '''
       for item in current_year_repeated_donors:
           index = current_year_repeated_donors.index(item)                                                    #This is to create an unique ID of each entry in current_year_repeated_donors (by indexing) since name is no longer here. Otherwise people donate from same zip and for same receipient will be counted as one. 
           temp_output = [item[0], item[1], item[2][-4:], item[3], item[3],'1']
           if index not in seen_index:                                                                         #Allowing only the latest entry gets into the calculation part.                                
                  seen_index.append(index) 
                  R_ID_and_zip = str(item[0]+item[1])                                                          
                  dict_percentile.setdefault(R_ID_and_zip,[])                                                  #Assign keys(R_ID and zip code) to dict_percentile
                  dict_percentile[R_ID_and_zip].append(int(temp_output[4]))                                    #and values (the personal transaction amount) under corresponding keys.
                  dict_percentile[R_ID_and_zip].sort()                                                         #Sorting for percentile calculation.
                  if not last_output:                                                                          #Skip the senario when last_output is initially an empty list.
                      pass
                  else:
                      for i in range(0, y):                                                                    #Calculations start here: 1. Match R_ID and zip 2. +1 to total number of transaction if from same R_ID and zip 3. calculate the running percentile
                           if last_output[i] not in calculated_last_output:       
                               if temp_output[0] == last_output[i][0] and temp_output[1] == last_output[i][1]:  #Identify if R_ID and zip are the same.
                                  temp_output[4] = str(float(last_output[i][4]) + float(temp_output[4]))
                                  temp_output[5] = str(int(last_output[i][5]) + 1)                              #Total no. of transaction + 1 if they are from same zip code and for same R_ID
                                  temp_output[3] = str(round(dict_percentile[R_ID_and_zip][math.ceil(((percentile/100)*int(temp_output[5]))-1)]))
                                  calculated_last_output.append(last_output[i]) 
                  last_output.append(temp_output)
                  y += 1
       while [] in last_output:                                                                                 #Remove empty entries in last_output.
           last_output.remove([])
       with open(sys.argv[3], 'w') as f:                                                                #Save results as text file.
           for i in range(0,len(last_output)):
               real_output = '|'.join(last_output[i])
               f.write('%s\n' % real_output)      
       '''
       Finish --- Group by receipient ID, zip code and calculations
       '''       
       line_count += 1
'''
FINISH --- Program
'''
