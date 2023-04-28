import ray
import boto3
import requests
import datetime

client = boto3.client('s3')
BUCKET_NAME = 'headlines-scrapc'


def capturar_html():
    url = 'https://www.eltiempo.com'
    url2 = 'https://www.elespectador.com'
    response = requests.get(url)
    response2 = requests.get(url2)
    html_file = f"{datetime.datetime.now().strftime('%Y-%m-%d')}.html"
    html_file2 = f"Es{datetime.datetime.now().strftime('%Y-%m-%d')}.html"
    client.put_object(Bucket=BUCKET_NAME, Key='raw/'+html_file, Body=response.content)
    client.put_object(Bucket=BUCKET_NAME, Key='raw/'+html_file2, Body=response2.content)
    
    
capturar_html()