import pandas as pd
import numpy as np

variables_district = pd.DataFrame({
    'District': ['BARCELONA', 'Ciutat Vella', 'L\'Eixample', 'Sants-Montjuïc', 'Les Corts', 'Sarrià-Sant Gervasi',
                 'Gràcia', 'Horta-Guinardó', 'Nou Barris', 'Sant Andreu', 'Sant Martí'],
    'Total': [1660314, 109672, 269349, 187026, 81576, 149201, 123276, 173944, 173552, 151537, 241181],
    'Percentage_Total': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    'Female': [869379, 50387, 142773, 96990, 43714, 80653, 66538, 92183, 91887, 79471, 124783],
    'Percentage_Female': [0.524, 0.459, 0.53, 0.519, 0.536, 0.541, 0.54, 0.53, 0.529, 0.524, 0.517],
    'Male': [790935, 59285, 126576, 90036, 37862, 68548, 56738, 81761, 81665, 72066, 116398],
    'Percentage_Male': [0.476, 0.541, 0.47, 0.481, 0.464, 0.459, 0.46, 0.47, 0.471, 0.476, 0.483],
    '% Nens (0-15 anys)': [0.129, 0.104, 0.109, 0.12, 0.132, 0.162, 0.124, 0.128, 0.139, 0.139, 0.136],
    '% Joves (16-24 anys)': [0.086, 0.096, 0.08, 0.082, 0.082, 0.105, 0.076, 0.084, 0.09, 0.083, 0.083],
    '% Adults joves (25-39 anys)': [0.227, 0.36, 0.259, 0.245, 0.192, 0.178, 0.246, 0.203, 0.196, 0.195, 0.212],
    '% Adults grans (40-64 anys)': [0.348, 0.32, 0.334, 0.354, 0.328, 0.339, 0.34, 0.356, 0.355, 0.366, 0.365],
    '% Gent gran (65 anys i més)': [0.211, 0.12, 0.218, 0.199, 0.266, 0.216, 0.214, 0.229, 0.22, 0.217, 0.204],
    "Nacionalitat espanyola": [0.776, 0.474, 0.747, 0.756, 0.852, 0.854, 0.794, 0.828, 0.791, 0.844, 0.789],
    "Nacionalitat estrangera": [0.224, 0.526, 0.253, 0.244, 0.148, 0.146, 0.206, 0.172, 0.209, 0.156, 0.211],
    '% Sin estudios': [0.016, 0.012, 0.009, 0.017, 0.01, 0.004, 0.011, 0.023, 0.03, 0.017, 0.018],
    '% Estudios primarios / certificado de escolaridad / EGB': [0.15, 0.203, 0.095, 0.184, 0.093, 0.051, 0.098, 0.167, 0.241, 0.179, 0.17],
    '% Bachillerato elemental / graduado escolar / ESO / FPI': [0.219, 0.237, 0.166, 0.241, 0.158, 0.118, 0.168, 0.251, 0.31, 0.264, 0.245],
    '% Bachillerato superior / BUP / COU / FPII / CFGM grado medio': [0.256, 0.213, 0.258, 0.251, 0.27, 0.273, 0.258, 0.271, 0.241, 0.272, 0.253],
    '% Estudios universitarios / CFGS grado superior': [0.346, 0.3, 0.462, 0.294, 0.455, 0.535, 0.454- 0.0010000000000001, 0.274, 0.241- 0.0790000000000002, 0.272-0.018, 0.299],
    '% No consta': [0.013, 0.035, 0.01, 0.013, 0.014, 0.019, 0.012, 0.014, 0.016, 0.014, 0.015],
    'Homeless': [1231 ,344, 297, 183, 43, 34, 32, 67, 54, 18, 159],
    '% Unemployment' : [1 , 0.0703, 0.046, 0.061, 0.0497, 0.0343, 0.0507, 0.0623, 0.079, 0.647, 0.063] # respecte població 16-64 anys 1.082.322 
}) 

variables_district['% Percentage_Homeless'] = variables_district['Homeless'] / variables_district['Total']
variables_district['Percentage_Total'] = (variables_district['Total'] / 1660314)
variables_district.drop(0,inplace=True)

# NATIONALITY / GENDER

nationality_gender = pd.read_csv('data/nationality/2022_nationality_gender.csv')
nationality_gender = nationality_gender[['Codi_Districte', 'Nom_Districte', 'NACIONALITAT_G', 'SEXE', 'Valor']] #7000 files

nationality_gender['SEXE'] = nationality_gender['SEXE'].replace({1:0, 2:1})
nationality_gender['Codi_Districte'] = nationality_gender['Codi_Districte'].apply(lambda x: x-1)
nationality_gender.rename(columns ={'Codi_Districte': 'D', 'NACIONALITAT_G': 'N', 'SEXE': 'G'}, inplace =True)
nationality_gender = nationality_gender.loc[nationality_gender['Valor'] != ".."]
nationality_gender['Valor'] = pd.to_numeric(nationality_gender['Valor'])

N_map = {1: '0', 2: '1', 3: '1'}
''' Variable no es diu igual!
1. Espanyola
2. Resta
3. Resta
'''

nationality_gender['N'] = nationality_gender['N'].map(lambda x: N_map.get(x))
nationality_gender = nationality_gender.groupby(['D', 'Nom_Districte', 'N', 'G'])['Valor'].sum().reset_index()
nationality_gender['Total_Sum'] = nationality_gender.groupby(['D', 'G'])['Valor'].transform('sum')
nationality_gender['Percentage'] = nationality_gender['Valor'] / nationality_gender['Total_Sum']
nationality_gender.drop(columns=['Total_Sum'], inplace=True)

# GENDER / DISTRICT
gender_district = pd.read_csv('data/gender/2022_pad_mdbas_gender.csv')
gender_district = gender_district[['Codi_Districte', 'Nom_Districte', 'SEXE', 'Valor']] 

gender_district['SEXE'] = gender_district['SEXE'].replace({1:0, 2:1})
gender_district['Codi_Districte'] = gender_district['Codi_Districte'].apply(lambda x: x-1)
gender_district.rename(columns= {'Codi_Districte': 'D', 'SEXE': 'G'}, inplace =True)
#gender_district.loc[type(nationality_gender['Valor']) != numeric]

# gender_district['Valor'] = pd.to_numeric(nationality_gender['Valor'])
gender_district = gender_district.groupby(['D', 'Nom_Districte', 'G'])['Valor'].sum().reset_index()
gender_district
gender_district['Total_Sum'] = gender_district.groupby(['D'])['Valor'].transform('sum')
gender_district['Percentage'] = gender_district['Valor'] / gender_district['Total_Sum']
#gender_district.drop(columns=['Total_Sum'], inplace=True)

# AGE / DISTRICT
age_district = pd.read_csv('data/age/2022_pad_mdbas_age.csv')
age_district = age_district[['Codi_Districte', 'Nom_Districte', 'EDAT_1', 'Valor']] 

age_district['Codi_Districte'] = age_district['Codi_Districte'].apply(lambda x: x-1)
age_district.rename(columns = {'Codi_Districte': 'D', 'EDAT_1': 'A'}, inplace =True)

