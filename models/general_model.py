
import pandas as pd
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.data_treated_opt import age_district, nationality_gender, variables_district, age_district, gender_district, nived_gender, unemp_gender, political, NUM_INCOME_BINS, NUM_RENT_BINS, pdfs_income_normalized, pdfs_rent_normalized
from data.data_treated import nationality_gender, decage_district, gender_district, nived_gender, unemp_gender
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD

# GEOGRAPHICAL BN
G = BayesianNetwork()
# Define nodes and edges
nodes = ['D', 'G', 'A', 'N', 'E', 'P', 'H', 'U', 'I', 'Rent'] 
edges = [
    ('D', 'G'), 
    ('D', 'A'),
    ('D', 'N'),
    ('D', 'E'), 
    ('D', 'U'), 
    ('D', 'P'),
    ('D', 'I'),
    ('D', 'Rent'),
    ('D', 'H')
]
G.add_nodes_from(nodes)
G.add_edges_from(edges)
cpd_D = TabularCPD('D', 10, np.transpose([list(variables_district['Percentage_Total'])]))
cpd_G = TabularCPD('G', 2, 
                    [np.transpose(list(gender_district['Percentage'].loc[gender_district['G']==0])),
                     np.transpose(list(gender_district['Percentage'].loc[gender_district['G']==1]))],
                    evidence = ["D"], evidence_card= [10],
                    )

cpd_P = TabularCPD('P', 15, 
                    [np.transpose(list(political['Percentage'].loc[political['P']=='CUP-G'])),
                     np.transpose(list(political['Percentage'].loc[political['P']=='Cs'])),
                     np.transpose(list(political['Percentage'].loc[political['P']=='ECP-PEC'])),
                     np.transpose(list(political['Percentage'].loc[political['P']=='ERC'])),
                     np.transpose(list(political['Percentage'].loc[political['P']=='FNC'])),
                     np.transpose(list(political['Percentage'].loc[political['P']=='IZQP'])),
                     np.transpose(list(political['Percentage'].loc[political['P']=='JxCat'])),
                     np.transpose(list(political['Percentage'].loc[political['P']=='MPIC'])),
                     np.transpose(list(political['Percentage'].loc[political['P']=='PCTC'])),
                     np.transpose(list(political['Percentage'].loc[political['P']=='PDeCAT'])),
                     np.transpose(list(political['Percentage'].loc[political['P']=='PNC'])),
                     np.transpose(list(political['Percentage'].loc[political['P']=='PP'])),
                     np.transpose(list(political['Percentage'].loc[political['P']=='PSC'])),
                     np.transpose(list(political['Percentage'].loc[political['P']=='RECORTES CERO-GV-M'])),
                     np.transpose(list(political['Percentage'].loc[political['P']=='VOX']))],
                    evidence = ["D"], evidence_card= [10]
                    )
cpd_H = TabularCPD('H', 2, 
                    [list(variables_district['% Percentage_Homeless']),
                     [1 - x for x in variables_district['% Percentage_Homeless']]],
                    evidence = ["D"], evidence_card= [10]
                    )

cpd_I = TabularCPD('I', NUM_INCOME_BINS-1, pdfs_income_normalized, 
                        evidence=['D'], evidence_card=[10])

cpd_Rent = TabularCPD('Rent', NUM_RENT_BINS-1, pdfs_rent_normalized, 
                      evidence=['D'], evidence_card=[10])



# VERSION 4

cpd_D = TabularCPD('D', 10, np.transpose([list(variables_district['Percentage_Total'])]))

percentage_gender = [np.transpose(list(gender_district['Percentage'].loc[gender_district['G'] == gender])) for gender in range(2)]

cpd_G = TabularCPD('G', 2,
                   percentage_gender, 
                    evidence = ["D"], evidence_card= [10],
                    )

# decimal age
percentage_age_group = np.transpose([decage_district[decage_district['D'] == d]['Percentage'].tolist() for d in range(10)])

cpd_DA = TabularCPD('DA', 6, 
                    percentage_age_group,
                    evidence=['D'], evidence_card=[10])

cpd_N = TabularCPD('N', 2, 
                    [np.transpose(list(nationality_gender['Percentage'].loc[nationality_gender['N']=='0'])),
                    np.transpose(list(nationality_gender['Percentage'].loc[nationality_gender['N']=='1']))],
                     evidence = ["D", "G"], evidence_card= [10, 2]
                     )

cpd_E = TabularCPD('E', 5, 
                    [np.transpose(list(nived_gender['Percentage'].loc[nived_gender['E']==1])),
                     np.transpose(list(nived_gender['Percentage'].loc[nived_gender['E']==2])),
                     np.transpose(list(nived_gender['Percentage'].loc[nived_gender['E']==3])),
                     np.transpose(list(nived_gender['Percentage'].loc[nived_gender['E']==4])),
                     np.transpose(list(nived_gender['Percentage'].loc[nived_gender['E']==5]))],
                    evidence = ["D", "G"], evidence_card= [10, 2]
                    )
cpd_U = TabularCPD('U', 2, 
                    [np.transpose(list(unemp_gender['Percentage'].loc[unemp_gender['U']== 0])),
                     np.transpose(list(unemp_gender['Percentage'].loc[unemp_gender['U']== 1]))],
                    evidence = ["D", "G"], evidence_card= [10, 2]
                    )


cpds_HM = [cpd_D, cpd_DA, cpd_G, cpd_N, cpd_E, cpd_I, cpd_Rent, cpd_U]


#H.add_cpds(*cpds_H)