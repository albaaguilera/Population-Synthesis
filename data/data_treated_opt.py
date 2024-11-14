import pandas as pd
import numpy as np

TOTAL_POPULATION = 1660314
NATIONALITY_MAP = {1: '0', 2: '1', 3: '1'}
SEX_REPLACE = {1: 0, 2: 1}
AGE_BIN_EDGES = [15, 24, 34, 44, 54, 64, 74]
AGE_BIN_LABELS = ['0', '1', '2', '3', '4', '5']

# Utility Functions
def calculate_percentage(df, numerator, denominator, new_col_name):
    df[new_col_name] = df[numerator] / df[denominator]
    return df

def preprocess_district(df, pop_total=TOTAL_POPULATION):
    df = df.drop(0)
    df['Percentage_Total'] = df['Total'] / pop_total
    df['% Percentage_Homeless'] = df['Homeless'] / df['Total']
    return df

def preprocess_data(file_path, rename_dict, group_by_cols, percentage_col, sum_col_name="Valor"):
    df = pd.read_csv(file_path)
    df = df.rename(columns=rename_dict)
    df[sum_col_name] = pd.to_numeric(df[sum_col_name].replace({"..": 0}), errors="coerce")
    df = df.groupby(group_by_cols)[sum_col_name].sum().reset_index()
    df['Total_Sum'] = df.groupby(group_by_cols[:-1])[sum_col_name].transform('sum')
    df[percentage_col] = df[sum_col_name] / df['Total_Sum']
    df = df.dropna()  # Eliminate rows with NaN values
    return df.drop(columns=['Total_Sum'])

# Initialize and preprocess 'variables_district'
variables_district = pd.DataFrame({
    'District': ['BARCELONA', 'Ciutat Vella', 'L\'Eixample', 'Sants-Montjuïc', 'Les Corts', 'Sarrià-Sant Gervasi',
                 'Gràcia', 'Horta-Guinardó', 'Nou Barris', 'Sant Andreu', 'Sant Martí'],
    'Total': [1660314, 109672, 269349, 187026, 81576, 149201, 123276, 173944, 173552, 151537, 241181],
    'Female': [869379, 50387, 142773, 96990, 43714, 80653, 66538, 92183, 91887, 79471, 124783],
    'Male': [790935, 59285, 126576, 90036, 37862, 68548, 56738, 81761, 81665, 72066, 116398],
    'Homeless': [1231, 344, 297, 183, 43, 34, 32, 67, 54, 18, 159]
})
variables_district = preprocess_district(variables_district)

# Nationality/Gender Data Preprocessing
nationality_gender = preprocess_data(
    'data/nationality/2022_nationality_gender.csv',
    rename_dict={'Codi_Districte': 'D', 'NACIONALITAT_G': 'N', 'SEXE': 'G'},
    group_by_cols=['D', 'Nom_Districte', 'N', 'G'],
    percentage_col='Percentage'
)

nationality_gender['G'] = nationality_gender['G'].replace(SEX_REPLACE)
nationality_gender['D'] = nationality_gender['D'] - 1
nationality_gender['N'] = nationality_gender['N'].map(NATIONALITY_MAP)

# Gender/District Data Preprocessing
gender_district = preprocess_data(
    'data/gender/2022_pad_mdbas_gender.csv',
    rename_dict={'Codi_Districte': 'D', 'SEXE': 'G'},
    group_by_cols=['D', 'Nom_Districte', 'G'],
    percentage_col='Percentage'
)
gender_district['G'] = gender_district['G'].replace(SEX_REPLACE)
gender_district['D'] = gender_district['D'] - 1