age_district['Valor'] = age_district['Valor'].replace({"..":0})
age_district['Valor'] = pd.to_numeric(age_district['Valor'])
age_district = age_district.groupby(['D', 'Nom_Districte', 'A'])['Valor'].sum().reset_index()
age_district['Total_Sum'] = age_district.groupby(['D'])['Valor'].transform('sum')
age_district['Percentage'] = age_district['Valor'] / age_district['Total_Sum']
age_district.drop(columns=['Total_Sum'], inplace=True)

# DECIMAL AGE / DISTRICT
def map_age_to_da(age):
    if 15 <= age <= 24:
        return '0'
    elif 25 <= age <= 34:
        return '1'
    elif 35 <= age <= 44:
        return '2'
    elif 45 <= age <= 54:
        return '3'
    elif 55 <= age <= 64:
        return '4'
    elif 65 <= age <= 74:
        return '5'
    #else:
        #return 0  # for ages outside your specified range

age_district['DA'] = age_district['A'].apply(map_age_to_da).dropna()
decage_district = age_district.groupby(['D', 'DA']).agg({'Percentage': 'sum'}).reset_index()
def normalize(group):
    group['Percentage'] /= group['Percentage'].sum()
    return group
decage_district = decage_district.groupby('D').apply(normalize)
decage_district = decage_district[['D', 'DA', 'Percentage']].reset_index(drop=True)

# NIV_ED / GENDER AND DISTRICT
nived_gender = pd.read_csv('data/status/2022_niv-educa_gender.csv') 
nived_gender = nived_gender[['Codi_Districte', 'Nom_Districte', 'NIV_EDUCA_esta', 'SEXE', 'Valor']] #7000 files

nived_gender['SEXE'] = nived_gender['SEXE'].replace({1:0, 2:1})
nived_gender['Codi_Districte'] = nived_gender['Codi_Districte'].apply(lambda x: x-1)

nived_gender.rename(columns ={'Codi_Districte': 'D', 'NIV_EDUCA_esta': 'E', 'SEXE': 'G'}, inplace =True)
nived_gender['Valor'] = nived_gender['Valor'].replace({"..":0})
nived_gender['Valor'] = pd.to_numeric(nived_gender['Valor'])

nived_gender = nived_gender.loc[nived_gender['E'] != 6]
nived_gender = nived_gender.groupby(['D', 'Nom_Districte', 'E', 'G'])['Valor'].sum().reset_index()
nived_gender['Total_Sum'] = nived_gender.groupby(['D', 'G'])['Valor'].transform('sum')
nived_gender['Percentage'] = nived_gender['Valor'] / nived_gender['Total_Sum']
nived_gender.drop(columns=['Total_Sum'], inplace=True)

# NIV ED / LLOC NAIXEMENT
nived_nationality =  pd.read_csv('data/status/2022_Ned_nationality.csv') 

# GENDER AND AGE GIVEN DISTRICT FOR THE ACCURACY
gender_age_district = pd.read_csv('data/gender_age/2022_pad_mdbas_gender_age.csv') 
gender_age_district = gender_age_district[['Codi_Districte', 'Nom_Districte', 'EDAT_1', 'SEXE', 'Valor']] #7000 files
gender_age_district['SEXE'] = gender_age_district['SEXE'].replace({1:0, 2:1})
gender_age_district['Codi_Districte'] = gender_age_district['Codi_Districte'].apply(lambda x: x-1)
gender_age_district.rename(columns= {'SEXE': 'G', 'EDAT_1': 'A', 'Valor': 'Count', 'Codi_Districte': 'D'}, inplace= True)
gender_age_district['Count'] = pd.to_numeric(gender_age_district['Count'].replace({"..":0}))

gender_age_district = gender_age_district.groupby(['D', 'G', 'A'])['Count'].sum().reset_index()
gender_age_district['Total_Sum'] = gender_age_district.groupby(['D'])['Count'].transform('sum')
gender_age_district['Percentage'] = gender_age_district['Count'] / gender_age_district['Total_Sum']
gender_age_district.drop(columns=['Total_Sum'], inplace=True)

# NATIONALITY AND AGE AND GENDER GIVEN DISTRICT FOR THE ACCURACY
nationality_quinqage_gender = pd.read_csv('data/nationality/2022_nationality_quinqage_gender.csv')
nationality_quinqage_gender.rename(columns= {'SEXE': 'G', 'EDAT_Q': 'QA', 'NACIONALITAT_G': 'N', 'Valor': 'Count', 'Codi_Districte': 'D'}, inplace= True)
nationality_quinqage_gender = nationality_quinqage_gender[['D', 'N', 'QA', 'G', 'Count']]
nationality_quinqage_gender['G'] = nationality_quinqage_gender['G'].replace({1:0, 2:1})
nationality_quinqage_gender['D'] = nationality_quinqage_gender['D'].apply(lambda x: x-1)
nationality_quinqage_gender['Count'] = pd.to_numeric(nationality_quinqage_gender['Count'].replace({"..":0}))
nationality_quinqage_gender = nationality_quinqage_gender.groupby(['D', 'N', 'G', 'QA'])['Count'].sum().reset_index()

nationality_quinqage_gender['Total_Sum'] = nationality_quinqage_gender.groupby(['D'])['Count'].transform('sum')
nationality_quinqage_gender['Percentage'] = nationality_quinqage_gender['Count'] / nationality_quinqage_gender['Total_Sum']
nationality_quinqage_gender.drop(columns=['Total_Sum'], inplace=True)

# QA to DA
def map_qa_to_group(qa):
    if 3 <= qa <= 4:   # Ages 15-24
        return '0'
    elif 5 <= qa <= 6: # Ages 25-34
        return '1'
    elif 7 <= qa <= 8: # Ages 35-44
        return '2'
    elif 9 <= qa <= 10: # Ages 45-54
        return '3'
    elif 11 <= qa <= 12: # Ages 55-64
        return '4'
    elif 13 <= qa <= 14: # Ages 65-74
        return '5'
    else:
        return None  # Exclude other ages
nationality_quinqage_gender['DA'] = nationality_quinqage_gender['QA'].apply(map_qa_to_group)
nationality_decage_gender = nationality_quinqage_gender.dropna(subset=['DA'])
nationality_decage_gender = nationality_decage_gender.groupby(['N', 'G', 'DA']).agg({'Count': 'sum', 'Percentage': 'sum'}).reset_index()
nationality_decage_gender['Percentage'] = nationality_decage_gender.groupby(['N', 'G'])['Percentage'].transform(lambda x: x / x.sum())

