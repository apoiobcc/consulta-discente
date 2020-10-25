from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import csv, os

def gen_plots(path, data, labels):
    '''
    generate pie plots for each question of CDE
    '''

    # one dictionary for each column to count each answer
    counter = [Counter() for i in range(len(labels))]
    for row in data:
        for i in range(len(labels)):
            counter[i][row[i]] += 1

    # fixing counter for multiple choice questions
    for i in [7, 8, 10]:
        aux = Counter()
        for k in counter[i].keys():
            for nk in k.split(';'):
                aux[nk] += counter[i][k]
        counter[i] = aux

    # generating plots for each column
    for i in range(len(labels)):
        # breaking big labels in 2 lines
        new_lbl = list(counter[i].keys())
        for j in range(len(new_lbl)):
            if (len(new_lbl[j]) < 50): continue
            pal = new_lbl[j].split(" ")
            new_lbl[j] = ' '.join(word for word in pal[:int(len(pal)/2)]) + '\n' + ' '.join(word for word in pal[int(len(pal)/2):])

        # modify this to change plot size
        fig, ax = plt.subplots(figsize=(15, 7))
        wedges, texts, autotexts = \
            plt.pie(counter[i].values(), labels=new_lbl, autopct='%1.1f%%')

        # amount and porcentage inside pie
        lst = list(counter[i].keys())
        sm = sum(counter[i].values())
        for j, a in enumerate(autotexts):
            amt = counter[i][lst[j]]
            a.set_text(str(amt) + ' (' + str(round(100.0*amt/sm, 2)) + '%)')

        plt.setp(autotexts, size=11, weight="bold")
        ax.set_title(labels[i], wrap=True)
        plt.savefig(path + "/" + str(i) + '.png', dpi=200)
        plt.close()

def get_disc_label():
    '''
    return list of distinct discplines and labels of csv
    '''
    # file with cde results, direct from forms
    file = csv.reader(open("results.csv", "r", encoding='utf-8'))
    disc = []
    lbl = None
    for row in file:
        if lbl == None: 
            lbl = row
            continue
        disc.append(row[1])
    disc = list(set(disc))
    return disc, lbl

def process_each(disciplines):
    '''
    generates graphs and other stuff for each discipline
    '''
    cnt = 0
    for d in disciplines:
        print("generating: " + d)

        # file with cde results, direct from forms
        file = csv.reader(open("results.csv", "r", encoding='utf-8'))

        path = d[:23].replace(' ', '-')
        # create subfolder
        if not os.path.exists(path):
            os.mkdir(path)

        # name of discipline to be appended in md
        f = open(path + "/name.txt", "w+")
        f.write("# " + d)
        f.close()

        # only rows of discipline d
        data = []
        for row in file:
            if row[1] != d: continue
            data.append(row)

        # comments about remote in col 11, to be appendend in md
        f = open(path + "/rmt_cmt.txt", "w+")
        for row in data:
            if len(row[11]) > 0:
                f.write("- " + row[11] + "\n")
        f.close()

        # general comments in column 22, to be appendend in md
        f = open(path + "/gen_cmt.txt", "w+")
        for row in data:
            if len(row[22]) > 0:
                f.write("- " + row[22] + "\n")
        f.close()

        gen_plots(path, data, labels)
        print("generated: " + d)
        cnt += 1
    
    return cnt

# discipline names list and columns labelss
disciplines, labels = get_disc_label()

# getting index for each column
for i in range(len(labels)):
    print(str(i) + ' -- ' + labels[i])

# counter for each discipline, sanity check
d_count = process_each(disciplines)

if d_count == len(disciplines):
    print("SUCESS!!!!!!!!!!!!!!!!!!")