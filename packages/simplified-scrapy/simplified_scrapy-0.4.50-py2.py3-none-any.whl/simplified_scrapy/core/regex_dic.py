import simplified_scrapy.core.logex
from simplified_scrapy.core.regex_helper import *
from simplified_scrapy.core.request_helper import extractHtml
from simplified_scrapy.extracter import ExtractModel
from simplified_scrapy.core.utils import absoluteUrl
from simplified_scrapy.core.dictex import Dict
class RegexDict(Dict):
  def listA(self, url=None,start=None,end=None,before=None):
    if(not self.innerHtml): return None
    return listA(self.innerHtml,url,start,end,before)

  def listImg(self, url=None,start=None,end=None,before=None):
    if(not self.innerHtml): return None
    return listImg(self.innerHtml,url,start,end,before)

  def getElementByID(self, id,start=None,end=None,before=None):
    if(not self.innerHtml): return None
    ele = getElementByID(id,self.innerHtml,start,end,before)
    return RegexDict(ele)

  # def getElementTextByID(self, id,start=None,end=None,before=None):
  #   if(not self.innerHtml): return None
  #   ele = getElementTextByID(id,self.innerHtml,start,end,before)
  #   return RegexDict(ele)

  def getElementByTag(self, tag,start=None,end=None,before=None):
    if(not self.innerHtml): return None
    ele = getElementByTag(tag,self.innerHtml,start,end,before)
    return RegexDict(ele)

  def getElementByClass(self, className,start=None,end=None,before=None):
    if(not self.innerHtml): return None
    ele = getElementByClass(className,self.innerHtml,start,end,before)
    return RegexDict(ele)

  def getElementsByTag(self, tag,start=None,end=None,before=None):
    if(not self.innerHtml): return None
    eles = getElementsByTag(tag,self.innerHtml,start,end,before)
    return self._convert2lst(eles)

  def getElementsByClass(self, className,start=None,end=None,before=None):
    if(not self.innerHtml): return None
    eles = getElementsByClass(className,self.innerHtml,start,end,before)
    return self._convert2lst(eles)

  def getElementByAttr(self, attr,value,start=None,end=None,before=None):
    if(not self.innerHtml): return None
    ele = getElementByAttr(attr,value,self.innerHtml,start,end,before)
    return RegexDict(ele)

  def getElement(self,tag,attr='class',value=None,start=None,end=None,before=None):
    if(not self.innerHtml): return None
    ele = getElement(tag,attr,value,self.innerHtml,start,end,before)
    return RegexDict(ele)

  def removeElement(self,tag,attr='class',value=None,start=None,end=None,before=None):
     if(self.innerHtml): 
      self.innerHtml = removeElement(tag,attr,value,self.innerHtml,start,end,before)
      self.text = self.innerText = removeHtml(self.innerHtml)
     return self

  def getElements(self,tag,attr='class',value=None,start=None,end=None,before=None):
    if(not self.innerHtml): return None
    eles = getElements(tag,attr,value,self.innerHtml,start,end,before)
    return self._convert2lst(eles)
    
  def getChildren(self,tag=None,start=None,end=None,before=None):
    if(not self.innerHtml): return None
    eles = getChildren(self.innerHtml,tag,start,end,before)
    return self._convert2lst(eles)

  # def getSection(self,start=None,end=None,before=None):
  #   if(not self.innerHtml): return None
  #   s,e=getSection(self.innerHtml,start,end,before)
  #   l = 0
  #   if before: l=len(before)
  #   elif start: l=len(start)
  #   return self.innerHtml[s+l:e]
  # def removeHtml(self):
  #   if(not self.innerHtml): return None
  #   self.innerHtml = removeHtml(self.innerHtml)
  #   return self.innerHtml
  def trimHtml(self):
    if(not self.innerHtml): return None
    self.innerHtml = trimHtml(self.innerHtml)
    return self.innerHtml
  
  def _convert2lst(self,eles):
    lst=[]
    if(eles):
      for e in eles:
        lst.append(RegexDict(e))
    return lst