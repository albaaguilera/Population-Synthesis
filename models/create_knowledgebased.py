from pgmpy.models import BayesianNetwork
from pgmpy.sampling import BayesianModelSampling
from pgmpy.estimators import ExpectationMaximization
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.data_treated_opt import ipums, merged_panel, social_values
from general_model import cpd_D, cpd_G, cpd_N, cpd_E, cpd_DA, cpd_U, cpd_I, cpd_Rent
from auxiliar_tools import extract_subset_CPDs

# DEFINIR EDGES I NODES of each model

parent_nodes = ['D', 'G', 'N', 'E', 'DA', 'U'] 
household_nodes = ['Ch', 'HR', 'S']
motiv_nodes = ['C', 'IF', 'IA', 'IT',
       'Ipol', 'Iemp', 'Irel', 'Iecon', 'IE', 'Ides', 'Sat', 'SF', 'SA', 'ST',
       'Semp', 'Secon', 'SE', 'Sdes', 'Ideo', 'Ipare', 'Imare', 'IP', 'Rel',
       'InterPolitica', 'Cap', 'Soc', 'Com', 'Indep', 'Femin', 'Ecolog',
       'Multiculturalism', 'JustOkupa', 'EconVsMedi', 'Immig', 'ConfMon',
       'ConfPol', 'ConfGov', 'Inglehart1', 'Inglehart2'] 
network_nodes = ['Nam', 'Gam1', 'DAam1', 'Uam1', 'Eam1', 'Nam1', 'Gam2', 'DAam2', 'Nam2', 'Uam2', 'Eam2', 'Gam3', 'DAam3', 'Nam3', 'Uam3', 'Eam3']
adit_hh_nodes = ['Tip']

ipums_nodes = ['G', 'DA','N', 'Ch', 'HR', 'U', 'E', 'S']
edges_demo_hh = [('G', 'S'), ('E', 'S'), ('DA', 'S'), ('G', 'Ch'), ('G', 'HR'), ('DA', 'Ch'), ('DA', 'HR'), ('E', 'Ch'), ('E', 'HR'), ('N', 'Ch'), ('N', 'HR')]

panel_nodes = network_nodes + adit_hh_nodes
edges_demo_net = [('Ch', 'Tip'), ('HR', 'Tip'), ('G', 'Tip'), ('N', 'Nam1'), ('N', 'Nam2'), ('N', 'Nam3'), ('G', 'Gam1'), ('G', 'Gam2'), ('G', 'Gam3'), ('DA', 'DAam1'), ('DA', 'DAam2'), ('DA', 'DAam3'), ('E', 'Eam1'), ('E', 'Eam2'), ('E', 'Eam3')]

nodes = parent_nodes + motiv_nodes
edges_demo_motiv = [
    ('D', 'G'), 
    ('D', 'DA'),
    ('D', 'N'),
    ('D', 'E'), 
    ('G', 'N'),
    ('G', 'E'),
    ('D', 'U'),
    ('G', 'U')
]

for parent in parent_nodes + ['Ch', 'HR']:
    for child in motiv_nodes:
        edges_demo_motiv.append((parent, child))

# CREAR BN H for Combined datasets
K_ipums = BayesianNetwork()  # Define structure & estimate CPDs using ipums dataset
K_panel = BayesianNetwork()  # Define structure & estimate CPDs using merged_panel dataset
K_social = BayesianNetwork()  # Define structure & estimate CPDs using valors_socials dataset

K_ipums.add_nodes_from(ipums_nodes)
K_ipums.add_edges_from(edges_demo_hh)

K_panel.add_nodes_from(network_nodes + ['Tip'] + ipums_nodes)
K_panel.add_edges_from(edges_demo_net)

K_social.add_nodes_from(['D'] + motiv_nodes + ipums_nodes)
K_social.add_edges_from(edges_demo_motiv)

estimator = ExpectationMaximization(K_ipums, ipums)
cpds_collective = extract_subset_CPDs(estimator.get_parameters(), household_nodes)

estimator = ExpectationMaximization(K_panel, merged_panel)
cpds_networks = extract_subset_CPDs(estimator.get_parameters(), network_nodes + ['Tip'])

estimator = ExpectationMaximization(K_social, social_values)
cpds_motiv = extract_subset_CPDs(estimator.get_parameters(), motiv_nodes)

K = BayesianNetwork()

# Add nodes and edges from each sub-model to the main model
K.add_nodes_from(ipums_nodes + network_nodes + ['Tip'] + ['D'] + motiv_nodes + ['I', 'Rent'])
K.add_edges_from(edges_demo_hh + edges_demo_net + edges_demo_motiv + [('D', 'I'), ('D', 'Rent')])

# Add CPDs from each sub-model to the main model
for cpd in cpds_collective:
    K.add_cpds(cpd)

for cpd in cpds_networks:
    K.add_cpds(cpd)

for cpd in cpds_motiv:
    K.add_cpds(cpd)

K.add_cpds(cpd_D, cpd_G, cpd_N, cpd_E, cpd_DA, cpd_U, cpd_I, cpd_Rent)

from pgmpy.readwrite import BIFWriter

writer = BIFWriter(K)
writer.write_bif('models/knowledge_based.pgmx')
