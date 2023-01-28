from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup
import random 
from random import choice
import time
import csv
import json
from lxml import etree
import math
import re
import multiprocessing
from multiprocessing import Pool
import aiohttp
import asyncio
import mpire
from mpire import WorkerPool
from fake_useragent import UserAgent
from datetime import datetime
import sys

hrefsBankVar = []
uagent = UserAgent()
itemsCount = 0 
agrForAmazon = 'amazon.com'
agrForEbey = 'ebay.com'
total_count = 0 
flag = False
determinantChanell = ''

with open("proxy.txt", encoding="utf-8") as file:
    PROXY_LIST = ''.join(file.readlines()).split('\n')

desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                  uagent.random,
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 UserAgent().chrome,
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 uagent.random,
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 UserAgent().chrome,
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                 uagent.random,
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 UserAgent().chrome,
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 uagent.random,
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']
desktop_accept = ['text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  '*/*',
                  'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                  'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                  'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8','application/signed-exchange;v=b3;q=0.9',
                  'text/html, */*; q=0.01',
                  ]

aceptLengv = [
            'en-US,en;q=0.8',
            'ru-RU,ru;q=0.9',
            ]

def random_headers(argLink):    
    device_memoryHelper = [2,4,8,16,32]
    sett = set()
    finHeaders = []
    headFront = [{
            'authority': f"www.{argLink}",
            'accept': choice(desktop_accept), 
            'User-Agent': choice(desktop_agents),           
            "accept-ch": "sec-ch-ua-model,sec-ch-ua-platform-version,sec-ch-ua-full-version",
            'accept-language': choice(aceptLengv),            
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': f'https://www.{argLink}',
            'device-memory': f'{choice(device_memoryHelper)}',
            'rtt': '200',            
            }]
    headersHelper = [       
            {"sec-fetch-dest": "empty"},
            {"sec-fetch-mode": "cors"},
            {"sec-fetch-site": "same-origin"},
            {"ect": "4g"},
            {"viewport-width": "386"}
    ]
    headersHelperFormated = []
    strr = ''
    for i in headersHelper[0:len(headersHelper)-random.randrange(0,5)]:
        strr += ((str(choice(headersHelper)))[1:-1]).strip() + ',' + ' '  
         
    sett.add(strr)    
    headersHelperFormated = list(sett)    
    finHeaders = headFront + headersHelperFormated
    finHeaders[1] = eval("{" + finHeaders[1] + "}")    
    finfin = finHeaders[0]|finHeaders[1]    
    return finfin

def proxyGenerator():
    proxiess = {
        "https": f"http://{choice(PROXY_LIST)}",
        "http": f"http://{choice(PROXY_LIST)}"     
    }
    return proxiess
def sessionReq(url1, shopArg):   
    global determinantChanell
    session = HTMLSession()
    session.trust_env = False 

    if determinantChanell == 1:       
       r = session.get(url1, headers=random_headers(shopArg), timeout=(3.15, 21.15))
    elif determinantChanell == 2:
        r = session.get(url1, headers=random_headers(shopArg), timeout=(3.15, 21.15), proxies=proxyGenerator())
    elif determinantChanell == 3:            
        randomChanel = choice(list(range(0, len(PROXY_LIST)+1)))  
        if randomChanel == 1:
            r = session.get(url1, headers=random_headers(shopArg), timeout=(3.15, 21.15))
        else:          
            r = session.get(url1, headers=random_headers(shopArg), timeout=(3.15, 21.15), proxies=proxyGenerator()) 
    else:        
        r = session.get(url1, headers=random_headers(shopArg), timeout=(3.15, 21.15))
           
    return r

