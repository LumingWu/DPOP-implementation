#script (python)
from clingo import Function, String
import pprint

"""
This section is subject to changes depend on 
"""
def get_root():
    return False

def get_variables():
    return ["var1", "var2"]

def get_targets():
    return ["var3"]

def get_contexts():
    return ["var4"]

def get_domains():
    return [("var1", ["rice", "noodle"]), ("var2", ["chicken", "beef"]), ("var3", ["java", "c++"]), ("var4", ["server", "game"])]

def get_constraints():
    return [(10, ("var1", "rice"), ("var2", "chicken")),
            (-5, ("var2", "chicken"), ("var3", "java"), ("var4", "game")),
            (5, ("var1", "noodle"), ("var3", "c++"), ("var4", "game")),
            (7, ("var2", "chicken"), ("var3", "java"), ("var4", "server")),
            (-10, ("var1", "rice"), ("var3", "c++")),
            (-2, ("var1", "noodle"), ("var3", "java"))
            ]

def get_utility_messages():
    return []

"""
A simulation of getting necessary information from the main node
"""
def init():
    return (get_root(), get_variables(), get_targets(), get_contexts(), get_domains(), get_constraints(), get_utility_messages())

"""
The main controller of all ASP programs.
"""
def main(prg):
        # simulate geting information from main node
        is_root, variables, targets, contexts, domains, constraints, utility_messages = init()
        # add constraints at start so the program has no problem with #show utility/1.
        add_dcop_constraints(prg, constraints)
        # generate all combinations of target and context assignments as a 2 dimensional symbol rows.
        utility_message = generate_utility_message(prg, targets, contexts, domains)
        # PRINT_STATEMENT - Feel free to comment it out, search this tag to find others.
        report_utility_message_dimensions(utility_message)
        optimal = search_optimal(prg, utility_message, variables)

        
"""
Generate a multidimensional utility message table.
"""
def generate_utility_message(prg, targets, contexts, domains):
    # want to get all answer sets / context combinations.
    prg.configuration.solve.models = 0
    # ground the facts
    for target in targets:
        prg.ground([("utility_target_dimension", [target])])
    for context in contexts:
        prg.ground([("utility_context_dimension", [context])])
    for variable, domain in domains:
        for value in domain:
            prg.ground([("utility_domain_dimension", [variable, value])])
    # store answer sets / context combinations into a list.
    context_combinations = []
    prg.ground([("utility_dimension", [])])
    # assume this is some stream, don't want to set handle as context_combinatons.
    with prg.solve(yield_=True) as handle:
        for model in handle:
            # shown=True to get what is displayed in clingo.
            context_combinations.append(model.symbols(shown=True)) 
            """
            In an asynchronous system:
            handle.get()
            Which is a wait for the model.
            Usually that comes from prog.solve_asyn().
            """
    return context_combinations

    
"""
Given a set of target and context variable assignment, find optimal.
"""
def search_optimal(prg, utility_message, variables):
    # only want one optimal variable assignment for each combination.
    prg.configuration.solve.models = 0
    # ground variables first.
    for variable in variables:
        prg.ground([("utility_optimization_variables", [variable])])
    # for each combination, find the optimal variable assignment.
    for query_assignment in utility_message:
        # store assignments
        assignments = []
        # simple print like clingo
        print("Utility Dimension")
        print(query_assignment)
        # combination is a symbol class.
        for symbol in query_assignment:
            # a string of the function
            name = symbol.name
            # a list of symbols, use .name
            arguments = symbol.arguments
            if name == "assignment":
                assignments.append(arguments)
        # assign_external the assignments to
        for assignment in assignments:
            prg.assign_external(Function("query_assignment", assignment), True)
        optimal_symbols = []
        with prg.solve(yield_=True) as handle:
            for model in handle:
                optimal_symbols.append(model.symbols(shown=True))
        for assignment in assignments:
            prg.release_external(Function("query_assignment", assignment))
        print("Utility Optimization")
        print(optimal_symbols)
        print("")

"""
Helper for adding utility into the program
"""
def add_dcop_constraints(prg, constraints):
    # normally, there are more than one constraints, this is special case
    if len(constraints) == 0:
        prg.add("utility", [], "utility(0).")
        prg.ground([("utility", [])])
    else:
        # add first constraint and its first condition, the format must have at least 1 constraint, each has at least 1 condition
        conditions = ["utility(Utility) :- Utility = #sum {\n", str(constraints[0][0]), " : query_assignment(\"", constraints[0][1][0], "\", \"", constraints[0][1][1], "\")"]
        # more than 1 condition of the first constraint
        if len(constraints[0]) > 2:
            for i in range(2, len(constraints[0])):
                conditions.extend([", query_assignment(\"", constraints[0][i][0], "\", \"", constraints[0][i][1], "\")"])
        # more than 1 constraint
        if len(constraints) > 1:
            for i in range(1, len(constraints)):
                # add first condition
                conditions.extend([";\n", str(constraints[i][0]), " : query_assignment(\"", constraints[i][1][0], "\", \"", constraints[i][1][1], "\")"])
                # add rest of the conditions
                if len(constraints[i]) > 2:
                    for j in range(2, len(constraints[i])):
                        conditions.extend([", query_assignment(\"", constraints[i][j][0], "\", \"", constraints[i][j][1], "\")"])
        conditions.append("\n}.")
        conditions = "".join(conditions)
        # PRINT_STATEMENT - Feel free to comment it out, search this tag to find others.
        report_dcop_constraints(conditions)
        # create and add a program through Python
        prg.add("utility", [], conditions)
    prg.ground([("utility", [])])
"""
Print methods to --outf=3 or stdout for user. 
"""
def report_utility_message_dimensions(utility_message):
    print("============================")
    print("|Utility Message Dimensions|")
    print("============================")
    for i in range(0, len(utility_message)):
        print("")
        print("Assignment #"),
        print(i + 1)
        print(utility_message[i])
        print("")
    print("============================")
    print("|Utility Message Dimensions|")
    print("============================")

def report_dcop_constraints(conditions):
    print("==================")
    print("|DCOP Constraints|")
    print("==================")
    print(conditions)
    print("==================")
    print("|DCOP Constraints|")
    print("==================")
#end.
