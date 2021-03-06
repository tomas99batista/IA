from collections import Counter 

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2018
# v1.81 - 2018/11/18
#

# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)

# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

# Devolve um par (val, f req), em que val é o valor local mais frequente, e freq é a frequência (percentagem) com que ocorre.
class AssocOne(Association):
    def __init__(self, e1, assoc ,e2):
        Relation.__init__(self, e1, assoc, e2)

# Devolve a média dos valores locais.
class AssocNum(Association):
    def __init__(self, e1, assoc ,e2):
        num = float(e2)
        Relation.__init__(self, e1, assoc, e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)

#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica

class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista

class SemanticNetwork:
    def __init__(self,ldecl=[]):
        self.declarations = ldecl
    def __str__(self):
        return my_list2string(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)
    def query_local(self,user=None,e1=None,rel=None,e2=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) ]
        return self.query_result
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    # 1 - lista (dos nomes) das associações existentes.
    def list_associations(self):
        # Se for uma instancia de association
        return list(set([ d.relation.name for d in self.declarations if isinstance (d.relation, Association)]))

    # 2 - Lista das entidades declaradas como instâncias de tipos.
    def list_objects(self):
        # Se for uma instancia de member
        return list(set([o.relation.entity1 for o in self.declarations if isinstance(o.relation, Member)]))
    
    # 3 - lista de utilizadores existentes na rede
    def list_users(self):
        return list(set([u.user for u in self.declarations]))

    # 4 - lista de tipos existente na rede
    def list_types(self):
        return list(set([t.relation.entity2 for t in self.declarations if isinstance(t.relation, Member) or isinstance(t.relation, Subtype)]
        + [ t.relation.entity1 for t in self.declarations if isinstance(t.relation, Subtype)]))

    # 5 - lista (dos nomes) das associações localmente declaradas.
    def list_local_assocs(self, entidade):
        return list(set([d.relation.name for d in self.declarations if isinstance(d.relation, Association) 
                        and (d.relation.entity1 == entidade or d.relation.entity2 == entidade)] ))

    # 6 - lista (dos nomes) das relações por ele declaradas
    def list_self_relations(self, user):
        return list(set([d.relation.name for d in self.declarations if d.user == user]))
   
    # 7 - dado um utilizador, número de associações diferentes por ele utilizadas nas relações que declarou
    def count_association_user(self, user):
        return len(set([ d.relation.name for d in self.declarations if isinstance(d.relation, Association) and d.user == user ]))

    # 8 - dada uma entidade, devolva uma lista de tuplos, em que cada tuplo contém (o nome de) 
    # uma associação localmente declarada e o utilizador que a declarou
    def list_associations_entities(self, entity):
        return list(set([ (d.relation.name, d.user) for d in self.declarations 
                        if isinstance(d.relation, Association) and (d.relation.entity1 == entity or d.relation.entity2 == entity)  
                        ] ))
    # 9 - dadas duas entidades (dois tipos, ou um tipo e um objecto), 

    # devolva True se a primeira for predecessora da segunda, e False caso contrário.
    def predecessor(self, A, B):
        rel = [d.relation for d in self.declarations if (isinstance(d.relation, Member) or isinstance(d.relation, Subtype))
                and d.relation.entity1 == B]
        
        if [r for r in rel if r.entity1 == B and r.entity2 == A] != []:
            return True

        return any([self.predecessor(A, r.entity2) for r in rel])

    # 10 - dadas duas entidades (dois tipos, ou um tipo e um objecto), 
    # em que a primeira é predecessora da segunda, devolva uma lista composta pelas entidades 
    # encontradas no caminho desde a primeira até à segunda entidade. Caso a primeira entidade 
    # não seja predecessora da segunda, a função retorna None.
    def predecessor_path(self, A, B):
        # Subtype('mamifero','vertebrado') -> Subtype('homem','mamifero') -> Member('socrates','homem')

        # Predecessores diretos        
        direct_predecessor = [d.relation for d in self.declarations if (isinstance(d.relation, Member) or isinstance(d.relation, Subtype))
                and d.relation.entity1 == B]

        # Se for direto
        if [r for r in direct_predecessor if r.entity2 == A] != []:
            return [A,B]

        # Recursivamente continua a procura do caminho        
        for p in direct_predecessor:
            pp = self.predecessor_path(A, p.entity2)
            if pp:
                return pp + [B]
        # Se nao encontrar nenhum
        return None # Se n for predecessor
            
    # 11a - obter todas as declarações de associações locais ou herdadas por uma entidade. 
    # A função recebe como entrada a entidade e, opcionalmente, o nome da associação.
    def query(self, entity, association = None):
        inherited = [self.query(d.relation.entity2, association) for d in self.declarations if d.relation.entity1 == entity and 
                    (isinstance(d.relation, Member) or isinstance(d.relation, Subtype))]
        return [item for sublist in inherited for item in sublist] + [d for d in self.declarations 
                if d.relation.entity1 == entity and isinstance(d.relation, Association) and (association == None or d.relation.name == association)]

    # 11b - obter todas as declarações locais (incluindo Member e Subtype) ou herdadas (apenas Association)por uma entidade.
    def query2(self, entity, relation = None):
        inherited = [self.query2(d.relation.entity2, relation) for d in self.declarations if d.relation.entity1 == entity and 
                    (isinstance(d.relation, Member) or isinstance(d.relation, Subtype))]

        return [item for sublist in inherited for item in sublist
                if not (isinstance(item.relation, Member) or  isinstance(item.relation, Subtype))] + [d for d in self.declarations 
                if d.relation.entity1 == entity and (relation == None or d.relation.name == relation)]

    # 12 - associação está declarada numa entidade, a entidade não herdará essa associação das entidades predecessoras
    def query_cancel(self, entity, association):
        inherited = [self.query_cancel(d.relation.entity2, association) for d in self.declarations if d.relation.entity1 == entity and 
                    (isinstance(d.relation, Member) or isinstance(d.relation, Subtype))]
        
        local = [d for d in self.declarations if d.relation.entity1 == entity 
                and (association == None or d.relation.name == association)]
        
        local_rels = [l.relation.name for l in local]

        return [item for sublist in inherited for item in sublist if not item.relation.name in local_rels] + local

    # 13 - lista com todas as declarações dessa associação em entidades descendentes desse tipo
    def query_down(self, entity, association):
        descendents = [self.query_down(d.relation.entity1, association) for d in self.declarations if d.relation.entity2 == entity 
                        and (isinstance(d.relation, Member) or isinstance(d.relation, Subtype))]
        print('DESCENDENTS', descendents)
        return [item for sublist in descendents for item in sublist] + [d for d in self.declarations
                if d.relation.entity1 == entity and d.relation.name == association and isinstance(d.relation, Association)]

    # 14 - dado um tipo e (o nome de) uma associação, devolva o valor mais frequente dessa associação nas entidades descendentes.
    def query_induce(self, entity, association):
        c = Counter([d.relation.entity2 for d in self.query_down(entity, association)])
        # Se for vazio nem entra no for
        for m in c.most_common(1):
            return m[0]

    # 15 - consultas de valores das associações locais de uma dada entidade
    def query_local_assoc(self, entity, relation):
        # Vai buscar as locais
        local_decl = self.query_local(e1=entity, rel=relation)
        # Se existe local_decl, se n existir nada n faz sentido ir
        
        # AssocOne
        if len(local_decl) and isinstance(local_decl[0].relation, AssocOne):
            counter = Counter([l.relation.entity2 for l in local_decl])
            return [(e, c/len(local_decl)) for e,c in counter.most_common(1) ]
        
        # AssocNum        
        elif len(local_decl) and isinstance(local_decl[0].relation, AssocNum):
            return sum([l.relation.entity2 for l in local_decl])/len(local_decl)
        
        else:
            counter = Counter([l.relation.entity2 for l in local_decl])
            fsum = 0
            valfrq = []
            for e,c in counter.items():
                if fsum < 0.75:
                    valfrq.append((e,c/len(local_decl)))
                    fsum += c/len(local_decl)
            return valfrq

    # 16 - dada uma entidade, E, e (o nome de) uma associação, A, devolva o valor, V , dessa associação nessa entidade
    # - Se todas as declarações locais de A em E atribuem o mesmo valor, V , à associação, 
    #       então é retornado esse valor, não levando em conta os valores eventualmente herdados.
    # - Caso contrário, retorna-se o valor, V , que maximiza a seguinte função:
    #       F (E, A, V) = ( L(E, A, V) + H(E, A, V)) / 2
    #       . L(E, A, V) é a percentagem de declarações de V para A na entidade E
    #       . H(E, A, V) é a percentagem de declarações similares nas entidades predecessoras de E
    def query_assoc_value(self, entity, association):
        pass

# Funcao auxiliar para converter para cadeias de caracteres
# listas cujos elementos sejam convertiveis para
# cadeias de caracteres
def my_list2string(list):
   if list == []:
       return "[]"
   s = "[ " + str(list[0])
   for i in range(1,len(list)):
       s += ", " + str(list[i])
   return s + " ]"
    

