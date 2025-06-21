import logging
import pandas as pd

from sqlalchemy import text
from helpers import engine, envio


def flash_padrao(comando_sql: str, flash_title: str = "FLASH ...", chat_name: str = "Sla"):
    with engine.begin() as conn:
        data = conn.execute(text(comando_sql)).fetchall()
    df = pd.DataFrame(data)

    try:
        mensagem = f'*{flash_title}*\n\n'
        for index in df.index:
            for col in df.columns:
                mensagem += f"{col}: {df[col][index]}\n"
            mensagem += '\n'
    except:
        mensagem = f'Falha na QUERY {flash_title}'

    logging.warning(mensagem[:20])

    enviado = envio(chat_name, mensagem)

    logging.warning('flash_padrao (%s): %s', chat_name, enviado) 


def flash_personalizado_pinbet():
    chat_name = 'Flash Pinbet'
    with engine.connect() as conn:
        result = conn.execute(text("CALL proc_flash_whatsapp_15min;")).fetchall()

    dict_helper = {}
    parametros_monetarios = [
        "Lucro (GGR)",
        "GGR Esporte",
        "GGR Cassino",
        "Depósitos",
        "Saque cliente",
        "Subtotal",
        "Saque afiliado",
        "Resultado",
        "FTD Total VR",
        "FTD DIA VR",
        "FTD RETENÇÃO VR",
    ]
    parametros_percentuais = [
        "FTD DIA QTD %",
        "FTD DIA %",
        "FTD RETENÇÃO %",
        "FTD DIA VR %",
        "FTD RETENÇÃO VR %",
    ]
    parametros_inteiros = [
        "FTD RETENÇÃO QTD",
        "TOTAL Cadastros do dia",
        "FTD Total QTD",
        "FTD DIA QTD",
    ]
    for data, hr, parametro, valor in result:
        valor_ajustado = round(valor, 2)
        if parametro in parametros_monetarios:
            if valor < 0:
                valor_ajustado = str(valor_ajustado).replace(
                    ".", ","
                ).replace('-', '')
                dict_helper[parametro] = "-R$ " + valor_ajustado
            else:
                dict_helper[parametro] = "R$ " + str(valor_ajustado).replace(".", ",")
        elif parametro in parametros_percentuais:
            dict_helper[parametro] = str(valor_ajustado) + "%"
        elif parametro in parametros_inteiros:
            dict_helper[parametro] = int(valor_ajustado)
        else:
            print(f"Parametro {parametro} nao cadastrado!")

    mensagem = f"""FLASH WTS 15 min 
PINBET 
POR DIA (Horário: {hr})

Lucro (GGR) {dict_helper['Lucro (GGR)']}
GGR Esporte {dict_helper['GGR Esporte']}
GGR Cassino {dict_helper['GGR Cassino']}

----
Depósitos: {dict_helper['Depósitos']}
Saque cliente: {dict_helper['Saque cliente']}
Subtotal: {dict_helper['Subtotal']}
Saque afiliado: {dict_helper['Saque afiliado']} Analisar
Resultado: {dict_helper['Resultado']}  DEP - TODOS OS SAQUES 
----

TOTAL Cadastros do dia : {dict_helper['TOTAL Cadastros do dia']}  
-----
FTD Total QTD: {dict_helper['FTD Total QTD']}
FTD DIA QTD {dict_helper['FTD DIA QTD']}
FTD DIA QTD % - ({dict_helper['FTD DIA %']} sobre o total FTD)
FTD RETENÇÃO QTD {dict_helper['FTD RETENÇÃO QTD']} ({dict_helper['FTD RETENÇÃO %']} sobre o total FTD)

FTD DEP TOTAL {dict_helper['FTD Total VR']}
FTD DIA  DEP {dict_helper['FTD DIA VR']} ({dict_helper['FTD DIA VR %']} sobre o total FTD)
FTD RETENÇÃO DEP {dict_helper['FTD RETENÇÃO VR']} ({dict_helper['FTD RETENÇÃO VR %']} sobre o total FTD)

----"""

    enviado = envio(chat_name, mensagem)

    logging.warning("%s - %s", chat_name, enviado)