# Age/District Data Preprocessing
age_district = preprocess_data(
    'data/age/2022_pad_mdbas_age.csv',
    rename_dict={'Codi_Districte': 'D', 'EDAT_1': 'A'},
    group_by_cols=['D', 'Nom_Districte', 'A'],
    percentage_col='Percentage'
)
age_district['D'] = age_district['D'] - 1
age_district = age_district[age_district['A'].between(15, 74)]
age_district['DA'] = pd.cut(age_district['A'], bins=AGE_BIN_EDGES, labels=AGE_BIN_LABELS, right=True).astype(str)
age_district = age_district[age_district['DA'] != 'None'].groupby(['D', 'DA']).agg({'Percentage': 'sum'}).reset_index()


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


# NIV_ED / GENDER AND DISTRICT
nived_gender = preprocess_data(
    'data/status/2022_niv-educa_gender.csv',
    rename_dict={'Codi_Districte': 'D', 'NIV_EDUCA_esta': 'E', 'SEXE': 'G'},
    group_by_cols=['D', 'Nom_Districte', 'E', 'G'],
    percentage_col='Percentage'
)
nived_gender['G'] = nived_gender['G'].replace(SEX_REPLACE)
nived_gender['D'] = nived_gender['D'] - 1
nived_gender = nived_gender[nived_gender['E'] != 6]  # Remove entries where education level (E) is 6, per original code

# POLITICAL INCLINATION / DISTRICT
political = pd.read_csv('data/political/A20211-Vots-DM.csv', sep = ';', usecols=['Nom Municipi', 'Districte', 'Sigles Candidatura', 'Vots'])
political = political.loc[political['Nom Municipi']== 'Barcelona']  #keep only barcelona and their districts
political.rename(columns ={'Districte': 'D', 'Sigles Candidatura': 'P'}, inplace =True)
political['Vots'].sum()   #617.013 persones amb vot registrat a barcelona

political = political.groupby(['D', 'P'])['Vots'].sum().reset_index()
political['Total_Sum'] = political.groupby(['D'])['Vots'].transform('sum')
political['Percentage'] = political['Vots'] / political['Total_Sum']
political.drop(columns=['Total_Sum'], inplace=True)
political['D'] = political['D'] - 1  # Adjust district codes by subtracting 1, as per the original code

# INCOME AND RENT / DISTRICT
from scipy.stats import gaussian_kde
NUM_DISTRICTS = 10
NUM_INCOME_BINS = 1000
NUM_RENT_BINS = 1000

income = pd.read_csv('data/salary/2021_income_ind.csv')
income.rename(columns={'Codi_Districte': 'D', 'Import_Renda_Bruta_€': 'I'}, inplace=True)
income['D'] -= 1  # Adjust district codes by subtracting 1
rent = pd.read_csv('data/rent/2023_lloguer_preu_trim.csv')
rent.rename(columns={'Codi_Districte': 'D', 'Preu': 'Rent'}, inplace=True)
rent['D'] -= 1
rent.dropna(inplace=True)  # Remove NA values

# KDE and PDF Calculation Functions
def calculate_district_pdf(data, column, bins, num_districts):
    """Calculate KDE PDFs for each district and normalize."""
    pdfs = np.zeros((len(bins) - 1, num_districts))  # Initialize PDF array

    for district in range(num_districts):
        district_data = data[data['D'] == district][column]
        if not district_data.empty:
            kde = gaussian_kde(district_data)
            pdfs[:, district] = kde.evaluate(bins[:-1])
    return pdfs / pdfs.sum(axis=0)

# INCOME: Discretization and KDE-based PDF Calculation
income_range = np.linspace(0, 47000, NUM_INCOME_BINS)
pdfs_income_normalized = calculate_district_pdf(income, 'I', income_range, NUM_DISTRICTS)

# RENT: Discretization and KDE-based PDF Calculation
rent_range = np.linspace(rent['Rent'].min(), rent['Rent'].max(), NUM_RENT_BINS)
pdfs_rent_normalized = calculate_district_pdf(rent, 'Rent', rent_range, NUM_DISTRICTS)

# MOTIVATIONAL DATA: ipums, panel, social_values and coll_social_values

