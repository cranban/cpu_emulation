def g_not(a):
    return ~a

def g_and(a,b):
    return a&b

def g_or(a,b):
    return a|b

def g_xor(a,b):
    return a^b

def g_nor(a,b):
    return ~(a|b)

def g_nand(a,b):
    return ~(a&b)

def g_xnor(a,b):
    return ~(a^b)

while True:
    usr=input("Enter two numbers along with the logic gate you want to use in the following format: a b gate\n")
    print("To quit type exit")
    x=usr.split()
    
    if x[2]=="not":
        print(g_not(bin(int(x[0])),0))
    
    elif x[2]=="and":
        print(g_and(bin(int(x[0])),bin(int(x[1]))))
    
    elif x[2]=="or":
        print(g_or(bin(int(x[0])),bin(int(x[1]))))
    
    elif x[2]=="xor":
        print(g_xor(bin(int(x[0])),bin(int(x[1]))))
    
    elif x[2]=="nor":
        print(g_nor(bin(int(x[0])),bin(int(x[1]))))
    
    elif x[2]=="nand":
        print(g_nand(bin(int(x[0])),bin(int(x[1]))))
    
    elif x[2]=="xnor":
        print(g_xnor(bin(int(x[0])),bin(int(x[1]))))
       
    
    
    
