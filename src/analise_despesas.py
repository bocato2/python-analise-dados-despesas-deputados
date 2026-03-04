
"""Projeto de análise de despesas parlamentares.

O script:
- lê dados CSV públicos da Câmara
- realiza agregações e análises
- identifica despesas atípicas (outliers)
- gera relatórios em CSV

Autor: Tiago Bocato
"""

import csv

def analisa_valor_br(s: str) -> float:
    if s is None:
        return 0.0
    s = s.strip()
    if s == "":
        return 0.0
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0

arquivo = "Ano-2026.csv"

with open(arquivo,"r",encoding="utf-8-sig",newline="") as f:
    leitor = csv.DictReader(f,delimiter=";")

    relatorio = {
    "ticket_medio":0.0,
    "total_registros": 0,
    "total_gasto": 0.0,

    "por_tipo": {},         ## txtDescricao -> soma vlrLiquido
    "por_deputado": {},     ## txNomeParlamentar -> soma vlrLiquido
    "por_partido": {},     # # sgPartido -> soma vlrLiquido
    "por_uf": {},          # # sgUF -> soma vlrLiquido
    "por_mes":{},

    "top_10_tipos": [],        # # lista de tuplas (tipo, valor)
    "top_10_deputados": [],     # lista de tuplas (deputado, valor)
    "top_10_fornecedores": [],

    "maior_despesa": {          # maior vlrLiquido individual
        "valor": 0.0,
        "deputado": None,
        "partido": None,
        "uf":None,
        "tipo": None,
        "fornecedor": None,
        "data": None
    },

    "outliers": []              # lista de registros "suspeitos"
}
    fornecedores = {}
    lista_out= list()
    valor_maior_despesa =float("-inf")
    for linha in leitor:
        relatorio["total_registros"] += 1
        valor = (float(analisa_valor_br(linha.get("vlrLiquido"))) or 0)
        relatorio["total_gasto"]+=valor
        #variaveis para agrupamento
        nome_deputado = (linha.get("txNomeParlamentar") or "").strip()#
        tipo_despesa = (linha.get("txtDescricao") or "").strip()#
        sigla_partido = (linha.get("sgPartido") or "LIDERANCA").strip() #
        fornecedor = (linha.get("txtFornecedor") or "").strip()
        data=linha.get("datEmissao")
        uf = (linha.get("sgUF") or "").strip()
        mes = (linha.get("numMes") or"")
        relatorio["por_tipo"][tipo_despesa] = relatorio["por_tipo"].get(tipo_despesa,0.0)+valor
        relatorio["por_deputado"][nome_deputado] = relatorio["por_deputado"].get(nome_deputado,0.0)+valor
        relatorio["por_partido"][sigla_partido] = relatorio["por_partido"].get(sigla_partido,0.0)+valor
        relatorio["por_uf"][uf]=relatorio["por_uf"].get(uf,0.0)+valor
        relatorio["por_mes"][mes]=relatorio["por_mes"].get(mes,0.0)+valor
        fornecedores[fornecedor]=fornecedores.get(fornecedor,0)+valor


        if valor > valor_maior_despesa:
            valor_maior_despesa=valor
            relatorio["maior_despesa"]={
                "valor":valor,
                "deputado":nome_deputado,
                "partido":sigla_partido,
                "uf":uf,
                "tipo":tipo_despesa,
                "fornecedor":fornecedor,
                "data":data
            }
        lista_out.append({"deputado":nome_deputado,"valor":valor,"tipo":tipo_despesa, "fornecedor":fornecedor})
    relatorio["top_10_tipos"]=sorted(relatorio["por_tipo"].items(), key=lambda x :x[1], reverse=True)[:10]
    relatorio["top_10_deputados"]=sorted(relatorio["por_deputado"].items(), key=lambda x :x[1],reverse=True)[:10] 
    relatorio["top_10_fornecedores"]=sorted(fornecedores.items(),key=lambda x :x[1],reverse=True)[:10]
    relatorio["ticket_medio"] = (relatorio['total_gasto']/relatorio['total_registros'] )
    for deputado in lista_out:
        if deputado["valor"]>relatorio["ticket_medio"]*10:
            relatorio["outliers"].append((deputado))
        

#print(relatorio)
#csv individual
with open("por_deputado.csv","w",newline="", encoding="utf-8") as f:
      
    writer = csv.writer(f)
    writer.writerow(["deputado","valor"])
    writer.writerows(relatorio["por_deputado"].items())

with open("por_partido.csv","w",encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["sigla","valor"])
    writer.writerows(relatorio["por_partido"].items())
#multiplos csv
relatorios_top_10 = {

    "top_10_deputados.csv":relatorio["top_10_deputados"],
    "top_10_fornecedores.csv":relatorio["top_10_fornecedores"]

}
for nome_arquivo, dados in relatorios_top_10.items():
    with open(nome_arquivo,"w",encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(["nome","valor"])
        writer.writerows(dados)


arquivo="outliers.csv"
with open(arquivo,"w",encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["deputado","valor","tipo","fornecedor"])
    writer.writerows(o.values() for o in relatorio["outliers"])



