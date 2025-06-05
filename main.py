import pandas as pd 
import numpy as np
from collections import deque
import os

# Essa função é responsável por receber uma cadeia e verificar se ela pertence a linguagem reconhecida pelo automato.
# Recebe o numero de cadeias que vão ser processadas, o conjunto de transições, o estado inicial e o conjunto de estados finais.
# A lógica é: Se ele encontrar a tupla (estado atual, simbolo), o estado atual recebe o resultando até que toda cadeia seja consumida.
# No final ele verifica se o estado de parada é um estado final
def verifica_cadeia(num_cadeias, transicoes, q0, F):
    for i in range(1, num_cadeias + 1):
        atual = q0
        cadeia = input("Digite a cadeia: ")
        for caractere in cadeia:
            tam = 0
            for items in transicoes:
                if atual == items[0] and caractere == items[1]:
                    atual = items[2]
                    break
                if tam == len(transicoes)-1 and (atual != items[0] and caractere != items[1]):
                    print("Cadeia Rejeitada - não há transições")
                    return
                tam+=1
        
        if atual in F:
            print("Cadeia Aceita :)")
        else:
            print 
            print("Cadeia Rejeitada - não antingiu um estado final")       
        
# ------------------------------------------------------------------------------------       
        
# Função para criar os arquivos de saídas 
# Cria uma pasta chamda outputs para colocar os arquivos dentro
# Recebe o nome do arquivo e o automato que será escrito
def cria_arquivo(nome, automato):
    if not os.path.exists("output"):
        os.makedirs("output")
    with open(nome, 'w') as file:
        # Escrevendo os estados
        file.write(f"Q: {', '.join(automato['Q'])}\n")
        
        # Escrevendo o alfabeto
        file.write(f"alfabeto: {', '.join(automato['alfabeto'])}\n")
        
        # Escrevendo as transições
        file.write("transicoes:\n")
        for origem, simbolo, destino in automato['transicoes']:
            file.write(f"{origem}, {simbolo} -> {destino}\n")
            
        # Escrevendo estado inicial
        file.write(f"q0: {automato['q0']}\n")
        
        # Escrevendo estados finais
        file.write(f"F: {', '.join(automato['F'])}\n")
            
# ------------------------------------------------------------------------------------

# Faz a operação de complemento do automato
# Transforma os estados finais em estados não finais e vice-versa
def complemento(AFD):
    # Recebe uma cópia dos estados do automato 
    novo_F = AFD["Q"].copy()
    
    # Retira os estados finais
    for state in AFD["F"]:
        novo_F.remove(state)
    
    # Torna os estados não finais em finais 
    AFD["F"] = novo_F
    
    cria_arquivo("output/complemento_ADF.txt", AFD)
    print("Arquivo do complemento criado!")
    
# ------------------------------------------------------------------------------------

def reverso(AFD):
    transicoes = AFD["transicoes"]
    aux: object
    
    # Reverte as transições do automato 
    for items in transicoes:
        aux = items[0]
        items[0] = items[2]
        items[2] = aux
    
    # Se houver mais de um estado final, ao fazer o reverso haverá um conjunto de estados iniciais. Isso precisa ser tratado.
    if len(AFD["F"]) != 1:
        aux = AFD["q0"]
        AFD["q0"] = "INICIO"
        for state in AFD["F"]:
            transicoes.append(["INICIO", '&', state])
        AFD["F"] = [aux]
    # Se não apenas inverta os dois
    else:
        aux = AFD["q0"]
        AFD["q0"] = AFD["F"]
        AFD["F"] = aux
    
    cria_arquivo("output/reverso_ADF.txt", AFD)
    print("Arquivo do reverso criado!")
    
# ------------------------------------------------------------------------------------

def AFND_to_AFD(Q, alfabeto, transicoes, q0, F):
    # Este bloco trata as transições vazia e adiciona estados gerados pro e-fechos
    for lines in transicoes:
        if lines[1] == "&":
            for items in transicoes:
                if items[2] == lines[0]:
                    items[2] = lines[0] + lines[2]
                    if lines[0] + lines[2] not in Q:
                        Q.append(lines[0] + lines[2])
            transicoes.remove(lines)
    
    # Remove o a possibilidade do vazio na máquina 
    if "&" in alfabeto:
        alfabeto.remove("&")
    
    # Cria um DataFrame para a visualização da transformação do AFND em AFD
    df = pd.DataFrame(index=alfabeto, columns=Q, dtype=object)
    visitados = []
    fila = deque()
    fila.append(q0)
    
    # - DFS para somente abrir estados que já foram acessados por outros 
    # - A partir do estado inicial, adiciona as transições dos estados, adiciona estados compostos (resultantes do não-determinismo)
    #   no Data Frame, e vai fazendo esse caminho até que a fila fique vazia e todos os estados tenham sido visitados.
    while fila:
        # Tratamento para estado simples {A, B, C, S, Z}
        if len(fila[0]) == 1:
            for lines in transicoes:
                if fila[0] == lines[0]:
                    if pd.isna(df.loc[lines[1], fila[0]]):
                        df.loc[lines[1], fila[0]] = lines[2]
                    else:
                        df.loc[lines[1], fila[0]] += lines[2]
                        if df.loc[lines[1], fila[0]] not in Q:
                            Q.append(df.loc[lines[1], fila[0]])
                            df[df.loc[lines[1], fila[0]]] = np.nan
                        
                    if df.loc[lines[1], fila[0]] not in fila:
                        if df.loc[lines[1], fila[0]] not in visitados:
                            fila.append(df.loc[lines[1], fila[0]])
                            
        # Tratamento para estados compostos {AB, SAZ, SC, BZ}
        else:
            for state in fila[0]:
                for lines in transicoes:
                    if state == lines[0]:
                        if pd.isna(df.loc[lines[1], fila[0]]):
                            df.loc[lines[1], fila[0]] = lines[2]
                            if df.loc[lines[1], fila[0]] not in Q:
                                Q.append(df.loc[lines[1], fila[0]])
                                df[df.loc[lines[1], fila[0]]] = np.nan
                        else:
                            df.loc[lines[1], fila[0]] += lines[2]
                            if df.loc[lines[1], fila[0]] not in Q:
                                Q.append(df.loc[lines[1], fila[0]])
                                df[df.loc[lines[1], fila[0]]] = np.nan
                                
                        if df.loc[lines[1], fila[0]] not in fila:
                            if df.loc[lines[1], fila[0]] not in visitados:
                                fila.append(df.loc[lines[1], fila[0]])
        
        visitados.append(fila.popleft())
        # print(f"fila: {fila}")
        # print(f"visitados: {visitados}")
    # Visualização da tabela de transições
    print("Tabela de transições)")
    print(df)
    print("\n")
    # Retira colunas não abertas 
    df = df.dropna(axis=1, how="all")   
    print("Retirando estados não atingidos)")
    print(df)
    
    Q2 = []
    transicoes2 = []
    F2 = []
    # Captura as informações do Data Frame
    for columns in df.columns:
        Q2.append(columns)
        for caractere in columns:
            if caractere in F:
                F2.append(columns)
                break
    # Captura as informações do Data Frame
    for state in Q2:
        for caractere in alfabeto:
            if pd.isna(df.loc[caractere, state]):
                continue
            else:
                transicoes2.append([state, caractere, df.loc[caractere, state]])
    # Estrutura o DFA
    M2 = {
        "Q": Q2,
        "alfabeto": alfabeto,
        "transicoes": transicoes2,
        "q0": q0,
        "F": F2
    }
    
    cria_arquivo("output/ADF.txt", M2)
    
    return M2
               
