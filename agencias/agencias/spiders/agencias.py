import os 
import scrapy
from pathlib import Path
from urllib.parse import urlparse

def verificar_apagar_arquivo(nome_arquivo):
    if os.path.exists(nome_arquivo):
        os.remove(nome_arquivo)
        print(f"O arquivo '{nome_arquivo}' foi apagado.")
    else:
        with open(nome_arquivo, mode='w', encoding='utf-8') as f:
            print(f"O arquivo '{nome_arquivo}' foi criado.")

class AgenciasSpider(scrapy.Spider):
    name = "agencias"

    verificar_apagar_arquivo("./dados/brasil.csv")
    with open("./dados/brasil.csv", mode='a', encoding='utf-8') as arquivo:
        arquivo.write(f'LINK;NOME')

    def start_requests(self):

        urls = [
              'https://agenciasbanco.com.br/agencias/ac/'
            #,'https://agenciasbanco.com.br/agencias/mg/'
            #,'https://agenciasbanco.com.br/agencias/rj/'
            #,'https://agenciasbanco.com.br/agencias/rs/'
            #,'https://agenciasbanco.com.br/agencias/pr/'
            #,'https://agenciasbanco.com.br/agencias/ba/'
            #,'https://agenciasbanco.com.br/agencias/sc/'
            #,'https://agenciasbanco.com.br/agencias/go/'
            #,'https://agenciasbanco.com.br/agencias/pe/'
            #,'https://agenciasbanco.com.br/agencias/pa/'
            #,'https://agenciasbanco.com.br/agencias/ce/'
            #,'https://agenciasbanco.com.br/agencias/es/'
            #,'https://agenciasbanco.com.br/agencias/df/'
            #,'https://agenciasbanco.com.br/agencias/ma/'
            #,'https://agenciasbanco.com.br/agencias/mt/'
            #,'https://agenciasbanco.com.br/agencias/ms/'
            #,'https://agenciasbanco.com.br/agencias/pb/'
            #,'https://agenciasbanco.com.br/agencias/rn/'
            #,'https://agenciasbanco.com.br/agencias/am/'
            #,'https://agenciasbanco.com.br/agencias/se/'
            #,'https://agenciasbanco.com.br/agencias/al/'
            #,'https://agenciasbanco.com.br/agencias/pi/'
            #,'https://agenciasbanco.com.br/agencias/ro/'
            #,'https://agenciasbanco.com.br/agencias/to/'
            #,'https://agenciasbanco.com.br/agencias/sp/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_cidades)

    def parse_cidades(self, response):
        
        urls_cidades = response.xpath("//section[contains(@class, 'row')]//a//@href").getall()
        for cidade in urls_cidades:

            #print(response.urljoin(url))
            yield scrapy.Request(url=response.urljoin(cidade), callback=self.parse_bairos)

    def parse_bairos(self, response):

        url_bairros = response.xpath("//div[contains(@class, 'site-index')]//div[contains(@class, 'row')]//ul//a//@href").getall()
        for bairro in url_bairros:

            #print(response.urljoin(bairro))
            yield scrapy.Request(url=response.urljoin(bairro), callback=self.parse_bancos)
        
    def parse_bancos(self, response):

        url_bancos = response.xpath("//div[contains(@class, 'site-index')]//ul//a//@href").getall()
        for banco in url_bancos:

            #print(response.urljoin(bairro))
            yield scrapy.Request(url=response.urljoin(banco), callback=self.parse_agencias)

    def parse_agencias(self, response):

        url_agencias = response.xpath("//div[contains(@class, 'site-index')]//ul//a//@href").getall()
        for agencia in url_agencias:

            #print(response.urljoin(agencia))
            yield scrapy.Request(url=response.urljoin(agencia), callback=self.get_data)

    def get_data(self, response):

        agencia = response.xpath("//h1[contains(@class, 'h3 form-group')]//text()").get()
        banco = response.xpath("//h1[contains(@class, 'h3 form-group')]//small//text()").get()
        nome = banco + ' ' + agencia

        #print(f'NOME: \n{nome}')

        #print('\n\n\nRESPOSTA')
        #print(response.urljoin(''))

        with open("./dados/brasil.csv", mode='a', encoding='utf-8') as arquivo:
            arquivo.write(f"""\n{response.urljoin('')};{nome}""")











        