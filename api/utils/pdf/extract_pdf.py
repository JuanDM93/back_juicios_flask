from pathlib import Path
from tika import parser # pip install tika
import requests

filename = Path('metadata.pdf')
url = 'https://www.poderjudicialcdmx.gob.mx/wp-content/PHPs/boletin/boletin_repositorio/140220201.pdf'
response = requests.get(url)
filename.write_bytes(response.content)

raw = parser.from_file('metadata.pdf')

text = raw['content']

x = text.find("PRIMERA SALA FAMILIAR")
print(x)

y = text.find("SEGUNDA SALA FAMILIAR")
print(y)

primera_sala_civil = text[x:y]

demandas = primera_sala_civil.split("\n\n")

for demanda in demandas:
    print(demanda)
    print("--------------------------------------")
    