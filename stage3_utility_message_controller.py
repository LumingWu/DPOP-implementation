#script (python)
import clingo
import pprint

"""
Sample Input
"""

def get_targets():
    return ["var3"]

def get_contexts():
    return ["var4"]

def get_domains():
    return [("var1", ["rice", "noodle"]), ("var2", ["chicken", "beef"]), ("var3", ["java", "c++"]), ("var4", ["server", "game"])]

"""
A simulation of getting necessary information from the main node
"""
def init():
    return (get_targets(), get_contexts(), get_domains())

"""
The main controller of all ASP programs.
"""
def main(prg):
        # simulate geting information from main node
        targets, contexts, domains = init()
        # generate all combinations of target and context assignments as a 2 dimensional symbol rows.
        utility_message = generate_utility_message(prg, targets, contexts, domains)
        report_utility_message_dimensions(utility_message)

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

"""
Sample Output

============================
|Utility Message Dimensions|
============================

Assignment # 1
[target_assignment("var4","game"), context_assignment("var3","java"), assignment("var4","game"), assignment("var3","java")]


Assignment # 2
[target_assignment("var4","game"), context_assignment("var3","c++"), assignment("var4","game"), assignment("var3","c++")]


Assignment # 3
[target_assignment("var4","server"), context_assignment("var3","java"), assignment("var4","server"), assignment("var3","java")]


Assignment # 4
[target_assignment("var4","server"), context_assignment("var3","c++"), assignment("var4","server"), assignment("var3","c++")]

============================
|Utility Message Dimensions|
============================

"""
#end.
