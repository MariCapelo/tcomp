import pandas as pd 
import numpy as np
from collections import deque

def AFND_to_AFD(Q, alfabeto, transicoes, q0, F):
    for lines in transicoes:
        if lines[1] == "&":
            for items in transicoes:
                if items[2] == lines[0]:
                    items[2] = lines[0] + lines[2]
                    if lines[0] + lines[2] not in Q:
                        Q.append(lines[0] + lines[2])
            transicoes.remove(lines)
    
    if "&" in alfabeto:
        alfabeto.remove("&")
    
    df = pd.DataFrame(index=alfabeto, columns=Q)
    visitados = []
    fila = deque()
    fila.append(q0[0])
    while fila:
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
        
    print(df)          
               
# ------------------------------------------------------------------------------------

def GLUD_to_AF(G):
    M = {
        "Q": [],
        "alfabeto": [],
        "transicoes": [],
        "q0": [],
        "F": ["Z"],
        "isAFN": False
    }
    
    transicoes = []
    
    for lines in G.keys():
        if len(M["q0"]) == 0:
            M["q0"].append(lines)
            
        if lines not in M["Q"]:
            M["Q"].append(lines)
            
        for items in G[lines]:
            if len(items) == 1:
                if items.islower() or items == "&" or items.isdigit():
                    transicoes.append([lines, items, "Z"])
                    if items not in M["alfabeto"]:
                        M["alfabeto"].append(items) 
                      
                elif items.isupper():
                    M["isAFN"] = True
                    transicoes.append([lines, "&", items])
                    if items not in M["Q"]:
                        M["Q"].append(items)
            
            elif len(items) == 2:
                transicoes.append([lines, items[0], items[1]])
                if items[0] not in M["alfabeto"]:
                    M["alfabeto"].append(items[0])
                M["isAFN"] = True
    M["Q"].append("Z")
    M["transicoes"] = transicoes
    return M
    
# ------------------------------------------------------------------------------------

def ler_arquivo(path):
    with open(path, "r", encoding="utf-8") as file:
        G = file.readlines()
        gramatic = []
        for lines in G: 
           gramatic.append(lines.replace("| ", "").replace("-> ", ":").strip()) 
           
    GLUD = {}
    P = []
    catch = False
    string = ""
    tam = 0
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
print(AFD)