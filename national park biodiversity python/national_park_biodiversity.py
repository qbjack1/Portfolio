import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency
from itertools import chain
import string

# ----- FETCHING, LOADING, INSPECTING, AND EXPLORING THE DATA ----- #

# ---- LOADING DATABASES ---- #
species_data = pd.read_csv('species_info.csv',encoding='utf-8')
observations_data = pd.read_csv('observations.csv', encoding='utf-8')

# ---- SPECIES DATABASE: INITIAL INSPECTIONS ---- #
print(f"Species Database (First 5 Records):\n{species_data.head()}", "\n")
print(f"Species Database Columns + Datatypes:\n{species_data.dtypes}", "\n")
print(f"Species Database Shape (ROWS, COLUMNS): {species_data.shape}", "\n")

# ---- SPECIES DATABASE: EDA ---- #
print(f"Species Database EDA:\n{species_data.describe()}", "\n")

# --- ANALYST'S NOTE --- #
print(f"ANALYST'S NOTE:\nBY EXPLORING THE SPECIES DATA, WE FIND THAT THERE ARE 5541 UNIQUE SPECIES, SCATTERED ALONG 7 CATEGORIES.", "\n")

# ---- SPECIES DATABASE: EXTRA INSPECTIONS ---- #
print(f"Number of Categories:{species_data.category.nunique()}")
print(f"Categories:\n{species_data.category.unique()}", "\n")

# ---- OBSERVATIONS DATABASE: INITIAL INSPECTIONS ---- #
print(f"Observations Database (First 5 Records):\n{observations_data.head()}", "\n")
print(f"Observations Database Columns + Datatypes:\n{observations_data.dtypes}", "\n")
print(f"Observations Database Shape (ROWS, COLUMNS): {observations_data.shape}", "\n")

# ---- OBSERVATIONS DATABASE: EDA ---- #
print(f"Observations Database EDA:\n{observations_data.describe()}", "\n")

# ----- FURTHER DATA EXPLORATIONS ----- #

# ---- SPECIES DATABASE: GROUP BY CATEGORY ---- #
print(species_data.groupby("category").size(), "\n")

# --- ANALYST'S NOTE --- #
print(f"ANALYST'S NOTE:\nBY FURTHER EXPLORING THE SPECIES DATA, WE FIND THAT VASCULAR PLANTS TAKE UP THE VAST MAJORITY, WITH AN AMOUNT OF 4470 UNIQUE SPECIES.\nREPTILES HAVE THE FEWEST UNIQUE SPECIES, COUNTED AT 79.", "\n")

# ---- SPECIES DATABASE: GROUP BY CONSERVATION STATUS ---- #
print(f"Number of Conservation Statuses:{species_data.conservation_status.nunique()}")
print(f"Unique Conservation Statuses:{species_data.conservation_status.unique()}", "\n")
print(f"Non-Endangered Species:{species_data.conservation_status.isna().sum()}")
print(species_data.groupby("conservation_status").size(), "\n")

# --- ANALYST'S NOTE --- #
print(f"ANALYST'S NOTE:\nWE CAN ALSO EXPLORE AS TO HOW MANY SPECIES ARE IN ANY RISK OF ENDANGERMENT.", "\n")

# ---- OBSERVATIONS DATABASE: CHECKING THE PARKS IN THE DATABASE ---- #
print(f"Number of Parks:{observations_data.park_name.nunique()}")
print(f"Unique parks:{observations_data.park_name.unique()}", "\n")

# --- ANALYST'S NOTE --- #
print(f"ANALYST'S NOTE: BY FURTHER EXPLORING THE OBSERVATIONS DATABASE, WE FIND THAT THERE ARE ONLY 4 NATIONAL PARKS IN THE DATABASE.", "\n")

# ---- OBSERVATIONS DATABASE: TOTAL OBSERVATIONS
print(f"Number of Observations:{observations_data.observations.sum()}", "\n")

# --- ANALYST'S NOTE --- #
print(f"ANALYST'S NOTE: THESE ARE THE TOTAL OBSERVED SPECIES IN ALL OF THE NATIONAL PARKS.", "\n")

# ----- ADVANCED DATA ANALYSIS ----- #

# ---- SPECIES DATA: ENDANGERMENT LEVEL CROSS TABULATION PLOT---- #
species_data.fillna('No Intervention', inplace=True)
conservationCategory = species_data[species_data.conservation_status != "No Intervention"]\
    .groupby(["conservation_status", "category"])['scientific_name']\
    .count()\
    .unstack()

ax = conservationCategory.plot(kind = 'bar', figsize=(8,6), 
                               stacked=True)
ax.set_xlabel("Conservation Status")
ax.set_ylabel("Number of Species")

plt.show()
plt.clf()

# ---- SPECIES DATA: CHI-SQUARED TESTS ---- #
species_data['is_protected'] = species_data.conservation_status != 'No Intervention'
category_counts = species_data.groupby(['category', 'is_protected'])\
                        .scientific_name.nunique()\
                        .reset_index()\
                        .pivot(columns='is_protected',
                                      index='category',
                                      values='scientific_name')\
                        .reset_index()
category_counts.columns = ['category', 'not_protected', 'protected']
category_counts['percent_protected'] = category_counts.protected / \
                                      (category_counts.protected + category_counts.not_protected) * 100

print(f"HYPOTHESIS TEST: ARE MAMMALS MORE LIKELY TO BE ENDANGERED THAN BIRDS?", "\n")
contingency1 = [[30, 146],
              [75, 413]]
print(chi2_contingency(contingency1), "\n")

# --- ANALYST'S NOTE --- #
print(f"ANALYST'S NOTE: WITH A P-VALUE OF 69%, WE CONCLUDE THAT THERE ISN'T ANY SIGNIFICANT RELATIONSHIP BETWEEN THE TWO VARIABLES.", "\n")

print(f"HYPOTHESIS TEST: ARE MAMMALS MORE LIKELY TO BE ENDANGERED THAN REPTILES?", "\n")
contingency2 = [[30, 146],
               [5, 73]]
print(chi2_contingency(contingency2), "\n")

# --- ANALYST'S NOTE --- #
print(f"ANALYST'S NOTE: WITH A P-VALUE OF 3.4%, WE CONCLUDE THAT THERE IS A SIGNIFICANT RELATIONSHIP BETWEEN THE TWO VARIABLES. MAMMALS ARE SHOWN TO HAVE A SIGNIFICANTLY HIGHER RATE OF PROTECTION COMPARED TO REPTILES.", "\n")