from flaskr import create_app
from models import Question, Category
import random

"""
    This code is to upload 6 sample categories and 12 sample questions to the
    trivia database
"""

sample_categories = [
    {'type': 'Science'},
    {'type': 'Art'},
    {'type': 'Geography'},
    {'type': 'History'},
    {'type': 'Entertainment'},
    {'type': 'Sports'}
]
sample_questions = [
    {
        'question': "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
        'answer': "Maya Angelou",
        'difficulty': 4
    },
    {
        'question': "What boxer's original name is Cassius Clay?",
        'answer': "Muhammad Ali",
        'difficulty': 4
    },
    {
        'question': "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
        'answer': "Apollo 13",
        'difficulty': 5
    },
    {
        'question': "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
        'answer': "Tom Cruise",
        'difficulty': 5
    },
    {
        'question': "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
        'answer': "Edward Scissorhands",
        'difficulty': 5
    },
    {
        'question': "Which is the only team to play in every soccer World Cup tournament?",
        'answer': "Brazil",
        'difficulty': 6
    },

    {
        'question': "Which country won the first ever soccer World Cup in 1930?",
        'answer': "Uruguay",
        'difficulty': 6
    },
    {
        'question': "Who invented Peanut Butter?",
        'answer': "George Washington Carver",
        'difficulty': 4
    },
    {
        'question': "What is the largest lake in Africa?",
        'answer': "Lake Victoria",
        'difficulty': 3
    },
    {
        'question': "In which royal palace would you find the Hall of Mirrors?",
        'answer': "The Palace of Versailles",
        'difficulty': 3
    },
    {
        'question': "The Taj Mahal is located in which Indian city?",
        'answer': "Agra",
        'difficulty': 3
    },
    {
        'question': "Which Dutch graphic artist–initials M C was a creator of optical illusions?",
        'answer': "The Palace of Versailles",
        'difficulty': 3
    },
]


def push_data():
    # Pushing sample categories
    for category in sample_categories:
        new_category = Category(**category)
        new_category.insert()

    # Pushing sample questions
    all_categories = Category.query.all()
    for question in sample_questions:
        new_question = Question(**question)
        new_question.category = random.choice(all_categories)
        new_question.insert()


if __name__ == '__main__':
    app = create_app(test_config=False)
    push_data()
