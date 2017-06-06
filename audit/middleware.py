# -*- coding: utf-8 -*-
import threading

class RequestMiddleware(object):
	thread_local = threading.local()

	def __init__(self, get_response):
		self.get_response = get_response
		# One-time configuration and initialization.        

	def __call__(self, request):
		# Code to be executed for each request before
		# the view (and later middleware) are called.
		self.thread_local.user = request.user

		response = self.get_response(request)

		# Code to be executed for each request/response after
		# the view is called.

		return response