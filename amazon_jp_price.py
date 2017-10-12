#! python3
import bs4, requests, sys, subprocess, time, logging, datetime, re
logging.disable(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')
if len(sys.argv) < 2:
    print('Usage: python amazon_jp_price.py [productid] - get productid price')
    sys.exit()
productid = sys.argv[1]
url = 'https://www.amazon.co.jp/gp/product/' + productid
print(url)

# def getProdName(url):
#     logging.debug('Start of getProdName')
#     res = requests.get(url)
#     amazonSoup = bs4.BeautifulSoup(res.text, "html.parser")
#     amazonElem = amazonSoup.select('#productTitle')
#     # logging.debug('The length of amazonElem is ' + str(len(jdElem)))
#     prodName = amazonElem[0].getText().strip()
#     logging.debug('product name is ' + prodName)
#     return prodName
#
# def getprice(url):
#     logging.debug('Start of getprice')
#     res = requests.get(url)
#     amazonSoup = bs4.BeautifulSoup(res.text, "html.parser")
#     amazonElem = amazonSoup.select('#priceblock_ourprice')
#     price = amazonElem[0].getText()
#     priceDecimal = ''
#     for i in price:
#         if i.isdecimal():
#             priceDecimal += i
#
#     return priceDecimal

# def getProdInfo(url):
#     logging.debug('Start of getProdInfo')
#     prodInfo = {}
#     res = requests.get(url)
#     amazonSoup = bs4.BeautifulSoup(res.text, "html.parser")
#     amzPriceElem = amazonSoup.select('#priceblock_ourprice')
#     price = amzPriceElem[0].getText()
#     priceDecimal = ''
#     for i in price:
#         if i.isdecimal():
#             priceDecimal += i
#
#     prodInfo['price'] = priceDecimal
#     logging.debug('product price is ' + prodInfo['price'])
#     amazonProdElem = amazonSoup.select('#productTitle')
#     # logging.debug('The length of amazonElem is ' + str(len(jdElem)))
#     prodName = amazonProdElem[0].getText().strip()
#
#     prodInfo['prodName'] = prodName
#     logging.debug('product name is ' + prodInfo['prodName'])
#     # logging.debug('prodInfo is ' + prodInfo.items())
#     return prodInfo

def getProdInfo(url):
    logging.debug('Start of getProdInfo')
    prodInfo = {}
    res = requests.get(url)
    amazonSoup = bs4.BeautifulSoup(res.text, "html.parser")
    amzElem = amazonSoup.find_all(id=re.compile(r'productTitle$|priceblock_ourprice$'))
    price = amzElem[1].getText()
    priceDecimal = ''
    for i in price:
        if i.isdecimal():
            priceDecimal += i

    prodInfo['price'] = priceDecimal
    logging.debug('product price is ' + prodInfo['price'])
    prodName = amzElem[0].getText().strip()

    prodInfo['prodName'] = prodName
    logging.debug('product name is ' + prodInfo['prodName'])
    # logging.debug('prodInfo is ' + prodInfo.items())
    return prodInfo

while True:
    try:
        # print(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ' - '+ getProdInfo(url)['prodName'] + ' - ' + getProdInfo(url)['price'])
        productInfo = getProdInfo(url)
        price = productInfo['price']
        prodName = productInfo['prodName']
        msg = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ' - '+ prodName + ' - ' + price
        logging.debug("The msg is " + msg)
        if int(price) < 440:
            # alarmFile = open('d:\\amazon\\alarmFile.txt', 'w')
            # alarmFile.write(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ' - '+ getProdName(url) + ' - ' + getprice(url))
            # alarmFile.close()
            # subprocess.Popen(['start', 'd:\\amazon\\alarmFile.txt'], shell=True)
            # subprocess.Popen(['start', 'd:\\amazon\\Sent.wav'], shell=True)
            requests.post('https://api.telegram.org/botbid/sendMessage?chat_id=uid&text=' + msg
                          + ' - ' + url)
        time.sleep(15)
    except Exception as e:
        print(e)
        continue