import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
import tornado.httpserver
import tornado.web
from tornado.curl_httpclient import CurlAsyncHTTPClient
import HttpServerWrapper
import HttpClientWrapper
import datetime
import JsonDecoder
import logging

logger = logging.getLogger(__name__)

class DefaultMsgHandler(tornado.web.RequestHandler):
		def post(self):
			logger.info("Received request from OTT")
			post_body = self.request.body
			logger.debug(post_body)
			msg = JsonDecoder.decodeIncomingMessage(post_body)
			for header in self.request.headers:
				msg.httpHeaders[header] = self.request.headers[header]
			if msg.messageType == "Status":
				logger.debug(msg.toString())
			else:
				self.onMessage(msg)

		def onMessage(self, msgObj):
			logger.debug("default on Mesasge")
			pass
		def onStatus(self, msg):
			pass
		def onError(self):
			pass
		def sendResponse(self, responseCode = 200, headers = {}, content = ""):
			logger.debug("sendingResponse", content)
			
			for key in headers:
				self.set_header(key, headers[key])
			self.set_status(responseCode)
			self.flush()

class DefaultResponseHandler:
		def handleResponse(self,response):
			logger.debug("reason", response.reason)
			logger.debug("code", response.code)
			logger.debug("error", response.error)
			logger.debug("body", response.body)
			logger.debug("headers", response.headers)
			logger.debug("headers", response.request)
			logger.debug("Not Implemented")

class DefaultHttpServerWrapper(HttpServerWrapper.HttpServerWrapper):
		def __init__(self, handler_class=DefaultMsgHandler):
			self.handler_class = handler_class
		
		def startHttpServer(self, port, webhook):
			logger.debug("starting http server")
			application = tornado.web.Application([(webhook, self.handler_class),], )
			server = tornado.httpserver.HTTPServer(application)
			server.listen(port)
			tornado.ioloop.IOLoop.current().start()
	
		def registerCallBack(self, callBack, timer, *args):
			logger.debug("registeringCallback")
			tornado.ioloop.IOLoop.current().add_timeout(datetime.timedelta(seconds=timer),callBack, args)

class DefaultHttpClientWrapper(HttpClientWrapper.HttpClientWrapper):
		def __init__(self, response_handler=DefaultResponseHandler):
			self.client = CurlAsyncHTTPClient()
			self.responseHandler = response_handler()

		def sendRequest(self, url = "",  body = "", headers ={}):
			logger.debug("sending Request")
			logger.debug(body)
			aReq = HTTPRequest(url=url, method = "POST", body=body, headers=headers)
			self.client.fetch(aReq, self.responseHandler.handleResponse)

		def registerCallBack(self, callBack, timer, *args, **kwargs):
			logger.debug("registeringCallback")
			tornado.ioloop.IOLoop.current().add_timeout(datetime.timedelta(seconds=timer),callBack, *args, **kwargs)

		def startTimer(self, callBack, timer, *args, **kwargs):
			logger.debug("registeringCallback")
			tornado.ioloop.IOLoop.current().add_timeout(datetime.timedelta(seconds=timer),callBack, *args, **kwargs)
'''
		def registerCallBack(self, callBack, timer, **kwargs):
			logger.debug("registeringCallback")
			tornado.ioloop.IOLoop.current().add_timeout(datetime.timedelta(seconds=timer),callBack, **kwargs)
'''