def paginationReply(url):
    global start_time    
    paginController = 0     
    lastPagin = 0
    agrForEbey = 'ebay.com'    
         
    try:
        r = sessionReq(url, agrForEbey)    
        if str(r) == '<Response [200]>':
            print('Первый ответ сервера положительный')
        if str(r) == '<Response [503]>':            
            print('Смените ip адрес вашего компьютера и попробуйте еще раз')
            sys.exit()

        if str(r) == '<Response [403]>':
            print('Программа вынуждена остановить работу из-за отказа сервера')
            sys.exit()

        if str(r) == '<Response [504]>':
            return  
        if str(r) == '<Response [404]>':
            print('Страница не найдена. Проверьте правильность url')
            sys.exit()
         
        try:    
            soup = BeautifulSoup(r.text, "lxml")
        except:
            pass            
        try:
            ptest = soup.find('h1', class_='srp-controls__count-heading')
            ptest = int(soup.find('h1', class_='srp-controls__count-heading').get_text().split(' ')[0].replace(',', '').replace('+', ''))
            lastPagin = math.ceil(int(ptest)/240)
        except Exception as ex: 
            pass           

    except Exception as ex: 
        paginController +=1
        if paginController >1:
            print('Упс! Что-то пошло не так')
            return
        else:            
            paginationReply(url)
            
    print(f"Всего в магазине страниц пагинации: {lastPagin}")        
    paginLimit = input('Введите лимит пагинации (через дефис, например: 10-20) или введите Enter(значение по умолчанию)', )
    if paginLimit == '' or paginLimit == ' ':
        hrefsBlockPagination = list(f"{url}&_ipg=240&_pgn={i}" for i in range(1, lastPagin+1))
        start_time = time.time()  
        asyncio.run(gather_registrator_eBay(hrefsBlockPagination))
        return    
    else:        
        try:
            startPagin = int((paginLimit.strip()).replace(' ', '').split('-')[0])
            finPagin = int((paginLimit.strip()).replace(' ', '').split('-')[1])
        except:
            paginLimit = input('Пожалуйста, введите лимит на пагинацию еще раз:', )
            try:
                startPagin = int((paginLimit.strip()).replace(' ', '').split('-')[0])
                finPagin = int((paginLimit.strip()).replace(' ', '').split('-')[1])
            except:
                print(f'Выбрано значение по умолчанию 1-{lastPagin}')
                hrefsBlockPagination = list(f"{url}&_ipg=240&_pgn={i}" for i in range(1, lastPagin+1))
                start_time = time.time()  
                asyncio.run(gather_registrator_eBay(hrefsBlockPagination))
                return     
                
        if startPagin > finPagin:            
            paginLimit = input('Пожалуйста, введите лимит на пагинацию еще раз:', )
            try:
                startPagin = int((paginLimit.strip()).replace(' ', '').split('-')[0])
                finPagin = int((paginLimit.strip()).replace(' ', '').split('-')[1])
            except:
                print(f'Выбрано значение по умолчанию 1-{lastPagin}')
                hrefsBlockPagination = list(f"{url}&_ipg=240&_pgn={i}" for i in range(1, lastPagin+1))
                start_time = time.time()  
                asyncio.run(gather_registrator_eBay(hrefsBlockPagination))
                return    
                
                  
        elif lastPagin < finPagin:
            hrefsBlockPagination = list(f"{url}&_ipg=240&_pgn={i}" for i in range(1, lastPagin+1))
        elif lastPagin > finPagin:
            if startPagin == 0:
                startPagin = 1 
            hrefsBlockPagination = list(f"{url}&_ipg=240&_pgn={i}" for i in range(startPagin, finPagin+1))
        elif lastPagin == finPagin:
            hrefsBlockPagination = list(f"{url}&_ipg=240&_pgn={i}" for i in range(1, lastPagin+1))

    start_time = time.time()  
    asyncio.run(gather_registrator_eBay(hrefsBlockPagination))            

async def linkerCapturerEbay(href): 
    global hrefsBankVar    
    global flag

    agrForEbey = 'ebay.com'
    while(True):
        flag = False
        countLincerCapturer = 0 
        countLincerCapturer2 = 0
        cycleControl = 0  
        try:            
            r = sessionReq(href, agrForEbey)
            if str(r) == '<Response [503]>':
                return
            if str(r) == '<Response [403]>':
                return
            if str(r) == '<Response [504]>':
                return  
            if str(r) == '<Response [404]>':
                return
            if str(r) == '<Response [400]>':
                return
            if str(r) == '<Response [443]>':
                return
                        
            try:
                soup = BeautifulSoup(r.text, "lxml")
                hrefs = soup.find_all('a', class_='s-item__link')            
                for item in hrefs:
                    if item is None:
                        cycleControl +=1
                        if cycleControl == 180:
                            countLincerCapturer +=1
                            if countLincerCapturer >1:
                                print('Не удалось собрать нужное количество ссылок')
                                return
                            else:                                
                                flag = True
                                break
                        continue 
                    else:
                        hrefsBankVar.append(item.get('href'))
            except:
                flag = True

        except Exception as ex:
            flag = True

        if flag == False:
            return 
        else:
            countLincerCapturer2 +=1
            if countLincerCapturer2 >1:
                print('Не удалось собрать нужное количество ссылок')
                return
            else:
                time.sleep(random.randrange(1,3))
                continue              

