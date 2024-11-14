# Value-Enriched Population-Synthesis

A framework that integrates a motivational layer with the traditional individual and household socio-demographic layers in synthetic populations. We extend the profile of agents by incorporating data on values, ideologies, opinions and vital priorities, which motivate the agents' behaviour. This motivational layer can help us develop a more nuanced decision-making mechanism for the agents in social simulation settings. Our methodology integrates microdata and macrodata within different Bayesian network structures: learnt, knowledge-based and hybrid.

The final selected synthetic population for Barcelona can be downloaded and information can be obtained about its attributes using the links below: 
- [Download Synthetic_Population_Barcelona_2024.csv](https://github.com/albaaguilera/Population-Synthesis/blob/main/Synthetic_Population_Barcelona_2024.csv)
- [Visualize Attribute Documentation](https://github.com/albaaguilera/Population-Synthesis/raw/main/attribute_documentation.html)

This repository is based on methods from Aguilera et al. (2024) [1].

## Structure
The github repository contains the following folders and files: 
1. **Data** input information we use to construct the BN structures
   - data_treated.py: clean and harmonize the csv datasets.
3. **Models** construction of the BN structures (learnt, knowledge-based and hybrid)
   - create_knowledgebased.py
   - create_learnt.ipnyb
   - create_hybrid.py
   - knowledgebased_model.pgmx
   - learnt_model.pgmx
   - hybrid_model.pgmx
5. **Results** output of the BN structures and validation of these samples
   - *samples*: synthetic populations generated with each model created.
   - *validation*: analysis to validate the synthetic populations (Wasserstein distances, regression lines and SRMSE).

## References

1. Aguilera, A., Albertí, M., Osman, N., & Curto, G. (2024). *Value-Enriched Population Synthesis: Integrating a Motivational Layer*. arXiv preprint arXiv:2408.09407. 

