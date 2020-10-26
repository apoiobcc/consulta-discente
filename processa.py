from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv, os

# Indices das colunas que apresentam comentarios sobre as sessões, atualizar de
# acordo com a consulta aplicada e indices impressos no terminal
COMENTARIO_REMOTO = 9
COMENTARIO_GERAL = 20
COMENTARIO_CONSULTA = 21

# Lista com os indices das colunas que são questões de multipla escolha
LISTA_MULTIPLA = [5, 6, 8]

def gen_plots(path, data, colunas):
    '''
    Gera um grafico de pizza para cada uma das questões da consulta
    '''

    # Criando um dicionario para cada coluna {chave->resposta, valor->contador}
    counter = [Counter() for i in range(len(colunas))]
    for i in range(len(colunas)):
        for row in data[colunas[i]].dropna():
            counter[i][row] += 1
    
    # Arrumando o contador para as questões de multipla escolha, colocar os 
    # indices delas na lista
    for i in LISTA_MULTIPLA:
        aux = Counter()
        for k in counter[i].keys():
            for nk in k.split(';'):
                aux[nk] += counter[i][k]
        counter[i] = aux

    # gerando os graficos para cada coluna
    for i in range(len(colunas)):

        # quebrando rotulos grandes em duas linha
        new_lbl = list(counter[i].keys())
        for j in range(len(new_lbl)):
            if (len(new_lbl[j]) < 50): continue
            pal = new_lbl[j].split(" ")
            new_lbl[j] = ' '.join(word for word in pal[:int(len(pal)/2)]) + '\n' + ' '.join(word for word in pal[int(len(pal)/2):])

        # modifique aqui para mudar o tamanho dos graficos
        fig, ax = plt.subplots(figsize=(15, 7))
        wedges, texts, autotexts = \
            plt.pie(counter[i].values(), labels=new_lbl, autopct='%1.1f%%', normalize=True)

        # quantidade e porcentagem dentro do grafico
        lst = list(counter[i].keys())
        sm = sum(counter[i].values())
        for j, a in enumerate(autotexts):
            amt = counter[i][lst[j]]
            a.set_text(str(amt) + ' (' + str(round(100.0*amt/sm, 2)) + '%)')

        # salvando
        plt.setp(autotexts, size=11, weight="bold")
        ax.set_title(colunas[i], wrap=True)
        plt.savefig(path + "/" + str(i) + '.png', dpi=200)
        plt.close()

def get_disc_colu(data):
    '''
    retorna uma lista com todas as displinas que foram avaliadas e outra lista 
    com as colunas do dataframe 
    '''
    colu = list(data.columns)
    disc = list(data[colu[1]].unique())
    return disc, colu

def processa(data, disciplinas, colunas):
    '''
    gera os graficos e outras coisas para cada disciplina
    '''
    cnt = 0
    for d in disciplinas:
        print("\n--- Generando: " + d)

        # dataframe reduzido só com essa disciplinas, data_disc
        data_disc = data[data[colunas[1]] == d]
        print('Numero de participações: ' + str(len(data_disc)))

        aux = d.split(' - ')
        aux.remove(aux[3])

        # nome do professor e da materia separados com '-'
        aux[0] = aux[0].replace(' ', '-')
        aux[-1] = aux[-1].replace(' ', '-')
        path = 'disciplinas/' + '_'.join(aux).replace(' ', '')
        
        # criando diretorio para a disciplina
        if not os.path.exists(path):
            os.mkdir(path)

        # nome da disciplina no markdown
        f = open(path + "/name.md", "w+")
        f.write("# " + d)
        f.close()

        # criando md para os comentarios sobre ensino romoto
        f = open(path + "/rmt_cmt.md", "w+")
        comentarios = data_disc[colunas[COMENTARIO_REMOTO]].dropna()
        for c in comentarios:
            f.write("- " + c + "\n")
        f.close()

        # criando md para os comentarios sobre ensino geral
        f = open(path + "/gen_cmt.md", "w+")
        comentarios = data_disc[colunas[COMENTARIO_GERAL]].dropna()
        for c in comentarios:
            f.write("- " + c + "\n")
        f.close()

        # criando md para os comentarios sobre a consulta
        f = open(path + "/con_cmt.md", "w+")
        comentarios = data_disc[colunas[COMENTARIO_CONSULTA]].dropna()
        for c in comentarios:
            f.write("- " + c + "\n")
        f.close()

        gen_plots(path, data_disc, colunas)
        print("Concluido!")
        cnt += 1

    return cnt

def main():
    '''
    rotina principal para o processamento
    '''

    # abrindo os resultados como um dataframe
    data = pd.read_csv("resultado.csv", delimiter=',')

    # nomes das disciplinas e rotulos das colunas
    disciplinas, colunas = get_disc_colu(data)

    # conferindo as disciplinas
    print('\n\n----- DISCIPLINAS')
    for i in range(len(disciplinas)):
        print(str(i) + ' -- ' + disciplinas[i])

    # conferindo as colunas
    print('\n\n----- COLUNAS')
    for i in range(len(colunas)):
        print(str(i) + ' -- ' + colunas[i])

    # criando diretorio para as disciplinas
    if not os.path.exists('disciplinas'):
        os.mkdir('disciplinas')

    # processando cada disciplina
    d_count = processa(data, disciplinas, colunas)

    if d_count == len(disciplinas):
        print("\n\nSUCESSO!!!!!!!!!!!!!!!!!!")

if __name__ == "__main__":
    main()