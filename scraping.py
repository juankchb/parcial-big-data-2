import boto3
import requests
from datetime import datetime


def f(url, header):
    bucket = 'headlines-scrapc'
    response = requests.get(url)
    html_url = response.content

    s3 = boto3.resource('s3')
    dt = datetime.now()
    date = dt.strftime('%Y-%m-%d')

    file_name = f'{header}/contenido-{date}.html'

    s3.Bucket(bucket).put_object(
        Key=file_name,
        Body=html_url,
    )

    print("Contenido guardado - " + file_name)


f('https://www.eltiempo.com/', 'tiempo')
f('https://www.elespectador.com/', 'espectador')