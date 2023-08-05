#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .models import *
import datetime
import sense_core as sd
from . import email_base, utils


class MonitEmialSender(object):
	
	def send_err_email(self, module, title,  subject, receiver_email):
		email_list = []
		if receiver_email:
			if type(receiver_email) == list:
				email_list = receiver_email
			elif type(receiver_email) == str:
				email_list = [receiver_email]
		else:
			return None
		send_res = self.send_email(module, title, subject, email_list)
		if not send_res or send_res == '':
			sd.log_info('[*] Module ' + module + ' errors email has send failed.')

	def send_email(self, module, title, subject, email_list=None):
		_now = datetime.datetime.now()
		msg_res = self._send_email_detail(module, email_list, subject, title)
		return msg_res
	
	def _send_email_detail(self, module, email_list, subject, title):
		if not email_list or len(email_list) == 0:
			sd.log_info('The receiver email is empty')
			return {}
		_res = email_base.send_email(module, email_list, subject, title)
		res = self._is_mail_failed(_res)
		if res:
			_res = utils.build_dic(code='Failed', flag='email', failed_list=res)
		else:
			_res = utils.build_dic(code='OK', flag='email', addr=email_list)
			sd.log_info('email send successful!!!')
		return _res

	def _is_mail_failed(self, res):
		if not isinstance(res, dict):
			return []
		if len(res) == 0:
			return False
		return list(res.keys())

