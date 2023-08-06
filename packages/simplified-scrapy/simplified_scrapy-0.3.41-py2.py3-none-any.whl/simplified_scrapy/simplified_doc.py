#!/usr/bin/python
#coding=utf-8
import types
import simplified_scrapy.core.logex
from simplified_scrapy.core.regex_helper import *
from simplified_scrapy.core.request_helper import extractHtml
from simplified_scrapy.extracter import ExtractModel
class SimplifiedDoc():
  def __init__(self, html=None,start=None,end=None,before=None):
    self.html=None
    self.last=None
    if(not html): return
    sec = getSection(html,start,end,before)
    if(sec): self.html=html[sec[0]:sec[1]]
    else: self.html=html
  def loadHtml(self,html,start=None,end=None,before=None):
    if(not html): return
    sec = getSection(html,start,end,before)
    if(sec): self.html=html[sec[0]:sec[1]]
    else: self.html=html
  
  def listA(self, html=None, url=None,start=None,end=None,before=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    return listA(html,url,start,end,before)

  def listImg(self, html=None, url=None,start=None,end=None,before=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    return listImg(html,url,start,end,before)

  def getElementByID(self, id, html=None,start=None,end=None,before=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self.last = getElementByID(id,html,start,end,before)
    if(self.last):
      self.last.getChildren=types.MethodType(_getChildren,self.last)
    return self.last
  # def getElementAttrByID(self, id,attr, html=None,start=None,end=None):
  #   if(not html):html=self.html
  #   if(not html and self.last):html=self.last.innerHtml
  #   self.last = getElementAttrByID(id,attr,html,start,end)
  #   return self.last

  def getElementTextByID(self, id, html=None,start=None,end=None,before=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    return getElementTextByID(id,html,start,end,before)

  def getElementByTag(self, tag, html=None,start=None,end=None,before=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self.last = getElementByTag(tag,html,start,end,before)
    if(self.last):
      self.last.getChildren=types.MethodType(_getChildren,self.last)
    return self.last

  def getElementByClass(self, className, html=None,start=None,end=None,before=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self.last = getElementByClass(className,html,start,end,before)
    if(self.last):
      self.last.getChildren=types.MethodType(_getChildren,self.last)
    return self.last

  def getElementsByTag(self, tag, html=None,start=None,end=None,before=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    return getElementsByTag(tag,html,start,end,before)

  def getElementsByClass(self, className, html=None,start=None,end=None,before=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    return getElementsByClass(className,html,start,end,before)

  def getElementByAttr(self, attr,value, html=None,start=None,end=None,before=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self.last = getElementByAttr(attr,value,html,start,end,before)
    return self.last

  def getElement(self,tag,attr='class',value=None, html=None,start=None,end=None,before=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self.last = getElement(tag,attr,value,html,start,end,before)
    if(self.last):
      self.last.getChildren=types.MethodType(_getChildren,self.last)
    return self.last

  def getElements(self,tag,attr='class',value=None, html=None,start=None,end=None,before=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    return getElements(tag,attr,value,html,start,end,before)

  def getParent(self,tag=None,attr=None,value=None,html=None,start=None,end=None,before=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    self.last = getParent(tag,attr,value,html,start,end,before)
    if(self.last):
      self.last.getChildren=types.MethodType(_getChildren,self.last)
    return self.last
    
  def getChildren(self,html=None,tag=None,start=None,end=None,before=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    return getChildren(html,tag,start,end,before)

  def getNexts(self,attr,value,html,tag=None,start=None,end=None,before=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    return getNexts(attr,value,html,tag,start,end,before)
  def getSection(self,html=None,start=None,end=None,before=None):
    if(not html):html=self.html
    if(not html and self.last):html=self.last.innerHtml
    s,e=getSection(html,start,end,before)
    l = 0
    if before: l=len(before)
    elif start: l=len(start)
    return html[s+l:e]
  def removeHtml(self,html):
    return removeHtml(html)
  def trimHtml(self,html):
    return trimHtml(html)
  def getObjByModel(self,html,url=None,models=[{"Type":3}],title=None):
    if(isinstance(models,str)):
      models = json.loads(models)
    if(isinstance(models,dict)):
      models = [models]
    return extractHtml(url,html,models,None,title)
def _getChildren(self,tag=None,start=None,end=None,before=None):
  return getChildren(self.innerHtml,tag,start,end,before)