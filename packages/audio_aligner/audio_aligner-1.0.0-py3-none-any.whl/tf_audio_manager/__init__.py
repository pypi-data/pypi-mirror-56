# -*- coding: utf-8 -*-

import json
import requests


class audio_aligner:
    def upload(self,path: str):
        """
        上传函数
        :param source:
        :return:
        """
        files = {'file': open('/Users/duyining/Desktop/chinese_test.zip', 'rb')}
        resp = requests.post('http://119.23.204.245:9073/aligner/upload',files = files)
        if resp.ok :
            status = json.loads(resp.text).get('code')
            return status
        else :
            return 'request failed'
    def list(self):
        """
        展示函数
        """
        print('111')
        resp = requests.post('http://119.23.204.245:9073/aligner/display')
        if resp.ok:
            status = json.loads(resp.text).get('code')
            try:
                if status == 0:
                    json_obj = json.loads(resp.text).get('data')[0]
                    temp = {'name': json_obj['org_filename'], 'status': json_obj['tags'],
                            'upload_time': json_obj['upload_time'], 'id': json_obj['task_id'],
                            'language': json_obj['language']}
                    return (temp)
            except Exception as error:
                return (error)
        else:
            return ('request failed')

    def chinese_align(self, id):
        """
        中文对齐函数
        """
        print('11')
        resp = requests.post('http://119.23.204.245:9073/aligner/chinese', {"id": id})

        if resp.ok:

            status = json.loads(resp.text).get('code')
            try:
                if status == '0':
                    json_obj = json.loads(resp.text).get('data')[0]
                    return json_obj
                else :
                    return json.loads(resp.text)
            except Exception as error:
                return error
        else:
            return ('request failed')

    def english_align(self,id):
        """
        英文对齐函数
        :return:
        """
        resp = requests.post('http://119.23.204.245:9073/aligner/english', {"id": id})
        if resp.ok:

            status = json.loads(resp.text).get('code')
            try:
                if status == '0':
                    json_obj = json.loads(resp.text).get('data')[0]
                    return json_obj
            except Exception as error:
                return error
        else:
            return ('request failed')

    def download(self,id):
        """
        下载函数
        :return:
        """
        resp = requests.post('http://119.23.204.245:9073/aligner/download', {'id': id})
        if resp.ok:

            status = json.loads(resp.text).get('code')
            try:
                if status == '0':
                    json_obj = json.loads(resp.text).get('data')[0]
                    return json_obj
            except Exception as error:
                return error
        else:
            return ('request failed')





if __name__ == "__main__":
    list()
