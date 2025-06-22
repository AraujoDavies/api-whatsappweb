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


def flash_personalizado_weebet(chat_name: str, comando_sql: str):
    with engine.connect() as conn:
        result = conn.execute(text(comando_sql)).fetchall()

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
    parametros_emoji = [
        "Lucro (GGR)",
        "Resultado",
    ]
    parametros_percentuais = [
        "FTD DIA QTD %",
        "FTD DIA %",
        "FTD RETENÇÃO %",
        "FTD DIA VR %",
        "FTD RETENÇÃO VR %",
        "Taxa de conversão",
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
            valor_formatado = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            emoji = ''
            if valor < 0:
                if parametro in parametros_emoji:
                    emoji = '🔻'
                valor_formatado = str(valor_formatado).replace('-', '')
                dict_helper[parametro] = "-R$ " + valor_formatado + emoji
            else:
                if parametro in parametros_emoji:
                    emoji = '🟡' if valor == 0 else '🔹'                   
                dict_helper[parametro] = "R$ " + str(valor_formatado) + emoji

        elif parametro in parametros_percentuais:
            dict_helper[parametro] = str(round(valor_ajustado)) + "%"

        elif parametro in parametros_inteiros:
            dict_helper[parametro] = int(valor_ajustado)

        else:
            print(f"Parametro {parametro} nao cadastrado!")

    mensagem = f"""*Resultado GGR* {dict_helper['Lucro (GGR)']} 
GGR Esporte {dict_helper['GGR Esporte']}
GGR Cassino {dict_helper['GGR Cassino']}

----

*Resultado DEP-SAQ-AF* {dict_helper['Resultado']}
Depósitos: {dict_helper['Depósitos']}
Saque cliente: {dict_helper['Saque cliente']}
Subtotal: {dict_helper['Subtotal']}
Saque afiliado: {dict_helper['Saque afiliado']} 

----

TOTAL Cadastros do dia : {dict_helper['TOTAL Cadastros do dia']}  ({dict_helper['Taxa de conversão']}) Taxa conversão FTD

-----

*FTD Total QTD* {dict_helper['FTD Total QTD']}
FTD DIA QTD: {dict_helper['FTD DIA QTD']} ({dict_helper['FTD DIA %']})
FTD RETENÇÃO QTD: {dict_helper['FTD RETENÇÃO QTD']} ({dict_helper['FTD RETENÇÃO %']})

*FTD DEP TOTAL* {dict_helper['FTD Total VR']}
FTD DIA DEP: {dict_helper['FTD DIA VR']} ({dict_helper['FTD DIA VR %']})
FTD RETENÇÃO DEP: {dict_helper['FTD RETENÇÃO VR']} ({dict_helper['FTD RETENÇÃO VR %']})

----"""

    enviado = envio(chat_name, mensagem)

    logging.warning("%s - %s", chat_name, enviado)