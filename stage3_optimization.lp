%*
Command: clingo-python stage3_optimization.lp stage3_optimization_controller.py --outf=3
*%

#program utility_optimization_variables(variable).
variables(variable).

#program utility_optimization_domains(variable, value).
domains(variable, value).

#program utility_optimization.
% Python controller will pass down the truth value for each.
#external assignment(Variable, Value) : domains(Variable, Value).

% assign each variable once.
1 {variable_assignment(Variable, Value) : domains(Variable, Value)} 1 :- variables(Variable).

% variable assignment is also assignment.
assignment(Variable, Value) :- variable_assignment(Variable, Value).

% optimize on each answer set based on utility. This is not working
% #maximize {Utility : utility(Utility)}.

#show assignment/2.
#show variable_assignment/2.
#show utility/1.