import pandas as pd
import numpy as np

# Utility functions
def load_data(file_path, columns_to_keep, rename_dict, delimiter=',', encoding=None):
    """Load CSV file with specified columns and rename them."""
    df = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding)
    df = df[columns_to_keep].rename(columns=rename_dict)
    return df

def apply_mappings(df, mappings):
    """Apply multiple column mappings in a single function call."""
    for column, mapping in mappings.items():
        df[column] = df[column].map(mapping)
    return df

def discretize_column(df, column, bins, labels):
    """Discretize a column based on specified bins and labels."""
    df[column] = pd.cut(df[column], bins=bins, labels=labels).astype(float)
    return df

# Discretization functions
def discretize_age(x):
    if x < 25: return 1
    elif x < 35: return 2
    elif x < 45: return 3
    elif x < 55: return 4
    elif x < 65: return 5
    return 6

def discretize_generic(x, boundaries, labels):
    """Discretize based on custom boundaries and labels."""
    for i, bound in enumerate(boundaries):
        if x < bound:
            return labels[i]
    return labels[-1]

# Load `social_values`
columns_to_keep_vs = [
    'DISTRICTE', 'SEXE', 'EDAT1574_1A6', 'NACIO_ACT_UE', 'HAB_RES_1A4', 
    'TE_FILLS_1A2', 'SITPERSONAL_1A4', 'CLASSESOC_ENT_1A5', 'SITLABORAL_1A9', 'ESTUDIS_1A6',
    'IMP_PERS_FAM_1A4', 'IMP_PERS_AMIC_1A4', 'IMP_PERS_TEMPS_1A4', 'IMP_PERS_POLITICA_1A4', 
    'IMP_PERS_FEINA_1A4', 'IMP_PERS_RELIGIO_1A4', 'IMP_PERS_ECON_1A4', 'IMP_PERS_ESTUDIAR_1A4',
    'IMP_PERS_DESENV_1A4', 'SATISF_PERS_1A10', 'SATISF_PERS_FAM_1A10', 'SATISF_PERS_AMIC_1A10', 
    'SATISF_PERS_TEMPS_1A10', 'SATISF_PERS_FEINA_1A10', 'SATISF_PERS_ECON_1A10', 'SATISF_PERS_ESTUDIAR_1A10', 
    'SATISF_PERS_DESENV_1A10', 'IDEO_1A8', 'IDEO_PARE_1A8', 'IDEO_MARE_1A8', 'IDEO_PARTIT', 
    'INTERES_POLITICA_1A4', 'ACORD_SOCIETAT_CONCEPT_Q01_1A3', 'ACORD_SOCIETAT_CONCEPT_Q02_1A3', 
    'ACORD_SOCIETAT_CONCEPT_Q03_1A3', 'SENTPERTI_1A5', 'RELIGIO', 'ACORD_SOCIETAT_CONCEPT_Q05_1A3', 
    'ACORD_SOCIETAT_CONCEPT_Q06_1A3', 'ACORD_SOCIETAT_CONCEPT_Q09_1A3', 'ACORD_SOCIETAT_JUSTIFICAR_Q04_1A3', 
    'PRIO_ESTAT_POLITICA_MEDIAMB_1A2', 'IMPACTE_IMMIG_PAIS_1A10', 'CONFIA_INSTITUCIO_Q01_1A4', 
    'CONFIA_INSTITUCIO_Q11_1A4', 'CONFIA_INSTITUCIO_Q12_1A4', 'IMP01_ESTAT_1A4', 'IMP02_ESTAT_1A4'
]
rename_dict_vs = {
    'DISTRICTE': 'D', 'SEXE': 'G', 'EDAT1574_1A6': 'DA', 'NACIO_ACT_UE': 'N',
    'TE_FILLS_1A2': 'Ch', 'SITPERSONAL_1A4': 'S', 'CLASSESOC_ENT_1A5': 'C',
    'SITLABORAL_1A9': 'U', 'ESTUDIS_1A6': 'E', 'HAB_RES_1A4': 'HR',
    'IMP_PERS_FAM_1A4': 'IF', 'IMP_PERS_AMIC_1A4': 'IA', 'IMP_PERS_TEMPS_1A4': 'IT',
    'SATISF_PERS_1A10': 'Sat', 'SATISF_PERS_FAM_1A10': 'SF', 'SATISF_PERS_AMIC_1A10': 'SA',
    'SATISF_PERS_TEMPS_1A10': 'ST', 'IDEO_1A8': 'Ideo', 'IDEO_PARTIT': 'IP'
    # Continue renaming all needed columns here
}
social_values = load_data('data/values/2021_valors_socials.csv', columns_to_keep_vs, rename_dict_vs)
social_values = social_values[social_values < 99].dropna()  # Remove "no answer" rows

