

# python package to run machine learning tasks

__version__ = "1.0.3"
__author__ = "Connor Beard"
__all__ = ['yeet','google_news']


from datetime import datetime
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  

import numpy as np

from bs4 import BeautifulSoup as bs
import re
import requests



def getSingleDayEvents(gRaw,h = 0.01,event_type = 0):
    tEvents,sPos,sNeg=np.zeros((gRaw.shape[0],gRaw.shape[1])),np.zeros((gRaw.shape[1])),np.zeros((gRaw.shape[1]))
    diff = gRaw
    diff = diff.replace(np.inf,0); diff = diff.fillna(0); 
    zeros = np.zeros(diff.shape[1])

    if event_type == 1:
        for i in diff.index[1:]:
            t = np.where(abs(diff.loc[i]) > h)
            tEvents[np.where(diff.index == i)[0][0],t] = 1;

    elif event_type == 1:
        for i in diff.index[1:]:
            t = np.where(diff.loc[i] > h)
            tEvents[np.where(diff.index == i)[0][0],t] = 1;

    elif event_type == -1:
        for i in diff.index[1:]:
            t = np.where(diff.loc[i] < -h)
            tEvents[np.where(diff.index == i)[0][0],t] = 1;

    else:
        return('event_type must be an integer in [-1,0,1]: -1 for negative triggers, 1 for positiive, 0 for both')
    
            
    return np.array(tEvents)


def getRelativeEvents(gRaw, func, numDayFilter=0):

    # function that should return indexes of when a stock first hits a n-day low

    # gRaw: raw dataset to analyze

    # function to use to analyze info (e.g. m-day standard deviation, m-day SMA??)
    # e.g. def func(v):
    #           result = np.std(v)
    #           return result

    # numDayFilter: for trailing events, number of days to ignore after an event is identified
    # for single day events, numDayFilter is 0
    
    tEvents,sPos,sNeg=np.zeros((gRaw.shape[0],gRaw.shape[1])),np.zeros((gRaw.shape[1])),np.zeros((gRaw.shape[1]))
    diff = gRaw
    diff = diff.replace(np.inf,0); diff = diff.fillna(0); 
    zeros = np.zeros(diff.shape[1])
      
    return np.array(tEvents)


def google_news(query = '', driver_path = '', date = datetime.today(),binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'):

    if driver_path == '':
        return('Must have chromedriver installed in a driver_path')
        
    a = query.split(' ')
    search = a[0]
    for word in range(1,len(a)):
        search += '+' + a[word]

    search = 'https://www.google.com/search?q='+search+'&biw=1342&bih=717&source=lnt&tbs=cdr%3A1%2Ccd_min%3A'+str(date.month) + '%2F' + str(date.day) + '%2F' + str(date.year) + '%2Ccd_max%3A' + str(date.month) + '%2F' + str(date.day) + '%2F' + str(date.year) + '&tbm=nws'

    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    chrome_options.binary_location = binary_location
    driver = webdriver.Chrome(executable_path=driver_path,chrome_options=chrome_options)

    driver.get(search)
    webpage = driver.page_source

    soup = bs(webpage,'lxml')


    INVISIBLE_ELEMS = ('style', 'script', 'head', 'title')
    RE_SPACES = re.compile(r'\s{3,}')



    text = ' '.join([
        s for s in soup.strings
        if s.parent.name not in INVISIBLE_ELEMS
    ])

    
    a = RE_SPACES.sub(' ',text)

    b = np.array(a.split('...'))

    return b

    
