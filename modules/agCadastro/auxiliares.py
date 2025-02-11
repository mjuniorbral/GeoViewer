# Função Auxiliar

def subStrings(string):
    """Retorna todas as combinações de substrings dentro de uma string.

    Args:
        string (_str_): Palavra ou frase a ser analisada
    """
    if type(string)!=str:
        raise Exception("Erro no tipo do argumento string")
    
    comb = []
    for i in range(len(string)):
        for j in range(len(string)):
            comb.append(string[i:j+1])
    retorno = []
    for i in comb:
        if not (i in retorno):
            retorno.append(i)
    return sorted(retorno)

def pegarNomeMaisProximo(nome,lista):
    """Compara nome com lista de nomes.
    Retorna o item da lista mais póximo do nome.

    Args:
        nome (_str_): nome sendo buscado
        lista (_list_): lista com o escopo de busca
    """
    nomeMaisProximo = ""
    proximidade = 0
    for item in lista:
        if nome == item:
            return item
        else:
            cont=0
            nomeAtual = ""
            for i in subStrings(item):
                for j in subStrings(nome):
                    if str.upper(i)==str.upper(j):
                        cont+=1
                        nomeAtual=i
            if cont>proximidade:
                nomeMaisProximo=nome
                proximidade=cont
    return nomeMaisProximo

def printList(lista):
    """Printar todo o conteúdo da lista um embaixo do outro.

    Args:
        lista (_list_): lista de objetos
    """
    for i in lista:
        print(i)
    return

def listStrVazias (n):
    """Criar uma lista com n strings vazias ("")

    Args:
        n (_int_): tamanho da lista
    """
    retorno = []
    if n==0:
        return []
    else:
        for i in range(n):
            retorno.append("")
    return retorno

def inverterDicio(dicio):
    """Retornar uma relação um dicionário.

    Args:
        dicio (_dict_): Dicionário de uma função não injetora. Pode ser sobrejetora ou não.
    """
    retorno = {}
    for i in dicio:
        if dicio[i] in retorno:
            retorno[dicio[i]].append(i)
        else:
            retorno[dicio[i]]=[i]
    return retorno

def list1DtoDicio(listaDeChaves,entrada=None):
    """Transformar uma lista de keys em um dicionário

    Args:
        listaDeChaves (_list_): Lista de Chaves para o novo dicionário
        entrada (_ _): Objeto a ser adicionado como valor para cada chave
    """
    retorno = {}
    for i in listaDeChaves:
        retorno[i]=entrada
    return retorno