# Value-Enriched Population-Synthesis

A framework that integrates a motivational layer with the traditional individual and household socio-demographic layers in synthetic populations. We extend the profile of agents by incorporating data on values, ideologies, opinions and vital priorities, which motivate the agents' behaviour. This motivational layer can help us develop a more nuanced decision-making mechanism for the agents in social simulation settings. Our methodology integrates microdata and macrodata within different Bayesian network structures: learnt, knowledge-based and hybrid.

The final selected synthetic population for Barcelona can be downloaded and information can be obtained about its attributes using the links below: 
- [Download Synthetic_Population_Barcelona_2024.csv](https://github.com/albaaguilera/Population-Synthesis/blob/main/Synthetic_Population_Barcelona_2024.csv)
- [Visualize Attribute Documentation](https://github.com/albaaguilera/Population-Synthesis/raw/main/attribute_documentation.html)

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

This repository is based on methods from Aguilera et al. (2024) [1].

## References

1. Smith, J., Doe, A., & Johnson, L. (2020). *Title of the paper*. Journal Name, 10(2), 123-456. DOI: [10.1234/example](https://doi.org/10.1234/example)

