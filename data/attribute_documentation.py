import pandas as pd

# Define attribute documentation organized by categories
attribute_info = [
    # Socio-demographic - Main
    {"Layer": "Socio-demographic", "Type": "Main", "Attribute": "D", "Definition": "District", "Description": "0: Ciutat Vella, 1: L'Eixample, 2: Sants-Montjuïc, 3: Les Corts, 4: Sarrià-Sant Gervasi, 5: Gràcia, 6: Horta-Guinardó, 7: Nou Barris, 8: Sant Andreu, 9: Sant Martí"},
    {"Layer": "Socio-demographic", "Type": "Main", "Attribute": "G", "Definition": "Gender", "Description": "0: Female, 1: Male"},
    {"Layer": "Socio-demographic", "Type": "Main", "Attribute": "A", "Definition": "Age Group", "Description": "1: 15-24, 2: 25-34, 3: 35-44, 4: 45-54, 5: 55-64, 6: 65-74"},
    {"Layer": "Socio-demographic", "Type": "Main", "Attribute": "N", "Definition": "Nationality", "Description": "0: Spanish, 1: Rest of EU / rest of world"},
    {"Layer": "Socio-demographic", "Type": "Main", "Attribute": "E", "Definition": "Educational level", "Description": "1: No completed obligatory education, 2: Obligatory (primary, EGB, ESO), 3: General secondary, 4: Professional secondary, 5: University, 6: Postgraduate"},
    {"Layer": "Socio-demographic", "Type": "Main", "Attribute": "U", "Definition": "Unemployment", "Description": "0: Unemployed, 1: Employed"},
    {"Layer": "Socio-demographic", "Type": "Main", "Attribute": "I", "Definition": "Income", "Description": "Monthly amount of income"},
    {"Layer": "Socio-demographic", "Type": "Main", "Attribute": "R", "Definition": "Rent", "Description": "Monthly amount of rent"},

    # Socio-demographic - Household
    {"Layer": "Socio-demographic", "Type": "Household", "Attribute": "Ph", "Definition": "People in household", "Description":  "1: Lives alone, 2: Lives with 1 person, 3: Lives with 2 persons, 4: Lives with 3+ persons"},
    {"Layer": "Socio-demographic", "Type": "Household", "Attribute": "Ch", "Definition": "Children in household", "Description": "0: No children, 1: One or more children"},

    # Socio-demographic - Network
    {"Layer": "Socio-demographic", "Type": "Network", "Attribute": "Fr", "Definition": "Number of friends", "Description": "Number from 0 to 3 or more friends"},
    {"Layer": "Socio-demographic", "Type": "Network", "Attribute": "G_1", "Definition": "Gender Friend 1", "Description": "0: Female, 1: Male"},
    {"Layer": "Socio-demographic", "Type": "Network", "Attribute": "A_1", "Definition": "Age Group Friend 1", "Description": "1: 15-24, 2: 25-34, 3: 35-44, 4: 45-54, 5: 55-64, 6: 65-74"},
    {"Layer": "Socio-demographic", "Type": "Network", "Attribute": "N_1", "Definition": "Nationality Friend 1", "Description": "0: Spanish, 1: Rest of EU / rest of world"},
    {"Layer": "Socio-demographic", "Type": "Network", "Attribute": "G_2", "Definition": "Gender Friend 2", "Description": "0: Female, 1: Male"},
    {"Layer": "Socio-demographic", "Type": "Network", "Attribute": "A_2", "Definition": "Age Group Friend 2", "Description": "1: 15-24, 2: 25-34, 3: 35-44, 4: 45-54, 5: 55-64, 6: 65-74"},
    {"Layer": "Socio-demographic", "Type": "Network", "Attribute": "N_2", "Definition": "Nationality Friend 2", "Description": "0: Spanish, 1: Rest of EU / rest of world"},
    {"Layer": "Socio-demographic", "Type": "Network", "Attribute": "G_3", "Definition": "Gender Friend 3", "Description": "0: Female, 1: Male"},
    {"Layer": "Socio-demographic", "Type": "Network", "Attribute": "A_3", "Definition": "Age Group Friend 3", "Description": "1: 15-24, 2: 25-34, 3: 35-44, 4: 45-54, 5: 55-64, 6: 65-74"},
    {"Layer": "Socio-demographic", "Type": "Network", "Attribute": "N_3", "Definition": "Nationality Friend 3", "Description": "0: Spanish, 1: Rest of EU / rest of world"},
    
    # Motivational - Values
    {"Layer": "Motivational", "Type": "Inglehart's Values", "Attribute": "Inglehart_1", "Definition": "If you had to choose among the following goals, which two do you consider the most important for our country to achieve?", "Description": "0: Maintaining order in the nation (Materialist Goal), 1: Giving people more say in important government decisions (Post-Materialist Goal), 2: Fighting rising prices (Materialist Goal), 3: Protecting freedom of speech (Post-Materialist Goal) "},
    {"Layer": "Motivational", "Type": "Inglehart's Values", "Attribute": "Inglehart_2", "Definition": "If you had to choose among the following goals, which two do you consider the most important for our country to achieve?", "Description": "0: Maintaining order in the nation (Materialist Goal), 1: Giving people more say in important government decisions (Post-Materialist Goal), 2: Fighting rising prices (Materialist Goal), 3: Protecting freedom of speech (Post-Materialist Goal) "},
    {"Layer": "Motivational", "Type": "Inglehart's Values", "Attribute": "Inglehart_index", "Definition": "Inglehart’s materialist/post-materialist index", "Description": "Degree of materialism to post-materialism (1 – 7)"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Benevolence", "Definition": "She/he always wants to help the people who are close to her/him. It is important to her/him to care for the well-being of the people she/he knows.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Self-Direction", "Definition": "She/he thinks it is important to be creative. She/he likes to do things in her/his own original way.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Self-Direction", "Definition": "She/he likes to make her/his own decisions about what she/he does. She/he wants to be free to plan and choose her/his activities for herself/himself.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Stimulation", "Definition": "She/he thinks it is important to have an exciting life. She/he likes to take risks and do a lot of different things.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Stimulation", "Definition": "She/he likes surprises and is always looking for new things to do. She/he thinks it is important to lead a life full of excitement.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Hedonism", "Definition": "She/he seeks every chance she/he can to have fun. It is important to her/him to do things that give her/him pleasure.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Hedonism", "Definition": "She/he really wants to enjoy life. Having a good time is very important to her/him.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Achievement", "Definition": "Being very successful is important to her/him. She/he hopes people will recognize her/his achievements.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Achievement", "Definition": "It is important to her/him to show her/his abilities. She/he wants people to admire what she/he does.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Power", "Definition": "She/he wants people to do what she/he says. She/he likes to be the one who makes decisions.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Power", "Definition": "It is important to her/him to be rich. She/he wants to have a lot of money and expensive things.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Security", "Definition": "It is important to her/him to live in secure surroundings. She/he avoids anything that might endanger her/his safety.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Security", "Definition": "She/he tries hard to avoid getting sick. Staying healthy is very important to her/him.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Conformity", "Definition": "She/he believes that people should do what they are told. She/he thinks people should follow rules at all times, even when no one is watching.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Conformity", "Definition": "She/he always behaves properly. She/he wants to avoid doing anything people would say is wrong.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Tradition", "Definition": "She/he thinks it is important to do things the way she/he learned from her/his family. She/he wants to follow their customs and traditions.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Tradition", "Definition": "It is important to her/him to be humble and modest. She/he tries not to draw attention to herself/himself.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Benevolence", "Definition": "She/he thinks it is important to be loyal to her/his friends. She/he wants to devote herself/himself to people close to her/him.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Universalism", "Definition": "She/he thinks it is important that every person in the world be treated equally. She/he believes everyone should have equal opportunities in life.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Universalism", "Definition": "She/he strongly believes that people should care for nature. Looking after the environment is important to her/him.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},
    {"Layer": "Motivational", "Type": "Schwartz's Values", "Attribute": "Universalism", "Definition": "She/he wants to understand people who are different from her/him. She/he tries to learn what they are like.", "Description": "1: Very similar to me, 2: Similar to me, 3: A little bit similar to me, 4: Not similar to me, 5: Not at all similar to me"},

    # Motivational - Ideologies
    {"Layer": "Motivational", "Type": "Ideologies", "Attribute": "Ideo", "Definition": "Individual’s ideology", "Description": "1: Extrema esquerra, 2: Esquerra, 3: Centre esquerra, 4: Centre, 5: Centre dreta, 6: Dreta, 7: Extrema dreta, 8: Apolític"},
    {"Layer": "Motivational", "Type": "Ideologies", "Attribute": "Ipare", "Definition": "Father's Ideology", "Description": "1: Extrema esquerra, 2: Esquerra, 3: Centre esquerra, 4: Centre, 5: Centre dreta, 6: Dreta, 7: Extrema dreta, 8: Apolític"},
    {"Layer": "Motivational", "Type": "Ideologies", "Attribute": "Imare", "Definition": "Mother's Ideology", "Description": "1: Extrema esquerra, 2: Esquerra, 3: Centre esquerra, 4: Centre, 5: Centre dreta, 6: Dreta, 7: Extrema dreta, 8: Apolític"},

    {"Layer": "Motivational", "Type": "Ideologies", "Attribute": "Cap", "Definition": "Alignment with capitalism", "Description": "1: Agree, 2: Disagree, 3: Neutral"},
    {"Layer": "Motivational", "Type": "Ideologies", "Attribute": "Soc", "Definition": "Alignment with socialism", "Description": "1: Agree, 2: Disagree, 3: Neutral"},
    {"Layer": "Motivational", "Type": "Ideologies", "Attribute": "Com", "Definition": "Alignment with communism", "Description": "1: Agree, 2: Disagree, 3: Neutral"},
    {"Layer": "Motivational", "Type": "Ideologies", "Attribute": "Indep", "Definition": "Alignment with independentism", "Description": "1: Agree, 2: Disagree, 3: Neutral"},
    {"Layer": "Motivational", "Type": "Ideologies", "Attribute": "Femin", "Definition": "Alignment with feminism", "Description": "1: Agree, 2: Disagree, 3: Neutral"},
    {"Layer": "Motivational", "Type": "Ideologies", "Attribute": "Ecolog", "Definition": "Alignment with ecologism", "Description": "1: Agree, 2: Disagree, 3: Neutral"},
    {"Layer": "Motivational", "Type": "Ideologies", "Attribute": "Pacif", "Definition": "Alignment with pacifism", "Description": "1: Agree, 2: Disagree, 3: Neutral"},
    {"Layer": "Motivational", "Type": "Ideologies", "Attribute": "AnimDef", "Definition": "Alignment with animals defense", "Description": "1: Agree, 2: Disagree, 3: Neutral"},
    {"Layer": "Motivational", "Type": "Ideologies", "Attribute": "Fascism", "Definition": "Alignment with fascism", "Description": "1: Agree, 2: Disagree, 3: Neutral"},
    {"Layer": "Motivational", "Type": "Ideologies", "Attribute": "Multiculturalism", "Definition": "Alignment with multiculturalism", "Description": "1: Agree, 2: Disagree, 3: Neutral"},	
    {"Layer": "Motivational", "Type": "Ideologies", "Attribute": "Racism", "Definition": "Alignment with racism", "Description": "1: Agree, 2: Disagree, 3: Neutral"},
    
    {"Layer": "Motivational", "Type": "Ideologies", "Attribute": "Polpart", "Definition": "Which political party represents you the most?", "Description": "1: PSC PSOE _ Partit dels Socialistes, 2: ERC _ Esquerra Republicana de Catalunya, 3: JxCAT _ Junts per Catalunya, 4: En Comú Podem / Podem en Comú / Podemos, 5: VOX, 6: CUP G _ Candidatura d’Unitat Popular Un Nou Cicle per Guanyar, 7: C’s Ciutadans _ Partido de la Ciutadania, 8: PDeCat (Partit Demòcrata Europeu Català), 9: PPC PP _ Partit Popular, 10: Altres, 11: Cap"},

    # Motivational - Opinions
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "CSoc", "Definition": "Perceived Social Class.", "Description": "1: High Class, 2: Medium-High Class, 3: Medium Class, 4: Medium-Low Class, 5: Low Class"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfPeople", "Definition": "Confidence in People", "Description": "1: Yes, 2: No, 3: Don't know"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "RacismSoc", "Definition": "Perception on degree of racism society", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "Machismo", "Definition": "Perception on society's machismo", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConservSoc", "Definition": "Perception on society's conservatism", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "Respectful_environmentSoc", "Definition": "Perception on society's respectful with the environment", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ProgressistSoc", "Definition": "Perception on society's progressism", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "IndividualistSoc", "Definition": "Perception on society's individualism", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "Optimist_futureSoc", "Definition": " Perception on society's Optimism towards the future", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ViolentSoc", "Definition": "Perception on society's violence", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "MaterialistSoc", "Definition": "Perception on society's materialism", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "DemocrataSoc", "Definition": "Perception on society's democracy", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "GenerousSoc", "Definition": "Perception on society's generosity", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "TolerantSoc", "Definition": "Perception on society's tolerance", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "CivicSoc", "Definition": "Perception on society's civism", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: Not at all"},
    
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "Abortation", "Definition": "How justifiable is abortion", "Description": "1: Always justifiable, 2: Justifiable in some cases, 3: Never justifiable"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "Occupation", "Definition": "How justifiable is occupation", "Description": "1: Always justifiable, 2: Justifiable in some cases, 3: Never justifiable"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "EconvsMedi", "Definition": "Which is a higher priority", "Description": "1: Environment over economy, 2: Economy over environment, 3: Don't know"},
    
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfMon", "Definition": "Trust in the monarchy", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: None at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "Interest_politics", "Definition": "Interest in politics, sports, culture, etc.", "Description": "Degree of interest (1 – 4)"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "View_controversial_topics", "Definition": "Views on controversial topics like immigration", "Description": "Varies by topic (1 – 3)"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "Confidence_institutions", "Definition": "Confidence in police, state, government", "Description": "Degree of confidence (1 – 4)"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfEjercito", "Definition": "Trust in the army", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: None at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfUniversity", "Definition": "Trust in the university", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: None at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfJustice", "Definition": "Trust in the justice tribunals", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: None at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfChurch", "Definition": "Trust in the church", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: None at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfBank", "Definition": "Trust in the bank", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: None at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfPoliticalParties", "Definition": "Trust in political parties", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: None at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfBigBusiness", "Definition": "Trust in big business", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: None at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfSindicatos", "Definition": "Trust in sindicatos", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: None at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfNGOs", "Definition": "Trust in NGOs", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: None at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfPolice", "Definition": "Trust in the police", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: None at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfGovernment", "Definition": "Trust in the government", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: None at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfGeneralitat", "Definition": "Trust in the Generalitat", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: None at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfCityHall", "Definition": "Trust in the city hall", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: None at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfEU", "Definition": "Trust in the EU", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: None at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfONU", "Definition": "Trust in the ONU", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: None at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfTelevision", "Definition": "Trust in television", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: None at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfPremsa", "Definition": "Trust in the press", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: None at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "ConfSocialNetworks", "Definition": "Trust in social networks", "Description": "1: A lot, 2: Quite a lot, 3: A little, 4: None at all"},

    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "InterPol", "Definition": "Interest in Politics", "Description": "1: Very interested, 2: Quite interested, 3: A little interested, 4.Not interested at all"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "Nationalism", "Definition": "In this scale, how do you feel?", "Description": "1: Only spanish, 2: More spanish than catalan, 3: More catalan than spanish, 4: Only catalan"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "NationalismFather", "Definition": "In this scale, how do you think your father feels?", "Description": "1: Only spanish, 2: More spanish than catalan, 3: More catalan than spanish, 4: Only catalan"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "NationalismMother", "Definition": "In this scale, how do you think your mother feels?", "Description": "1: Only spanish, 2: More spanish than catalan, 3: More catalan than spanish, 4: Only catalan"},
    
    
    # Motivational - Vital Priorities
    {"Layer": "Motivational", "Type": "Vital Priorities", "Attribute": "IF", "Definition": "Importance given to Family", "Description": "1: Very much, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Vital Priorities", "Attribute": "IFr", "Definition": "Importance given to Friends", "Description": "1: Very much, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Vital Priorities", "Attribute": "ISt", "Definition": "Importance given to Studies", "Description": "1: Very much, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Vital Priorities", "Attribute": "IWo", "Definition": "Importance given to Work", "Description": "1: Very much, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Vital Priorities", "Attribute": "IRel", "Definition": "Importance given to Religion", "Description": "1: Very much, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Vital Priorities", "Attribute": "IMon", "Definition": "Importance given to Money and Material Goods", "Description": "1: Very much, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Vital Priorities", "Attribute": "IPol", "Definition": "Importance given to Politics", "Description": "1: Very much, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Vital Priorities", "Attribute": "IFree", "Definition": "Importance given to Free Time", "Description": "1: Very much, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Vital Priorities", "Attribute": "IPD", "Definition": "Importance given to Personal Development", "Description": "1: Very much, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Vital Priorities", "Attribute": "SF", "Definition": "Satisfaction towards one's Family", "Description": "1: Very much, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Vital Priorities", "Attribute": "SFr", "Definition": "Satisfaction towards one's Friends", "Description": "1: Very much, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Vital Priorities", "Attribute": "SSt", "Definition": "Satisfaction towards one's Studies", "Description": "1: Very much, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Vital Priorities", "Attribute": "SWo", "Definition": "Satisfaction towards one's Work", "Description": "1: Very much, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Vital Priorities", "Attribute": "SMon", "Definition": "Satisfaction towards one's economic situation", "Description": "1: Very much, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Vital Priorities", "Attribute": "SFree", "Definition": "Satisfaction towards one's Free Time", "Description": "1: Very much, 2: Quite a lot, 3: A little, 4: Not at all"},
    {"Layer": "Motivational", "Type": "Vital Priorities", "Attribute": "SPD", "Definition": "Satisfaction towards one's Personal Development", "Description": "1: Very much, 2: Quite a lot, 3: A little, 4: Not at all"}
]

attribute_df = pd.DataFrame(attribute_info)
html_output = attribute_df.to_html(index=False)

with open("attribute_documentation.html", "w") as f:
    f.write(html_output)

print("Documentation saved as 'attribute_documentation.html'")
