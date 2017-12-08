%*
Command: clingo leave_no_context.lp 0
0 for unlimited models.
*%
% n is the number of variables of an agent.
#const n = 2.
variables(1..n).

% Domain is a finite set of possible value assignments for a variable.
%*
Format: domain(Variable, (D1;...;Dm)). Equivalent to domain(Variable, D1). ... domain(Variable, Dm).
*%
domain(1, ("java";"c";"prolog")).

domain(2, ("ajax";"soap";"rest")).

% A constraint in Constraint Programming is a utility function given some variable assignments.
%*
Format: constraint(CompositeKey, Utility) :- assignment(Variable, Value), ..., assignment(Variable, Value).
		CompositeKey is a tuple of (Variable,..., Variable) to identify the origin of the utility. 
			utility(12) = utility(12) even if they came from different assignments.
		In addition, CompositeKey must be sorted.
*%

constraint(1, 10) :- assignment(1, "java").
constraint(1, 12) :- assignment(1, "c").
constraint(1, 5) :- assignment(1, "prolog").

constraint(2, 10) :- assignment(2, "ajax").
constraint(2, 12) :- assignment(2, "soap").
constraint(2, 5) :- assignment(2, "rest").

% Integrity Constraint: Exactly 1 assignment for a variable 
:- assignment(Variable, Value1), assignment(Variable, Value2), Value1 != Value2.

% An assignment is for a given variable, assign exactly one value that is in its domain.  
assignment(Variable, Value) : domain(Variable, Value) :- variables(Variable).

%*
assignment(Variable, Value) : domain(Variable, Value) is true if domain(Variable, Value) is false or both are true.
domain(Variable, Value) will never be false, so this adds a check on if assignment(Variable, Value) can be true.
It helps the integrity constraint to check that.

assignment(Variable, Value) :- variables(Variable), domain(Variable, Value).
assignment(Variable, Value) is true if Variable is in range and there is a domain for the variable. It forces all domain values can be assigned to the variable, violating the integrity constraint.
*%

% utility for each variable assignment is the sum of constraint values.
utility(Utility) :- Utility = #sum {Value : constraint(Variable, Value)}.

#show assignment/2.
#show utility/1.