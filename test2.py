from bs4 import BeautifulSoup
from datetime import datetime
import boto3
import csv
import json

s3 = boto3.client('s3')

dt = datetime.now()
year = dt.year
month = dt.month
day = dt.day

date = dt.strftime('%Y-%m-%d')

file_name = f'contenido-{date}.csv'

eltiempo = 'https://www.eltiempo.com'
elespectador = 'https://www.elespectador.com'

response_eltiempo = s3.get_object(
    Bucket='headlines-scrapc',
    Key=f'tiempo/contenido-{date}.html'
)

response_elespectador = s3.get_object(
    Bucket='headlines-scrapc',
    Key=f'espectador/contenido-{date}.html'
)

html_eltiempo = response_eltiempo['Body'].read().decode('utf-8')
html_elespectador = response_elespectador['Body'].read().decode('utf-8')


def procesing_eltiempo(html, filename):

    soup = BeautifulSoup(html, 'html.parser')
    headlines = soup.find_all("h3",class_="title-container")
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['categoria', 'titular', 'enlace'])
        for headline in headlines:
            title = headline.text.strip()
            headless_link = headline.find("a")["href"]
            category = headless_link.split('/')[1]
            full_link = f'{eltiempo}{headless_link}'
            csv_writer.writerow([category, title, full_link])

    with open(filename, 'r') as csv_file:
        s3.put_object(
            Bucket='parcial2definitivo',
            Key=f'tiempo/year{year}/month{month}/day{day}/{filename.split(".")[0]}.csv',
            Body=csv_file.read()
        )

    return print("Contenido guardado - El tiempo" + filename)


def procesing_elespectador(html, filename):
    soup = BeautifulSoup(html, 'html.parser')
    headlines = soup.find_all("h2", class_="Card-Title Title Title")

    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['categoria', 'titular', 'enlace'])
        for headline in headlines:
            title = headline.text.strip()
            headless_link = headline.find("a")["href"]
            category = headless_link.split('/')[1]
            full_link = f'{elespectador}{headless_link}'
            csv_writer.writerow([category, title, full_link])

    with open(filename, 'r') as csv_file:
        s3.put_object(
            Bucket='parcial2definitivo',
            Key=f'elespectador/year{year}/month{month}/day{day}/{filename.split(".")[0]}.csv',
            Body=csv_file.read()
        )

    return print("Contenido guardado - El Espectador " + filename)
    
    
procesing_eltiempo(html_eltiempo, file_name)
procesing_elespectador(html_elespectador, file_name)
