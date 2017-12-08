a("v1").
b("v3").

#program someprogram.
#show utility/1.

#script (python)
from clingo import Function, Number, parse_term

def main(prg):
	prg.ground([("base", [])])
	prg.add("utility", [], "utility(Utility) :- Utility = #sum {1 : a(\"v1\"); 2 : a(v2); 3 : b(\"v3\")}.")
	prg.ground([("utility", [])])
	prg.solve()
#end.

