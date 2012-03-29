#-*- encoding:utf-8 -*-
'''
Created on 2012-3-27

@author: zhangdong
'''

import urllib2
import urllib
import JsonHelper
from ApiError import APIError;
from urllib2 import HTTPError
'''
获取url内容
'''
def getInfoByUrl(url):
    print url;
    print "aaa"
    try:
        response=urllib2.urlopen(url);
    except HTTPError as e:
        raise  APIError(e.code,e.msg,"");
    html=response.read();
    return html;

'''
提交内容
'''
def postInfo(url,params):
    request = urllib2.Request(url,urllib.urlencode(params));
    response = urllib2.urlopen(request);
    result=response.read();
    print result;
    return result;

'''
获取某一请求的状态
'''

def getGetUrlData(url):
    return JsonHelper.getDataByJson(getInfoByUrl(url));

def getPostUrlData(url,params):
    return JsonHelper.getDataByJson(postInfo(url,params));

def getInfoByRequest(request):
    try:
        response=urllib2.urlopen(request);
    except HTTPError as e:
        raise  APIError(e.code,e.msg,"");
    html=response.read();
    return html;

def getGetRequestData(request):
    return JsonHelper.getDataByJson(getInfoByRequest(request));

def postInfoByRequest(request):
    
    try:
        response = urllib2.urlopen(request);
    except HTTPError as e:
        raise  APIError(e.code,e.msg,"");
    result=response.read();
    return result; 

def getPostByRequestData(request):
    return JsonHelper.getDataByJson(postInfoByRequest(request));