def linksHandlerAmazon(total):
    if total is None:
        return
    try:
        model = total['model'].lower()
    except:
        pass    
    agrForAmazon = 'amazon.com'    
    targetLinkPattern = 'https://www.amazon.com'

    while(True):
        finResult = []
        counterRetry = 0
        counterExceptions = 0                     
        quanityTargetItems = 0
        flagEx1 = False
        try:
            r = ''   
            r = sessionReq(total['linkSrchAmazon'], agrForAmazon)
            if str(r) == '<Response [503]>':
                print('Желтая карточка от Amazon')            
                return

            if str(r) == '<Response [403]>':
                print('Amazon отверг запрос')
                return

            if str(r) == '<Response [504]>':
                return  
            if str(r) == '<Response [404]>':
                print('Страница не найдена')
                return 
            if str(r) == '<Response [400]>':
                return 
            if str(r) == '<Response [443]>':
                print('Проблемы с подключениемю. Проверьте интернет соединение')                
                counterExceptions +=1
                if counterExceptions >1:
                    return
                else:                    
                   continue 
               
        except Exception as ex:
            return
        try:
            soup = BeautifulSoup(r.content, "html.parser")
            soup2 = BeautifulSoup(r.text, "lxml")
            dom = etree.HTML(str(soup)) 
        except:
            return
        try:                   
            gf = dom.xpath('//*[@id="search"]/span/div/h1/div/div[1]/div/div/span[1]//text()')[0]       
            try:    
                quanityTargetItems = int(gf)
            except:
                try:
                    quanityTargetItems = int(gf.split(' ')[0])
                except:                                     
                    try:                
                        quanityTargetItems = int(gf.split(' ')[0].split('-')[1])                                           
                    except Exception as ex:
                        print(f"что-то не так с количеством товаров Amazon  {ex}")
                        return

        except Exception as ex:            
            return
        if quanityTargetItems > 50:
            quanityTargetItems = 50        
        try:
            resultProto = []
            firstBlock = soup2.find_all('div', attrs= {'class': 'a-row', 'class': 'a-size-base', 'class': 'a-color-base'})

            for f, x in enumerate(firstBlock):
                targetLinkPattern = 'https://www.amazon.com'                                         
                targetLink = ''
                targetPrice  = ''
                titleCritery = ''

                try:
                    targetPrice = x.find('span', class_= 'a-offscreen').get_text() 
                except:
                    pass  
                try:              
                    targetLink = x.find_next().get('href')
                except:
                    pass                    
                try:
                    titleCritery1Arr = []
                    titleCritery1Arr = targetLink.split('/')[1].split('-')
                    for it in titleCritery1Arr:       
                        it = it.lower()
                        if it == model or it == model[:-1]:
                            titleCritery = model
                            break                    
                        
                except:                        
                    pass
                try:                       
                    asinArr = targetLink.split('/')
                    for i, a in enumerate(asinArr):
                        if asinArr[i] == 'dp':
                            asin = asinArr[i+1]                                               
                except:
                    pass
                
                resultProto.append({
                    "targetLink": str(f"{targetLinkPattern}{targetLink}").strip(),
                    "titleCritery": str(titleCritery.strip()),
                    "targetPrice": str(targetPrice).strip(),
                    "asin": str(asin).strip()
                })                                        
                if len(resultProto) == quanityTargetItems:                                               
                    break
            if len(resultProto) == 1:
                if resultProto[0]['asin'] == '' or resultProto[0]['asin'] == None:                    
                    flagEx1 = True               
                                        
            elif len(resultProto) > 1:
                if resultProto[1]['asin'] == '' or resultProto[1]['asin'] == None:
                    flagEx1 = True         
            if flagEx1 == True:         
                counterRetry += 1
                if counterRetry > 1:
                    return
                else:
                    time.slep(random.randrange(1,4))
                    continue   
    
        except Exception as ex:
            pass
                
        finally:           
            finResult.append({                
                "urlEbayItem": total["urlItem"],
                "title": total["title"],
                "price": total['price'],
                "quanity": total['quanity'],
                "delivery": total['delivery'],
                "brand": total['brand'],
                "model": total['model'],                
                "amazonBlock": resultProto,                               
            })

            try:
                return finResult[0]
            except:
                return

