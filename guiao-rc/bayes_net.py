

class BayesNet:

    def __init__(self, ldep=None):  # Why not ldep={}? See footnote 1.
        if not ldep:
            ldep = {}
        self.dependencies = ldep

    # Os dados estao num dicionario (var,dependencies)
    # em que as dependencias de cada variavel
    # estao num dicionario (mothers,prob);
    # "mothers" e' um frozenset de pares (mothervar,boolvalue)
    def add(self,var,mothers,prob):
        self.dependencies.setdefault(var,{})[frozenset(mothers)] = prob

    # Probabilidade conjunta de uma dada conjuncao 
    # de valores de todas as variaveis da rede
    def jointProb(self,conjunction):
        prob = 1.0
        for (var,val) in conjunction:
            for (mothers,p) in self.dependencies[var].items():
                if mothers.issubset(conjunction):
                    prob*=(p if val else 1-p)
        return prob

    def indivProb(self, var, val):
        return sum([self.jointProb(c) for c in [c for c in self.gen_conjuctions(list(self.dependencies.keys())) if (var, val) in c]])

    def gen_conjuctions(self, variables):
        if len(variables) == 1:
            return [(variables[0], True)], [(variables[0], False)]
        remain = self.gen_conjuctions(variables[1:])
        l = []
        for r in remain:
            l.append(r + [(variables[0], True)])
            l.append(r + [(variables[0], False)])
        return l

# Footnote 1:
# Default arguments are evaluated on function definition,
# not on function evaluation.
# This creates surprising behaviour when the default argument is mutable.
# See:
# http://docs.python-guide.org/en/latest/writing/gotchas/#mutable-default-arguments