mappings_vs = {
    'G': {1: 0, 2: 1},
    'DA': lambda x: discretize_age(x) - 1,
    'D': lambda x: x - 1,
    'E': {6: 5},
    'N': {1: 0, 2: 1, 3: 1},
    'U': {6: 0},
    'S': {1: 2, 2: 0, 3: 1, 4: 1},
    'Ch': {2: 0, 1: 1}
}
social_values = apply_mappings(social_values, mappings_vs)

# Load and preprocess `ipums`
columns_to_keep_ipums = ['SEX', 'AGE', 'NATION', 'NCHILD', 'PERSONS', 'EMARST', 'EEMPSTAT', 'EDUCES']
rename_dict_ipums = {
    'SEX': 'G', 'AGE': 'DA', 'NATION': 'N', 'NCHILD': 'Ch', 'PERSONS': 'HR', 
    'EMARST': 'S', 'EEMPSTAT': 'U', 'EDUCES': 'E'
}
ipums = load_data('data/household/ipums.csv', columns_to_keep_ipums, rename_dict_ipums)
ipums = ipums.dropna()

mappings_ipums = {
    'G': {1: 1, 2: 0},
    'DA': lambda x: discretize_age(x) - 1,
    'N': {43120: 0},
    'Ch': lambda x: 0 if x == 0 else 1,
    'S': {1: 2, 2: 0, 3: 1, 4: 1, 5: 1},
    'U': {120: 0, 121: 0}
}
ipums = apply_mappings(ipums, mappings_ipums)
ipums['HR'] = ipums['HR'].map(lambda x: min(x, 4))

# Load and preprocess `merged_panel`
columns_to_keep_panel = [
    'KL012001EG2', 'L005001E', 'L007001E', 'KE001001EG3', 'KT002001EH1R3', 
    'KL006001E', 'KF031001ER1', 'KR185001E', 'KR167001E', 'KR173001E', 'KR170001E',
    'KR176001E', 'KR107001E', 'KR168001E', 'KR174001E', 'KR171001E', 'KR075001E', 
    'KR110001E', 'KR169001E', 'KR175001E', 'KR178001E', 'KR078001E', 'KR113001E', 
    'KP017001LG2'
]
rename_dict_panel = {
    'KL012001EG2': 'DA', 'L005001E': 'G', 'L007001E': 'N', 'KE001001EG3': 'E',
    'KL006001E': 'S', 'KF031001ER1': 'Ch', 'KP017001LG2': 'household_id'
}
panelind = load_data('data/household/Matrius_K/K_INDI.csv', columns_to_keep_panel, rename_dict_panel, delimiter=';')
panelind = panelind[panelind['DA'] >= 15].loc[(panelind >= 0).all(axis=1)]

panelllar = load_data('data/household/Matrius_K/K_LLAR.csv', ['P017001LG2', 'KL001001LR1', 'KL018001LR1'], {'P017001LG2': 'household_id', 'KL001001LR1': 'HR', 'KL018001LR1': 'Tip'}, delimiter=';')
merged_panel = pd.merge(panelind, panelllar, on='household_id', how='inner').dropna()

