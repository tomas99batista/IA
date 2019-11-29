def comprimento(lista):
    if lista == []:
        return 0
    return 1 + comprimento(lista[1:])

def sum(lista):
    if lista == []:
        return 0
    else:
        return lista[0] + sum(lista[1:])

def exists(lista, num):
    if lista == []:
        return False
    return lista[0] == num or exists(lista[1:], num)

def concatenation(lista1, lista2):
    if lista1 == []:
        return lista2
    if lista2 == []:
        return lista1
    lista1.append(lista2[0])
    return concatenation(lista1, lista2[1:])

def inverse(lista):
    if lista == []:
        return []
    return inverse(lista[1:]) + [lista[0]]


lista = [1,2,3,4,5]
lista2 = [6,7,8]
print(comprimento(lista))
print(sum(lista))
print(exists(lista, 4))
print(concatenation(lista,lista2))
print(inverse(lista))