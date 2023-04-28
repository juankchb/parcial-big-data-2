import boto3
import datetime
from bs4 import BeautifulSoup

# Create a boto3 S3 client
client = boto3.client('s3')

def lambda2():
    # Create a boto3 S3 resource
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('headlines-scrapc')
    
    # Get an object from the specified bucket
    obj = bucket.Object("raw/"+f"{datetime.datetime.now().strftime('%Y-%m-%d')}.html")
    
    # Read the contents of the file and parse it with BeautifulSoup
    body = obj.get()['Body'].read()
    soup = BeautifulSoup(body, 'html.parser')
    properties = soup.find_all('div', {'class': 'article-details'})
    properties2 = soup.find_all('div', {'class': 'category-published'})
    data = []

    for property, property2 in zip(properties, properties2):
        category = property2.find('a', {'class': lambda x: x and 'category' in x.split()})
        if category is not None:
            category_text = category.string.strip()
        else:
            category_text = ''

        title = property.find('a', {'class': 'title page-link'})
        link = title['href']
        title_text = title.string.strip()
        data.append(f"{category_text},{title_text},{link}") # Append as a formatted string
    
    # Create the contents of the CSV file
    s = "Categoria,Titular,Enlace\n"
    for fila in data:
        s += fila + "\n"
    
    # Save the CSV file to an S3 bucket
    client.put_object(Body=s.encode('utf-8'), Bucket='parcial2definitivo', Key=f"periodico=ElTiempo/year={datetime.datetime.now().strftime('%Y')}/month={datetime.datetime.now().strftime('%m')}/day={datetime.datetime.now().strftime('%d')}.csv")

# Call the lambda2 function
lambda2()

def lambda3():
    # Create a boto3 S3 resource
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('headlines-scrapc')
    # Get an object from the specified bucket
    obj = bucket.Object("raw/"+f"Es{datetime.datetime.now().strftime('%Y-%m-%d')}.html")
    # Read the contents of the file and parse it with BeautifulSoup
    body = obj.get()['Body'].read()
    soup = BeautifulSoup(body, 'html.parser')
    properties = soup.find_all('div', {'class': 'Card-Container'})
    data = []

    for property in properties:
        category_element = property.find('h4', {'class': 'Card-Section Section'})
        if category_element is not None:
            category_link = category_element.find('a')
            if category_link is not None:
                category = category_link.text.strip()
            else:
                category = ''
                continue
        else:
            category = ''
            continue
        print("Esto es: ", category)
        title = property.find('h2', {'class': 'Card-Title Title Title'})
        link = property.find('a', {'href': lambda x: x in x.split()})
        if title is not None:
            title_text = title.string.strip()
        else:
            title_text = ''

        if link is not None:
            link_text = link['href']
        else:
            link_text = ''

        data.append(f"{category},{title_text},{link_text}")

    s = "Categoria,Titular,Enlace\n"
    for fila in data:
        s += fila + "\n"
    # Save the CSV file to an S3 bucket
    client = boto3.client('s3')
    client.put_object(Body=s.encode('utf-8'), Bucket='parcial2definitivo', Key=f"periodico=ElEspectador/year={datetime.datetime.now().strftime('%Y')}/month={datetime.datetime.now().strftime('%m')}/day={datetime.datetime.now().strftime('%d')}.csv")

# Call the lambda3 function
lambda3()