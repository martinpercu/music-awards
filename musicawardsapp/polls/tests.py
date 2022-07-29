import datetime
from urllib import response

from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse

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
        time_now = timezone.now() - datetime.timedelta(days=0.0)
        time_almost_far_from_present = timezone.now() - datetime.timedelta(days=0.99)
        present_question = Question(question_text="Question in exactly same moment for testing?", pub_date=time_now)
        almost_present_question = Question(question_text="Question in exactly same moment for testing?", pub_date=time_almost_far_from_present)
        self.assertIs(present_question.was_published_recently(), True)
        self.assertIs(almost_present_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question with the given "question_text".
    Use days to indique when the question was or will be published. 
    Negative number indicates days in the past. Posive ones days in the future
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)



class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """If no question exist, a raisonable message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls here in" and "re here there is a probl")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_show_question_of_future(self):
        """If a question from future is show returns False"""
        time_in_future = timezone.now() + datetime.timedelta(days=30)
        question_from_future = Question(question_text="Question from the future?", pub_date=time_in_future)
        question_from_future.save()
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Question from the future?")


    def test_show_question_of_future_2(self):
        """A question from FUTURE does not be displayed in the index:polls"""
        create_question("Question from the Future", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls here in")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_show_question_of_past(self):
        """A question from PAST will be displayed in the index:polls"""
        question = create_question("Question from the Past", days=-1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])


    def test_past_and_future_questions(self):
        """ If there are future and past question. Only the past ones must to be showed"""
        question_past = create_question(question_text= "Question from past", days=-20)
        question_future = create_question(question_text= "Question from past", days=20)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [question_past]
        )

    def test_two_past_questions(self):
        """ If there are 2 question in the past must to be displayed both of them"""
        question_past_1 = create_question(question_text= "Question from past", days=-20)
        question_past_2 = create_question(question_text= "Question from past", days=-22)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [question_past_1, question_past_2]
        )

    def test_two_future_questions(self):
        """ If there are 2 question from the future no one will be displayed"""
        question_future_1 = create_question(question_text= "Question from past", days=10)
        question_future_2 = create_question(question_text= "Question from past", days=8)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            []
        )
        

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """ If in the detail view we try a with a question with a pub_date in the future must returns a 404 error"""
        question_future = create_question(question_text= "Question from past", days=10)
        url = reverse('polls:detail', args=(question_future.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)



    def test_past_question(self):
        """ If in the detail view we try a with a question with a pub_date in the past must show the question_text"""
        question_in_the_past = create_question(question_text= "Question from past", days=-1)
        url = reverse('polls:detail', args=(question_in_the_past.id,))
        response = self.client.get(url)
        self.assertContains(response, question_in_the_past.question_text)
        