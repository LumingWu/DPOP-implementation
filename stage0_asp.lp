%*
Clingo command:
	run file: $ clingo file_directory
*%

% Variables
%*
programming_language, food, drink
*%

% Domain
%*
programming_language: java, c, prolog, "answer set programming".
food: "fried chicken", brocoli, "fried rice", pasta, cheese.
drink: water, coke, coffee.
*%

% Context Agent
% Fodor

% Assignment
%* Assume all of the domains are possible assignments *%

%* 1-nary assignment is self assignment
	It represents the domain of self.
	Format: assignment(Variable, Value).
*%
assignment("programming language1", java).
assignment("programming language1", c).
assignment("food1", "fried chicken").
assignment("food2", "cheese").

%* 2-nary assignment is context assignment
	It represents the domain of context.
	Notice that although the variable name is the same, Fodor can have different domain for the same variable name.
	Format: assignment(Agent, Variable, Value).
*%
assignment(fodor, "programming language1", java).
assignment(fodor, "programming language2", prolog).
% Sorry, Professor, I made some safe assumption.
assignment(fodor, "food1", pasta).
assignment(fodor, "food2", cheese).

% Constraints(Not the constraint in ASP)
%* A set of positive rule that takes a certain number of variables(specifying the owner) and return a utility. *%

% If two people share the same preference, utility 10
utility(10) :- programming_language(java), programming_language(fodor, java).
utility(10) :- programming_language(prolog), programming_language(fodor, prolog).

% If two people don't share the same preference, utility 0
utility(0) :- programming_language(c), not programming_language(fodor, c).

% If two people would hate the other for some preference.
% Luming would make enemy to anyone that does not like fried chicken.
utility(-10) :- food("fried chicken"), not food(fodor, "fried chicken").

