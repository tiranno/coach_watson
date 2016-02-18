#!/usr/bin/env python

import requests
import json
import sys

class Watson:
    QA_URL = 'https://dal09-gateway.watsonplatform.net/instance/579/deepqa/v1/question'
    failsafe = {
        u'What is a dumbbell?' : 'Barbells with a short rod are called dumbbells.',
        u'How do I perform a deadlift?' : """
            The deadlift is a very effective compound exercise for strengthening the lower back, but also exercises many
             other major muscle groups, including quads, hamstrings and abdominals. It is a challenging exercise, as
             poor form or execution can cause serious injury. A deadlift is performed by grasping a dead weight on the
             floor and, while keeping the back very straight, standing up by contracting the erector spinae (primary
             lower back muscle). When performed correctly the role of the arms in the deadlift is only that of cables
             attaching the weight to the body; the musculature of the arms should not be used to lift the weight. There
             is no movement more basic to everyday life than picking a dead weight up off of the floor, and for this
             reason focusing on improving one's deadlift will help prevent back injuries.
            """,
        u'What\'s an isometric exercise?' : """
            An isometric exercise is a form of exercise involving the static contraction of a muscle without any visible
             movement in the angle of the joint. The term \"isometric\" combines the Greek words \"Isos\" (equal) and
             \"metria\" (measuring), meaning that in these exercises the length of the muscle and the angle of the joint
              do not change, though contraction strength may be varied. This is in contrast to isotonic contractions, in
               which the contraction strength does not change, though the muscle length and joint angle do.
            """
    }

    def __init__(self, user, password):
        self.USER = user
        self.PASS = password

    def ask(self, question):
        data = json.dumps({'question':{'questionText':question}})
        headers = {'content-type':'application/json', 'accept':'application/json', 'X-SyncTimeout':'30'}
        answer = ''
        try:
            auth = requests.auth.HTTPBasicAuth(self.USER, self.PASS)
            r = requests.post(Watson.QA_URL, data=data, headers=headers, auth=auth)
            answer = json.loads(r.text)[u'question'][u'evidencelist']
            for a in answer:
                if a.has_key(u'text'):
                    if a.has_key(u'metadataMap'):
                        if a[u'metadataMap'].has_key(u'originalfile'):
                            print a[u'metadataMap'][u'originalfile'][:11]
                            if a[u'metadataMap'][u'originalfile'][:11] == 'CoachWatson':
                                answer = a[u'text']
                                break
        except:
            if Watson.failsafe.has_key(question):
                answer = Watson.failsafe[question]
            else:
                answer = 'Please ask again.'

        return answer

def main(question, user, password):
    watson = Watson(user, password)
    answer = watson.ask(question)
    print(answer)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print ('Usage: ' + __file__ + ' <question> <username> <password>')
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
