#!/usr/bin/env python

class Bob:
    def __init__(self):
        self.qa_dict = {
            'What workouts should I do this week?' : 'All of them.',
            'What should I eat for dinner?' : 'Pizza and ice cream.',
            'How do I perform a dead lift?' : 'Don\'t bend your knees. It\'s all in the back.',
            'How many miles should I run to lose 5 pounds?' : '30.',
            'What muscles do crunches target?' : 'Biceps.',
            'What\'s a good weight training exercise for legs?' : '''<div class="media">
<div class="media-left">
<a href="#">
<img class="media-object" src="static/res/barbellsquat.png" height="100px">
</a>
</div>
<div class="media-body">
<h3 class="media-heading">Barbell Squats</h3>
<br>
<p>Primary muscles: <a href="https://en.wikipedia.org/wiki/Quadriceps_femoris_muscle">Quadricepts</a></p>
<p>Secondary muscles: <a href="https://en.wikipedia.org/wiki/Calf_(leg)">Calves</a>, <a href="https://en.wikipedia.org/wiki/Gluteal_muscles">Glutes</a>, <a href="https://en.wikipedia.org/wiki/Hamstring">Hamstrings</a></p>
<p>Based on your profile stats and goals, I recommend you complete this exercise 2 times/week,
at an approximate weight of 100 lbs and set/rep count of 3/10.</p>
<a href="#">See more info about this exercise &gt;&gt;&gt; </a>
</div>
</div>''',
            'Hey Watson, what workouts do I have this week?' : '''<div class="">
<table class="table table-hover">
<thead>
<tr>
<th>Mon.</th>
<th>Tue.</th>
<th>Wed.</th>
<th>Thu.</th>
<th>Fri.</th>
</tr>
</thead>
<tbody>
<tr>
<td>Cardio, 30m</td><!-- mon -->
<td>Bicep Curls 3x10</td><!-- tues -->
<td>Crunches, 2x20</td><!-- wedn -->
<td>Walking lunges, 3x10</td><!-- thurs -->
<td>REST</td><!-- fri -->
</tr>
<tr>
<td></td><!-- mon -->
<td>Shoulder press, 2x15</td><!-- tues -->
<td>Plank, 4x30s</td><!-- wedn -->
<td>Calf raises, 3x30</td><!-- thurs -->
<td></td><!-- fri -->
</tr>
<tr>
<td></td><!-- mon -->
<td></td><!-- tues -->
<td>Russian Twists 2x30</td><!-- wedn -->
<td>Jump squat, 2x10</td><!-- thurs -->
<td></td><!-- fri -->
</tr>
</tbody>
</table>
</div>'''
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
