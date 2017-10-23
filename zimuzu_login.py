#! python3
import requests, time, logging, json

# logging.disable(logging.DEBUG)
logging.basicConfig(filename='/home/pi/zimuzu_login.log', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')

url = 'http://www.zimuzu.tv/User/Login/ajaxLogin'
kv = {'Accept': 'application/json, text/javascript, */*; q=0.01',
      'Accept-Encoding': 'gzip, deflate',
      'Connection': 'keep-alive',
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.52 Safari/537.36'}

payload = {'account': 'uesrname', 'password': 'password', 'remember': '0', 'url_back': 'http://www.zimuzu.tv/'}
res = requests.session()
response = res.post(url, headers=kv, data=payload)
info = json.loads(response.content.decode('utf-8'))['info']
logging.debug('The response info is ' + info)


