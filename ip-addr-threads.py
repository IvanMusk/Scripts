# 基于python3批量查资产归属，多线程版
# 连接频率过高时会出现接口拒绝连接情况，调整WORD_THREAD与sleep()
import xlrd
import pathlib
from xlutils.copy import copy
import requests
from bs4 import BeautifulSoup
import time
import threading

WORD_THREAD = 30

data = xlrd.open_workbook('1.xls')
table = data.sheet_by_name('Sheet1')
nrows = table.nrows
wb = copy(data)
ws = wb.get_sheet("Sheet1")

def function():
    for m in range(nrows):
        if m >= 1:
            try:
                ip = table.row_values(m)[0].strip()
                res = requests.get(f'http://www.ip138.com/ips138.asp?ip={ip}&action=2')
                soup = BeautifulSoup(res.content, 'html5lib')
                loc = soup.find_all('table')[2].tbody.find_all('tr')[2].td.ul.li.text[5:]
                ws.write(m, 5, loc)
                print(f'ip: {ip} loc: {loc}')
            except Exception as e:
                print(e)
                wb.save('1.xls')
                break
        time.sleep(1)   # 以防连接频率过高导致接口拒绝连接，可酌情修改
if __name__ == '__main__':
    threads = []
    start_time = time.time()
    for i in range(WORD_THREAD):
        thread = threading.Thread(target=function)
        thread.start()
        threads.append(thread)

    for thread in threads:
            thread.join()

wb.save('1.xls')
