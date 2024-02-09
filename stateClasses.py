from aiogram.dispatcher.filters.state import StatesGroup, State


class FeedbackState(StatesGroup):
    take_quest = State()
    checker = State()
class bot_ans(StatesGroup):
    user_id=State()
    ans=State()

class AnswerState(StatesGroup):
    user_id = State()
    take_response = State()