def hendlerLinks(link):
    result = []
    upc = ''
    agrForEbey = 'ebay.com'        
    dNotApl = 'does not apply'
    notAv = 'not available'
    try:            
        r = sessionReq(link, agrForEbey)       
        if str(r) == '<Response [503]>':
            print('Желтая карточка от Ebay')
            return

        if str(r) == '<Response [403]>':
            print('Ebay отверг запрос')
            return

        if str(r) == '<Response [504]>':
            return  
        if str(r) == '<Response [404]>':
            return 
        if str(r) == '<Response [400]>':
            return 
        if str(r) == '<Response [443]>':
            return                        
        soup = BeautifulSoup(r.text, "lxml")           
        priceChecer = soup.find('div', class_='x-price-primary').find('span', class_='ux-textspans').get_text().strip()
        price = ''
        try:
            price = soup.find('div', class_='x-price-primary').find('span', class_='ux-textspans').get_text().strip()
        except:   
            price = ''             
            
        title = ''
        try:
            title = soup.find('h1', class_='x-item-title__mainTitle').find('span', class_='ux-textspans').get_text().strip()
        except:           
            title = ''
    
        quanity = ''            
        try:
            quanity = soup.find('span', id='qtySubTxt').find('span').get_text().strip()
        except:
            try:
                quanity = soup.find('span', id='qtySubTxt').find('span').find('span').get_text().strip()
            except:                
                quanity = ''
            quanity = ''             
            
        delivery_text = ''
        try:
            delivery = soup.find('div', class_='ux-labels-values--deliverto').find('div', class_='col-9').find('div').find_all('span', class_='ux-textspans--BOLD')
            delivery_text = f"Estimated between {delivery[0].get_text()} and {delivery[1].get_text()}"
            for dell in delivery[0:-2]:
                delivery_text += dell.get_text()                    
        except:            
            delivery = ''

        brand = ''
         
        try:
            brand = soup.find(attrs={'itemprop': 'brand'}).find('span', class_='ux-textspans').get_text().strip()                
        except:                       
            try:
                CompatibleBrand = soup.find_all('div', class_='ux-layout-section__row')
                cpBrd = 'compatible brand'     

                for row in CompatibleBrand:
                    section = row.find_all('span', class_='ux-textspans')
                    for j, compBrand in enumerate(section):                                        
                        try:
                            try:
                                sec = (f"{section[j].get_text().strip()}").lower() 
                            except:
                                sec = section[j].get_text().strip()
                                         
                            match = re.search(f'{r}"{cpBrd}"', sec)
                            if match:
                                brand = section[j+1].get_text().strip() 
                                break 
                        except: 
                            continue                                             
            except:
                brand = ''
                 
        brand_namePatern = ''            
        try:
            brdArr = brand.split(' ')
            if len(brdArr) >1:                                
                for itBrN in brdArr:
                    brand_namePatern += itBrN + '+'
                brand = brand_namePatern[0:len(brand_namePatern)-1]
            else:
                pass
                
        except:
            pass         

        model = ''
        try:
            model = soup.find(attrs={'itemprop': 'mpn'}).find('span', class_='ux-textspans').get_text().strip()                   
        except:           
            try:
                model = soup.find(attrs={'itemprop': 'model'}).find('span', class_='ux-textspans').get_text().strip()                   
            except:
                model = ''
            
        model_itemPatern = ''            
        try:
            modelArr = model.split(', ')
            if len(modelArr) >1:
                               
                for itModN in modelArr:
                    model_itemPatern += itModN + '+'
                model = model_itemPatern[0:len(model_itemPatern)-1]
            else:
                pass                
        except:
               pass 
        try:
            mod = ''
            mod = model.lower()            
        except:
            mod = model                     

        if model == '' or mod == dNotApl or mod == notAv:
           model = ''  

        upc = ''
        try:
            upc = soup.find(attrs={'itemprop': 'gtin13'}).find('span', class_='ux-textspans').get_text().strip()                         
        except Exception as ex:          
            try:   
                upc = soup.find_all('div', class_='ux-layout-section__row')
                upcUpc = 'upc'
                
                for row in upc:
                    section = row.find_all('span', class_='ux-textspans')
                    for j, upcc in enumerate(section):
                                            
                        try:
                            try: 
                               ses = (f"{section[j].get_text().strip()}").lower()
                            except:
                                ses = section[j].get_text().strip()
                                       
                            match = re.search(f'{r}"{upcUpc}"', ses)
                            if match:
                                upc = section[j+1].get_text().strip()                               
                                break
                        except: 
                            continue
            except:
                upc = ''                                                                    
        try:
            up = ''
            up = upc.lower()            
        except:
            up = upc
 
        if upc == '' or up == dNotApl or up == notAv:
           upc = ''
        else:
            try:
                int(upc[1]) 
                upc = upc 
            except:
                try:
                    int((upc.split(', ')[0])[1])
                    upc = upc.split(', ')[0]
                except:
                    upc = ''

        linkSrchAmazon = ''
        
        try:
            if upc != '' and model != '':
               linkSrchAmazon = f"https://www.amazon.com/s?k={brand}+{model}+{upc}"
            elif upc != '' and model == '':
                linkSrchAmazon = f"https://www.amazon.com/s?k={brand}+{upc}"
                
            elif upc == '' and model != '':
                linkSrchAmazon = f"https://www.amazon.com/s?k={brand}+{model}"
            else:
                linkSrchAmazon = ''               
        except: 
            pass

        result.append({
            "urlItem": link,
            "title": str(title),
            "price": str(price),                
            "quanity": str(quanity),
            "delivery": str(delivery_text),
            "brand": str(brand),            
            "model": str(model),
            "upc": str(upc),
            "linkSrchAmazon": f"{str(linkSrchAmazon)}",                          
        })  
                
    except Exception as ex:
        pass     
    finally:
        try: 
           return linksHandlerAmazon(result[0])
        except:
            return