# NIV ED AND AGE AND GENDER GIVEN DISTRICT FOR THE ACCURACY
nived_qa_gender = pd.read_csv('data/status/2022_ned_quinqage_gender.csv')
nived_qa_gender.rename(columns= {'SEXE': 'G', 'EDAT_Q': 'QA', 'NIV_EDUCA_esta': 'E', 'Valor': 'Count', 'Codi_Districte': 'D'}, inplace= True)
nived_qa_gender = nived_qa_gender[['D', 'E', 'QA', 'G', 'Count']]
nived_qa_gender['G'] = nived_qa_gender['G'].replace({1:0, 2:1})
nived_qa_gender['D'] = nived_qa_gender['D'].apply(lambda x: x-1)
nived_qa_gender['Count'] = pd.to_numeric(nived_qa_gender['Count'].replace({"..":0}))
nived_qa_gender = nived_qa_gender.groupby(['D', 'E', 'G', 'QA'])['Count'].sum().reset_index()
nived_qa_gender['Total_Sum'] = nived_qa_gender.groupby(['D'])['Count'].transform('sum')
nived_qa_gender['Percentage'] = nived_qa_gender['Count'] / nived_qa_gender['Total_Sum']
nived_qa_gender.drop(columns=['Total_Sum'], inplace=True)

# UNEMPLOYMENT / GENDER AND DISTRICT
unemp_gender = pd.read_csv('data/status/2022_atur_per_sexe.csv') 
unemp_gender = unemp_gender[['Codi_Districte', 'Demanda_ocupacio', 'Sexe', 'Nombre']] #7000 files
unemp_gender['Sexe'] = unemp_gender['Sexe'].replace({'Dones':0, 'Homes':1})
unemp_gender['Codi_Districte'] = unemp_gender['Codi_Districte'].apply(lambda x: x-1)
unemp_gender.rename(columns ={'Codi_Districte': 'D', 'Demanda_ocupacio': 'U', 'Sexe': 'G', 'Nombre': 'Valor'}, inplace =True)
unemp_gender['Valor'] = unemp_gender['Valor'].replace({"..":0})
unemp_gender['Valor'] = pd.to_numeric(unemp_gender['Valor'])
unemp_gender['U'] = unemp_gender['U'].replace({"Atur Registrat":0, "Demanda No Aturats": 1})

unemp_gender = unemp_gender.groupby(['D', 'U', 'G'])['Valor'].sum().reset_index()
unemp_gender['Total_Sum'] = unemp_gender.groupby(['D', 'G'])['Valor'].transform('sum')
unemp_gender['Percentage'] = unemp_gender['Valor'] / unemp_gender['Total_Sum']
unemp_gender.drop(columns=['Total_Sum'], inplace=True)

unemp_gender = unemp_gender.loc[unemp_gender['D']!=98]  #cuidado hi ha un codi districte 98 amb dades que trec pero que no se que son

# UNEMPLOYMENT / AGE, GENDER AND DISTRICT
unemp_gender_quinqage = pd.read_csv('data/status/2023_unemp_gender_quinqage.csv') 
unemp_gender_quinqage['Districte'] = unemp_gender_quinqage.index
unemp_gender_quinqage.columns = unemp_gender_quinqage.columns.str.replace('\n', '', regex=False)
for col in unemp_gender_quinqage.columns:
    if col != 'D':
        unemp_gender_quinqage[col] = pd.to_numeric(unemp_gender_quinqage[col], errors='coerce')

unemp_gender_quinqage= unemp_gender_quinqage[['Districte','Total aturades', '<20 anys.1', '20-24 anys.1', '25-29 anys.1', '30-44 anys.1', '45 i més anys.1', 'Total aturats.1','<20 anys.2', '20-24 anys.2', '25-29 anys.2', '30-44 anys.2','45 i més anys.2']] # borro U/D , em quedo amb U/ G, QA, D

# POLITICAL INCLINATION / DISTRICT 
political = pd.read_csv('data/political/A20211-Vots-DM.csv', sep = ';')
political = political.loc[political['Nom Municipi']== 'Barcelona']  #keep only barcelona and their districts
political = political[['Districte', 'Sigles Candidatura', 'Vots']] #keep the columns i am interested on
political.rename(columns ={'Districte': 'D', 'Sigles Candidatura': 'P'}, inplace =True)
political['Vots'].sum()   #617.013 persones amb vot registrat a barcelona

political = political.groupby(['D', 'P'])['Vots'].sum().reset_index()
political['Total_Sum'] = political.groupby(['D'])['Vots'].transform('sum')
political['Percentage'] = political['Vots'] / political['Total_Sum']
political.drop(columns=['Total_Sum'], inplace=True)
political['D'] = political['D'].apply(lambda x: x-1)

# INCOME / DISTRICT
income = pd.read_csv('data/salary/2021_income_ind.csv')
income.rename(columns = {'Codi_Districte': 'D', 'Import_Renda_Bruta_€': 'I'}, inplace =True)
income = income[['D', 'I']]
income['D'] = income['D'].apply(lambda x: x-1)

# RENT / DISTRICT
rent = pd.read_csv('data/rent/2023_lloguer_preu_trim.csv') #lloguer mitja mensual per domicili?
rent.rename(columns = {'Codi_Districte': 'D', 'Preu': 'Rent'}, inplace =True)
rent = rent[['D', 'Rent']]
rent['D'] = rent['D'].apply(lambda x: x-1)
rent = rent.dropna() #19 valors NA districte 7 sobretot, 6 i 8

#DISCRETIZATION CONTINUOUS VARIABLES
# INCOME
from scipy.stats import gaussian_kde
# Perform KDE on the income data
income_data = income['I']  # replace with your actual income column
kde = gaussian_kde(income_data)
# Number of bins for discretizing income
num_bins = 1000
income_range = np.linspace(0, 47000, num_bins)

# Initialize an array to hold the PDFs for each district
pdfs = np.zeros((num_bins, 10))  # 10 districts

# Estimate and store KDE for each district
for district in range(10):
    district_data = income[income['D'] == district]['I'] 
    if len(district_data) > 0:
        kde = gaussian_kde(district_data)
        pdfs[:, district] = kde.pdf(income_range)

# Normalize each column (district) in the PDFs array
pdfs_I_normalized = pdfs / pdfs.sum(axis=0)

# RENT
# Determine the range for rent
max_rent = rent['Rent'].max()
min_rent = rent['Rent'].min()
num_bins_rent = 1000
rent_bins = np.linspace(min_rent, max_rent, num_bins_rent)

# Initialize an array for the PDFs for rent
pdfs_rent = np.zeros((num_bins_rent-1, 10))  # Assuming 10 districts

# KDE for each district
for district in range(10):
    district_rent_data = rent[rent['D'] == district]['Rent']
    if not district_rent_data.empty:
        kde_rent = gaussian_kde(district_rent_data)
        pdfs_rent[:, district] = kde_rent.evaluate(rent_bins[:-1])

pdfs_rent_normalized = pdfs_rent / pdfs_rent.sum(axis=0)


# SOCIAL VALUES
social_values = pd.read_csv('data/values/2021_valors_socials.csv')
  
