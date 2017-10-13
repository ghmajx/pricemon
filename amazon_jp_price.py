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
kv = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.52 Safari/537.36'}
print(url)


def getProdInfo(url):
    logging.debug('Start of getProdInfo')
    prodInfo = {}
    res = requests.get(url, headers=kv)
    amazonSoup = bs4.BeautifulSoup(res.text, "html.parser")
    amzElem = amazonSoup.find_all(id=re.compile(r'productTitle$|priceblock_ourprice$'))
    # Version 0.3:
    priceRaw = amzElem[1].getText()
    priceRegex = re.compile(r'\d+\.?\d*')
    mo = priceRegex.search(priceRaw)
    price = mo.group()
    logging.debug('After Regex the price is ' + price)

    prodInfo['price'] = price
    logging.debug('product price is ' + prodInfo['price'])
    prodName = amzElem[0].getText().strip()

    prodInfo['prodName'] = prodName
    logging.debug('product name is ' + prodInfo['prodName'])
    return prodInfo


while True:
    try:
        productInfo = getProdInfo(url)
        price = productInfo['price']
        prodName = productInfo['prodName']
        msg = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ' - ' + prodName + ' - ' + price
        logging.debug("The msg is " + msg)
        if float(price) < 440:
            requests.post('https://api.telegram.org/botbid/sendMessage?chat_id=uid&text=' + msg
                          + ' - ' + url)
        time.sleep(15)
    except Exception as e:
        print(e)
        continue
