import streamlit as st
from simpleai.search import CspProblem, backtrack

st.title('Cryptarithmetic Solver')

# Input text boxes for the three words
word1 = st.text_input('Enter first word:')
word2 = st.text_input('Enter second word:')
word3 = st.text_input('Enter third word:')

if st.button('Solve'):
    # Create variables and domains
    variables = tuple(set(word1 + word2 + word3))
    domains = {}
    for variable in variables:
        if variable in [word1[0], word2[0], word3[0]]:
            domains[variable] = list(range(1, 10))
        else:
            domains[variable] = list(range(10))

    # Define constraints
    def constraint_unique(variables, values):
        return len(values) == len(set(values))

    def constraint_add(variables, values):
        if len(set(values)) < len(values):
            return False
        w1 = ''.join([str(values[variables.index(c)]) for c in word1])
        w2 = ''.join([str(values[variables.index(c)]) for c in word2])
        w3 = ''.join([str(values[variables.index(c)]) for c in word3])
        return int(w1) + int(w2) == int(w3)

    constraints = [
        (variables, constraint_unique),
        (variables, constraint_add),
    ]

    # Create problem and solve
    problem = CspProblem(variables, domains, constraints)
    output = backtrack(problem)

    # Display solution
    if output:
        # Calculate the sum in the format 'word1 + word2 = word3'
        word1_solution = ''.join([str(output.get(variables.index(c), c)) for c in word1])
        word2_solution = ''.join([str(output.get(variables.index(c), c)) for c in word2])
        word3_solution = ''.join([str(output.get(variables.index(c), c)) for c in word3])
        sum_solution = f"{word1_solution} + {word2_solution} = {word3_solution}"
        st.success(f'Solution: {sum_solution}')

        # Calculate the numeric sum
        num1 = int(''.join([str(output.get(c, c)) for c in word1]))
        num2 = int(''.join([str(output.get(c, c)) for c in word2]))
        num3 = int(''.join([str(output.get(c, c)) for c in word3]))
        st.info(f'Sum: {num1} + {num2} = {num3}')

        # Display a table of letter to number mapping
        st.write("Letter to Number Mapping:")
        table_data = {"Letter": list(variables), "Number": [output.get(c, c) for c in variables]}
        st.table(table_data)
    else:
        st.warning('No solutions found.')