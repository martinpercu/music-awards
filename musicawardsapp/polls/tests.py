import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

# Create your tests here.
# Models
# Views
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """was_published_recently returns False for question whose pub_date is in the future"""
        time_in_future = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="Question in the future for testing?", pub_date=time_in_future)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_past_question(self):
        """was_published_recently returns False for question whose pub_date is in the past"""
        time_in_the_past = timezone.now() - datetime.timedelta(days=1.01)
        past_question = Question(question_text="Question in the past for testing?", pub_date=time_in_the_past)
        self.assertIs(past_question.was_published_recently(), False)

    def test_was_published_recently_with_same_moment_question(self):
        """was_published_recently returns True for question whose pub_date is in the future"""
        time = timezone.now() - datetime.timedelta(days=0.0)
        time_almost_far_from_present = timezone.now() - datetime.timedelta(days=0.99)
        present_question = Question(question_text="Question in exactly same moment for testing?", pub_date=time)
        almost_present_question = Question(question_text="Question in exactly same moment for testing?", pub_date=time)
        self.assertIs(present_question.was_published_recently(), True)
        self.assertIs(almost_present_question.was_published_recently(), True)