# COLLECTIVE VALUES
social_values_cat = pd.read_csv('data/values/collective_values.csv', encoding='windows-1252', delimiter=';')

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

social_values_cat = social_values_cat.loc[:, columns_to_keep]

# rename columns
new_column_names = {'DISTRICTE': 'D', 'SEXE': 'G', 'EDAT': 'DA', 'CIUTADANIA': 'N', 'ESTUDIS_1_6': 'E',
                    'ESTAT_CIVIL_2': 'S', 'CLASSE_SOCIAL_SUBJECTIVA_1_7': 'C', 'SIT_LAB': 'U','FILLS': 'Ch',
                    'PERSONES_LLAR': 'HR'}
social_values_cat.rename(columns=new_column_names, inplace=True)

# Neteja dades
values_to_remove = ['Valor perdut per error tècnic', 'Valor perdut per omissió de resposta', "Valor perdut per mode d'administració de l'enquesta"]
social_values_cat.replace(values_to_remove, np.nan, inplace=True)
social_values_cat.dropna(inplace=True)
print('Rows after cleaning: ', social_values_cat.shape[0])

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
social_values_cat['DA'] = social_values_cat['DA'].apply(discretize_age)

def discretize_llar(x):
    x = int(x)
    if x < 2:
        return 1
    elif x == 2:
        return 2
    else:
        return 3

social_values_cat['HR'] = social_values_cat['HR'].apply(discretize_llar)

def discretize_fills(x):
    x = int(x)
    if x == 0:
        return 1
    else:
        return 2

social_values_cat['Ch'] = social_values_cat['Ch'].apply(discretize_fills)

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

social_values_cat['POSTMAT_1A'] = social_values_cat['POSTMAT_1A'].apply(discretize_inglehart_1)
social_values_cat['POSTMAT_1B'] = social_values_cat['POSTMAT_1B'].apply(discretize_inglehart_1)
social_values_cat['POSTMAT_2A'] = social_values_cat['POSTMAT_2A'].apply(discretize_inglehart_2)
social_values_cat['POSTMAT_2B'] = social_values_cat['POSTMAT_2B'].apply(discretize_inglehart_2)

# Encode values into a single variable
social_values_cat['Inglehart_index'] = (
    (social_values_cat['POSTMAT_1A'] - 1)*2 + # give more importance to the first selection
    (social_values_cat['POSTMAT_1B'] - 1) +
    (social_values_cat['POSTMAT_2A'] - 1)*2 +
    (social_values_cat['POSTMAT_2B'] - 1)
) # 0 -> full materialist, 6 -> full post-materialist

social_values_cat.drop(columns=['POSTMAT_1A', 'POSTMAT_1B', 'POSTMAT_2A', 'POSTMAT_2B'], inplace=True)

def discretize_ideo(x):
    x = int(x[0:2])
    if x < 4:
        return 1 # esquerra
    elif x < 7:
        return 2 # centre
    else:
        return 3 #dretes

social_values_cat['IDEOL_0_10'] = social_values_cat['IDEOL_0_10'].apply(discretize_ideo)

def discretize_des_gen(x):
    x = int(x[0:2])
    if x < 4:
        return 1 # perjudici homes
    elif x < 7:
        return 2 # centre
    else:
        return 3 # perjudici dones

social_values_cat['DESIGUALTATS_GENERE'] = social_values_cat['DESIGUALTATS_GENERE'].apply(discretize_des_gen)

def discretize_medi(x):
    if x == 'D’acord' or x=='Molt d’acord':
        return 1 # prioritat economia
    elif x == 'Ni d’acord ni en desacord':
        return 2 # centre
    elif x == 'En desacord' or x=='Molt en desacord':
        return 3 # prioritat medi ambient

