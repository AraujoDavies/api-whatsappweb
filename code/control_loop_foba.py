# while True:
#     engine = db_mysql()
#     with engine.begin() as c:
#         disparadores_ativos = c.execute(text('select * from tbl_cadastro_whatsapp where status = "H";')).fetchall()
#     engine.dispose()

#     for disparador in disparadores_ativos:
#         id = disparador[0]
#         whatsapp_chat_name = disparador[1]
#         titulo_da_mensagem = disparador[2]
#         comando_sql_para_coletar_dados = disparador[3]
#         renomear_as_colunas = disparador[4]
#         exibir_as_colunas = disparador[5]
#         schedule = disparador[6]
#         ultima_extracao = disparador[8]

#         atende_tempo_schedule = False
#         tempo_ultima = "PRIMEIRO ENVIO"
#         if ultima_extracao != None:
#             diferenca_ultima_extracao = datetime.datetime.now() - ultima_extracao
#             atende_tempo_schedule = diferenca_ultima_extracao.total_seconds() / 60 > schedule
#             tempo_ultima = int(round(diferenca_ultima_extracao.seconds / 60, 0))
#         logging.warning(f"{whatsapp_chat_name} - atende tempo de schedule: {atende_tempo_schedule} Tempo desde a última extração {tempo_ultima} Min.")

#         if ultima_extracao == None or atende_tempo_schedule:
#             # rotina
#             if disparador_whats(
#                     driver,
#                     whatsapp_chat_name,
#                     titulo_da_mensagem,
#                     comando_sql_para_coletar_dados,
#                     renomear_as_colunas,
#                     exibir_as_colunas
#                     ):
#                 # se disparador for true atualiza data de ultimo envio
#                 update_dtExtracao(id)
#     driver.quit()