columns_motivational = ['IMP_PERS_FAM_1A4','IMP_PERS_AMIC_1A4', 'IMP_PERS_TEMPS_1A4', 'IMP_PERS_POLITICA_1A4',
                   'IMP_PERS_FEINA_1A4', 'IMP_PERS_RELIGIO_1A4', 'IMP_PERS_ECON_1A4',
                   'IMP_PERS_ESTUDIAR_1A4', 'IMP_PERS_DESENV_1A4', 'SATISF_PERS_1A10',
                   'SATISF_PERS_1A4', 'SATISF_PERS_FAM_1A10', 'SATISF_PERS_AMIC_1A10',
                   'SATISF_PERS_TEMPS_1A10', 'SATISF_PERS_FEINA_1A10', 'SATISF_PERS_ECON_1A10',
                   'SATISF_PERS_ESTUDIAR_1A10', 'SATISF_PERS_DESENV_1A10', 'SATISF_PERS_FAM_1A4',
                   'SATISF_PERS_AMIC_1A4', 'SATISF_PERS_TEMPS_1A4', 'SATISF_PERS_FEINA_1A4',
                   'SATISF_PERS_ECON_1A4','SATISF_PERS_ESTUDIAR_1A4', 'SATISF_PERS_DESENV_1A4'] 

columns_to_keep = ['DISTRICTE','SEXE', 'EDAT1574_1A6', 'NACIO_ACT_UE',
                    'ESTUDIS_1A6'] + columns_motivational


# KeyError: "['HAB_RES_NRE', 'SOCI_Q11_1A11'] not in index" les he esborrat
social_values = social_values.loc[:, columns_to_keep]

# valors_socials.dropna(inplace=True) removes too much rows
social_values.fillna(-1, inplace=True)

social_values['DISTRICTE'] = social_values['DISTRICTE'].apply(lambda x: x-1)
social_values['SEXE'] = social_values['SEXE'].apply(lambda x: x-1)
social_values.rename(columns ={'DISTRICTE': 'D', 'NACIO_ACT_UE': 'N', 'SEXE': 'G', 'EDAT1574_1A6': 'DA', 'ESTUDIS_1A6': 'E'}, inplace =True)
social_values['N'] = social_values['N'].apply(lambda x: x-1)
social_values['E'] = social_values['E'].apply(lambda x: x-1)

# import random
# #randomly generate A value column based on DA decimal age
# def generate_age(decimal_age):
#     if decimal_age == 1:
#         return random.randint(15, 24)
#     elif decimal_age == 2:
#         return random.randint(25, 34)
#     elif decimal_age == 3:
#         return random.randint(35, 45)
#     elif decimal_age == 4:
#         return random.randint(45, 54)
#     elif decimal_age == 5:
#         return random.randint(55, 64)
#     elif decimal_age == 6:
#         return random.randint(65, 74)
#     else:
#         return None
# social_values['A'] = social_values['DA'].apply(generate_age)
# social_values.drop(columns=['DA'], inplace=True)

social_values = social_values.loc[social_values['E'] != 98]
social_values['E'].unique()

import pandas as pd

valors_socials = pd.read_csv('data/values/2021_valors_socials.csv')

# variables socio-demogràfiques i laborals
columns_to_keep = ['DISTRICTE', 'SEXE', 'EDAT1574_1A6', 'NACIO_ACT_UE',
                   'HAB_RES_1A4', 'TE_FILLS_1A2', 'SITPERSONAL_1A4', 'CLASSESOC_ENT_1A5',
                   'SITLABORAL_1A9', 'ESTUDIS_1A6']

# Esborrant 'PROF_ACT_B' tenc totes les columnes!

# nivells d'importància
columns_to_keep.extend(['IMP_PERS_FAM_1A4', 'IMP_PERS_AMIC_1A4','IMP_PERS_TEMPS_1A4',
                        'IMP_PERS_POLITICA_1A4', 'IMP_PERS_FEINA_1A4', 'IMP_PERS_RELIGIO_1A4', 'IMP_PERS_ECON_1A4',
                        'IMP_PERS_ESTUDIAR_1A4', 'IMP_PERS_DESENV_1A4'])

# nivells de satisfacció
columns_to_keep.extend(['SATISF_PERS_1A10', 'SATISF_PERS_FAM_1A10','SATISF_PERS_AMIC_1A10',
                        'SATISF_PERS_TEMPS_1A10', 'SATISF_PERS_FEINA_1A10', 'SATISF_PERS_ECON_1A10',
                        'SATISF_PERS_ESTUDIAR_1A10', 'SATISF_PERS_DESENV_1A10'])

# ideologia
columns_to_keep.extend(['IDEO_1A8', 'IDEO_PARE_1A8', 'IDEO_MARE_1A8', 'IDEO_PARTIT', 'INTERES_POLITICA_1A4',
                        'ACORD_SOCIETAT_CONCEPT_Q01_1A3', 'ACORD_SOCIETAT_CONCEPT_Q02_1A3', 'ACORD_SOCIETAT_CONCEPT_Q03_1A3',
                        'SENTPERTI_1A5', 'RELIGIO','ACORD_SOCIETAT_CONCEPT_Q05_1A3', 'ACORD_SOCIETAT_CONCEPT_Q06_1A3', 'ACORD_SOCIETAT_CONCEPT_Q09_1A3',
                        'ACORD_SOCIETAT_JUSTIFICAR_Q04_1A3', 'PRIO_ESTAT_POLITICA_MEDIAMB_1A2',
                        'IMPACTE_IMMIG_PAIS_1A10', 'CONFIA_INSTITUCIO_Q01_1A4',
                        'CONFIA_INSTITUCIO_Q11_1A4', 'CONFIA_INSTITUCIO_Q12_1A4', 'IMP01_ESTAT_1A4', 'IMP02_ESTAT_1A4'])

valors_socials = valors_socials.loc[:, columns_to_keep]

# rename columns
new_column_names = {'DISTRICTE': 'D', 'SEXE': 'G', 'EDAT1574_1A6': 'DA', 'NACIO_ACT_UE': 'N',
                    'TE_FILLS_1A2': 'Ch', 'SITPERSONAL_1A4': 'S', 'CLASSESOC_ENT_1A5': 'C',
                    'SITLABORAL_1A9': 'U', 'ESTUDIS_1A6': 'E', 'HAB_RES_1A4': 'HR',
                    'IMP_PERS_FAM_1A4': 'IF', 'IMP_PERS_AMIC_1A4': 'IA', 'IMP_PERS_TEMPS_1A4': 'IT',
                    'SATISF_PERS_1A10': 'Sat', 'SATISF_PERS_FAM_1A10': 'SF', 'SATISF_PERS_AMIC_1A10': 'SA',
                    'SATISF_PERS_TEMPS_1A10': 'ST', 'IDEO_1A8': 'Ideo', 'IDEO_PARTIT': 'IP',
                    'ACORD_SOCIETAT_CONCEPT_Q01_1A3': 'Cap', 'ACORD_SOCIETAT_CONCEPT_Q02_1A3': 'Soc', 'ACORD_SOCIETAT_CONCEPT_Q03_1A3': 'Com',
                    'SENTPERTI_1A5': 'Indep', 'RELIGIO': 'Rel',

                    'IMP_PERS_POLITICA_1A4': 'Ipol', 'IMP_PERS_FEINA_1A4': 'Iemp', 'IMP_PERS_RELIGIO_1A4': 'Irel', 'IMP_PERS_ECON_1A4': 'Iecon',
                    'IMP_PERS_ESTUDIAR_1A4': 'IE', 'IMP_PERS_DESENV_1A4': 'Ides',
                    'SATISF_PERS_FEINA_1A10': 'Semp', 'SATISF_PERS_ECON_1A10': 'Secon', 'SATISF_PERS_ESTUDIAR_1A10': 'SE', 'SATISF_PERS_DESENV_1A10': 'Sdes',
                    'IDEO_PARE_1A8': 'Ipare', 'IDEO_MARE_1A8': 'Imare', 'INTERES_POLITICA_1A4': 'InterPolitica',
                    'ACORD_SOCIETAT_CONCEPT_Q05_1A3': 'Femin', 'ACORD_SOCIETAT_CONCEPT_Q06_1A3': 'Ecolog', 'ACORD_SOCIETAT_CONCEPT_Q09_1A3': 'Multiculturalism',
                    'ACORD_SOCIETAT_JUSTIFICAR_Q04_1A3': 'JustOkupa', 'PRIO_ESTAT_POLITICA_MEDIAMB_1A2': 'EconVsMedi',
                    'IMPACTE_IMMIG_PAIS_1A10': 'Immig', 'CONFIA_INSTITUCIO_Q01_1A4': 'ConfMon',
                    'CONFIA_INSTITUCIO_Q11_1A4': 'ConfPol', 'CONFIA_INSTITUCIO_Q12_1A4': 'ConfGov', 'IMP01_ESTAT_1A4': 'Inglehart1', 'IMP02_ESTAT_1A4': 'Inglehart2'
                    }
