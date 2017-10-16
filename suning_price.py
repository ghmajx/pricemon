#! python3
import bs4, requests, sys, subprocess, time, logging, datetime, json, re
#logging.disable(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')
if len(sys.argv) < 2:
    print('Usage: python suning_price.py [productid] - get productid price')
    sys.exit()
productid = sys.argv[1]
nameUrl = 'https://product.suning.com/0000000000/' + productid + '.html'
priceUrl = 'https://pas.suning.com/nspcsale_0_000000000%s_000000000%s_0000000000_10_010_0100101.html' % (productid,productid)
kv = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.52 Safari/537.36'}
logging.debug('The name url is ' + nameUrl +'\n' +
              'The price url is ' + priceUrl)

def getProdName(url):
    logging.debug('Start of getProdName')
    res = requests.get(url, headers=kv)
    snSoup = bs4.BeautifulSoup(res.text, "html.parser")
    snElem = snSoup.select('#itemDisplayName')
    prodName = snElem[0].getText().strip()
    logging.debug('product name is ' + prodName)
    return prodName

def getprice(url):
    logging.debug('Start of getprice')
    res = requests.get(url, headers=kv)
    priceRaw = json.loads(res.text[7:-2])['data']['price']['saleInfo'][0]['netPrice']
    logging.debug('priceRaw is ' + priceRaw)
    priceRegex = re.compile(r'\d+\.?\d*')
    mo = priceRegex.search(priceRaw)
    price = mo.group()
    logging.debug('After Regex the price is ' + price)
    return price


while True:
    try:
        price = getprice(priceUrl)
        prodName = getProdName(nameUrl)
        msg = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ' - ' + prodName + ' - ' + price
        logging.debug('The msg is ' + msg)
        if float(price) < 8000:
            requests.post(
                'https://api.telegram.org/botbid/sendMessage?chat_id=uid&text=' + msg
                + ' - ' + nameUrl)
        time.sleep(100)
    except Exception as e:
        print(e)
        continue
