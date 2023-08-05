"""
音频对齐sdk
"""
# -*- coding: utf-8 -*-

import json
import threading
import requests


class AudioAligner:
    """
    语音对齐类
    """

    def __init__(self, host='', port='', protocol='http'):
        """
        初始化函数
        :param host:
        :param port:
        :param protocol:
        """
        self._cookies = ''
        # self.host = '{}://{}'.format(protocol, '119.23.204.245')
        self.host = '{}://{}'.format(protocol, host)
        # self.port = '9073'
        self.port = port
        self.url = '{}:{}'.format(self.host, self.port)

    def upload(self, path: str):
        """
        上传函数
        :param path:
        :return:
        """
        files = {'file': open(path, 'rb')}
        resp = requests.post(self.url + '/aligner/upload', files=files, cookies=self._cookies)
        self._cookies = resp.cookies
        if not resp.ok:
            return 'request failed'
        status = json.loads(resp.text)
        return status

    def check_status(self, job_id):
        """
        查看状态函数
        :param job_id:
        :return:
        """
        resp = requests.get(self.url + '/aligner/check', {'id': str(job_id)}, cookies=self._cookies)
        return json.loads(resp.text)

    def list(self, page=0):
        """
        展示函数
        """
        resp = requests.get(self.url + '/aligner/display', {page: page}, cookies=self._cookies)
        result = []
        if resp.ok:
            status = json.loads(resp.text).get('code')
            try:
                if status == 0:
                    json_obj = json.loads(resp.text).get('data')
                    for i in json_obj:
                        temp = {'name': i['org_filename'], 'status': i['tags'],
                                'upload_time': i['upload_time'], 'id': i['task_id'],
                                'language': i['language']}
                        result.append(temp)
                    return result
            except Exception as error:
                return repr(error)
        else:
            return 'request failed'

    def chinese_align(self, task_id):
        """
        中文对齐函数
        """
        resp = requests.post(self.url + '/aligner/chinese', {"id": task_id})

        if resp.ok:

            status = json.loads(resp.text).get('code')
            try:
                if status == '0':
                    json_obj = json.loads(resp.text).get('data')[0]
                    return json_obj
                return json.loads(resp.text)
            except Exception as error:
                return error
        else:
            return 'request failed'

    def chinese_thread(self, task_id):
        """
        异步函数
        :param task_id:
        :return:
        """

        _thread = threading.Thread(target=self.chinese_align, args=(task_id,))
        _thread.start()
        return 'start'

    def english_align(self, task_id):
        """
        英文对齐函数
        :return:
        """
        resp = requests.post(self.url + '/aligner/english', {"id": task_id})

        if resp.ok:

            status = json.loads(resp.text).get('code')
            try:
                if status == '0':
                    json_obj = json.loads(resp.text).get('data')[0]
                    return json_obj
                return json.loads(resp.text)
            except Exception as error:
                return error
        else:
            return 'request failed'

    def english_thread(self, task_id):
        """
        异步函数
        :param task_id:
        :return:
        """

        async_t = threading.Thread(target=self.english_align, args=(task_id,))
        async_t.start()
        return 'start'

    def download(self, task_id, file_path):
        """
        下载函数
        :return:
        """
        file_path = file_path
        resp = requests.get(self.url + '/aligner/download', {'id': task_id})
        try:
            with open(file_path, 'wb') as file:
                file.write(resp.content)
                return 'success'
        except Exception as error:
            return error