valors_socials.rename(columns=new_column_names, inplace=True)

valors_socials.dropna(inplace=True)

# delete rows with 'no answer' (99)
valors_socials = valors_socials[valors_socials < 99].dropna()

# HARMONITZAR LES DADES

G_map = {1: 0, 2: 1} # 1: Dona, 2: Home
valors_socials['G'] = valors_socials['G'].map(lambda x: G_map.get(x))

valors_socials['DA'] = valors_socials['DA'].map(lambda x: x-1)

'''
Ciutat Vella: 1
Eixample: 2
Sants-Montjuïc: 3
Les Corts: 4
Sarrià-Sant Gervasi: 5 
Gràcia: 6
Horta-Guinardó: 7  
Nou Barris: 8 
Sant Andreu: 9 
Sant Martí: 10
'''
valors_socials['D'] = valors_socials['D'].map(lambda x: x-1)

'''
1. No ha acabat els estudis obligatoris
2. Obligatoris (primària, EGB, ESO)
3. Secundaris generals (batxillerat, PREU, BUP, COU)
4. Secundaris professionals (comerç, FP1, FP2, mòduls grau mitjà/superior)
5. Universitaris (graus, diplomatura, llicenciatura)
6. Post universitaris (màster, postgrau, doctorat que requereixin titulació universitària)
'''
valors_socials['E'] = valors_socials['E'].map(lambda x: 5 if x==6 else x)
valors_socials['E'] = valors_socials['E'].map(lambda x: x-1)

''' 'DA' is ok
1. De 15 a 24 anys  
2. De 25 a 34 anys  
3. De 35 a 44 anys  
4. De 45 a 54 anys  
5. De 55 a 64 anys  
6. De 65 a 74 anys
'''

N_map = {1: 0, 2: 1, 3: 1}
''' Variable no es diu igual!
1. Espanyola
2. Resta
3. Resta
'''
valors_socials['N'] = valors_socials['N'].map(lambda x: N_map.get(x))

'''
1. Treballa per compte propi (com autònom/a o amb contractació de personal)
2. Treballa per compte propi, però actualment amb aturada d'activitat
3. Treballa per compte d'altri (com assalariat/ada) 
4. Treballa per compte d'altri actualment afectat/da per un ERO amb reducció o ERTO
5. Cobra jubilació, prejubilació o pensió o incapacitació laboral
6. Està a l'atur (inclou ERO total) / Busca feina
7. Tasques de la llar (no remunerades)
8. Estudia
9. Rendista
'''
valors_socials['U'] = valors_socials['U'].map(lambda x: 0 if x==6 else 1)

S_map = {1: 2, 2: 0, 3: 1, 4: 1}
'''
1. Solter/a
2. Casat/ada / amb parella (amb la que conviu)
3. Separat/ada / divorciat/ada
4. Vidu / vídua

ha de ser 0: married, 1: divorced/vidu, 2: single
'''
valors_socials['S'] = valors_socials['S'].map(lambda x: S_map.get(x))

''' 'HR' ESTÀ OK
1. Viu sol
2. Viu amb 1 persona
3. Viu amb 2 persones
4. Viu amb 3+ persones
'''

Ch_map = {2: 0, 1: 1} # 1: té fills, 2: no té fills
valors_socials['Ch'] = valors_socials['Ch'].map(lambda x: Ch_map.get(x))
valors_socials['D'] = valors_socials['D'].apply(lambda x: x + 1)

# Assuming clusterHSP and clusterSSP are already loaded as DataFrames
# clusterHSP = pd.read_csv('path_to_clusterHSP.csv')
# clusterSSP = pd.read_csv('path_to_clusterSSP.csv')

def discretize_inglehart(x):
    if x == '3' or x == '1':
        return 1  # materialistes
    elif x == '4' or x == '2':
        return 2  # post materialistes
    else:
        return None
datasets = [valors_socials]
for dataset in datasets:
    dataset['Inglehart1'] = dataset['Inglehart1'].astype(str).apply(discretize_inglehart)
    dataset['Inglehart2'] = dataset['Inglehart2'].astype(float).astype(int).astype(str).apply(discretize_inglehart)
    #     # Calculate the Inglehart_index
    dataset['Inglehart_index'] = dataset['Inglehart1'] * 2 + dataset['Inglehart2']
    #dataset.drop(columns=['Inglehart1', 'Inglehart2'], inplace=True)

# IPUMS
ipums = pd.read_csv('data/household/ipums.csv')
columns_to_keep = ['SEX', 'AGE', 'NATION',
                   'NCHILD', 'PERSONS', 'EMARST',
                   'EEMPSTAT', 'EDUCES']

ipums = ipums.loc[:, columns_to_keep]
new_column_names = {'SEX': 'G', 'AGE': 'DA', 'NATION': 'N',
                    'NCHILD': 'Ch', 'EMARST': 'S',
                    'EEMPSTAT': 'U', 'EDUCES': 'E', 'PERSONS': 'HR'}
ipums.rename(columns=new_column_names, inplace=True)
ipums.dropna(inplace=True) # de 200.000 a 120.000
#############
# HARMONITZAR LES DADES
#############
G_map = {1: 1, 2: 0} # 1: Male, 2: Female
ipums['G'] = ipums['G'].map(lambda x: G_map.get(x))

def discretize_age(x):
    # age already satisfies 15>=x<=74
    if x < 25:
        return 1
    elif x < 35:
        return 2
    elif x < 45:
        return 3
    elif x < 55:
        return 4
    elif x < 65:
        return 5
    else:
        return 6

