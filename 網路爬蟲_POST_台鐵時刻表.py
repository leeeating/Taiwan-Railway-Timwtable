#!/usr/bin/env python
# coding: utf-8

# ## **使用POST方法來爬取台鐵的時刻表**
# ### [列車時刻/車次查詢](https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime)

# In[1]:


# 可以去掉 python 輸出時，因為軟體版本所引起的警告的警告。
import warnings
warnings.filterwarnings('ignore')


# In[2]:


import requests

# 注意：所選的日期 (rideDate) 一定要今天或之後才會有資料
#
payload = {    
    '_csrf':'e7666daa-56a6-41b9-aba1-34141ed8e04b',
    'startStation':'3300-臺中',
    'endStation':'1080-桃園',
    'transfer':'ONE',
    'rideDate':'2022/06/03',
    'startOrEndTime':'true',
    'startTime':'00:00',
    'endTime':'23:59',
    'trainTypeList':'ALL',
    'query':'查詢'
}

url_address = 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip112/querybytime'
    
res_post = requests.post(url_address, data = payload) 

res_post.encoding = 'utf-8'  # 為了能夠順利讓網頁中的中文字正確的呈現出來

#print (res_post.text) # 看一下網頁的內容


# ### **剖析網頁內容，瞭解要抓的表格在哪裡**

# In[3]:


from bs4 import BeautifulSoup

soup = BeautifulSoup(res_post.text, 'html.parser')

# 表格標籤特徵為 <table class="itinerary-controls">
tables = soup.select('table[class="itinerary-controls"]')

print('共掃出 %d 個表格！\n' % len(tables))


# ### **用 Pandas 資料科學套件來讀取爬出的表格**

# In[4]:


import pandas as pd

tables = pd.read_html(str(tables))

print('共掃出 %d 個表格！\n' % len(tables))
   
#print(table_columns)


# ### **看一下每一個表格**

# In[5]:


tables[0]


# In[6]:


tables[1]


# In[7]:


tables[2]


# In[8]:


tables[3]


# In[9]:


tables[4]


# In[10]:


tables[5]


# ### **看一下表格上有哪一些欄位**

# In[11]:


for name in tables[0].columns:
    
    print(name)


# ### **選擇特定欄位內的資料寫入最後結果的表格內**

# In[12]:


# 修改 pandas 顯示設定
pd.set_option('display.max.columns', 20)

pd.set_option('display.max.rows', None) # 顯示全部


# In[13]:


#column_fields = ['車種車次 (始發站 → 終點站)', '出發時間', '抵達時間', '行駛時間', '經由', '全票', '孩童票']

column_fields = tables[0].columns[:9]

df = pd.DataFrame( 
                   tables[0], 
                   columns = column_fields
                  ) 

df.index += 1

df  # 顯示 df 表格


# ### **抽出所要的表格內容**

# In[14]:


df2 = pd.DataFrame(columns = column_fields) 

for i in range(1, df.index.stop, 5):
    
    #append row to the dataframe
    df2 = df2.append(df.loc[i,:], ignore_index = True)
    
df2.index += 1 # 調整最後表格的索引值由 1 開始，而不是依預設值從 0 開始

df2  # 顯示 df2 表格

