%*
Command: clingo-python stage3_utility_message.lp stage3_utility_message_controller.py --outf=3
*%

%*
Generate facts in creation of ASP.
This can be done by other ways:
	(1) Pass the parameters down by prg.ground([("program_name", [arguments,...])]) do it multiple times for multiple sets of arguments.
		In ASP, #program program_name(arguments,...).
		Arguments must not be variables, instead, treat them as #const arguments.
		For example, domain(arguments,...).
		Use this to pass arguments to program without parsing the ASP code.

	(2) prg.assign_external(Function("fact_name", [Symbols,...]), True).
		In ASP, #external fact_name(Variables,...) : some_domain(Variables,...).
		Use this when the fact fact_name is not always true.

	(3) prg.add("program_name", [some_parameters], "ANY ASP CODE")
		prg.ground([("program_name", [some_arguments])])
		Use this when grounding rules, aggregates, optimzations, and constraints.
*%

#program utility_target_dimension(target).
target_variables(target).

#program utility_context_dimension(context).
context_variables(context).

#program utility_domain_dimension(variable, value).
domains(variable, value).

#program utility_dimension.

% distinguish target and context for dimension_reduction.
target_assignment(Variable, Value) : domains(Variable, Value) :- context_variables(Variable).
context_assignment(Variable, Value) : domains(Variable, Value) :- target_variables(Variable).

% target and context are also assignments. For dimension optimiization.
assignment(Variable, Value) :- target_assignment(Variable, Value).
assignment(Variable, Value) :- context_assignment(Variable, Value).

#show target_assignment/2.
#show context_assignment/2.
#show assignment/2.
