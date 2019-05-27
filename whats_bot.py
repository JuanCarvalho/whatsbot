from selenium import webdriver
import os
from time import sleep


class zapbot:
    # O local de execução do nosso script
    dir_path = os.getcwd()
    # O caminho do chromedriver
    chromedriver = os.path.join(dir_path, "chromedriver.exe")
    # Caminho onde será criada pasta profile
    profile = os.path.join(dir_path, "profile", "wpp")

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # Configurando a pasta profile, para mantermos os dados da seção
        self.options.add_argument(
            r"user-data-dir={}".format(self.profile))
        # Inicializa o webdriver
        self.driver = webdriver.Chrome(
            self.chromedriver, chrome_options=self.options)
        # Abre o whatsappweb
        self.driver.get("https://web.whatsapp.com/")
        # Aguarda alguns segundos para validação manual do QrCode
        self.driver.implicitly_wait(15)

    def ultima_msg(self):
        """ Captura a ultima mensagem da conversa """
        try:
            post = self.driver.find_elements_by_class_name("_3_7SH")
            ultimo = len(post) - 1
            # O texto da ultima mensagem
            texto = post[ultimo].find_element_by_css_selector(
                "span.selectable-text").text
            return texto
        except Exception as e:
            print("Erro ao ler msg, tentando novamente!")

    def envia_msg(self, msg):
        """ Envia uma mensagem para a conversa aberta """
        try:
            sleep(2)
            # Seleciona acaixa de mensagem
            self.caixa_de_mensagem = self.driver.find_element_by_class_name("_2S1VP")
            # Digita a mensagem
            self.caixa_de_mensagem.send_keys(msg)
            sleep(1)
            # Seleciona botão enviar
            self.botao_enviar = self.driver.find_element_by_class_name("_35EW6")
            # Envia msg
            self.botao_enviar.click()
            sleep(2)
        except Exception as e:
            print("Erro ao enviar msg", e)

    def envia_media(self, fileToSend):
        """ Envia media """
        try:
            # Clica no botão adicionar
            self.driver.find_element_by_css_selector("span[data-icon='clip']").click()
            # Seleciona input
            attach = self.driver.find_element_by_css_selector("input[type='file']")
            # Adiciona arquivo
            attach.send_keys(fileToSend)
            sleep(3)
            # Seleciona botão enviar
            send = self.driver.find_element_by_xpath("//div[contains(@class, 'yavlE')]")
            # Clica no botão enviar
            send.click()
        except Exception as e:
            print("Erro ao enviar media", e)

    def abre_conversa(self, contato):
        """ Abre a conversa com um contato especifico """
        try:
            # Seleciona a caixa de pesquisa de conversa
            self.caixa_de_pesquisa = self.driver.find_element_by_class_name("jN-F5")
            # Digita o nome ou numero do contato
            self.caixa_de_pesquisa.send_keys(contato)
            sleep(2)
            # Seleciona o contato
            self.contato = self.driver.find_element_by_xpath("//span[@title = '{}']".format(contato))
            # Entra na conversa
            self.contato.click()
        except Exception as e:
            raise e


bot = zapbot()
bot.abre_conversa("+55 11 99999-9999")
bot.envia_msg("Olá, sou o bot whatsapp! Para receber ajuda digite: /help")
imagem = bot.dir_path + "/imagem.jpg"
msg = ""
while msg != "/quit":
    sleep(1)
    msg = bot.ultima_msg()
    if msg == "/help":
        bot.envia_msg("""Bot: Esse é um texto com os comandos válidos:
            /help (para ajuda)
            /mais (para saber mais)
            /quit (para sair)
            """)
    elif msg == "/mais":
        bot.envia_media(imagem)
    elif msg == "/quit":
        bot.envia_msg("Bye bye!")
