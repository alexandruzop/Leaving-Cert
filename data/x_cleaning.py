''''
-program should ignore all blank cells
-program should remove duplicate entires
-program should convert every cell into a suitable format
-only look at data from 2008 - 2024
-program should perform relevant abstraction to simplify datasets
-program should create new files with the cleaned datasets
-program should extract statistics from cleaned files
-program should create new data bases ready for graphing

'''
#info learned while coding

"""
LAMBDA: splits entries word by word, aplies a function to each entry & extracts/returns desired outcome based on a T/F condition set
MULTIPLE DATASETS: name each dataset differently and no issues occur
MODULES: need to be installed via cmd for VS code unlike Thonny
ORDER: some parts of code only function if ordered in a specific way
"""

#modules
import pandas as pd
import numpy as np  
from statistics import mean, median , mode 
from collections import defaultdict
import csv




#CLEANING DATA

                                                #HOUSE INDEX FILE
#reading excel file
df = pd.read_csv('x_house_i1.csv') 

"""
filtering by year
"""
#month mapping for numercial values
#months stored as words, 
month_mapping_index = {
    'January': '01', 'February': '02', 'March': '03', 'April': '04',
    'May': '05', 'June': '06', 'July': '07', 'August': '08',
    'September': '09', 'October': '10', 'November': '11', 'December': '12'
}

#splitting date into year and month
df[['Year', 'Month']] = df['MONTH'].str.split(' ', expand=True)
df['Month'] = df['Month'].map(month_mapping_index)
#dropping concatonated date and keeping year and month seperate
df = df.drop(columns=['MONTH'])
#putting month and year columns next to each other
df = df[['Year', 'Month'] + [col for col in df.columns if col not in ['Year', 'Month']]]

#changing title on column
df['UNIT'] = df['UNIT'].replace('Base', 'Index')



"""
filtering by region (absraction)
"""
#changing names of rows
df.replace("National excluding Dublin - houses", "National Excluding Dublin", inplace=True)
df.replace("National - houses", "National", inplace=True)

#changing values containg "dublin" to just dublin
df['Type of Residential Property'] = df['Type of Residential Property'].apply(
    lambda x: 'Dublin' if isinstance(x, str) and 'Dublin' in x and 'National Excluding Dublin' not in x else x)

#filtering by desired values to keep
values_to_keep = ['Dublin', 'National Excluding Dublin', 'National']
df.loc[~df['Type of Residential Property'].isin(values_to_keep), 'Type of Residential Property'] = 'Rest Of Country'
df.rename(columns={"Type of Residential Property": "Location"}, inplace=True)


"""
Removing % (formatting)
"""

#lambda checks if % is present in each row retruning T/F statement
df = df[~df.astype(str).apply(lambda x: x.str.contains('%')).any(axis=1)]

"""
removing duplicate entries
"""

print(df.duplicated())
#drops duplicate entries
df.drop_duplicates(inplace = True)

"""
removes rows with blank cells
"""

cleaned_df = df.dropna()
# Save the cleaned DataFrame to a new CSV file (cleaned.index)
cleaned_df.to_csv("cleaned.index.csv", index=False)

"""
changing format
"""
#changing base Base100=2015 to % 
df['UNIT'] = df['UNIT'].replace("Base", "Index")


"""STATISTICS"""

#defining variables
input_index = "cleaned.index.csv"
output_index = "st_index.csv"
#lambda sets a condition to be checked
data_by_year = defaultdict(lambda: defaultdict(list))
mean_values = []

#opeining files
with open(input_index,'r') as file:
    reader = csv.DictReader(file)
    #iterating through rows
    for row in reader:
        year = int(row['Year']) 
        location = row['Location']
        #adding numeric values to new spreasheet
        value = float(row['VALUE']) if row['VALUE'] else None
        if value is not None:
            data_by_year[year][location].append(value)


#finding means and rounding to nearest whole number for each year and region
#iterating through each year using for loop
for year in sorted(data_by_year):
    locations = data_by_year[year]
    mean_row = {
        'Year': year,
        'Dublin Mean': round(mean(locations['Dublin'])) if 'Dublin' in locations else None,
        'National Mean': round(mean(locations['National'])) if 'National' in locations else None,
        'National Excl Dublin Mean': round(mean(locations['National Excluding Dublin'])) if 'National Excluding Dublin' in locations else None,
    }
    #appending mean values to rows in spreadsheet
    mean_values.append(mean_row)