social_values_cat['ACTITUD_MEDIAMBIENT'] = social_values_cat['ACTITUD_MEDIAMBIENT'].apply(discretize_medi)

def discretize_immi(x):
    if x == 'D’acord' or x=='Molt d’acord':
        return 1 # immigració dolenta
    elif x == 'Ni d’acord ni en desacord':
        return 2 # centre
    elif x == 'En desacord' or x=='Molt en desacord':
        return 3

social_values_cat['ACTITUD_IMMIGRACIO'] = social_values_cat['ACTITUD_IMMIGRACIO'].apply(discretize_immi)

def discretize_poli(x):
    x = int(x[0:2])
    if x < 4:
        return 1 # no confia
    elif x < 7:
        return 2 # centre
    else:
        return 3 # confia

social_values_cat['CONFI_POLICIA'] = social_values_cat['CONFI_POLICIA'].apply(discretize_poli)


def discretize_VHB(x):
    if x == 'No s’assembla a mi' or x=='No s’assembla gens a mi':
        return 1
    elif x == 'S’assembla poc a mi' or x=='S’assembla una mica a mi':
        return 2
    elif x == 'S’assembla a mi' or x=='S’assembla molt a mi':
        return 3

social_values_cat['VHB_A_AUTODIRECCIO1'] = social_values_cat['VHB_A_AUTODIRECCIO1'].apply(discretize_VHB)
social_values_cat['VHB_B_PODER1'] = social_values_cat['VHB_B_PODER1'].apply(discretize_VHB)
social_values_cat['VHB_C_UNIVERSALISME1'] = social_values_cat['VHB_C_UNIVERSALISME1'].apply(discretize_VHB)
social_values_cat['VHB_D_ASSOLIMENT1'] = social_values_cat['VHB_D_ASSOLIMENT1'].apply(discretize_VHB)
social_values_cat['VHB_E_SEGURETAT1'] = social_values_cat['VHB_E_SEGURETAT1'].apply(discretize_VHB)
social_values_cat['VHB_F_ESTIMULANT1'] = social_values_cat['VHB_F_ESTIMULANT1'].apply(discretize_VHB)
social_values_cat['VHB_G_CONFORMITAT1'] = social_values_cat['VHB_G_CONFORMITAT1'].apply(discretize_VHB)
social_values_cat['VHB_H_UNIVERSALISME2'] = social_values_cat['VHB_H_UNIVERSALISME2'].apply(discretize_VHB)
social_values_cat['VHB_I_TRADICIO1'] = social_values_cat['VHB_I_TRADICIO1'].apply(discretize_VHB)
social_values_cat['VHB_J_HEDONISME1'] = social_values_cat['VHB_J_HEDONISME1'].apply(discretize_VHB)
social_values_cat['VHB_K_AUTODIRECCIO2'] = social_values_cat['VHB_K_AUTODIRECCIO2'].apply(discretize_VHB)
social_values_cat['VHB_L_BENEVOLENCIA1'] = social_values_cat['VHB_L_BENEVOLENCIA1'].apply(discretize_VHB)
social_values_cat['VHB_M_ASSOLIMENT2'] = social_values_cat['VHB_M_ASSOLIMENT2'].apply(discretize_VHB)
social_values_cat['VHB_N_SEGURETAT2'] = social_values_cat['VHB_N_SEGURETAT2'].apply(discretize_VHB)
social_values_cat['VHB_O_ESTIMULANT2'] = social_values_cat['VHB_O_ESTIMULANT2'].apply(discretize_VHB)
social_values_cat['VHB_P_CONFORMITAT3'] = social_values_cat['VHB_P_CONFORMITAT3'].apply(discretize_VHB)
social_values_cat['VHB_Q_PODER2'] = social_values_cat['VHB_Q_PODER2'].apply(discretize_VHB)
social_values_cat['VHB_R_BENEVOLENCIA2'] = social_values_cat['VHB_R_BENEVOLENCIA2'].apply(discretize_VHB)
social_values_cat['VHB_S_UNIVERSALISME3'] = social_values_cat['VHB_S_UNIVERSALISME3'].apply(discretize_VHB)
social_values_cat['VHB_T_TRADICIO2'] = social_values_cat['VHB_T_TRADICIO2'].apply(discretize_VHB)
social_values_cat['VHB_U_HEDONISME2'] = social_values_cat['VHB_U_HEDONISME2'].apply(discretize_VHB)

