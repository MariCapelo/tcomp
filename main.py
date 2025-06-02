def ler_arquivo(path):
    with open(path, "r", encoding="utf-8") as file:
        G = file.readlines()
        gramatic = []
        for lines in G: 
           gramatic.append(lines.replace(" ->", ":").strip()) 

    return gramatic


file_path = input("Digite o nome do arquivo:\n")
gramatic = ler_arquivo(file_path)
print(gramatic)