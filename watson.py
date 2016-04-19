#!/usr/bin/env python

import requests
import json
import sys

class Watson:
    QA_URL = 'https://dal09-gateway.watsonplatform.net/instance/579/deepqa/v1/question'
    failsafe = {
        u'What is a dumbbell?' : 'Barbells with a short rod are called dumbbells.',
        u'How do I perform a deadlift?' : """The deadlift is a very effective compound exercise for strengthening the lower back, but also exercises many
             other major muscle groups, including quads, hamstrings and abdominals. It is a challenging exercise, as
             poor form or execution can cause serious injury. A deadlift is performed by grasping a dead weight on the
             floor and, while keeping the back very straight, standing up by contracting the erector spinae (primary
             lower back muscle). When performed correctly the role of the arms in the deadlift is only that of cables
             attaching the weight to the body; the musculature of the arms should not be used to lift the weight. There
             is no movement more basic to everyday life than picking a dead weight up off of the floor, and for this
             reason focusing on improving one's deadlift will help prevent back injuries.""",
        u'What\'s an isometric exercise?' : """An isometric exercise is a form of exercise involving the static contraction of a muscle without any visible
             movement in the angle of the joint. The term "isometric" combines the Greek words "Isos" (equal) and
             "metria" (measuring), meaning that in these exercises the length of the muscle and the angle of the joint
              do not change, though contraction strength may be varied. This is in contrast to isotonic contractions, in
               which the contraction strength does not change, though the muscle length and joint angle do.""",
       u'How much water should I drink a day?' : 'Drink 8 - 10 glasses of water a day.',
       u'How many servings of vegetables do I need in a day?' : '2.5 cups for individuals who get less than 30 minutes of moderate physical activity per day, beyond normal daily activities. Individuals who are more physically active may be able to consume more while staying within calorie needs.',
       u'Is running on ground better than running on a treadmill?' : 'You can multi-task if you go outdoors! At my old job, I used to run to the post office to drop off mail. You could end your run at the grocery store and then walk back with groceries as your cool-down. It\'s easier to do a hill workout naturally than constantly pushing the buttons on a treadmill especially if you want to do a really steep hill (which can take FOREVER on the treadmill to adjust). You could run to friend\'s/relative\'s house and have them prepare you a nice post-run meal ;-) and then have them drive you home or you could run back. You can scope out the fine guys running with their shirts off or fine girls running in their sports bra (I once saw my vice president working out in her sports bra at our gym, that was awkward to see so much skin on a co-worker but she did have a nice six-pack.). Source:https://fitness.stackexchange.com/questions/1040',
       u'How do I train for a marathon?' : 'The best way to get injured with marathon training is to not have a solid running base. Slowly increase your mileage by increasing duration / distance NOT intensity. Your training should mirror the race your planning to run. Any training plan worth its salt will give you a recommend base. Hal Higdon\'s novice plan recommends: but ideally before starting a marathon program, you should have been running about a year. You should be able to comfortably run distances between 3 and 6 miles. You should be training 3-5 days a week, averaging 15-25 miles a week. You should have run an occasional 5-K or 10-K race. It is possible to run a marathon with less of a training base (particularly if you come from another sport), but the higher your fitness level, the easier this 18-week program will be. A good book is Pfitzinger\'s Advanced Marathoning (don\'t let the title scare you). It has a lot of the background info on how the plans were constructed, etc. In short: Run lots, have a good base, have proper shoes, and take care of your body. Source:https://fitness.stackexchange.com/questions/1772',
       u'How many calories should I eat in a day?' : 'Well, you can figure out how many calories your body burns in a resting state (BMR) by using one of the various calculators on the Internet. Once you get your resting BMR, you just have to multiply that by your activity factor, and that should give you a rough estimate of how many calories you burn in a day. Source:https://fitness.stackexchange.com/questions/948.'
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

    @staticmethod
    def get_S2T_token():
        url = 'https://stream.watsonplatform.net/authorization/api/v1/token?url=https://stream.watsonplatform.net/speech-to-text/api'
        token = ''
        auth = requests.auth.HTTPBasicAuth('0b462a68-399a-4215-af5d-12d202626755', 'lZlK8NpmVSAK')
        r = requests.get(url, auth=auth)
        token = r.text
        return token

    @staticmethod
    def get_T2S_token():
        auth = requests.auth.HTTPBasicAuth('5f6e100d-796c-4e85-879f-671b96332e0e', 'JAiEdmecnpzJ') 
        token = ''
        return token

def main(question, user, password):
    watson = Watson(user, password)
    print(watson.get_S2T_token())
    answer = watson.ask(question)
    print(answer)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print ('Usage: ' + __file__ + ' <question> <username> <password>')
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
