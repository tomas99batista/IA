def separar(lista):
    if lista == []:
        return [], []
    a,b = lista[0]
    la, lb = separar(lista[1:])
    
    return [a] + la, [b] + lb

def remove_e_conta(lista, elem):
    if lista == []:
        return [], 0
    
    l,c = remove_e_conta(lista[1:], elem)
    
    if lista[0] == elem:
        return l, c+1
    else:
        return [lista[0]] + l, c
    
    
l = [(1,'a'), (2, 'b'), (3, 'c'), (4,'d')]
l2 = [1,2,3,4,5, 3, 3]
print(separar(l))
print(remove_e_conta(l2, 3))