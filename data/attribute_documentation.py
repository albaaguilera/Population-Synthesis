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

    # Socio-demographic - Household
    {"Layer": "Socio-demographic", "Type": "Household", "Attribute": "Ph", "Definition": "People in household", "Description":  "1: Lives alone, 2: Lives with 1 person, 3: Lives with 2 persons, 4: Lives with 3+ persons"},
    {"Layer": "Socio-demographic", "Type": "Household", "Attribute": "Ch", "Definition": "Children in household", "Description": "0: No children, 1: One or more children"},

    # Socio-demographic - Network
    {"Layer": "Socio-demographic", "Type": "Network", "Attribute": "Fr", "Definition": "Number of friends", "Description": "Number from 0 to 3 or more friends"},
    {"Layer": "Socio-demographic", "Type": "Network", "Attribute": "X_Fr_2", "Definition": "Friends' main demographic attributes", "Description": "Friends' age, gender, education, etc."},

    # Motivational - Values
    {"Layer": "Motivational", "Type": "Values", "Attribute": "Inglehart_index", "Definition": "Inglehart’s materialist/post-materialist index", "Description": "Degree of materialism to post-materialism (1 – 7)"},
    {"Layer": "Motivational", "Type": "Values", "Attribute": "Schwartz_values", "Definition": "Alignment with Schwartz's fundamental values", "Description": "Degree of agreement or alignment with 10 fundamental values (1 – 7)"},

    # Motivational - Ideologies
    {"Layer": "Motivational", "Type": "Ideologies", "Attribute": "Ideo", "Definition": "Individual’s and parents’ ideology", "Description": "Political spectrum (1 – 8)"},
    {"Layer": "Motivational", "Type": "Ideologies", "Attribute": "Alignment_capitalism", "Definition": "Alignment with capitalism, socialism, etc.", "Description": "Degree of agreement (1 – 3)"},
    {"Layer": "Motivational", "Type": "Ideologies", "Attribute": "Alignment_feminism", "Definition": "Alignment with feminism, ecologism, multiculturalism, etc.", "Description": "Degree of agreement (1 – 3)"},

    # Motivational - Opinions
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "Interest_politics", "Definition": "Interest on politics, sports, culture, etc.", "Description": "Degree of interest (1 – 4)"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "View_controversial_topics", "Definition": "Views on controversial topics like immigration", "Description": "Varies by topic (1 – 3)"},
    {"Layer": "Motivational", "Type": "Opinions", "Attribute": "Confidence_institutions", "Definition": "Confidence in police, state, government", "Description": "Degree of confidence (1 – 4)"},

    # Motivational - Vital Priorities
    {"Layer": "Motivational", "Type": "Vital Priorities", "Attribute": "Importance_family", "Definition": "Importance given to family, friends, etc.", "Description": "Degree of importance (1 – 4)"},
    {"Layer": "Motivational", "Type": "Vital Priorities", "Attribute": "Satisfaction_life", "Definition": "Satisfaction with life aspects", "Description": "Degree of satisfaction (1 – 10)"},
]

attribute_df = pd.DataFrame(attribute_info)
html_output = attribute_df.to_html(index=False)

with open("attribute_documentation.html", "w") as f:
    f.write(html_output)

print("Documentation saved as 'attribute_documentation.html'")
