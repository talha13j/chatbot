from pyswip import Prolog

# Create a Prolog object
prolog = Prolog()

# Consult the knowledge base file
prolog.consult('knowledgebase.pl')

def write_fact_and_rules(query):
    # Append the query to the knowledge base file
    with open('knowledgebase.pl', 'a') as kb_file:
        kb_file.write(query + '.\n')

def get_results(query):
    # Execute the query and retrieve the results
    results = list(prolog.query(query))
    return results

def print_results(results):
    # Print the results to the console
    for result in results:
        for key, value in result.items():
            print(key + ': ' + value)
        print('---')

def check_relation(name, relation):
    # Construct the Prolog query
    query = f"{relation}(X, {name})"
    
    # Execute the query and print the results
    results = get_results(query)
    if results:
        print(f"The following person(s) have the {relation} relation with {name}:")
        print_results(results)
    else:
        print(f"No one has the {relation} relation with {name}.")