ipums['DA'] = ipums['DA'].apply(discretize_age)

ipums['N'] = ipums['N'].map(lambda x: 0 if x==43120 else 1)

ipums['Ch'] = ipums['Ch'].map(lambda x: 0 if x==0 else 1)

S_map = {1: 2, 2: 0, 3: 1, 4: 1, 5: 1}
ipums['S'] = ipums['S'].map(lambda x: S_map.get(x))

ipums['U'] = ipums['U'].map(lambda x: 0 if (x==120 or x==121) else 1)

def discretize_edu(x):
    # age already satisfies 15>=x<=74
    if x < 300:
        return 1
    elif x < 320:
        return 2
    elif x < 410:
        return 3
    elif x < 431:
        return 4
    else:
        return 5

ipums['E'] = ipums['E'].apply(discretize_edu)
ipums['HR'] = ipums['HR'].map(lambda x: 4 if x>4 else x)
ipums['DA'] = ipums['DA'].map(lambda x: x-1)
ipums['E'] = ipums['E'].map(lambda x: x-1)
#treure potser ipums.drop(columns= ['S'], inplace = True)

#PANEL
panelind = pd.read_csv('data/household/Matrius_K/K_INDI.csv',delimiter=';')
columns_to_keep_ind = ['KL012001EG2', 'L005001E', 'L007001E', 'KE001001EG3', 'KT002001EH1R3', 
                   'KL006001E', 'KF031001ER1', 'KR185001E', 'KR167001E', 'KR173001E', 'KR170001E','KR176001E', 'KR107001E',
                   'KR168001E', 'KR174001E', 'KR171001E', 'KR075001E', 'KR110001E',
                   'KR169001E', 'KR175001E', 'KR178001E', 'KR078001E', 'KR113001E',
                   'KP017001LG2']
panelind = panelind.loc[:, columns_to_keep_ind]
# rename columns
new_column_names = {'KL012001EG2': 'DA', 'L005001E': 'G', 'L007001E': 'N', 'KT002001EH1R3': 'U', 'KE001001EG3': 'E',
                    'KL006001E': 'S', 'KF031001ER1': 'Ch',
                    'KR185001E': 'Nam', 'KR167001E': 'Gam1', 'KR173001E': 'DAam1', 'KR170001E': 'Nam1', 'KR176001E': 'Uam1', 'KR107001E': 'Eam1',
                    'KR168001E': 'Gam2', 'KR174001E': 'DAam2', 'KR171001E': 'Nam2', 'KR075001E': 'Uam2', 'KR110001E': 'Eam2',
                    'KR169001E': 'Gam3', 'KR175001E': 'DAam3', 'KR178001E': 'Nam3', 'KR078001E': 'Uam3', 'KR113001E': 'Eam3',
                    'KP017001LG2': 'household_id'
                    }
panelind.rename(columns=new_column_names, inplace=True)

panelind = panelind[panelind['DA'] >= 15] # keep only people over 15
panelind = panelind.loc[(panelind >= 0).all(axis=1)] # negative values represent unanswered questions

panelllar = pd.read_csv('data/household/Matrius_K/K_LLAR.csv',delimiter=';') 
columns_to_keep_llar = ['P017001LG2', 'KL001001LR1', 'KL018001LR1']
panelllar = panelllar.loc[:, columns_to_keep_llar]
# rename columns
new_column_names = {'P017001LG2': 'household_id', 'KL001001LR1': 'HR', 'KL018001LR1': 'Tip'}
panelllar.rename(columns=new_column_names, inplace=True)

# merge them by household id, which is P017001L
merged_panel = pd.merge(panelind, panelllar, on='household_id', how='inner')

merged_panel.drop('household_id', axis=1, inplace=True) # once merged, we don't want household_id in the model
merged_panel.dropna(inplace=True)

# HARMONITZAR LES DADES

G_map = {1: 1, 2: 0}
merged_panel['G'] = merged_panel['G'].map(lambda x: G_map.get(x))

E_map = {1: 1, 2: 1, 3: 1, 4: 1,
         3: 2, 9: 2, 10: 2, 
         7: 3, 8: 3, 11: 3, 13: 3,
         5: 4, 6: 4, 8: 4, 9: 4,
         12: 5, 14: 5, 15: 5, 16: 5}
merged_panel['E'] = merged_panel['E'].map(lambda x: E_map.get(x))
merged_panel['E'] = merged_panel['E'].map(lambda x: x-1)
def discretize_age(x):
    # age already satisfies 15>=x<=74
    if x < 25:
        return 1
    elif x < 35:
        return 2
    elif x < 45:
        return 3
    elif x < 55:
        return 4
    elif x < 65:
        return 5
    else:
        return 6

merged_panel['DA'] = merged_panel['DA'].apply(discretize_age)
merged_panel['DA'] = merged_panel['DA'].map(lambda x: x-1)

N_map = {1: 0, 2: 0, 3: 1}
'''
ha de ser 0: Espanyola, 1: Resta
'''
merged_panel['N'] = merged_panel['N'].map(lambda x: N_map.get(x))

U_map = {1: 1, 2: 0, 3: 1}
'''
ha de ser 0: atur, 1: ocupat
'''
merged_panel['U'] = merged_panel['U'].map(lambda x: U_map.get(x))

S_map = {1: 0, 2: 2, 3: 1, 4: 1, 5: 1}
'''
ha de ser 0: married, 1: divorced/vidu, 2: single
'''
merged_panel['S'] = merged_panel['S'].map(lambda x: S_map.get(x))

merged_panel['Ch'] = merged_panel['Ch'].map(lambda x: 0 if x==0 else 1)

merged_panel['HR'] = merged_panel['HR'].map(lambda x: 4 if x>4 else x)

# VALORS SOCIALS CAT

import pandas as pd
import numpy as np

valors_socials_cat = pd.read_csv('data/values/collective_values.csv', encoding='windows-1252', delimiter=';')

# variables socio-demogràfiques i laborals
# eliminat: 'DISTRICTE'
columns_to_keep = ['MUNICIPI', 'COMARCA', 'PROVINCIA','SEXE', 'EDAT', 'CIUTADANIA', 'ESTUDIS_1_6', 'ESTAT_CIVIL_2',
                   'CLASSE_SOCIAL_SUBJECTIVA_1_7', 'SIT_LAB', 'FILLS', 'PERSONES_LLAR']

# Inglehart’s
columns_to_keep.extend(['POSTMAT_1A', 'POSTMAT_1B','POSTMAT_2A','POSTMAT_2B'])

# Schwartz’s
columns_to_keep.extend(['VHB_A_AUTODIRECCIO1', 'VHB_B_PODER1','VHB_C_UNIVERSALISME1',
                        'VHB_D_ASSOLIMENT1', 'VHB_E_SEGURETAT1', 'VHB_F_ESTIMULANT1',
                        'VHB_G_CONFORMITAT1', 'VHB_H_UNIVERSALISME2',
                        'VHB_I_TRADICIO1', 'VHB_J_HEDONISME1','VHB_K_AUTODIRECCIO2',
                        'VHB_L_BENEVOLENCIA1', 'VHB_M_ASSOLIMENT2', 'VHB_N_SEGURETAT2',
                        'VHB_O_ESTIMULANT2', 'VHB_P_CONFORMITAT3','VHB_Q_PODER2',
                        'VHB_R_BENEVOLENCIA2', 'VHB_S_UNIVERSALISME3', 'VHB_T_TRADICIO2', 'VHB_U_HEDONISME2'])

