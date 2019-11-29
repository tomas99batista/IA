from constraintsearch import *

def border_constraint(pais1, cor1, pais2, cor2):
    return cor1 != cor2

def make_constraint_graph(mapa):
    # 2 paises vizinhos n partilham a mesma cor
    return { (X,Y):border_constraint for X in mapa.keys() for Y in mapa[X] }

def make_domains(fronteiras, lista_cores):
    return {pais:lista_cores for pais in fronteiras.keys()}

mapa_a = {
    'a' : 'bed',
    'b' : 'aec',
    'c' : 'bed',
    'd' : 'aec',
    'e' : 'abcd',
}

mapa_b = {
    'a' : 'bed',
    'b' : 'aec',
    'c' : 'bef',
    'd' : 'aef',
    'e' : 'abcdf',
    'f' : 'dec',
}

mapa_c = {
    'a' : 'defb',
    'b' : 'afc',
    'c' : 'bfgd',
    'd' : 'aegc',
    'e' : 'adfg', 
    'f' : 'abcge',
    'g' : 'aecd',
}
cores = ['red', 'green', 'blue', 'yellow', 'white']

cs = ConstraintSearch(make_domains(mapa_c, cores), make_constraint_graph(mapa_c))

print(cs.search())
