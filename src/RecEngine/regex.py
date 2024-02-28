import re
import threading

def extract_description(html):
    matches = re.findall(r'<p class="lead">(.*?)</p>', html, re.DOTALL)#extragem descrierile
    description=''
    for match in matches:
            cleaned_text = match.split('\n', 1)[0].strip()#excludem partea cu livrarea
            description+=cleaned_text
    return description
   

def extract_characteristics_timeout(html_content,):
    if(len(html_content)>10000):
        return "Content too long"
    result = timeout_wrapper(extract_characteristics, (html_content,), 10000)
    if result is None:
        return "Timeout Reached"
    else:
        return result
    


def extract_characteristics(html):
    pattern = r'<td.*?>(.*?)<\/td><td.*?><strong>(.*?)</strong><\/td>'#extragem caracteristicile si valorile
    matches = re.findall(pattern, html)

    data = {}
    for match in matches:
        characteristic = match[0].strip()
        if(characteristic=='Nr. elemente'):
            characteristic='Număr elemente'
        values = re.split(r',|și|\+| | {2}',match[1])#despartim valorile dupa "," "și" "+""
        values = [value.strip() for value in values]  #stergem spatii ramase
        values=[value.replace(" ","") for value in values]#stergem spatiile dintre valoare si unitatea de masura
        values=[value.replace("mm","") for value in values]
        values=[value.replace("cm","") for value in values]
        
        values = [value.split('&')[0] for value in values]
        
        values=list(filter(None,values))
        values=[value.capitalize() for value in values]
        data[characteristic] = values
    return data

def timeout_wrapper(func, args, timeout):
    result = [None]
    def wrap():
        result[0] = func(*args)
    thread = threading.Thread(target=wrap)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        return None  # Return None if timeout is reached
    return result[0]  # Otherwise, return the result
    

