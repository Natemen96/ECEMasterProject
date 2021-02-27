# import requests
import os
import csv
# from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver as web
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

PATH = 'ECEMasterProject/scripts/Data/TexasBlackout.csv'

def write_to_csv(tosave):
    "Helper function to write to csv to make data collection less painful"
    if not os.path.exists(PATH):
        with open(PATH, 'w', newline='') as csvfile:
            csvfile.close()
    with open(PATH, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(tosave)

IDS = [1510,1734,1762,1801,1858,
1726, 1805, 1657, 1937, 1972,
1861, 1512, 1676, 1511,1593,
1637,1513, 2095, 1584, 1583,
1808, 2314, 1822, 1340, 1392, 1350, 1393, 1493,
1959, 1653, 1573, 1668, 1444, 1360, 1380, 1492, 1351,  
1800, 1528, 1955, 1667, 1369, 3720, 1420, 1333, 1330, 1442, 1358, 1390, 1378, 1422, 1457,1580,
1765, 1478, 1429, 1771, 1416, 1474, 1395, 1479, 1500, 1405, 1498, 1367, 1354,1403, 1366, 1400, 1382, 1591, 1587,1582,
1385, 1365, 1336, 1467, 1379, 1412, 1468, 1472, 1449, 1450, 1476, 1364, 1461, 1414, 1487, 1499, 1592, 1585, 3168, 1586, 
1327, 1430, 1402, 1441, 1447, 1477, 1346, 1372, 1376, 1399, 1470, 1411, 1375, 1446, 1396, 1469, 1463, 1589, 
4169, 4176, 1363, 1458, 1428, 1497, 1373, 1438, 1387, 1473, 1352, 1462, 1353, 1342, 1356, 1337, 1398, 1383, 1326, 1349, 1445, 1590, 
1489, 1361, 1484, 1455, 1404, 1480, 1357, 1433, 1854, 1440, 1423, 1971, 1359, 1434,1426, 1425, 1401, 1328, 1464,
1377, 1482, 1408, 1451, 1362, 1466, 1475, 1437, 1417, 2415, 2588, 2554, 2555, 1343, 1495, 1335, 1439, 1460, 1639, 1452, 
1483, 1407, 2092, 2145, 1527, 1679, 1443, 1701, 1530, 1671, 2057, 2058,
1453, 1339, 3704, 1486, 1374, 1456, 2589, 3167, 2548, 2445, 2525, 1424, 2239, 2523, 1391, 1344, 1389, 1944, 1355, 1715, 1638, 
1394, 1348, 1418, 1485, 1436, 1830, 1496, 1413, 1368, 1804, 1488, 1406, 1491, 1381, 
1432, 1502, 1370, 1384, 1421, 1331, 1435, 1334, 1388, 1345, 1431, 1338, 1386, 
1427, 1459, 1490, 1371, 1410, 1465, 1448, 1419, 1501, 1409, 1341, 1415, 
1471, 1397, 1494, 1347, 1332, 1581, 1454, 1329, 1481]

i =0
# print(len(IDS))
def main(IDS):
    global i
    while True:
        try:
            for id in IDS:
                # driver = web.Chrome(executable_path=binary_path)
                driver = web.Chrome(ChromeDriverManager().install())
                driver.get(f'https://poweroutage.us/area/county/{id}')

                name = "//h1[@id='CountyName']"
                tracked = '/html[1]/body[1]/div[2]/div[3]/div[1]/div[1]/div[2]'
                out = '/html[1]/body[1]/div[2]/div[3]/div[2]/div[1]/div[2]'
                out_per =  '/html[1]/body[1]/div[2]/div[3]/div[3]/div[1]/div[2]'
                metrics = [name,tracked, out,out_per ]
                tosave = []
                tosave.append(id)
                for met in metrics:
                    data = driver.find_element_by_xpath(met).get_attribute("innerHTML")
                    tosave.append(data)
                tosave.append((datetime.now()))
                print(tosave)
                write_to_csv(tosave)
                driver.close()
            i = i+1
            print(i)
            time.sleep(60*5)
        except Exception as e:
            print(e)
            main(IDS)

main(IDS)