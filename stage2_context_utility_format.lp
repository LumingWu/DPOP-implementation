%*
Command: clingo leave_context.lp --outf=3
0 for unlimited models.
*%

% No interval because not all variables of an agent is like that.
variables(1;3).
context(2;4).

domain(1, ("java";"c";"prolog")).

domain(2, ("ajax";"soap";"rest")).

domain(3, ("chicken";"beef")).

domain(4, ("beer", "wine")).

% Guaranteed to assign something.
assignment(Variable, Value) : domain(Variable, Value) :- variables(Variable).
assignment(Variable, Value) : domain(Variable, Value) :- context(Variable).

% Constraints are now defined as part of utility evaluation, no more unique constraint. Con: Don't know how Utility is evaluated.
utility(Utility) :- Utility = #sum {
	10: assignment(1, "java"), assignment(4, "wine");
	-10: assignment(1, "java"), assignment(4, "beer");
	5: assignment(1, "java"), assignment(2, "rest"), assignment(3, "chicken");
	2: assignment(2, "soap"), assignment(3, "beef");
	100: assignment(3, "beef"), assignment(4, "beer");
	-20: assignment(1, "prolog"), assignment(2, "ajax");
	-10: assignment(1, "prolog"), assignment(2, "ajax"), assignment(3, "beef")
}.

#show assignment/2.
#show utility/1.
