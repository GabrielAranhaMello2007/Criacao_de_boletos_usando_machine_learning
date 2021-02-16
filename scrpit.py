from selenium import webdriver
import pandas as pd
import time


email_login = ''
email_senha = ''
arquivo_word = ''  # Aqui vai a lista aonde você quer gerar os boletos
clientes_df = pd.read_excel(arquivo_word, dtype={'Cliente': object})  


driver = webdriver.Chrome()
driver.get('https://acesso.pagseguro.uol.com.br/')

driver.find_element_by_id('user').send_keys(email_login)  # modifique aqui com seu email
driver.find_element_by_id('password').send_keys(email_senha)  # modifique aqui com sua senha
time.sleep(5)
driver.find_element_by_xpath('//*[@id="__next"]/div/div/main/div/div/div/form/div/div/div/div/div[3]/button').click()

no = input('Enter para continuar')

while len(driver.find_elements_by_id('menu')) == 0:
    time.sleep(10)

for linha in clientes_df.index:
    divida = clientes_df.loc[linha, 'Valor Total Devido'] - clientes_df.loc[linha, 'Valor Pago']
    if divida > 0:
        driver.get('https://pagseguro.uol.com.br/operations/charging.jhtml')
        email = clientes_df.loc[linha, 'Email']
        driver.find_element_by_xpath('//*[@id="newRequestForm"]/div[1]/section[1]/div/fieldset[1]/input').send_keys(
            email)
        nome = clientes_df.loc[linha, 'Nome']
        driver.find_element_by_xpath('//*[@id="newRequestForm"]/div[1]/section[1]/div/fieldset[2]/input').send_keys(
            nome)
        driver.find_element_by_xpath('//*[@id="newRequestForm"]/div[1]/section[2]/div/fieldset[1]/input').send_keys(
            'Cobrança pagamento atrasado')

        valor = divida
        texto_valor = f'{valor:.2f}'
        driver.find_element_by_xpath('//*[@id="newRequestForm"]/div[1]/section[2]/div/fieldset[2]/div/input').send_keys(
            texto_valor)
        driver.find_element_by_id('sendNewCharging').click()

        time.sleep(2)