async def gather_registrator_eBay(hrefsBlockPagination):
    global hrefsBankVar   
    async with aiohttp.ClientSession() as session:       
        tasks = [] 
        for href in hrefsBlockPagination:
            task = asyncio.create_task(linkerCapturerEbay(href))
            tasks.append(task)
        await asyncio.gather(*tasks)      
    gather_Linker_Ebay(hrefsBankVar)
    hrefsBankVar = []
    
def gather_Linker_Ebay(hrefsBank):   
    print(f"Всего в магазине товаров: {len(hrefsBank)}")
    hrefsBank = list(filter(None, hrefsBank))
    # n = multiprocessing.cpu_count() * 10  
    n = 21
    
    with WorkerPool(n_jobs = n) as p2:                      
        finRes = p2.map(hendlerLinks, hrefsBank)        
        writerr(finRes) 
        hrefsBank = [] 
        finRes = []

def writerr(total):
    print('Запись результатов')
    global total_count
    total = list(filter(None, total)) 
    total = list(filter(lambda item: item['amazonBlock'] != [], total))
    total = list(filter(lambda item: item['amazonBlock'] != '', total))
    
    for item in total:
        item['amazonBlock'] = list(filter(lambda it: it['asin'] != '', item['amazonBlock']))
    for item in total:
        amazonLink = ''
        amazonPrice = ''
        amazonAsin = ''
        if len(item['amazonBlock']) > 1:
            item['amazonBlockNew'] = list(filter(lambda it: it['titleCritery'] != '', item['amazonBlock']))
            if len(item['amazonBlockNew']) == 0:
                item['amazonBlock'] = item['amazonBlock'][0:7] 
            else:              
                item['amazonBlock'] = item['amazonBlockNew']                   
            del item['amazonBlockNew']
      
        for it in item['amazonBlock']:
            if len(item['amazonBlock']) == 0:
                try:
                    amazonLink = it['targetLink'] + '\n'
                    amazonPrice = it['targetPrice'] + '\n'
                    amazonAsin = it['asin'] + '\n'
                except:
                    pass
                break
            else:
                try:
                    amazonLink += it['targetLink'] + '\n'
                    amazonPrice += it['targetPrice'] + '\n'
                    amazonAsin += it['asin'] + '\n'
                except:
                    pass
        item['amazonLink'] = amazonLink
        item['amazonPrice'] = amazonPrice
        item['amazonAsin'] = amazonAsin                                
        del item['amazonBlock']    
     
    total_count = len(total) 
    now = datetime.now() 
    curentTimeForFile = now.strftime("%m_%d_%Y__%H_%M")     

    with open(f'Result_{curentTimeForFile}.json', "a", encoding="utf-8") as file: 
        json.dump(total, file, indent=4, ensure_ascii=False)

    with open(f'Result_{curentTimeForFile}.csv', 'w', newline='', encoding='cp1251', errors="ignore") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Ссылка на eBay маназин','Название товара', 'Цена', 'Наличие на складе', 'Дата доставки', 'Бренд', 'Модель', 'Ссылка на соответствующий товар на Amazon', 'Цена на Amazon', 'Асин'])
        for item in total:
            writer.writerow([item['urlEbayItem'], item ['title'], item['price'], item['quanity'], item['delivery'], item['brand'], item['model'], item['amazonLink'], item['amazonPrice'], item['amazonAsin']])      


    total = []
    
    
