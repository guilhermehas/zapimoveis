def fileToString(fname):
    with open(fname) as f:
        content = f.readlines()
    content = ''.join(content)
    return content


def getUrlVector(url):
    fc = url.find('''"pagina":"''')+len('''"pagina":"''')
    for i, it in enumerate(url[fc:]):
        if it not in '1234567890':
            break

    return [url[:fc],url[fc+i:]]


s1 = fileToString('scriptjs.js')

s2 = 'return (function () {\n' \
     '%s\n' \
     ' })()' % (s1)



from pyvirtualdisplay import Display
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

display = Display(visible=0, size=(800, 600))
display.start()

#capabilities = DesiredCapabilities.CHROME
#capabilities['loggingPrefs'] = { 'browser':'ALL' }

#driver = webdriver.Chrome(desired_capabilities=capabilities)

def saveInExcel(vet,outfile='out'):
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active

    for it in vet:
        ws.append(it)
    wb.save(outfile+'.xls')

vtotal = []
global vtotal

def getPage(fname, url):
    print(fname)
    urlv = getUrlVector(url)

    messages = ""
    i = 1
    messageAnt = []
    while True:
        print("\tPagina {} ".format(i),end="")
        try:
            driver = webdriver.Firefox()

            urln = urlv[0]+str(i)+urlv[1]

            driver.get(urln)
            message = driver.execute_script(s2)
            
            if not message or message in messageAnt:
                break

            messageAnt.append(message)
            if len(messageAnt) > 5:
                messageAnt.pop(0)

            messages += message
        except:
            print("Erro!")
            pass
        print()
        i += 1
        driver.close()


    def messagesToVet(text):
        vet = []
        texts = text.splitlines()
        st = set()
        for it in texts:
            v1 = it.split(';')
            v1 = v1[(len(v1)>5):]
            if ' a ' in v1[-1]:
                v1[-1] = sum(map(int,v1[-1].split(' a ')))//2
            vshape = tuple(v1)
            if vshape not in st:
                vet.append(v1)
            st.add(vshape)

        return vet

    vet = messagesToVet(messages)
    global vtotal
    vtotal += vet
    saveInExcel(vet,outfile=fname)
    print('\n')

def getNamesUrls():
    with open('urls.txt') as f:
        urlsv = [it.strip() for it in f.readlines()]
    names = urlsv[::3]
    urls = urlsv[1::3]
    return zip(names, urls)

for bairro, url in getNamesUrls():
    getPage(bairro,url)

saveInExcel(vtotal,outfile='total')
