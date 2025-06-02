def GLUD_to_AFN():
    print("something")


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
        
        print(lines[0])
        GLUD[lines[0]] = P.copy()
        string = ""            
        P.clear()
        catch = False
        tam = 0
                             
    return GLUD

#------------------------------------------------------------------
# Main Function 
file_path = input("Digite o nome do arquivo:\n")
gramatic = ler_arquivo(file_path)
print(gramatic)


    