# ------------------------------------------------------------------------------------

def GLUD_to_AF(G):
    M = {
        "Q": [],
        "alfabeto": [],
        "transicoes": [],
        "q0": "",
        "F": ["Z"],
    }
    
    transicoes = []
    
    for lines in G.keys():
        # Define o primeiro não-terminal encontrado como estado inicial
        if len(M["q0"]) == 0:
            M["q0"] = lines
        
        # Adiciona o não-terminal ao conjunto de estados, se ainda não estiver
        if lines not in M["Q"]:
            M["Q"].append(lines)
        
        # Percorre as produções associadas a esse não-terminal
        for items in G[lines]:
            if len(items) == 1:
                # Caso seja um terminal (minúscula, dígito ou '&' para vazio)
                if items.islower() or items == "&" or items.isdigit():
                    transicoes.append([lines, items, "Z"])
                    if items not in M["alfabeto"]:
                        M["alfabeto"].append(items) 
                        
                # Caso seja um não-terminal (letra maiúscula)      
                elif items.isupper():
                    transicoes.append([lines, "&", items])
                    if items not in M["Q"]:
                        M["Q"].append(items)
            # Se a produção possui 2 símbolos (terminal seguido de não-terminal)
            elif len(items) == 2:
                transicoes.append([lines, items[0], items[1]])
                if items[0] not in M["alfabeto"]:
                    M["alfabeto"].append(items[0])
                    
    # Garante que o estado final 'Z' sempre estará presente no conjunto de estados
    M["Q"].append("Z")
    M["transicoes"] = transicoes
    
    cria_arquivo("output/AFND.txt", M)
    
    return M
    
# ------------------------------------------------------------------------------------

# Ler o arquivo que contém a Gramática Linear Unitária a Direita
def ler_arquivo(path):
    folder = "gramaticas/"
    folder += path
    with open(folder, "r", encoding="utf-8") as file:
        G = file.readlines()
        gramatic = []
        for lines in G: 
           gramatic.append(lines.replace("| ", "").replace("-> ", ":").strip()) 
           
    GLUD = {}
    P = []
    catch = False
    string = ""
    tam = 0
    # Loop para formatar a Gramática retirada do arquivo.txt em um dicionário
    for lines in gramatic:
        for item in lines:
            if tam == (len(lines) - 1):
                string += item
                P.append(string)
                break
            
            if item == ":" :
                catch = True
                tam+=1
                continue
                
            if catch :
                if item != " " :
                    string += item
                else:
                    P.append(string)
                    string = ""
                    
            tam+=1
        
        GLUD[lines[0]] = P.copy()
        string = ""            
        P.clear()
        catch = False
        tam = 0
                             
    return GLUD

#------------------------------------------------------------------
# Main Function
print("\nBEM VINDO/A À SIMULAÇÃO DE AUTOMATOS")
file_path = input("Digite o nome do arquivo:\n")
gramatic = ler_arquivo(file_path)

print("-"*40)
print("Você entrou a Gramática Linear a Direita:")
print(gramatic)

print("-"*40)

print("Autômato Finito gerado:")
AF = GLUD_to_AF(gramatic)
for keys, values in AF.items():
       print(f"{keys}: {values}")
       
print("-"*40)

print("Transformação do AF em AFD:")
AFD = AFND_to_AFD(AF["Q"], AF["alfabeto"], AF["transicoes"], AF["q0"], AF["F"])
print("\nADF)")
for keys, values in AFD.items():
       print(f"{keys}: {values}")
       
print("-"*40)

print("Testando cadeias:")
num_cadeias = input("Digite a quantidade de cadeias que quer testar: ")
verifica_cadeia(int(num_cadeias),AFD["transicoes"], AFD["q0"], AFD["F"])

print("-"*40)
complemento(AFD.copy())
reverso(AFD.copy())

print ('- Verifique a pasta "output"')

