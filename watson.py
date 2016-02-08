#!/usr/bin/env python

import requests
import json
import sys

class Watson:
    QA_URL = 'https://dal09-gateway.watsonplatform.net/instance/579/deepqa/v1/question'

    def __init__(self, user, password):
        self.USER = user
        self.PASS = password

    def ask(self, question):
        data = json.dumps({'question':{'questionText':question}})
        headers = {'content-type':'application/json', 'accept':'application/json', 'X-SyncTimeout':'30'}
        auth = requests.auth.HTTPBasicAuth(self.USER, self.PASS)
        r = requests.post(Watson.QA_URL, data=data, headers=headers, auth=auth)
        return r.text

def main(question, user, password):
    watson = Watson(user, password)
    answer = watson.ask(question)
    print(answer)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print ('Usage: ' + __file__ + ' <question> <username> <password>')
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
