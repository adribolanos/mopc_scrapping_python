from requests_html import HTMLSession
import pprint
import pandas as pd

session = HTMLSession()

headers = {
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}

r = session.get('https://tembiapo.mopc.gov.py/', verify=False, headers=headers)

script = r.html.xpath('//script')[1].text
parts = script.split(",")
urls = []

for part in parts:
     if part.startswith(" url"):
            urls.append(part)
urls2 = []
for link in urls:
    link = link.replace("constructions.push", "")
    link = link.split(";")
    for l in link:
        if l.startswith(" url"):
            l = l.replace(" url: ", "")
            l = l.replace("})", "")
            l = l.replace("'", "")
            urls2.append(l)
            print(l)

result = []
for elemento in urls2:
    columns = {}
    r = session.get('https://tembiapo.mopc.gov.py' + elemento, verify=False, headers=headers)
    campo = r.html.find('#info .form-group')
    for e in campo:
        key = e.find('label', first=True).text
        value = e.find('p', first=True).text
        columns[key] = value
        result.append(columns)

pprint.pprint(result)
df = pd.DataFrame(
            result, columns=['Nombre', 'Tipo', 'Estado', 'Departamento - Ciudad', 'Información Adicional','Contratista', 'Extension de la Obra', 'Localidades Beneficiadas', 'Fecha de Inicio', 'Fecha de Finalización','Plazo de Ejecución (en meses)', 'Avance', 'Fuente de Financiación'])
df.to_csv('result.csv', index=False)


