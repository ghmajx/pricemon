#! python3
import bs4, requests, sys, subprocess, time, logging, datetime, json

logging.disable(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')
if len(sys.argv) < 2:
    print('Usage: python jd_price.py [productid] - get productid price')
    sys.exit()
productid = sys.argv[1]
nameUrl = 'https://item.jd.com/' + productid + '.html'
priceUrl = 'https://p.3.cn/prices/mgets?skuIds=J_' + productid
kv = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.52 Safari/537.36'}
logging.debug('The name url is ' + nameUrl + '\n' +
              'The price url is ' + priceUrl)


def getProdName(url):
    logging.debug('Start of getProdName')
    res = requests.get(url, headers=kv)
    jdSoup = bs4.BeautifulSoup(res.text, "html.parser")
    jdElem = jdSoup.select('.sku-name')
    prodName = jdElem[0].getText().strip()
    logging.debug('product name is ' + prodName)
    return prodName


def getprice(url):
    logging.debug('Start of getprice')
    res = requests.get(url, headers=kv)
    priceRaw = json.loads(res.text)[0]['p']
    logging.debug('priceRaw is' + priceRaw)
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