def determinantChanellFunc():
    determinantChanell = input('Выберите способ подключения: 1 - VPN; 2 - Proxy; 3 - Proxy and VPN', )
    try:
        determinantChanell = int(determinantChanell.strip())
    except:        
        determinantChanell = 1
    return determinantChanell

def reciveInput():
    global start_time 
    global determinantChanell
    determinantChanell = determinantChanellFunc()

    url = input('Введите адрес магазина', ) 
    start_time = time.time()    
    print('Старт...') 
    paginationReply(url)
    
def main():
    global total_count
    global start_time   
    
    reciveInput()            
    finish_time = time.time() - start_time
    print(f"Общее время работы парсера:  {math.ceil(finish_time)} сек")
    if len(total_count) == 0:
        print('Упс! Что-то пошло не так...')
    print(f"Общее количество товаров:  {total_count}")
    sys.exit()
    
if __name__ == "__main__":
    main()

# python eScraperNew.py




# git clone https://github.com/Sonnik9/secRespPAES


# win + R (optionalfeatures)
# (open powerShall
# - Открываем терминал PowerShell от админа.
# - Вставляем и запускаем - Set-ExecutionPolicy RemoteSigned
# - На вопрос отвечаем - A) 
# выбираем оболочку в терминале

#  python -m venv venv
# venv\Scripts\activate

# python -m pip install --upgrade pip
# pip install requests_html
# pip install -U pip requests_html
# pip freeze > requirements.txt
# ... затем устанавл недостоющие библиотеки

# pip install aiohttp
# pip install mpire    
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib - для гугл таблиц

# pip install -U pip setuptools ?? - не нужно

# если не получается запушить
# git config --global push.autoSetupRemote true
# git push

# /////////////////////////////////ССЫЛКА НА МАГАЗИН
# https://www.ebay.com/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering&_ssn=worxtools&store_cat=0&store_name=worxlawnandgardenequipment&_oac=1
# https://www.ebay.com/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering&_ssn=paedistributing&store_cat=0&store_name=paedistributing&_oac=1&LH_PrefLoc=1&LH_ItemCondition=3&LH_BIN=1



# ////////////////// имя страницы гугл таблицы(сперва создайте)
# //////// https://docs.google.com/spreadsheets/d/1E8ApONqNaH9EXH8eeyOssTC2RNDRFyZ7njVucOnRNPs/ - ссылка на гугл таблицу

