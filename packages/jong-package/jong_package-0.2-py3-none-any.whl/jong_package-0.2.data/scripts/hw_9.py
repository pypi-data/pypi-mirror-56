import pandas as pd 
df = pd.read_csv('test1112.csv')
var_1 = df['Var1']
var_2 = df['Var2']
n = len(var_1)
for i in range(n):
    d1 = ((3-var_1)**2 + (3-var_2)**2)**(1/2)
    d2 = ((11-var_1)**2 + (11-var_2)**2)**(1/2)
    d3 = ((25-var_1)**2 + (25-var_2)**2)**(1/2)
    if d1 < d2 and d1 < d3:
        print(d1, "is the smallest")
    elif d2 < d1 and d2 < d3:
        print(d2, "is the smallest")
    else:
        print(d3, "is the smallest") 

