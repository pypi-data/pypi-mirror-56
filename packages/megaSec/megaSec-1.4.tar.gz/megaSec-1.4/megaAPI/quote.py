# -*- coding: utf-8 -*-
from ctypes import c_int ,c_char_p,CDLL
import time,os

SHO = 0x01
size = 1024
dlen = 1024
      
class UFIIS:
    """quote class"""
    def __init__(self):
               
        #報價主機連線
        self.connect = -99
        
        #傳送
        self.request = -99
        
        #接收
        self.receive= -99
        
        #接收資料
        self.buffer = bytes(size)
        
        #格式化資料
        self.bufferFormat = ''
        
        #dict data
        self.bufferDict = None
        
        #訊息
        self.msg = ''
        
        path = os.path.dirname(__file__)
        if(os.environ['path'].find(path) == -1):
            os.environ['path'] += ";{}".format(path)
                             
        hllDll = CDLL("uFIISAPI.dll")
        self.uFIIS_initialize = hllDll.uFIIS_initialize
        self.uFIIS_connect = hllDll.uFIIS_connect
        self.uFIIS_request = hllDll.uFIIS_request
        self.uFIIS_recv = hllDll.uFIIS_recv
        self.uFIIS_subscribe = hllDll.uFIIS_subscribe
        self.uFIIS_unsubscribe = hllDll.uFIIS_unsubscribe
        self.uFIIS_disconnect = hllDll.uFIIS_disconnect
        self.uFIIS_deinitialize = hllDll.uFIIS_deinitialize
        
        hllDll.uFIIS_initialize.argtypes = [c_char_p,c_int, c_char_p,c_char_p,c_int]
        hllDll.uFIIS_connect.argtypes = [c_char_p,c_int, c_char_p,c_char_p,c_char_p]
        hllDll.uFIIS_request.argtypes = [c_char_p,c_int]
        hllDll.uFIIS_recv.argtypes = [c_char_p,c_int]
        hllDll.uFIIS_subscribe.argtypes = [c_int,c_char_p]
        hllDll.uFIIS_unsubscribe.argtypes = [c_int,c_char_p]
        hllDll.uFIIS_disconnect.argtypes = []
        hllDll.uFIIS_deinitialize.argtypes = []
        
        hllDll.uFIIS_initialize.restype = c_int
        hllDll.uFIIS_connect.restype = c_int
        hllDll.uFIIS_request.restype = c_int
        hllDll.uFIIS_recv.restype = c_int
        hllDll.uFIIS_subscribe.restype = c_int
        hllDll.uFIIS_unsubscribe.restype = c_int
        hllDll.uFIIS_disconnect.restype = c_int
        hllDll.uFIIS_deinitialize.restype = c_int
        
    
    def setInitialize(self,verifyServerIP,verifyServerPort,uid,pwd):                
        """
        "驗證登入身份"    
        """
        verifyServerIP =  (c_char_p)(bytes(verifyServerIP,encoding='ASCII'))
        verifyServerPort =  (c_int)(verifyServerPort)
        uid =  (c_char_p)(bytes(uid,encoding='ASCII'))
        pwd =  (c_char_p)(bytes(pwd,encoding='ASCII'))               
        return  self.uFIIS_initialize(verifyServerIP,verifyServerPort,uid,pwd,(c_int)(64 * 1024))
    
    
    def setConnect(self,quoteServerIP,quoteServerPort):   
        """
        報價主機連線
        """
        quoteServerIP = (c_char_p)(bytes(quoteServerIP,encoding='ASCII'))
        quoteServerPort = (c_int)(quoteServerPort)       
        self.connect = self.uFIIS_connect(quoteServerIP, quoteServerPort,(c_char_p)(b'SFIF'),(c_char_p)(b'SFIF'),(c_char_p)(b'SYSTEX'))
        return self.connect
    
    
    def setRequest(self,market,code,tag35 = "0x03"):
        """
        設定要取得的回補資料
        """
        szContent = ""
        szPacket = ""
        iDataLen = 0
        iLen = 0;
        iCheckSum = 0
        szTag8 = "8=SFIF1.0"
        szTag35 = f"35={tag35}"
        szTag12 = "12=9001"
        szTag13 = "13=FIISCom"
        szTag36 = f"36={market}" 
        szTag55 = f"55={code}"
      
        szContent = '%s%c%s%c%s%c%s%c%s%c'%(szTag35, SHO,szTag36, SHO,szTag55, SHO,szTag12, SHO,szTag13, SHO)
        
        iLen = len(szContent)
                
        for i in range(iLen):
         iCheckSum+=ord(szContent[i])
        
        iCheckSum %=256
        
        szTag9 = "9=%d"%(iLen)
        szTag10 = "10=%d"%(iCheckSum)
        szPacket = '%s%c%s%c%s%s%c'%(szTag8, SHO,szTag9, SHO,szContent,szTag10, SHO)
        iDataLen = len(szPacket)
                
        self.request = self.uFIIS_request((c_char_p)(bytes(szPacket, encoding = "UTF-8")),(c_int)(iDataLen))
        time.sleep(0.5)
        return self.request
        
        
    
    def setRecv(self):
        """
        收資料
        """
        self.buffer = bytes(size)
        self.bufferFormat = ''
        self.bufferDict = None
        if(self.connect < 0):
            self.msg = "Not connected yet"
            return self.receive
               
        self.receive = self.uFIIS_recv((c_char_p)(self.buffer),(c_int)(dlen))
        
        if(self.receive > 0):            
            self.bufferFormat = self.buffer.decode(encoding = "big5").rstrip('\x00').rstrip('{:c}'.format(0x01))
            self.bufferDict = dict(item.split("=") for item in self.bufferFormat.split('{:c}'.format(0x01)))
        elif(self.receive < 0):
            if (self.receive == -3):                    
                self.msg = "Coneection is trminated. Please try to re-connect again."
            else:            
                self.msg = "Coneection is error"
        else:
            self.msg = "No data"
            
        return self.receive
        
    
    def setSubscribe(self,market,code):
        """
        訂閱商品即時行情
        """
        market = (c_int)(int(market, 16))
        code = (c_char_p)(bytes(code,encoding='ASCII'))            
        return self.uFIIS_subscribe(market,code)
         
    
    
    def setUnSubscribe(self,market,code):
        """
        取消訂閱商品
        """
        market = (c_int)(int(market, 16))
        code = (c_char_p)(bytes(code,encoding='ASCII'))        
        return self.uFIIS_unsubscribe(market,code)
    
    
    def setDisconnect(self):
        """
        釋放連線
        """
        self.uFIIS_disconnect()
    
    
    def setDeinitialize(self):
        """
        釋放資源
        """
        self.uFIIS_deinitialize()

