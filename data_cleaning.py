# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 08:13:34 2024

@author: hoang
"""

# Import modules
import pandas as pd
import numpy as np
from collections import Counter
from difflib import get_close_matches
 
# Read the datasets
job_skills = pd.read_csv('Datasets/job_skills.csv')
job_summary = pd.read_csv('Datasets/job_summary.csv')
job_posting = pd.read_csv('Datasets/job_postings.csv')

# Create a copy of each dataset to make original datasets remain intact
skills_df = job_skills.copy()
summary_df = job_summary.copy()
job_df = job_posting.copy()

# ------------------------------------------------------------------------------
# Extract salary in Job Summary dataset

# Extract the salary having the format like $xxx - $xxx
summary_df['salary1'] = summary_df.job_summary.str.extract(
    r'(\$\d+(?:\.\d{2})?(?:,\d{3})*(?: ?[–\- ] ?\$\d+(?:\.\d{2})?(?:,\d{3})*)?)', expand=False)
# Extract the salary including spaces and string like "to", "and", and "USD" in between
summary_df['salary2'] = summary_df.job_summary.str.extract(
    r'(\$\d{1,3}(?:,\d{3})*(?: ?[–\- ]?(?:to|and) ?\$\d{1,3}(?:,\d{3})*)?(?: ?USD)?)', expand=False)

# Combine the two salary columns together
summary_df['salary'] = summary_df.apply(lambda x: x.salary1 if len(
    str(x.salary1)) > len(str(x.salary2)) else x. salary2, axis=1)

# Get the mininum and maximum salary using string split method based on the seperators '-', 'to', or 'and'.
summary_df['min_salary'] = summary_df['salary'].str.split(
    '[-–]|to|and').str.get(0).str.strip()
summary_df['max_salary'] = summary_df['salary'].str.split(
    '[-–]|to|and').str.get(1).str.strip()
summary_df['min_salary'] = summary_df['min_salary'].str.split().str.get(0)
summary_df['max_salary'] = summary_df['max_salary'].str.split().str.get(0)

# Remove the "$" sign and ","
summary_df['min_salary'] = summary_df['min_salary'].str.replace(
    "$", "").str.replace(",", "")
summary_df['max_salary'] = summary_df['max_salary'].str.replace(
    "$", "").str.replace(",", "")

# Convert the data type into float
summary_df['min_salary'] = summary_df['min_salary'].astype('float')
summary_df['max_salary'] = summary_df['max_salary'].astype('float')

# Adjust the min salary
summary_df['min_salary'] = summary_df.apply(lambda x: np.nan if (
    pd.isna(x.max_salary) and (x.min_salary < 13)) else x.min_salary, axis=1)

# Create a function to convert different types of salary to annual salary
def annual_salary(x):
    # hourly to annually salary
    if x < 100:
        return x * 40 * 52
    # daily to annually salary
    elif x < 500:
        return x * 5 * 52
    # weekly to annually salary
    elif x < 4000:
        return x * 52
    # monthly to annually salary
    elif x < 20000:
        return x * 12
    return x

# Apply the function to both min and max salary columns
summary_df['min_salary'] = summary_df['min_salary'].apply(annual_salary)
summary_df['max_salary'] = summary_df['max_salary'].apply(annual_salary)
# Create a column for average salary based on min and max salary
summary_df['ave_salary'] = summary_df[['min_salary', 'max_salary']].mean(axis=1)

# Select desired columns from the DataFrame
salary_df = summary_df[['job_link', 'min_salary', 'max_salary', 'ave_salary']]
# Save the DataFrame to a csv file
salary_df.to_csv('Datasets/job_salary.csv', index=False)

# ------------------------------------------------------------------------------
# Create a DF containing most common job skills from the Job Skill dataset

# Merge all skills from the entire dataset into a concatenated string
skills = ''
for skill in skills_df.job_skills:
    skills += str(skill).lower()

# Split each skill by a ',', returning a list of skills
skills = skills.split(', ')

# Count each skills' frequency from the skill list
counts = Counter(skills)

# Filter 2000 most common skills
top_2000 = Counter(dict(counts.most_common(2000)))

# Create a function to merge similar label
def merge_similar_label(count_dict):
    merged_counts = {}
    merged = set()
    
    for label, count in count_dict.items():
        if label in merged:
            continue              # Skip if already merged
            
        # Find the most similar label to the current label with 85% of similarity
        similar_labels = get_close_matches(label, count_dict.keys(), cutoff=0.85)
        
        # Choose the most appropriate label among similar labels
        chosen_label = min(similar_labels, key=len)
        
        # Sum the counts of the similar labels and assign them to the chosen label
        merged_counts[chosen_label] = sum(count_dict[lb] for lb in similar_labels)
        
        # Mark the similar labels as merged
        merged.update(similar_labels)
        
    return merged_counts


merged_counts = merge_similar_label(top_2000)
# Choose 100 most common skills
merged_counts = Counter(merged_counts).most_common(100) 
skill_count_df = pd.DataFrame(merged_counts, columns=['skill', 'counts'])

# Communication skill
communication = skill_count_df.loc[skill_count_df.skill.str.contains('communication')]
skill_count_df = skill_count_df.drop(communication.index, axis=0)
skill_count_df.loc[len(skill_count_df)] = ['communication', communication.counts.sum()]

# Save the DataFrame to a csv
skill_count_df.to_csv('Datasets/common_job_skills.csv', index=False)

#------------------------------------------------------------------------------
# Clean the job posting dataset
# Standardize job title
def standardize_job_title(title):    
    if all(item in title for item in ['data', 'warehouse']):
        return 'Data Warehouse Engineer'
    elif 'database' in title:
        return 'Database Management Specialist'
    elif 'consultant' in title:
        return 'Data Analytics Consultant'
    elif all(item in title for item in ['data', 'engineer']) or 'elt' in title:
        return 'Data Engineer'
    elif all(item in title for item in ['data', 'architect']):
        return 'Data Architect'
    elif all(item in title for item in ['data', 'operation']):
        return 'Data Operation Specialist'
    elif all(item in title for item in ['data', 'governance']):
        return 'Data Governance'
    elif all(item in title for item in ['data', 'center']):
        return 'Data Center'
    elif all(item in title for item in ['data', 'scientist']):
        return 'Data Scientist'
    elif all(item in title for item in ['data', 'science']):
        return 'Data Scientist'
    elif all(item in title for item in ['machine', 'learning']):
        return 'AI & ML Engineer'
    elif all(item in title for item in ['ml', 'engineer']):
        return 'AI & ML Engineer'
    elif all(item in title for item in ['ai', 'ml']):
        return 'AI & ML Engineer'
    elif 'mlops' in title:
        return 'AI & ML Engineer'
    elif all(item in title for item in ['data', 'manager']):
        return 'Data Manager'
    elif all(item in title for item in ['product', 'manager']):
        return 'Product Manager'
    elif all(item in title for item in ['data', 'visualization']):
        return 'Data Visualization Specialist'
    elif all(item in title for item in ['data', 'analyst']):
        return 'Data Analyst'
    elif all(item in title for item in ['finance', 'analyst']):
        return 'Data Analyst'
    elif all(item in title for item in ['data', 'analytics']):
        return 'Data Analyst'
    elif all(item in title for item in ['data', 'analysis']):
        return 'Data Analyst'
    elif all(item in title for item in ['data', 'model']):
        return 'Data Modeler'
    elif 'data' in title:
        return 'Data Specialist'
    else:
        return 'Other'

# Apply the function to the job_title column
job_df['cleaned_title'] = job_df['job_title'].apply(lambda x: standardize_job_title(x.lower()))

# Extract city and state from the job_location columns
job_df['job_city'] = job_df['job_location'].str.split(',').str.get(0).str.strip()
job_df['state'] = job_df['job_location'].str.split(',').str.get(1).str.strip()

# Map the city to its corresponding state
city_state_mapping = {'New York City': 'NY', 
                      'Buffalo': 'NY', 
                      'San Francisco': 'CA',
                      'Dallas': 'TX',
                      'Houston': 'TX',
                      'Los Angeles': 'CA',
                      'DC': 'Washington D.C',
                      'Boston': 'MA',
                      'Atlanta': 'GA'}
# Create a function to extract the city and state 
# if the city data happens to have that kind of city format
def standardize_location(x):
    for ct, st in city_state_mapping.items():
        if ct.lower() in str(x.job_city).lower():
            x['job_city'] = ct
            x['state'] = st
            return x
    x['state'] = 'Unknown'
    return x
# Filter data having missing values in the state column and apply that function to the DataFrame
job_df.loc[job_df['state'].isna(), ['job_city', 'state']] = job_df.loc[job_df['state'].isna(), ['job_city', 'state']].apply(standardize_location, axis=1)

# Create a function to fix the state name 
def state_cleaning(x):    
    if x.state == 'United States':  # If the state's name is "United States", replace it
        x['state'] = x.job_city     # with the city, and make the city a missing value
        x['job_city'] = np.nan
    return x
# Apply the function to the dataset
job_df = job_df.apply(state_cleaning, axis=1)

# Import the state's name and abbreviation mapping from an external file
from US_states import state_abbreviations

# Create a function to replace the state name with its abbreviation
def state_abbre(x):
    for state in state_abbreviations:
        if state.lower() in x.lower():
            x = state_abbreviations[state]
    return x

# Apply the function to the state column
job_df['state'] = job_df['state'].apply(state_abbre)


# Dropping unnecessary columns
cleaned_df = job_df[['job_link', 'last_processed_time', 'first_seen', 'cleaned_title', 'company',
       'job_city', 'state', 'search_city', 'search_country', 'search_position', 'job_level',
       'job_type']]
cleaned_df.rename(columns={'cleaned_title':'job_title'}, inplace=True)

# Filter job opennings in the US
us_job = cleaned_df.query('search_country == "United States"')

# Save the DFs to csv file
us_job.to_csv("Datasets/US_job_postings.csv", index=False)
cleaned_df.to_csv("Datasets/cleaned_job_postings.csv", index=False)
