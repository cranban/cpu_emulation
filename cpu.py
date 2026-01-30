def g_not(a):
    return a^1

def g_and(a, b):
    return a & b

def g_or(a, b):
    return a | b

def g_xor(a, b):
    return a ^ b

def g_nor(a, b):
    return (a | b)^1

def g_nand(a, b):
    return (a & b)^1

def g_xnor(a, b):
    return (a ^ b)^1

while True:
    usr = input(
        "Enter two numbers and a logic gate in the format: a b gate\n"
        "To quit type exit\n"
    )

    if usr == "exit":
        break

    x = usr.split()

    a = int(x[0])
    b = int(x[1])
    gate = x[2]

    if gate == "not":
        print(g_not(a))

    elif gate == "and":
        print(g_and(a, b))

    elif gate == "or":
        print(g_or(a, b))

    elif gate == "xor":
        print(g_xor(a, b))

    elif gate == "nor":
        print(g_nor(a, b))

    elif gate == "nand":
        print(g_nand(a, b))

    elif gate == "xnor":
        print(g_xnor(a, b))

