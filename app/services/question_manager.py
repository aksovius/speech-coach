user_questions = {}

def set_user_question(user_id, question):
    user_questions[user_id] = question

def get_user_question(user_id):
    return user_questions.get(user_id)
