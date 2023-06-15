import re


text="""<div class="portfolio-description">
                        <p class="lead">Bunul gust și simplitatea culorii negre este întotdeauna &nbsp;alegere ta câștigătoare când vine vorba despre accesoriile pe care le asortezi ținutelor de zi sau de seară, însă neapărat în combinație cu alte culori. Am ales să realizăm un colier negru cu nuanțe argintii, deoarece culoarea argintie este culoarea înțelepciunii. Colierul negru-argintiu va inspira eleganță și stil, eficiență și profesionalism, senzualitate sau meditație.</p><table border="0" cellpadding="0" cellspacing="0" width="315" class="table table-sm"><tbody><tr height="19"><td height="19" width="192">Diametru</td><td width="123"><strong>15 cm</strong></td></tr><tr height="19"><td height="19">Dimensiune elemente</td><td><strong>30 mm</strong></td></tr><tr height="19"><td height="19">Nr. elemente</td><td><strong>5</strong></td></tr><tr height="19"><td height="19">Culoare</td><td><strong>Negru + argintiu</strong></td></tr><tr height="19"><td height="19">Material de bază</td><td><strong>Lemn</strong></td></tr><tr height="19"><td height="19">Culoare bază colier</td><td><strong>Argintiu</strong></td></tr><tr height="19"><td height="19">Finisaj</td><td><strong>Lucios</strong></td></tr></tbody></table>
                        <br>
                        <p class="lead">
                            <strong>
                                Livrarea produselor din stoc se face în maxim 2 zile lucrătoare.
                                Pentru comenzi speciale, vă rugăm să ne contactați.
                                Termenul de execuție (pentru produsele ce nu sunt în stoc) este de 2-4 zile lucrătoare.
                            </strong>
                        </p>
                    </div>"""

def extract_description(html):
    matches = re.findall(r'<p class="lead">(.*?)</p>', html, re.DOTALL)#extragem descrierile
    description=''
    if matches:
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
        values = re.split(r',|și|\+',match[1])#despartim valorile dupa "," "și" "+""
        values = [value.strip() for value in values]  #stergem spatii ramase
        values=[value.replace(" ","") for value in values]#stergem spatiile dintre valoare si unitatea de masura
        values=[value.capitalize() for value in values]
        data[characteristic] = values
    print(data)
    

extract_characteristics(text)