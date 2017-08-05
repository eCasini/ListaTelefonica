# Carrega os dados do arquivo dados.json
import json
import sqlite3

fileHandle = open("dados.json")
dados = ""
for line in fileHandle:
    dados += str(line)
# print(dados)
info = json.loads(dados)
con = sqlite3.connect("ListaTelDB.sqlite")
cur = con.cursor()
for lista in info:
    # print(lista[0])
    nomeArea = lista[0]
    ramalArea = lista[1]
    cur.execute('INSERT OR IGNORE INTO Area (nome, ramal) VALUES (?, ?)', (nomeArea, ramalArea))
    # print(lista[1])
    con.commit()
    # pega o ID referente ao nome da ultima área inserida
    cur.execute('SELECT id FROM Area WHERE nome = ? ', (nomeArea, ))
    area_id = cur.fetchone()[0]
    for subarea in lista[2]:
        # print(subarea[0])
        nomeSubArea = subarea[0]
        ramalSubArea = subarea[1]
        cur.execute('INSERT OR IGNORE INTO SubArea (nome, ramal, area_id) VALUES (?, ?, ?)', (nomeSubArea, ramalSubArea, area_id))
        # print(subarea[1])
        con.commit()
