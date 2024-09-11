def separador(path_csv,sep=","):
    out_lines = []
    try:
        with open(path_csv) as arquivo:
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
                    out_lines.append("".join(newLine),end="")
                else:
                    out_lines.append(line.replace(",",";"),end="")
                    
    finally:
        arquivo.close()
    return "\n".join(out_lines)