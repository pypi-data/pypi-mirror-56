#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/11/21 11:49
# @Author  : chaonan
# @FileName: middleware.py
import logging
import datetime

logger = logging.getLogger('access.request')


class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        info = self.get_extra(request,response)
        msg = "{user_id} access {build_absolute_uri} ".format(**info)
        logger.info(msg=msg, extra=info)
        return response

    def get_extra(self, request, response):
        result = {}
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
        if not ip:
            ip = request.META.get("REMOTE_ADDR")
        result['ip'] = ip
        result['from_system'] = request.META.get('HTTP_FROM_SYSTEM')
        result['device_info'] = request.META.get('HTTP_DEVICE_INFO')
        result['full_path'] = request.get_full_path()
        result['user_id'] = request.user.id
        result['build_absolute_uri'] = request.build_absolute_uri()
        result['access_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        result['status_code'] = response.status_code
        return result