#adding to new spreadsheet under row names and column names
with open(output_index, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['Year', 'Dublin Mean', 'National Mean', 'National Excl Dublin Mean'])
    writer.writeheader()
    writer.writerows(mean_values)


                                                 #RANGE 


#read csv file
file_path = "st_index.csv"
data = pd.read_csv(file_path)

# Define columns to process
columns_to_process = ['Dublin Mean', 'National Mean', 'National Excl Dublin Mean']

# Create new row for range
range_row = {'Year': ''}
#iterate through each column using for loop
for column in columns_to_process:
    # Find range
    max_index = data[column].max()
    min_index = data[column].min()
    max_year = data.loc[data[column] == max_index, 'Year'].values[0]
    min_year = data.loc[data[column] == min_index, 'Year'].values[0]
    range_value = max_index - min_index

    # Add to new row
    range_row[f'{column} Range'] = range_value
    range_row[f'{column} Max Year'] = max_year
    range_row[f'{column} Min Year'] = min_year

# Create DataFrame for range row
range_df = pd.DataFrame([range_row])
data_with_range = pd.concat([data, range_df], ignore_index=True)

#save to csv
data_with_range.to_csv(file_path, index=False)



                                                #RENT CLEANING 


#reading the file 
af = pd.read_csv('x_rent_i1.csv') 
"""
removing duplicate entries
"""
print(af.duplicated())
#drops duplicate entries
af.drop_duplicates(inplace = True)

"""
filtering by all property types (abstraction)
"""

af['Property Type'] = af['Property Type'].apply(
    lambda x: x if str(x).lower() in [''] else 'All Property Types'
)

"""
filtering by all bedrooms (narrows dataset)
"""
af = af[af['Number of Bedrooms'] == 'All bedrooms']


"""
filtering by region
"""
# Update the 'Location' column
af['Location'] = af['Location'].apply(
    lambda x: 'Dublin' if 'dublin' in str(x).lower() else 'Rest of Country'
)

"""
filtering by year (2008 onwards)
"""
af = af[af['Year'] >= 2008]

"""
removes rows with blank cells
"""
#drops rows with blank cells
cleaned_af = af.dropna()

# Save the cleaned DataFrame to a new CSV file
cleaned_af.to_csv("cleaned.rent.csv", index=False)


"""STATISTICS""" #reusing code

#defining variables
input_rent = "cleaned.rent.csv"
output_rent = "st_rent.csv"
rent_data_by_year = defaultdict(lambda: defaultdict(list))
mean_rent_values = []

#opening files and reading columns
with open(input_rent, 'r') as file:
    reader = csv.DictReader(file)
    #iterating through rows
    for row in reader:
        year = int(row['Year'])
        location = row['Location']
        #appending numeric values to new spreadsheet
        rent_value = float(row['VALUE']) if row['VALUE'] else None
        #if value is not none, append to new spreadsheet
        if rent_value:
            rent_data_by_year[year][location].append(rent_value)

#iterate through each region for each year
for year, locations in sorted(rent_data_by_year.items()):
    #appending mean values to rows in spreadsheet
    mean_rent_values.append({
        #getting mean and rounding to 2 deciaml places
        'Year': year,
        'Dublin Mean Rent': round(mean(locations['Dublin']),2) if 'Dublin' in locations else None,
        'Rest of Country Mean Rent': round(mean(locations['Rest of Country']),2) if 'Rest of Country' in locations else None,
    })

#outputting to new file
with open(output_rent, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['Year', 'Dublin Mean Rent', 'Rest of Country Mean Rent'])
    # #writing header & rows
    writer.writeheader()
    writer.writerows(mean_rent_values)


                                         #RANGE (reusing code)


# Read the rent data file
file_path = "st_rent.csv"
rent_data = pd.read_csv(file_path)

# Round the rent mean values to 2 decimal places
rent_data[['Dublin Mean Rent', 'Rest of Country Mean Rent']] = rent_data[
    ['Dublin Mean Rent', 'Rest of Country Mean Rent']
].round(2)

# Define columns to process
columns_to_process = ['Dublin Mean Rent', 'Rest of Country Mean Rent']

# Create a dictionary for the new row with range details
range_row = {'Year': ''}
for column in columns_to_process:
    # Calculate range, max year, and min year
    max_value = rent_data[column].max()
    min_value = rent_data[column].min()
    max_year = rent_data.loc[rent_data[column] == max_value, 'Year'].values[0]
    min_year = rent_data.loc[rent_data[column] == min_value, 'Year'].values[0]
    range_value = max_value - min_value

    # Add details to the new row
    range_row[f'{column} Range'] = round(range_value, 2)
    range_row[f'{column} Max Year'] = max_year
    range_row[f'{column} Min Year'] = min_year

