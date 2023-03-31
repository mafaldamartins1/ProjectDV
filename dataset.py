# Import packages
import pandas as pd

### DATA IMPORTING AND TREATMENT

# Specify the path to CSV file
file_path = 'https://raw.githubusercontent.com/mafaldamartins1/ProjectDV/main/dataset_US_executions.csv'

# Read the CSV file into a pandas dataframe
df = pd.read_csv(file_path)

# Remove space in the beginning of ' Male' from the 'Sex' column
df['Sex'] = df['Sex'].replace(' Male','Male')

# Join 'no' values with 'No' in the 'Foreign National' column
df['Foreign National'] = df['Foreign National'].replace('no','No')

# Change the type of the 'Execution Date' column to Date
df['Execution Date'] = pd.to_datetime(df['Execution Date'])
df['Execution Year'], df['Execution Month'] = df['Execution Date'].dt.year, df['Execution Date'].dt.month

# Join both 'White' values of column 'Race' together
df.loc[df['Race'].str.startswith('White'), 'Race'] = 'White'
# Join both 'South' values of column 'Region' together
df.loc[df['Region'].str.startswith('South'), 'Region'] = 'South'

# Remove space in the end of 'Oklahoma ' from the 'State' column
df['State'] = df['State'].replace('Oklahoma ','Oklahoma')

# Join 'Multiple' and 'Multiple (including White)' in the 'Victim(s) Race(s)' column
df['Victim(s) Race(s)'] = df['Victim(s) Race(s)'].replace('Multiple (including White)','Multiple')

# Remove columns with missing values - 'Middle Name(s)' and 'Suffix'
df.drop(columns=["Middle Name(s)", "Suffix"])

# Create new columns for the number of victims per race
df['Number of White Victims'] = df['Number of White Male Victims'] + df['Number of White Female Victims']
df['Number of Black Victims'] = df['Number of Black Male Victims'] + df['Number of Black Female Victims']
df['Number of Latino Victims'] = df['Number of Latino Male Victims'] + df['Number of Latino Female Victims']
df['Number of Asian Victims'] = df['Number of Asian Male Victims'] + df['Number of Asian Female Victims']
df['Number of Native American Victims'] = df['Number of Native American Male Victims'] + df['Number of American Indian or Alaska Native Female Victims']
df['Number of Other Race Victims'] = df['Number of Other Race Male Victims'] + df['Number of Other Race Female Victims']

# drop das outras?

state_codes = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}
df['Race'] = df['Race'].replace('American Indian or Alaska Native','Native American')

# Create a new column in your dataframe that maps state names to state codes
df['State Code'] = df['State'].map(state_codes)

print(df.columns)

