# -*- coding: utf-8 -*-
'''
Created on 2012-3-27

@author: zhangdong

'''

import time;
from ApiError import APIError;
import UrlHelper;
import urllib2,urllib;
from MultipartPostHandler import MultipartPostHandler;
import cookielib;

NO_CLIENT = -1;
NO_USER = -2;
SUCCESS_CODE=200;

class ApiClient():
    clientId=None;
    clientSecret=None;
    userName=None;
    userPassword=None;
    redirect_uri=None;#返回地址
    host=None;
    access_token=None;
    refresh_token=None;
    expireTime=3600;#过期时间，默认为3600秒，一小时
    header=None;
    
    updateTime=None;#上次更新时间，用来更新token。避免用户取消授权或服务器出错后，重复获取token。
    
    def __init__ (self,clientId,clientSecret,userName=None,userPassword=None,redirect_uri=None,host="api.diandian.com"):
        self.clientId=clientId;
        self.clientSecret=clientSecret;
        self.userName=userName;
        self.userPassword=userPassword;
        self.redirect_uri=redirect_uri;
        self.host=host;
        self.setAccessToken();
    
    def setAccessToken(self):
        if self.clientId==None or self.clientSecret==None:
            raise  APIError(NO_CLIENT,"no client or clientSercet","oauth");
        if self.userName==None or self.userPassword==None: #暂时只支持 grant_type=password
            raise APIError(NO_USER,"userName or userPassword can not be none","oauth");
        if self.access_token!=None:  #如果已有access_token已有了，就reflesh吧。
            url= "https://%s/oauth/token?client_id=%s&client_secret=%s&grant_type=refresh_token&refresh_token=%s&scope=read,write" %(self.host,self.clientId,self.clientSecret,self.refresh_token);
        else:
            url="https://%s/oauth/token?client_id=%s&client_secret=%s&grant_type=password&username=%s&password=%s&scope=read,write" %(self.host,self.clientId,self.clientSecret,self.userName,self.userPassword);
        data=UrlHelper.getGetUrlData(url);
        self.access_token=data["access_token"];
        self.refresh_token=data["refresh_token"];
        self.updateTime=int(time.time());
        
    
    def getAccessToken(self):
        if self.access_token==None or int(time.time())>(self.updateTime+self.expireTime-60) : #未初始化或已过期，更新accessToken。增加60秒的缓冲，以配网速或各机器之间时间的冲图
            self.setAccessToken();
        return self.access_token;
    
    def getInfo(self,url):
        accessToken=self.getAccessToken();
        request=urllib2.Request(url);
        request.add_header('Authorization', 'bearer %s' % accessToken)
        return UrlHelper.getGetRequestData(request);
    
    def postInfo(self,url,params,upload=False):
        accessToken=self.getAccessToken();
        if(not upload):
            request=urllib2.Request(url);
            request.add_header('Authorization', 'bearer %s' % accessToken);
            request.add_data(urllib.urlencode(params));
            return UrlHelper.getPostByRequestData(request);
        else:
            print "uploadData";
            cookies = cookielib.CookieJar()
            multipartPostPostHandler=MultipartPostHandler(accessToken);
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),
                                    multipartPostPostHandler)
            return opener.open(url,params).read();
    def setToken(self,accessToken,refreshToken):
        self.access_token=accessToken;
        self.refresh_token=refreshToken;
                   
    
    


def main():
#    test=ApiClient("d93ed7dae7","667ce0989baf21218149666ca1408bc3","zd0309@163.com","diandian","127.0.0.1","api.diandian.com");
    test=ApiClient("0b3f45b266","bff5853860017b56daaab6eff43f94c8","zd0309@163.com","diandian","127.0.0.1","api.diandian.com");
    print test.getAccessToken();
    print test.refresh_token;
#    print test.expireTime;
#    print test.updateTime;
#    home=test.getInfo("http://10.0.3.19:8080/v1/user/home");
#    print home;
#    params={"type":"link","state":"published","tag":"ddtest,zdtest","title":"zdTest","url":"www.diandian.com","description":"apitest"};
#    print test.postInfo("http://10.0.3.19:8080/v1/blog/apitest.diandian.com/post", params);
    params={"type":"photo","state":"published","tag":"ddtest,zdtest","caption":"apitest","data":open("data.jpg")};
    print test.postInfo("http://10.0.3.19:8080/v1/blog/apitest.diandian.com/post", params,True);

if __name__=="__main__":
    main()
    
        
    
            
