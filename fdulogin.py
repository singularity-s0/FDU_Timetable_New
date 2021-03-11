# !/usr/bin/env python
# --------------------------------------------------------------
# File:          fdulogin.py
# Project:       FDU_Timetable
# Created:       Tuesday, 12th November 2019 9:32:46 pm
# @Author:       Molin Liu, MSc in Data Science
# Contact:          molin@live.cn
# Last Modified: Tuesday, 12th November 2019 9:32:51 pm
# Copyright  © Rockface 2019 - 2020     © Recallu 2019 - 2020
# --------------------------------------------------------------

'''
复旦大学统一身份认证登录
'''

import requests
import time
import datetime
import pytz
import os
import pickle
import time
from bs4 import BeautifulSoup
# User's modules
from FDU_headers import HEADER_CAPTCHA, HEADER_LOGIN, HEADER_LT
from utils import parseCookie, saveHtml
from log import LogConfig

'''
Initialize Logger
'''
logger = LogConfig('console').getLogger()


class FDU_User():
    '''
    Class FDU_User is designed for logining to 
    teaching system.
    '''

    def __init__(self, fdu_id, fdu_pw):
        self.__session = requests.Session()
        self.__cookies = None
        self.__fdu_id = fdu_id
        self.__fdu_pw = fdu_pw
        self.__form_login = {}
        self.__gen_header = {}

        self._needCaptcha()
        self._get_lt()
        time.sleep(2)
        resp_login = self.login()
        saveHtml('Login', resp_login.text, resp_login.status_code)

    def _get_lt(self):
        '''
        Get lt verification code
        '''
        header = HEADER_LT
        response = self.__session.get(
            "http://uis.fudan.edu.cn/authserver/login?service=http%3A%2F%2Fjwfw.fudan.edu.cn%2Feams%2Flogin.action", headers=header)
        if response.status_code == 200:
            logger.info("SUCCESS: Get lt code.")
        else:
            logger.error("FAIL: Get lt code.")
        if response.status_code == 200:
            parsed_text = BeautifulSoup(response.text, 'lxml')
            self.__form_login['lt'] = (parsed_text.body.find(
                'input', attrs={'name': 'lt', 'type': 'hidden'}))['value']
            self.__form_login['_eventId'] = (parsed_text.body.find(
                'input', attrs={'name': '_eventId', 'type': 'hidden'}))['value']
            self.__form_login['execution'] = (parsed_text.body.find(
                'input', attrs={'name': 'execution', 'type': 'hidden'}))['value']
            self.__form_login['dllt'] = (parsed_text.body.find(
                'input', attrs={'name': 'dllt', 'type': 'hidden'}))['value']
            self.__form_login['_eventId'] = (parsed_text.body.find(
                'input', attrs={'name': '_eventId', 'type': 'hidden'}))['value']
            self.__cookies = response.cookies.get_dict()
            self.__cookies.update(
                {"route": "261c7137ce5a442a6edfb7812f5be6ad"})
        else:
            raise Exception(
                "Cannot connect to FDU Teaching Affair login page.")

    def login(self):
        '''
        Login to jwfw.fdu
        '''
        waiting_time = 3
        logger.info("Wait for %ds." % waiting_time)
        time.sleep(waiting_time)
        url = "http://uis.fudan.edu.cn/authserver/login?service=http%3A%2F%2Fjwfw.fudan.edu.cn%2Feams%2Flogin.action"
        form_data = {
            "username": self.__fdu_id,
            "password": self.__fdu_pw,
        }
        self.__form_login.update(form_data)
        logger.info(self.__form_login)
        login_header = HEADER_LOGIN
        self._needCaptcha()
        response = self.__session.post(
            url, data=self.__form_login, headers=login_header, cookies=self.__cookies, timeout=40, allow_redirects=False)
        if response.status_code == 200:
            logger.error(self.__cookies)
            logger.error("Login Fails")
        if response.status_code == 302:  # First redirect
            logger.info("SUCCESS: Login")
            auth_cookies = response.cookies.get_dict()
            set_cookies = parseCookie(response.headers['Set-Cookie'])
            self.__cookies.update(auth_cookies)
            self.__cookies.update(set_cookies)
            resp_1 = self.login_redirect(response, 1)
            resp_2 = self.login_redirect(resp_1, 2)
            return resp_2

    def _needCaptcha(self):
        '''
        Generate time stamp for needcaptcha
        Auth will be expired 1 day 
        '''

        header = HEADER_LOGIN
        self.__gen_header = header
        pst_now_0 = datetime.datetime.now(pytz.timezone("Etc/GMT+0"))
        time_stamp = int(float(pst_now_0.strftime("%s.%f"))*1000)
        url = "http://uis.fudan.edu.cn/authserver/needCaptcha.html?username=%s&_=%s" % (
            self.__fdu_id, time_stamp)
        response = self.__session.get(url, headers=header)
        if response.status_code == 200:
            logger.info("SUCCESS: Pass needCaptcha check.")
        else:
            logger.error("FAIL: needCaptcha check")
        return response

    def login_redirect(self, response, index):
        '''
        Handle redirect
        '''
        logger.info("Redirect to %s" % response.url)
        url = response.url
        header = HEADER_LOGIN
        resp = self.__session.get(
            url, headers=header, cookies=self.__cookies)
        logger.info("Redirect_%d: %d" % (index, resp.status_code))
        set_cookies = parseCookie(resp.headers['Set-Cookie'])
        self.__cookies.update(set_cookies)
        saveHtml('Redirct_%d' % index, resp.text, resp.status_code)
        return resp

    def finish_login(self):
        return self.__session, self.__cookies
