from pgmpy.models import BayesianNetwork
from pgmpy.sampling import BayesianModelSampling
from pgmpy.estimators import ExpectationMaximization
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.data_treated import ipums, merged_panel, valors_socials
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
       'ConfPol', 'ConfGov'] 
network_nodes = ['Nam', 'Gam1', 'DAam1', 'Uam1', 'Eam1', 'Nam1', 'Gam2', 'DAam2', 'Nam2', 'Uam2', 'Eam2', 'Gam3', 'DAam3', 'Nam3', 'Uam3', 'Eam3']
adit_hh_nodes = ['Tip']

ipums_nodes = ['G', 'DA','N', 'Ch', 'HR', 'U', 'E', 'S']
# Add useful dependencies found in model L for Hh variables (S, Hr and Ch)
# Remove dependencies to D, G, N, E, DA, U as their CPDs are already imported
edges_demo_hh = [('G', 'Ch'),
                 ('DA', 'S'),
                 ('DA', 'HR'),
                 ('DA', 'Ch'),
                 ('N', 'S'),
                 ('HR', 'Ch'),
                 ('HR', 'S'),
                 ('S', 'Ch'),
                 ('E', 'HR')]

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
# Add useful dependencies found in model L for Mot variables
# Remove dependencies to D, G, N, E, DA, U as their CPDs are already imported
edges_demo_motiv.extend([('G', 'Ch'),
                    ('DA', 'Ch'),
                    ('DA', 'HR'),
                    ('DA', 'S'),
                    ('N', 'S'),
                    ('N', 'Indep'),
                    ('N', 'Rel'),
                    ('HR', 'S'),
                    ('HR', 'Ch'), 
                    ('S', 'Ch'),
                    ('U', 'Semp'),
                    ('U', 'Secon'),
                    ('E', 'HR'),
                    ('IA', 'IT'),
                    ('IA', 'IF'),
                    ('Iemp', 'IE'),
                    ('Irel', 'ConfMon'),
                    ('IE', 'Ides'),
                    ('SA', 'IA'),
                    ('Sdes', 'Sat'),
                    ('Ideo', 'IP'),
                    ('Ideo', 'InterPolitica'),
                    ('Ideo', 'Soc'),
                    ('Imare', 'Ipare'),
                    ('Imare', 'Ideo'),
                    ('InterPolitica', 'Ipol'),
                    ('Soc', 'Com'),
                    ('Soc', 'Femin'),
                    ('Com', 'Cap'),
                    ('Rel', 'Irel'),
                    ('Femin', 'Ecolog'),
                    ('Femin', 'Multiculturalism'),
                    ('Ecolog', 'EconVsMedi'),
                    ('ConfMon', 'ConfPol'),
                    ('ConfPol', 'ConfGov'),
                    ('ConfPol', 'JustOkupa')])


# CREAR BN H for Combined datasets
H_ipums = BayesianNetwork()  # Define structure & estimate CPDs using ipums dataset
H_panel = BayesianNetwork()  # Define structure & estimate CPDs using merged_panel dataset
H_social = BayesianNetwork()  # Define structure & estimate CPDs using valors_socials dataset

H_ipums.add_nodes_from(ipums_nodes)
H_ipums.add_edges_from(edges_demo_hh)

H_panel.add_nodes_from(network_nodes + ['Tip'] + ipums_nodes)
H_panel.add_edges_from(edges_demo_net)

H_social.add_nodes_from(['D'] + motiv_nodes + ipums_nodes)
H_social.add_edges_from(edges_demo_motiv)

estimator = ExpectationMaximization(H_ipums, ipums)
cpds_collective = extract_subset_CPDs(estimator.get_parameters(), household_nodes)

estimator = ExpectationMaximization(H_panel, merged_panel)
cpds_networks = extract_subset_CPDs(estimator.get_parameters(), network_nodes + ['Tip'])

estimator = ExpectationMaximization(H_social, valors_socials)
cpds_motiv = extract_subset_CPDs(estimator.get_parameters() , motiv_nodes)

H = BayesianNetwork()

# Add nodes and edges from each sub-model to the main model
H.add_nodes_from(ipums_nodes + network_nodes + ['Tip'] + ['D'] + motiv_nodes + ['I', 'Rent'])
H.add_edges_from(edges_demo_hh + edges_demo_net + edges_demo_motiv + [('D', 'I'), ('D', 'Rent')])

# Add CPDs from each sub-model to the main model
for cpd in cpds_collective:
    H.add_cpds(cpd)

for cpd in cpds_networks:
    H.add_cpds(cpd)

for cpd in cpds_motiv:
    H.add_cpds(cpd)

H.add_cpds(cpd_D, cpd_G, cpd_N, cpd_E, cpd_DA, cpd_U, cpd_I, cpd_Rent)

inference = BayesianModelSampling(H)
sample = inference.forward_sample(size=10)

from pgmpy.readwrite import BIFWriter

writer = BIFWriter(H)
writer.write_bif('models/hybrid_model.pgmx')