# Altres columnes que m'han semblat interessants
columns_to_keep.extend(['LLOC_NAIX', 'LLENGUA_IDENTIFICACIO','IMP_FAMILIA','IMP_AMICS',
                        'IMP_LLEURE', 'IMP_POLITICA','IMP_TREBALL','IMP_RELIGIO','SATIS_VIDA',
                        'CONFI_SOCIAL_WVS_1', 'SALUT','FELICITAT','ACTITUD_ECONOMIA','ACTITUD_IMMIGRACIO',
                        'ACTITUD_MEDIAMBIENT', 'DESIGUALTATS_GENERE','ECON_MERITOCRACIA','MEDIAMBIENT_CREIXEMENT',
                        'IMMIGRACIO_CULTURA', 'CONFI_POLICIA','CONFI_POLITICS','IDEOL_0_10','PERSONA_RELIGIOSA',
                        'DEPENDENCIA_ECO_PARES', 'INGRESSOS_1_15','INFO_POL_TV_FREQ','FREQ_CONSUM_INTERNET'])

valors_socials_cat = valors_socials_cat.loc[:, columns_to_keep]

# rename columns
new_column_names = {'DISTRICTE': 'D', 'SEXE': 'G', 'EDAT': 'DA', 'CIUTADANIA': 'N', 'ESTUDIS_1_6': 'E',
                    'ESTAT_CIVIL_2': 'S', 'CLASSE_SOCIAL_SUBJECTIVA_1_7': 'C', 'SIT_LAB': 'U','FILLS': 'Ch',
                    'PERSONES_LLAR': 'HR'}
valors_socials_cat.rename(columns=new_column_names, inplace=True)

# Neteja dades
values_to_remove = ['Valor perdut per error tècnic', 'Valor perdut per omissió de resposta', "Valor perdut per mode d'administració de l'enquesta"]
valors_socials_cat.replace(values_to_remove, np.nan, inplace=True)
valors_socials_cat.dropna(inplace=True)
print('Rows after cleaning: ', valors_socials_cat.shape[0])

def discretize_age(x):
    x = int(x)
    if x < 25:
        return 1
    elif x < 35:
        return 2
    elif x < 45:
        return 3
    elif x < 55:
        return 4
    elif x < 65:
        return 5
    else:
        return 6
valors_socials_cat['DA'] = valors_socials_cat['DA'].apply(discretize_age)

def discretize_llar(x):
    x = int(x)
    if x < 2:
        return 1
    elif x == 2:
        return 2
    else:
        return 3

valors_socials_cat['HR'] = valors_socials_cat['HR'].apply(discretize_llar)

def discretize_fills(x):
    x = int(x)
    if x == 0:
        return 1
    else:
        return 2

valors_socials_cat['Ch'] = valors_socials_cat['Ch'].apply(discretize_fills)

def discretize_inglehart_1(x):
    if x == 'Combatre la pujada dels preus' or x == 'Mantenir l’ordre en el país':
        return 1 # materialistes
    elif x == 'Protegir la llibertat d’expressió' or x == 'Augmentar la participació dels ciutadans en les decisions importants del govern':
        return 2 # post materialistes
    else:
        return None
    
def discretize_inglehart_2(x):
    if x == 'Una economia estable' or x == 'La lluita contra la delinqüència':
        return 1 # materialistes
    elif x == 'Avançar cap a una societat menys impersonal i més humana' or x == 'Avançar cap a una societat on les idees siguin més important que els diners':
        return 2 # post materialistes
    else:
        return None

valors_socials_cat['POSTMAT_1A'] = valors_socials_cat['POSTMAT_1A'].apply(discretize_inglehart_1)
valors_socials_cat['POSTMAT_1B'] = valors_socials_cat['POSTMAT_1B'].apply(discretize_inglehart_1)
valors_socials_cat['POSTMAT_2A'] = valors_socials_cat['POSTMAT_2A'].apply(discretize_inglehart_2)
valors_socials_cat['POSTMAT_2B'] = valors_socials_cat['POSTMAT_2B'].apply(discretize_inglehart_2)

# Encode values into a single variable
valors_socials_cat['Inglehart_index'] = (
    (valors_socials_cat['POSTMAT_1A'] - 1)*2 + # give more importance to the first selection
    (valors_socials_cat['POSTMAT_1B'] - 1) +
    (valors_socials_cat['POSTMAT_2A'] - 1)*2 +
    (valors_socials_cat['POSTMAT_2B'] - 1)
) # 0 -> full materialist, 6 -> full post-materialist

valors_socials_cat.drop(columns=['POSTMAT_1A', 'POSTMAT_1B', 'POSTMAT_2A', 'POSTMAT_2B'], inplace=True)

def discretize_ideo(x):
    x = int(x[0:2])
    if x < 4:
        return 1 # esquerra
    elif x < 7:
        return 2 # centre
    else:
        return 3 #dretes

valors_socials_cat['IDEOL_0_10'] = valors_socials_cat['IDEOL_0_10'].apply(discretize_ideo)

def discretize_des_gen(x):
    x = int(x[0:2])
    if x < 4:
        return 1 # perjudici homes
    elif x < 7:
        return 2 # centre
    else:
        return 3 # perjudici dones

valors_socials_cat['DESIGUALTATS_GENERE'] = valors_socials_cat['DESIGUALTATS_GENERE'].apply(discretize_des_gen)

def discretize_medi(x):
    if x == 'D’acord' or x=='Molt d’acord':
        return 1 # prioritat economia
    elif x == 'Ni d’acord ni en desacord':
        return 2 # centre
    elif x == 'En desacord' or x=='Molt en desacord':
        return 3 # prioritat medi ambient

valors_socials_cat['ACTITUD_MEDIAMBIENT'] = valors_socials_cat['ACTITUD_MEDIAMBIENT'].apply(discretize_medi)

def discretize_immi(x):
    if x == 'D’acord' or x=='Molt d’acord':
        return 1 # immigració dolenta
    elif x == 'Ni d’acord ni en desacord':
        return 2 # centre
    elif x == 'En desacord' or x=='Molt en desacord':
        return 3

valors_socials_cat['ACTITUD_IMMIGRACIO'] = valors_socials_cat['ACTITUD_IMMIGRACIO'].apply(discretize_immi)

def discretize_poli(x):
    x = int(x[0:2])
    if x < 4:
        return 1 # no confia
    elif x < 7:
        return 2 # centre
    else:
        return 3 # confia

valors_socials_cat['CONFI_POLICIA'] = valors_socials_cat['CONFI_POLICIA'].apply(discretize_poli)


