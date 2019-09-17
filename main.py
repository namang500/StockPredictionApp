
# coding: utf-8

# In[148]:


from flask import  Flask , app , json , Request , Response , jsonify , request , redirect 
import pandas as pd
import numpy as np
import os 
import datetime 
import glob
import pyodbc
import time
import socket    


# In[149]:


app = Flask(__name__)


# In[156]:


## function definition

def time_warp():
    """
    in : nothing
    out: formatted datetime
    """
    ts = datetime.datetime.now().timestamp()
    offset= 122380.0 + 34580.0
    display_time =int(ts - offset )
    display_time= datetime.datetime.fromtimestamp(display_time)
    display_time=display_time.strftime("%Y-%m-%d %H:%M:00")
    return str(display_time)



# In[158]:


class StockPrice():
    
    company_stock_data_path = list()
    company_names = list()
    company_image_url_path = dict()
    company_stock_data = dict()
    DATA_FILE_PATH = ""
    IMG_FILE_PATH = ""
    data_columns = list()
    
    hostname = "" 
    IPAddr = ""
    
    def __init__(self):
        
        self.hostname = socket.gethostname()    
        self.IPAddr = socket.gethostbyname(self.hostname)
        
        self.company_image_url_path = {
            "NSE_HDFCBANK" :"https://i.imgur.com/BRnZzIS.png",
            "NSE_COALINDIA":"https://i.imgur.com/0517oD4.png",
            "NSE_HINDUNILVR":"https://i.imgur.com/5fYQyeZ.png",
            "NSE_ICICIBANK":"https://i.imgur.com/1Pi3LgR.png?1",
            "NSE_INFY":"https://i.imgur.com/sN9t2tx.png",
            "NSE_ITC":"https://i.imgur.com/8KkRHYc.png",
            "NSE_KOTAKBANK":"https://i.imgur.com/oBWoOI5.png",
            "NSE_LT":"https://i.imgur.com/wyfbr94.png",
            "NSE_RELIANCE":"https://i.imgur.com/Vo749Xm.png",
            "NSE_SBIN":"https://i.imgur.com/hZyyZfv.png",
            "NSE_TCS":"https://i.imgur.com/RNPwhbR.png",
            "NSE_ONGC":"https://i.imgur.com/mlgzDgF.png",
            "NSE_MARUTI":"https://i.imgur.com/BeE5yRH.png"
        }

        self.DATA_FILE_PATH = "stock_data"
        self.data_columns = [ 'open' , 'high' , 'low' , 'close' , 'volume']
        
        for file in os.listdir(self.DATA_FILE_PATH):
            self.company_stock_data_path.append(os.path.join(self.DATA_FILE_PATH , file))
            self.company_names.append(file.split('.csv')[0])
            
        for company_name in self.company_names:
            self.company_stock_data[company_name] = dict()
            
            
    
    def read_stock_data(self):
        
        for file in os.listdir(self.DATA_FILE_PATH):
            
            company_name = file.split('.csv')[0]
            self.company_stock_data[company_name] = pd.read_csv(os.path.join(self.DATA_FILE_PATH , file) , index_col = 'date' )[self.data_columns].to_dict('index')
            
    
            


# In[159]:


sp = StockPrice()
sp.__init__()
sp.read_stock_data()


# In[160]:


@app.route('/')
def test_api():
    return jsonify({"company_name" :   'company_name'})




@app.route('/homepage')
def get_homepage():
    
    
    i = 1
    curr_time = time_warp()
    response = list()
    company_stock_detail = {"company_name": "null", 
                                 "company_id": "null", 
                                 "company_img_url": "null", 
                                 "company_img_url": "null", 
                                 "company_current_price": "null",
                                "company_stock_price_delta" : "null",
                                "company_detailed_url" : "null"}


    for company_name in sp.company_stock_data.keys():

        try:
            response.append({"company_name" :   str(company_name) , 
                    "company_id" : str(i) , 
                    "company_img_url" : str(sp.company_image_url_path[company_name]),
                    "company_current_price" : str(sp.company_stock_data[company_name][curr_time]['close']),
                    "company_stock_price_delta" : str(round(sp.company_stock_data[company_name][curr_time]['close'] - sp.company_stock_data[company_name][curr_time]['open'] , 2)), 
                    "company_detailed_url" : "http://{}:5002/detailpage/{}".format(sp.IPAddr , company_name)
                            })
            
        except Exception:
            
            fall_back_stock_detail = company_stock_detail
            fall_back_stock_detail['company_name'] = str(company_name)
            fall_back_stock_detail['company_id'] = str(i)
            fall_back_stock_detail["company_img_url"] = str(sp.company_image_url_path[company_name])
            
            response.append(fall_back_stock_detail)

        i+=1

    return jsonify(response)
        
        
    

@app.route('/detailpage/<company_name>')
def get_detail_page(company_name):
    
    response = list()
    
    curr_time = time_warp()
    date_list = [value for value in sp.company_stock_data[company_name]]
    idx = [i for i, d in enumerate(date_list) if curr_time in d]
    stock_data_list = date_list[int(idx[0]) : ][::-1]
    
    for i in stock_data_list:
        response.append({ 'time' : int(time.mktime(time.strptime(i, "%Y-%m-%d %H:%M:%S"))),
                          'close' : float(sp.company_stock_data[company_name][i]['close'])})
        
    return jsonify(response)

    
    
    
    
    


# In[161]:


# sp.company_stock_data['NSE_COALINDIA']
# # curr_time = time_warp()
# # date_list = [value for value in sp.company_stock_data['NSE_COALINDIA']]
# # idx = [i for i, d in enumerate(date_list) if curr_time in date_list]

# # stock_data_list = date_list[idx[0] : ][::-1]
# # stock_data_list


# In[162]:


# for company_name in sp.company_stock_data.keys():
#     for time in sp.company_stock_data[company_name].keys():
#         print(sp.company_stock_data[company_name])
#         break


# In[ ]:


if(__name__=="__main__"):
    app.run(host="0.0.0.0",port=5002)


