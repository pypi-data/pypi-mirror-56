import asyncio
import pyppeteer
class _RequestRenderAsync():
  def __init__(self, options, verify, headless, browser_args):
    self.options = options
    self.verify = verify
    self.headless = headless
    self.__browser_args = browser_args
    if(options.get('headless') != None):
      self.headless=options.get('headless')
    if(options.get('verify') != None):
      self.verify=options.get('verify')
  async def browser(self):
    if not hasattr(self, "_browser"):
      self._browser = await pyppeteer.launch(self.options,
        ignoreHTTPSErrors=not(self.verify), headless=self.headless, args=self.__browser_args)
    return self._browser

  async def inject_request(self,req):
    """
    resourceType:
        document, stylesheet, image, media, font, script, texttrack, 
        xhr, fetch, eventsource, websocket, manifest, other
    """
    if req.resourceType in ['media','image']:
      await req.abort()
    else:
      await req.continue_()

  async def inject_response(self,res):
    if res.request.resourceType in ['xhr']:
      print(res.request.url)
  async def afterNewPage(self,page):
    pass
  async def _get(self,url,js=None):
    browser = await self.browser()
    page = await browser.newPage()
    await self.afterNewPage(page)
    await page.setRequestInterception(True)
    page.on('request', self.inject_request)
    page.on('response',self.inject_response)
    await page.goto(url)
    if(js):
      await page.evaluate(js)
    else:
      await page.evaluate(
          '''() =>{Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    doc = await page.content()
    cookies = page.cookies
    await page.close()
    return (doc,cookies)
  
  async def _close(self):
    if hasattr(self, "_browser"):
      await self._browser.close()

class RequestRender():
  def __init__(self, options={}, verify : bool = False, headless : bool = True,
                browser_args : list = ['--disable-infobars','--no-sandbox']):
    if(not options): options={}
    self.options = options
    self.verify = verify
    self.headless = headless
    self.__browser_args = browser_args
    if(options.get('headless') != None):
      self.headless=options.get('headless')
    if(options.get('verify') != None):
      self.verify=options.get('verify')
  async def __browser(self):
    if not hasattr(self, "_browser"):
      self._browser = await pyppeteer.launch(self.options,
        ignoreHTTPSErrors=not(self.verify), headless=self.headless, args=self.__browser_args)
    return self._browser

  async def inject_request(self,req):
    """
    resourceType:
        document, stylesheet, image, media, font, script, texttrack, 
        xhr, fetch, eventsource, websocket, manifest, other
    """
    if req.resourceType in ['media','image']:
      await req.abort()
    else:
      await req.continue_()

  async def inject_response(self,res):
    if res.request.resourceType in ['xhr']:
      print(res.request.url)
  async def afterNewPage(self,page):
    await page.setRequestInterception(True)
    page.on('request', self.inject_request)
    page.on('response',self.inject_response)
    
  async def afterGoto(self,page,js):
    if(js):
      await page.evaluate(js)
    else:
      await page.evaluate(
          '''() =>{Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
  async def _get(self,url,js=None):
    browser = await self.__browser()
    page = await browser.newPage()
    await self.afterNewPage(page)
    await page.goto(url)
    await self.afterGoto(page,js)
    doc = await page.content()
    cookies = page.cookies
    await page.close()
    return (doc,cookies)
  
  async def _close(self):
    if hasattr(self, "_browser"):
      await self._browser.close()

  def get(self,url,callback,extr_data=None,js=None):
    asyncio.get_event_loop().run_until_complete(self._getContent(url,callback,extr_data,js))
  def getCookies(self,url,callback,extr_data=None):
    asyncio.get_event_loop().run_until_complete(self._getCookies(url,callback,extr_data))

  async def _getAsync(self,url,js=None):
    u=url
    if(not isinstance(url,str)):
      u=url.get('url')
    await self.__browser()
    res = await self._get(u,js)
    return res
  async def _getContent(self,url,callback,extr_data=None,js=None):
    res = await self._getAsync(url,js)
    if(callback):
      callback(res[0],url,extr_data)
    return res[0]
  async def _getCookies(self,url,callback,extr_data=None):
    res = await self._getAsync(url)
    if(callback):
      callback(res[1],url,extr_data)
    return res[1]

  def close(self):
    asyncio.get_event_loop().run_until_complete(self._close())
      
