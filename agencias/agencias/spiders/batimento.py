import os 
import scrapy
from pathlib import Path
from urllib.parse import urlparse

def verificar_apagar_arquivo(nome_arquivo):
    if os.path.exists(nome_arquivo):
        os.remove(nome_arquivo)
        print(f"O arquivo '{nome_arquivo}' foi apagado.")
    else:
        with open(nome_arquivo, 'a') as f:
            print(f"O arquivo '{nome_arquivo}' foi criado.")

class BatimentoSpider(scrapy.Spider):
    name = "batimento"

    dicionario_batimento = {}

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
        CAMINHO_HREF = "//section[contains(@class, 'row')]//a//@href"
        CAMINHO_TEXT = "//section[contains(@class, 'row')]//a//text()"

        urls_cidades = response.xpath(CAMINHO_HREF).getall()
        nome_logico = [i.split('/')[3] for i in response.xpath(CAMINHO_HREF).getall()]
        qtd = [i[-2] for i in response.xpath(CAMINHO_TEXT).getall()]

        for i in range(len(urls_cidades)):
            cidade = nome_logico[i] + ' (' + qtd[i] + ')'
            self.dicionario_batimento[cidade] = {}
            yield scrapy.Request(url=response.urljoin(urls_cidades[i]), callback=self.parse_bairros, meta={'cidade': cidade})

    def parse_bairros(self, response):
        cidade = response.meta.get('cidade')
        CAMINHO_HREF = "//div[contains(@class, 'site-index')]//div[contains(@class, 'row')]//ul//a//@href"
        CAMINHO_TEXT = "//div[contains(@class, 'site-index')]//div[contains(@class, 'row')]//ul//a//text()"

        url_bairros = response.xpath(CAMINHO_HREF).getall()
        nome_logico = [i.split('/')[4] for i in response.xpath(CAMINHO_HREF).getall()]
        qtd = [i[-2] for i in response.xpath(CAMINHO_TEXT).getall()]

        for i in range(len(url_bairros)):
            bairro = nome_logico[i] + ' (' + qtd[i] + ')'
            self.dicionario_batimento[cidade][bairro] = {}
            yield scrapy.Request(url=response.urljoin(url_bairros[i]), callback=self.parse_bancos, meta={'cidade': cidade, 'bairro': bairro})

    def parse_bancos(self, response):
        cidade = response.meta.get('cidade')
        bairro = response.meta.get('bairro')
        CAMINHO_HREF = "//div[contains(@class, 'site-index')]//ul//a//@href"
        CAMINHO_TEXT = "//div[contains(@class, 'site-index')]//ul//a//text()"

        url_bancos = response.xpath(CAMINHO_HREF).getall()
        nome_logico = [i.split('/')[5] for i in response.xpath(CAMINHO_HREF).getall()]
        qtd = [i[-2] for i in response.xpath(CAMINHO_TEXT).getall()]

        for i in range(len(url_bancos)):
            banco = nome_logico[i] + ' (' + qtd[i] + ')'
            self.dicionario_batimento[cidade][bairro][banco] = []
            yield scrapy.Request(url=response.urljoin(url_bancos[i]), callback=self.parse_agencias, meta={'cidade': cidade, 'bairro': bairro, 'banco': banco})

    def parse_agencias(self, response):
        cidade = response.meta.get('cidade')
        bairro = response.meta.get('bairro')
        banco = response.meta.get('banco')
        CAMINHO_HREF = "//div[contains(@class, 'site-index')]//ul//a//@href"
        CAMINHO_TEXT = "//div[contains(@class, 'site-index')]//ul//a//text()"

        url_agencias = response.xpath(CAMINHO_HREF).getall()
        nome_agencias = response.xpath(CAMINHO_TEXT).getall()

        for i in range(len(url_agencias)):
            agencia = nome_agencias[i]
            self.dicionario_batimento[cidade][bairro][banco].append(agencia)

    def closed(self, reason):
        print('Scraping concluído.')
        print('dicionario_batimento:')
        print(self.dicionario_batimento)

        # Lista para armazenar os dados
        dados = []

        # Iterar sobre o dicionário para descompactar os dados
        for cidade, bairros in self.dicionario_batimento.items():
            for bairro, bancos in bairros.items():
                for banco, agencias in bancos.items():
                    for agencia in agencias:
                        dados.append((cidade, bairro, banco, agencia))

        import pandas as pd

        verificar_apagar_arquivo("./dados/batimento.csv")
        df = pd.DataFrame(dados, columns=['CIDADE', 'BAIRRO', 'BANCO', 'AGENCIA'])
        df.to_csv("./dados/batimento.csv", index=False)
        print('salvou')
