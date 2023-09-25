import re

def extract_description(html):
    matches = re.findall(r'<p class="lead">(.*?)</p>', html, re.DOTALL)#extragem descrierile
    description=''
    if matches is not None:
        for match in matches:
            cleaned_text = match.split('\n', 1)[0].strip()#excludem partea cu livrarea
            description+=cleaned_text
        return description
    else:
        print("No matches found.")


def extract_characteristics(html):
    pattern = r'<td.*?>(.*?)<\/td><td.*?><strong>(.*?)</strong><\/td>'#extragem caracteristicile si valorile
    matches = re.findall(pattern, html)

    data = {}
    for match in matches:
        characteristic = match[0].strip()
        if(characteristic=='Nr. elemente'):
            characteristic='Număr elemente'
        values = re.split(r',|și|\+| |  ',match[1])#despartim valorile dupa "," "și" "+""
        values = [value.strip() for value in values]  #stergem spatii ramase
        values=[value.replace(" ","") for value in values]#stergem spatiile dintre valoare si unitatea de masura
        values=[value.replace("mm","") for value in values]
        values=[value.replace("cm","") for value in values]
        
        values = [value.split('&')[0] for value in values]
        
        values=list(filter(None,values))
        values=[value.capitalize() for value in values]
        data[characteristic] = values
    return data
    

