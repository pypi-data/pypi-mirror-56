#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .models import *
import datetime
import sense_core as sd
from . import msg_base, utils
import time


class MonitMsgSender(object):
	
	def send_err_message(self, module, title, phone_list):
		if phone_list:
			if type(phone_list) == list:
				phone_list = phone_list
			elif type(phone_list) == str:
				phone_list = [phone_list]
		else:
			return None
		send_res = self.send_message(module, title, phone_list)
		if not send_res:
			sd.log_info('[*] Module ' + module + ' errors message has been sent failed.')

	def send_message(self, module, title, phone_list):
		msg_res = self._send_msg_detail(phone_list, module, title)
		return msg_res
	
	def _send_msg_detail(self, phone_list, module, err_title):
		failed_list = []
		suc_list = []
		template_code = sd.config('aliyun_sms', 'msg_template', '')
		if template_code == '':
			sd.log_info('The template code is empty')
			return None
		if not phone_list or len(phone_list) == 0:
			sd.log_info('The receiver phone is empty')
			return None
		for phone in phone_list:
			if not phone:
				sd.log_info('[ALIYUN] ' + str(phone) + ' is not a phone number!')
				continue
			res = eval(
				msg_base.send_sms(phone, template_code, {'code': -9, 'message': '(' + module + ') ' + err_title}).decode())
			res_suc, res_failed = self._parse_msg_res(res, phone)
			suc_list.extend(res_suc)
			failed_list.extend(res_failed)
			time.sleep(2)
		if len(failed_list) == 0:
			res = utils.build_dic(code='OK', flag='message', addr=phone_list, content=template_code)
			sd.log_info('message send successful!!!')
		else:
			res = utils.build_dic(code='Failed', flag='message', content=template_code, failed_list=failed_list,
								  suc_list=suc_list)
		return res
	
	def _parse_msg_res(self, res, phone):
		failed_list = []
		suc_list = []
		if not isinstance(res, dict) or 'Code' not in res:
			return None
		if res['Code'] == 'OK':
			suc_list.append(phone)
		else:
			failed_list.append(phone)
		return suc_list, failed_list