# Append the new row to the dataset
rent_data_with_range = pd.concat([rent_data, pd.DataFrame([range_row])], ignore_index=True)

#save to csv
rent_data_with_range.to_csv(file_path, index=False)




                                           #HOMELESS CLEANING

#reading file
cf = pd.read_csv('x_homeless_i1.csv') 
"""
Getting rid of decimals (foramtting)
"""
numbers = cf.select_dtypes(include=[np.number]).columns
#rounds down to nearest whole number
cf[numbers] = cf[numbers].apply(np.floor).astype('Int64')
"""
removing total columns and rows
"""
cf.drop(columns=["Totals"], inplace=True)
#removes rows with total in them
cf = cf[~cf.apply(lambda row: row.astype(str).str.contains('total', case=False).any(), axis=1)]


"""
removing duplicate entries
"""
print(cf.duplicated())
#drops duplicate entries
cf.drop_duplicates(inplace = True)

"""
removing "estimates"
"""
cf = cf.drop(columns=['estimates'])

"""
removes rows with blank cells
"""
cleaned_cf = cf.dropna()
# Save the cleaned DataFrame to a new CSV file
cleaned_cf.to_csv("cleaned.homeless.csv", index=False)



"""STATISTICS"""

#add up each age interval for a pie chart
#get 2024 total for heat map
#get the mode for the age interval with the highest homeless rate
#get the mode for the region with the highest homless rate

#HEATMAP
#read data
file_path = "cleaned.homeless.csv" 
output_file_path = "st_homeless_heatmap.csv"
#read data
hf = pd.read_csv(file_path)

"""
look at only 2024 -- current total
"""
hf_2024 = hf[hf['Year'] == 2024].copy()
# Get age columns
age_columns = [col for col in hf_2024.columns if col.startswith('Ages')]
"""
convert age columns to integers
"""
hf_2024.loc[:, age_columns] = hf_2024[age_columns].apply(pd.to_numeric, errors='coerce')

"""
sum of age columns
"""
hf_2024.loc[:, 'Total'] = hf_2024[age_columns].sum(axis=1)

"""
create new dataframe
"""
region_totals = hf_2024[['Region', 'Total']]
region_totals.to_csv(output_file_path, index=False)

                                                
                                                #MODE
#read data
file_path = "st_homeless_heatmap.csv"
data = pd.read_csv(file_path)

#find max (mode) and respective region
max_value = data['Total'].max()
max_region = data.loc[data['Total'] == max_value, 'Region'].iloc[0]

#new row made
data['Modal Region'] = None
data['Mode Amount'] = None

#add data to new row
max_row_index = data.loc[data['Total'] == max_value].index[0]
data.loc[max_row_index, 'Modal Region'] = max_region
data.loc[max_row_index, 'Mode Amount'] = max_value

# Save to CSV
output_path = "st_homeless_heatmap.csv"
data.to_csv(output_path, index=False)


#PIE CHART (code reused)

# Read data
file_path = "cleaned.homeless.csv" 
output_file_path = "st_homeless_piechart.csv"
hf = pd.read_csv(file_path)

"""
Look at only 2024
"""
hf_2024 = hf[hf['Year'] == 2024]

"""
get ages from colums
"""
age_columns = [col for col in hf_2024.columns if col.startswith('Ages')]

"""
Convert age columns to integers
"""
hf_2024.loc[:, age_columns] = hf_2024[age_columns].apply(pd.to_numeric, errors='coerce')
"""
Sum values for each age column
"""
age_totals = hf_2024[age_columns].sum().reset_index()
age_totals.columns = ['Age Interval', 'Total']

"""
Save to CSV
"""
age_totals.to_csv(output_file_path, index=False)

                                                    
                                         #MODE (resuing codee)

# Read data
file_path = "st_homeless_piechart.csv"
data = pd.read_csv(file_path)

#find max (mode) and respective age
max_value = data['Total'].max()
max_age = data.loc[data['Total'] == max_value, 'Age Interval'].iloc[0]

#add new column

data['Modal Age'] = None
data['Mode Amount'] = None

#create new row
max_row_index = data.loc[data['Total'] == max_value].index[0]
data.loc[max_row_index, 'Modal Age'] = max_age
data.loc[max_row_index, 'Mode Amount'] = max_value

#save to csv
output_path = "st_homeless_piechart.csv"
data.to_csv(output_path, index=False)


#finally done!!!!! :)




