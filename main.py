# To do
#
# Caso a pasta de destino já exista na hora de copiar uma pasta, o script dá erro e não copia os arquivos diferentes

import os
import shutil
import re

def extrair_nome_arquivo(caminho):
    # Expressão regular para extrair o nome do arquivo
    padrao = r'[^\\/:*?"<>|\r\n]+\.([^\\/:*?"<>|\r\n]+)$'
    # Procurar o padrão na string
    resultado = re.search(padrao, caminho)
    if resultado:
        return resultado.group(0)
    else:
        return None

def encontrar_arquivo(nome_arquivo):
    # Obtém o diretório AppData do usuário local
    appdata_dir = os.getenv('APPDATA')

    if appdata_dir:
        # Constrói o caminho completo para o arquivo
        caminho_arquivo = os.path.join(appdata_dir, 'LouvorJA', nome_arquivo)
        
        # Verifica se o arquivo existe
        if os.path.exists(caminho_arquivo):
            return caminho_arquivo
        else:
            return None
    else:
        return None

def copiar_arquivo(origem, destino):
    if os.path.isfile(origem): # Se for arquivo na hora de copiar
        try:
            shutil.copyfile(origem, destino)
            print("Copiado " + origem)
            return True
        except shutil.SameFileError:
            print("Arquivo já pronto " + origem)
            return True
        except Exception as e:
            print(f"Erro ao copiar o arquivo: {e}")
            return False
    elif os.path.isdir(origem): #Se for pasta na hora de copiar
        try:
            shutil.copytree(origem, destino)
            print("Copiado " + origem)
            return True
        except shutil.SameFileError:
            print("Pasta já pronta " + origem)
            return True
        except Exception as e:
            print(f"Erro ao copiar a pasta: {e}")
            return False


def processar_arquivo(arquivo):
    novo_conteudo = []
    caminho_liturgia = "C:\\liturgia\\temp"

    with open(arquivo, 'r') as arquivo_original:
        for linha in arquivo_original:
            if linha.startswith("subitem=Arquivo"):
                # Altera o caminho
                linha = "subitem=Arquivo C:\\liturgia\\" + extrair_nome_arquivo(linha) + "\n"
            elif linha.startswith("subitem=Pasta"):
                # Altera o caminho
                linha = "subitem=Pasta C:\\liturgia\\" + linha.replace("subitem=Pasta ", "").split(os.path.sep)[-2] + "\\\n"
            elif linha.startswith("dir="):
                # Copia o arquivo para "C:\liturgia" e altera o caminho
                caminho_origem = linha.split('=')[1].strip()
                nome_arquivo = os.path.basename(caminho_origem)
                if os.path.isfile(caminho_origem):
                    novo_caminho = os.path.join("C:\\liturgia\\temp", nome_arquivo)
                else:
                    novo_caminho = "C:\\liturgia\\temp\\" + caminho_origem.split(os.path.sep)[-2]
                
                if copiar_arquivo(caminho_origem, novo_caminho):
                    linha = f"dir={novo_caminho}\n"

            novo_conteudo.append(linha)

    # Escreve o novo conteúdo de volta no arquivo
    with open(arquivo, 'w') as arquivo_modificado:
        arquivo_modificado.writelines(novo_conteudo)

    # Copia o arquivo liturgia.ja para a pasta C:\liturgia
    destino_liturgia = os.path.join(caminho_liturgia, os.path.basename(arquivo))
    shutil.copyfile(arquivo, destino_liturgia)

# Nome do arquivo que você quer acessar
nome_arquivo = 'liturgia.ja'

pasta_liturgia = "C:\\liturgia\\temp"

if not os.path.exists (pasta_liturgia) :
    os.makedirs (pasta_liturgia)

# Encontra o caminho completo do arquivo
caminho_arquivo = encontrar_arquivo(nome_arquivo)

if caminho_arquivo:
    # Processa o arquivo
    processar_arquivo(caminho_arquivo)
    print("Processamento concluído.")
else:
    print("O arquivo não foi encontrado.")
