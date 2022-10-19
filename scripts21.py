def check(n):
    if type(n) == int:
        return(n)
    if "Валет" in n.lower():
        return 2
    if "Дама" in n.lower():
        return 3
    if "Король" in n.lower():
        return 4
    if "Туз" in n.lower():
        return 11