# Encode values into a single variable
social_values_cat['Universalism'] = ((social_values_cat['VHB_C_UNIVERSALISME1'] - 1) +
                                     (social_values_cat['VHB_H_UNIVERSALISME2'] - 1) +
                                     (social_values_cat['VHB_S_UNIVERSALISME3'] - 1))

social_values_cat['Stimulation'] = ((social_values_cat['VHB_F_ESTIMULANT1'] - 1) +
                                     (social_values_cat['VHB_O_ESTIMULANT2'] - 1))

social_values_cat['Hedonism'] = ((social_values_cat['VHB_J_HEDONISME1'] - 1) +
                                     (social_values_cat['VHB_U_HEDONISME2'] - 1))

social_values_cat['Self-Direction'] = ((social_values_cat['VHB_A_AUTODIRECCIO1'] - 1) +
                                     (social_values_cat['VHB_K_AUTODIRECCIO2'] - 1))

social_values_cat['Achievement'] = ((social_values_cat['VHB_D_ASSOLIMENT1'] - 1) +
                                     (social_values_cat['VHB_M_ASSOLIMENT2'] - 1))

social_values_cat['Power'] = ((social_values_cat['VHB_B_PODER1'] - 1) +
                                     (social_values_cat['VHB_Q_PODER2'] - 1))

social_values_cat['Security'] = ((social_values_cat['VHB_E_SEGURETAT1'] - 1) +
                                     (social_values_cat['VHB_N_SEGURETAT2'] - 1))

social_values_cat['Conformity'] = ((social_values_cat['VHB_F_ESTIMULANT1'] - 1) +
                                     (social_values_cat['VHB_O_ESTIMULANT2'] - 1))

social_values_cat['Tradition'] = ((social_values_cat['VHB_I_TRADICIO1'] - 1) +
                                     (social_values_cat['VHB_T_TRADICIO2'] - 1))

social_values_cat['Benevolence'] = ((social_values_cat['VHB_L_BENEVOLENCIA1'] - 1) +
                                     (social_values_cat['VHB_R_BENEVOLENCIA2'] - 1))


social_values_cat.drop(columns=['VHB_A_AUTODIRECCIO1', 'VHB_B_PODER1','VHB_C_UNIVERSALISME1',
                                'VHB_D_ASSOLIMENT1', 'VHB_E_SEGURETAT1', 'VHB_F_ESTIMULANT1',
                                'VHB_G_CONFORMITAT1', 'VHB_H_UNIVERSALISME2',
                                'VHB_I_TRADICIO1', 'VHB_J_HEDONISME1','VHB_K_AUTODIRECCIO2',
                                'VHB_L_BENEVOLENCIA1', 'VHB_M_ASSOLIMENT2', 'VHB_N_SEGURETAT2',
                                'VHB_O_ESTIMULANT2', 'VHB_P_CONFORMITAT3','VHB_Q_PODER2',
                                'VHB_R_BENEVOLENCIA2', 'VHB_S_UNIVERSALISME3', 'VHB_T_TRADICIO2', 'VHB_U_HEDONISME2'], inplace=True)

# Export final datasets
social_values.to_csv('data/social_values.csv', index=False)
ipums.to_csv('data/ipums.csv', index=False)
merged_panel.to_csv('data/merged_panel.csv', index=False)
social_values_cat.to_csv('data/social_values_cat.csv', index=False)
