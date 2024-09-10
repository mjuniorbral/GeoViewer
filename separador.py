sep = ","
try:
    with open("AGLBRPINC02(7).csv") as arquivo:
        for line in arquivo.readlines():
            if line[0]=="-":
                newLine = []
                cont = 0
                for c in line:
                    if c == sep:
                        cont+=1
                        if cont%2==0:
                            newLine.append(";")
                        else:
                            newLine.append(c)
                        continue
                    newLine.append(c)
                print("".join(newLine),end="")
            else:
                print(line.replace(",",";"),end="")
                
finally:
    arquivo.close()