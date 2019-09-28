def optimize(exp): 
    
    etype = exp[0] 
    
    if etype == "binop":
        
        a = optimize(exp[1])
        op = exp[2]
        b = optimize(exp[3])

        # Try Arithmetic Laws
        if op == "*" and (a == ("number",0) or b == ("number",0)):
            
            return ("number",0) 
        
        elif op == "*" and a == ("number",1):
            
            return b
        
        elif op == "*" and b == ("number",1):
            
            return a
        
        elif op == "+" and a == ("number",0):
            
            return b
        
        elif op == "+" and b == ("number",0):
            
            return a
        
        elif op == "-" and a == b:
            
            return ("number",0)
        
        if a[0] == "number" and b[0] == "number":
            
            if op == "+":
                
                return ("number", a[1]+b[1])
            
            if op == "-":
                
                return ("number", a[1]-b[1])
                
            if op == "*":
                
                return ("number", a[1]*b[1])
        
        return ("binop",a,op,b)
            
    return exp 


zero            = ("number", 0.0) 
one             = ("number", 1.0) 
two             = ("number", 2.0) 
xerxes          = ("var","xerxes") # Kings and Queens of Persia and Macedonia
darius          = ("var","darius") 
antiochus       = ("var","antiochus") 
musa            = ("var","musa")   

def plus(a,b):
    
        return ("binop",a,"+",b) 
        
def minus(a,b):
    
        return ("binop",a,"-",b) 
        
def times(a,b):
    
        return ("binop",a,"*",b) 

exp1 = times(two,zero) 
print (optimize(exp1) == zero) 

exp2 = times(darius,minus(two,two))
print (optimize(exp2) == zero) 

exp3 = minus(plus(zero,plus(one,plus(two,zero))),two)
print (optimize(exp3) == one)

five = plus(two,plus(two,one))
exp4 = times(five,(plus(minus(musa,musa),plus(musa,zero))))
print (optimize(exp4) == ('binop', ('number', 5.0), '*', ('var', 'musa')))

big_exp = zero

for i in range(10):
    
        big_exp = ("binop",big_exp,"+",("number",i))
        
print (optimize(big_exp) == ("number", 45.0)) # 0+1+2+3+4+5+6+7+8+9
