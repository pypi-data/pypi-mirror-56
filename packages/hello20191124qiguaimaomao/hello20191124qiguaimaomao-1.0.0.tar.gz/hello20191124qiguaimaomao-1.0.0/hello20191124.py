if(5>3):
    print("hello world")

movies=["THE holy grail","the dab","the dec"]
print(movies[0])
print(movies)
print(len(movies))
movies.append("fly me")
print(movies)
print(movies.pop())
movies.insert(1,1978)
movies.insert(3,1988)
movies.append(1999)
print(movies)
for m in movies:
    print(m)
count=0
while count<len(movies):
    print(movies[count])
    count=count+1
movies.append(["hello","myworld"])
for m in movies:
    if isinstance(m,list):
        for n in m:
            print(n)
    else:
        print(m)
movies[6].append(["last","first"])
print(movies)
def print_lol(the_list,needType=False,level=0):
    """a recursive functionprint list  """
    for item in the_list:
        if isinstance(item,list):
            print_lol(item,needType,level+1)
        else:
            if needType:
                for num in range(level):
                    print("\t",end='')                
            print(item)
print_lol(movies,True,0)
print_lol(movies)
            
    

