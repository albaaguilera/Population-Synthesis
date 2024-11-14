# Value-Enriched Population-Synthesis
A framework that integrates a motivational layer with the traditional individual and household socio-demographic layers in synthetic populations. We extend the profile of agents by incorporating data on values, ideologies, opinions and vital priorities, which motivate the agents' behaviour. This motivational layer can help us develop a more nuanced decision-making mechanism for the agents in social simulation settings. Our methodology integrates microdata and macrodata within different Bayesian network structures: learnt, knowledge-based and hybrid.

## STRUCTURE
The github repository contains the following folders: 
1. **Data** input information we use to construct the BNs.
   - data_treated.py: cleans and harmonize the csv datasets.
3. **Models** construction of the BN structures (learnt, knowledge-based and hybrid)
   - create_knowledgebased.py
   - create_learnt.ipnyb
   - create_hybrid.py
5. **Results** synthetic samples generated in the cluster.
6. **Validation** functions to validate the synthetic populations (Wasserstein distances, regression lines and SRMSE).
