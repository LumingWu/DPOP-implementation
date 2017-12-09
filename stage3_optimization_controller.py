#script (python)
from clingo import Function, String
import pprint

"""
Sample Input
"""

"""
From utility_message's output. Can connect through pipe, stream, or a local Python server.
We can simply pass down only assignment answers in each set.
"""
def get_assignments():
    return [("assignment(\"var4\",\"game\")", "assignment(\"var3\",\"java\")"),
            ("assignment(\"var4\",\"game\")", "assignment(\"var3\",\"c++\")"),
            ("assignment(\"var4\",\"server\")", "assignment(\"var3\",\"java\")"),
            ("assignment(\"var4\",\"server\")", "assignment(\"var3\",\"c++\")")
            ]

def get_variables():
    return ["var1", "var2"]

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

"""
A simulation of getting necessary information from the main node
"""
def init():
    return (get_assignments(), get_variables(), get_domains(), get_constraints())

"""
The main controller of all ASP programs.
"""
def main(prg):
        # simulate geting information from main node
        assignments, variables, domains, constraints = init()
        ground_facts(prg, variables, domains)
        optimized_results = optimization(prg, assignments, constraints)
        report_optimization(optimized_results)

def ground_facts(prg, variables, domains):
    # ground variables
    for variable in variables:
        prg.ground([("utility_optimization_variables", [variable])])
    # ground domains
    for variable, domain in domains:
        for value in domain:
            prg.ground([("utility_optimization_domains", [variable, value])])
    
"""
Given a set of target and context variable assignment, find optimal.
"""
def optimization(prg, assignments, constraints):
    # only want one optimal variable assignment for each combination. change to 0 to see other alternatives
    prg.configuration.solve.models = 1
    # parse the assignments to be groundable 
    assignments = parsed_assignments(assignments)
    # ground the optimization program
    prg.ground([("utility_optimization", [])])
    # add constraints, the program will have problem with #show utility/1. But this program works only if added after we grounded optimization program.
    add_dcop_constraints(prg, constraints)
    # for each combination, find the optimal variable assignment.
    optimized_results = []
    for assignment in assignments:
        # assign_external the facts to
        for variable, value in assignment:
            prg.assign_external(Function("assignment", [String(variable), String(value)]), True)
        optimal_symbols = []
        with prg.solve(yield_=True) as handle:
            for model in handle:
                optimal_symbols.append(model.symbols(shown=True))
        for assignment in assignments:
            prg.release_external(Function("assignment", assignment))
        optimized_results.append(optimal_symbols)
    return optimized_results

def parsed_assignments(assignments):
    groundables = []
    for assignment in assignments:
        groundable = []
        for fact in assignment:
            splitted = fact.split("\"")
            groundable.append((splitted[1], splitted[3]))
        groundables.append(groundable)
    return groundables

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
        conditions = ["utility(Utility) :- Utility = #sum {\n", str(constraints[0][0]), " : assignment(\"", constraints[0][1][0], "\", \"", constraints[0][1][1], "\")"]
        # more than 1 condition of the first constraint
        if len(constraints[0]) > 2:
            for i in range(2, len(constraints[0])):
                conditions.extend([", assignment(\"", constraints[0][i][0], "\", \"", constraints[0][i][1], "\")"])
        # more than 1 constraint
        if len(constraints) > 1:
            for i in range(1, len(constraints)):
                # add first condition
                conditions.extend([";\n", str(constraints[i][0]), " : assignment(\"", constraints[i][1][0], "\", \"", constraints[i][1][1], "\")"])
                # add rest of the conditions
                if len(constraints[i]) > 2:
                    for j in range(2, len(constraints[i])):
                        conditions.extend([", assignment(\"", constraints[i][j][0], "\", \"", constraints[i][j][1], "\")"])
        conditions.append("\n}.")
        conditions = "".join(conditions)
        # PRINT_STATEMENT - Feel free to comment it out, search this tag to find others.
        report_dcop_constraints(conditions)
        # create and add a program through Python
        prg.add("utility", [], conditions)
    prg.ground([("utility", [])])

"""
Print functions
"""
def report_dcop_constraints(conditions):
    print("==================")
    print("|DCOP Constraints|")
    print("==================")
    print(conditions)
    print("==================")
    print("|DCOP Constraints|")
    print("==================")

def report_optimization(optimized_results):
    print("==============")
    print("|Optimization|")
    print("==============")
    for i in range(0, len(optimized_results)):
        print("")
        print("Utility Message Cell #"),
        print(i + 1)
        print("")
        optimized_result_set = optimized_results[i]
        for j in range(0, len(optimized_result_set)):
            print("")
            print("Optimal Answer Set Rank #"),
            print(j + 1)
            print(optimized_results[i][j])
            print("")
    print("==============")
    print("|Optimization|")
    print("==============")

"""
Sample Output

==================
|DCOP Constraints|
==================
utility(Utility) :- Utility = #sum {
10 : assignment("var1", "rice"), assignment("var2", "chicken");
-5 : assignment("var2", "chicken"), assignment("var3", "java"), assignment("var4", "game");
5 : assignment("var1", "noodle"), assignment("var3", "c++"), assignment("var4", "game");
7 : assignment("var2", "chicken"), assignment("var3", "java"), assignment("var4", "server");
-10 : assignment("var1", "rice"), assignment("var3", "c++");
-2 : assignment("var1", "noodle"), assignment("var3", "java")
}.
==================
|DCOP Constraints|
==================
==============
|Optimization|
==============

Utility Message Cell # 1


Optimal Answer Set Rank # 1
[assignment("var1","rice"), assignment("var2","chicken"), assignment("var3","java"), assignment("var4","game"), variable_assignment("var1","rice"), variable_assignment("var2","chicken"), utility(5)]


Utility Message Cell # 2


Optimal Answer Set Rank # 1
[assignment("var1","rice"), assignment("var2","chicken"), assignment("var3","java"), assignment("var3","c++"), assignment("var4","game"), variable_assignment("var1","rice"), variable_assignment("var2","chicken"), utility(-5)]


Utility Message Cell # 3


Optimal Answer Set Rank # 1
[assignment("var1","rice"), assignment("var2","chicken"), assignment("var3","java"), assignment("var3","c++"), assignment("var4","server"), assignment("var4","game"), variable_assignment("var1","rice"), variable_assignment("var2","chicken"), utility(2)]


Utility Message Cell # 4


Optimal Answer Set Rank # 1
[assignment("var1","rice"), assignment("var2","chicken"), assignment("var3","java"), assignment("var3","c++"), assignment("var4","server"), assignment("var4","game"), variable_assignment("var1","rice"), variable_assignment("var2","chicken"), utility(2)]

==============
|Optimization|
==============

"""
#end.
