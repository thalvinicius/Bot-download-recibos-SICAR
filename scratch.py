from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pathlib import Path
import csv
from tkinter import messagebox

##Desenvolvido por Thalles Vinicius



messagebox.showinfo('Processamento Iniciado', 'O download dos recibos foi iniciado...')

# abrir navegador e acessar o link
url_login = ('https://www.car.gov.br/#/intranet/acesso')

driver = Chrome()


driver.get(url_login)

driver.maximize_window()

# colocar usuário
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[2]/div[1]/div/div[2]/form/div[1]/input"))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[2]/div[1]/div/div[2]/form/div[1]/input"))).send_keys('user')

# colocar senha
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[2]/div[1]/div/div[2]/form/div[2]/input"))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[2]/div[1]/div/div[2]/form/div[2]/input"))).send_keys('password')

# clicar em logar
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[2]/div[1]/div/div[2]/form/div[3]/div[2]/input"))).click()

# selecionar gestor monitoramento
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[2]/div[1]/div/div[1]/div/div/div[2]/form/div[3]/div[2]/div[1]/label"))).click()

# entrar no gestor monitoramento
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div/div/button"))).click()

# entrar no modulo monitoramento
WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "/html/body/div[1]/div/a/div[2]/span"))).click()

# 1. abrir o arquivo
with open('seuarquivo.csv', "r") as origem:


    # 2. ler a tabela e verificar se o recibo já foi baixado na pasta
    tabela_reader = csv.reader(origem, delimiter=';')

    next(tabela_reader, None)

    for i, linha in enumerate(tabela_reader):

        if (linha[1] == ''):
            continue

        file_name = linha[1][0:2] + '-'+linha[1][2:9]+'-'+linha[1][9:]+'.pdf'
        path = Path("pasta_destino_download"+file_name)

        if path.is_file():
            continue

        print("Realizando download do Recibo: " + str(linha[1]))

        # digitar numero recibo
        time.sleep(5)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[2]/div[2]/div[1]/uib-accordion[2]/div/div/div/div[2]/div/form/div[1]/div[1]/div/input"))).send_keys(linha[1])

        # pesquisar numero recibo
        time.sleep(5)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[2]/div[2]/div[1]/uib-accordion[2]/div/div/div/div[2]/div/form/div[7]/span"))).click()

        # xpath do campo ação
        time.sleep(10)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id=\"dropdownMenu1\"]"))).click()

        # xpath da ação baixar recibo
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id=\"dropdownAcoes\"]/ul/li[2]/a"))).click()

        # xpath do campo limpar
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id=\"accordionPesquisaBasica\"]/div/div[2]/div/form/div[7]/a"))).click()
        
        # tempo de espera para carregamento do framework
        time.sleep(5)

        # adicionar infrmação na tabela resultado
        destino = open('resultado.csv', "a", newline='')

        file_name = linha[1][0:2] + '-'+linha[1][2:9]+'-'+linha[1][9:]+'.pdf'
        path = Path("pasta_destino_download"+file_name)

        if (path.is_file()):
            linha.insert(2, 'OK')

            tabela_writer = csv.writer(destino, delimiter=';')
            tabela_writer.writerow(linha)

        destino.close()

messagebox.showinfo('Processamento Finalizado', 'Recibos baixados com sucesso')