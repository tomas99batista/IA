def juntar(l1, l2):
    if l1 == [] or l2 == []:
        return []
    if len(l1) != len(l2):
        return None
    a = l1[0]
    b = l2[0]
    
    
l1 = [1,2,3,4,5]
l2 = [6,7,8]
print(juntar(l1, l2))
    