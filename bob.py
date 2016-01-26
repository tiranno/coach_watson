#!/usr/bin/env python

class Bob:
    def __init__(self):
        self.qa_dict = {
            'What workouts should I do this week?' : 'All of them.',
            'What should I eat for dinner?' : 'Pizza and ice cream',
            'How do I perform a dead lift?' : 'Don\'t bend your knees. It\'s all in the back.',
            'How many miles should I run to lose 5 pounds?' : '30.',
            'What muscles do crunches target?' : 'Biceps.'
        }
        self.wrong_question = 'Try again.'

    def ask(self, question):
        if (self.qa_dict.has_key(question)):
            return self.qa_dict[question]
        else:
            return self.wrong_question

    def __str__(self):
        return str(self.qa_dict)

def main():
    bob = Bob()
    print(bob)

if __name__ == '__main__':
    main()
