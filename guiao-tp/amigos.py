from constraintsearch import *

def amigos_constraint(a1, t1, a2, t2):
    c1, b1 = t1
    c2, b2 = t2

    # Partilharem os mesmos objetos
    if c1 == c2 or b1 == b2:
        return False

    # Se usar as proprias coisas
    if a1 in [c1, b1] or a2 in [c2, b2]:
        return False

    # Chapeu e bicla pertencem a amigos diferentes
    if c1 == b1 or c2 == b2:
        return False

    # O que leva o chapéu de Cláudio anda na bicicleta de Bernardo.
    if c1 == 'c' and b1 != 'b':
        return False

    return True

def make_constraint_graph(amigos):
    # 2 paises vizinhos n partilham a mesma cor
    return { (X,Y):amigos_constraint for X in amigos for Y in amigos if X != Y }

def make_domains(amigos):
    return {a: [(b, c) for b in amigos for c in amigos 
                if a!= b and a!= c and b!= c] 
                for a in amigos }

amigos = ['a', 'b', 'c',]

cs = ConstraintSearch(make_domains(amigos), make_constraint_graph(amigos))

print(cs.search())
print(cs.calls)