def discretize_VHB(x):
    if x == 'No s’assembla a mi' or x=='No s’assembla gens a mi':
        return 1
    elif x == 'S’assembla poc a mi' or x=='S’assembla una mica a mi':
        return 2
    elif x == 'S’assembla a mi' or x=='S’assembla molt a mi':
        return 3

valors_socials_cat['VHB_A_AUTODIRECCIO1'] = valors_socials_cat['VHB_A_AUTODIRECCIO1'].apply(discretize_VHB)
valors_socials_cat['VHB_B_PODER1'] = valors_socials_cat['VHB_B_PODER1'].apply(discretize_VHB)
valors_socials_cat['VHB_C_UNIVERSALISME1'] = valors_socials_cat['VHB_C_UNIVERSALISME1'].apply(discretize_VHB)
valors_socials_cat['VHB_D_ASSOLIMENT1'] = valors_socials_cat['VHB_D_ASSOLIMENT1'].apply(discretize_VHB)
valors_socials_cat['VHB_E_SEGURETAT1'] = valors_socials_cat['VHB_E_SEGURETAT1'].apply(discretize_VHB)
valors_socials_cat['VHB_F_ESTIMULANT1'] = valors_socials_cat['VHB_F_ESTIMULANT1'].apply(discretize_VHB)
valors_socials_cat['VHB_G_CONFORMITAT1'] = valors_socials_cat['VHB_G_CONFORMITAT1'].apply(discretize_VHB)
valors_socials_cat['VHB_H_UNIVERSALISME2'] = valors_socials_cat['VHB_H_UNIVERSALISME2'].apply(discretize_VHB)
valors_socials_cat['VHB_I_TRADICIO1'] = valors_socials_cat['VHB_I_TRADICIO1'].apply(discretize_VHB)
valors_socials_cat['VHB_J_HEDONISME1'] = valors_socials_cat['VHB_J_HEDONISME1'].apply(discretize_VHB)
valors_socials_cat['VHB_K_AUTODIRECCIO2'] = valors_socials_cat['VHB_K_AUTODIRECCIO2'].apply(discretize_VHB)
valors_socials_cat['VHB_L_BENEVOLENCIA1'] = valors_socials_cat['VHB_L_BENEVOLENCIA1'].apply(discretize_VHB)
valors_socials_cat['VHB_M_ASSOLIMENT2'] = valors_socials_cat['VHB_M_ASSOLIMENT2'].apply(discretize_VHB)
valors_socials_cat['VHB_N_SEGURETAT2'] = valors_socials_cat['VHB_N_SEGURETAT2'].apply(discretize_VHB)
valors_socials_cat['VHB_O_ESTIMULANT2'] = valors_socials_cat['VHB_O_ESTIMULANT2'].apply(discretize_VHB)
valors_socials_cat['VHB_P_CONFORMITAT3'] = valors_socials_cat['VHB_P_CONFORMITAT3'].apply(discretize_VHB)
valors_socials_cat['VHB_Q_PODER2'] = valors_socials_cat['VHB_Q_PODER2'].apply(discretize_VHB)
valors_socials_cat['VHB_R_BENEVOLENCIA2'] = valors_socials_cat['VHB_R_BENEVOLENCIA2'].apply(discretize_VHB)
valors_socials_cat['VHB_S_UNIVERSALISME3'] = valors_socials_cat['VHB_S_UNIVERSALISME3'].apply(discretize_VHB)
valors_socials_cat['VHB_T_TRADICIO2'] = valors_socials_cat['VHB_T_TRADICIO2'].apply(discretize_VHB)
valors_socials_cat['VHB_U_HEDONISME2'] = valors_socials_cat['VHB_U_HEDONISME2'].apply(discretize_VHB)

# Encode values into a single variable
valors_socials_cat['Universalism'] = ((valors_socials_cat['VHB_C_UNIVERSALISME1'] - 1) +
                                     (valors_socials_cat['VHB_H_UNIVERSALISME2'] - 1) +
                                     (valors_socials_cat['VHB_S_UNIVERSALISME3'] - 1))

valors_socials_cat['Stimulation'] = ((valors_socials_cat['VHB_F_ESTIMULANT1'] - 1) +
                                     (valors_socials_cat['VHB_O_ESTIMULANT2'] - 1))

valors_socials_cat['Hedonism'] = ((valors_socials_cat['VHB_J_HEDONISME1'] - 1) +
                                     (valors_socials_cat['VHB_U_HEDONISME2'] - 1))

valors_socials_cat['Self-Direction'] = ((valors_socials_cat['VHB_A_AUTODIRECCIO1'] - 1) +
                                     (valors_socials_cat['VHB_K_AUTODIRECCIO2'] - 1))

valors_socials_cat['Achievement'] = ((valors_socials_cat['VHB_D_ASSOLIMENT1'] - 1) +
                                     (valors_socials_cat['VHB_M_ASSOLIMENT2'] - 1))

valors_socials_cat['Power'] = ((valors_socials_cat['VHB_B_PODER1'] - 1) +
                                     (valors_socials_cat['VHB_Q_PODER2'] - 1))

valors_socials_cat['Security'] = ((valors_socials_cat['VHB_E_SEGURETAT1'] - 1) +
                                     (valors_socials_cat['VHB_N_SEGURETAT2'] - 1))

valors_socials_cat['Conformity'] = ((valors_socials_cat['VHB_F_ESTIMULANT1'] - 1) +
                                     (valors_socials_cat['VHB_O_ESTIMULANT2'] - 1))

valors_socials_cat['Tradition'] = ((valors_socials_cat['VHB_I_TRADICIO1'] - 1) +
                                     (valors_socials_cat['VHB_T_TRADICIO2'] - 1))

valors_socials_cat['Benevolence'] = ((valors_socials_cat['VHB_L_BENEVOLENCIA1'] - 1) +
                                     (valors_socials_cat['VHB_R_BENEVOLENCIA2'] - 1))


valors_socials_cat.drop(columns=['VHB_A_AUTODIRECCIO1', 'VHB_B_PODER1','VHB_C_UNIVERSALISME1',
                                'VHB_D_ASSOLIMENT1', 'VHB_E_SEGURETAT1', 'VHB_F_ESTIMULANT1',
                                'VHB_G_CONFORMITAT1', 'VHB_H_UNIVERSALISME2',
                                'VHB_I_TRADICIO1', 'VHB_J_HEDONISME1','VHB_K_AUTODIRECCIO2',
                                'VHB_L_BENEVOLENCIA1', 'VHB_M_ASSOLIMENT2', 'VHB_N_SEGURETAT2',
                                'VHB_O_ESTIMULANT2', 'VHB_P_CONFORMITAT3','VHB_Q_PODER2',
                                'VHB_R_BENEVOLENCIA2', 'VHB_S_UNIVERSALISME3', 'VHB_T_TRADICIO2', 'VHB_U_HEDONISME2'], inplace=True)

valors_socials['D'] = valors_socials['D'].map(lambda x: x-1)
#print(valors_socials['Inglehart_index'].value_counts())
valors_socials.to_csv('valors_socials.csv', index=False)
# ipums.to_csv('ipums.csv', index=False)
# merged_panel.to_csv('merged_panel.csv', index=False)

