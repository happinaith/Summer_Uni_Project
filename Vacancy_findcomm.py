import logging
from Parser import *
from aiogram.filters import Command, StateFilter
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.fsm.state import StatesGroup, State
#from aiogram.filters.command import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)

logging.basicConfig(level=logging.INFO)

TOKEN = "7251236153:AAH1zGT_oTpH8X7n31pYqzhzXbpeFAWe1nc"

bot = Bot(TOKEN)

#dp = Dispatcher()
router = Router()

experience_id = ["noExperience", "between1And3", "between3And6", "moreThan6"]
employment_id = ["full", "part", "project", "volunteer", "probation"]
schedule_id = ["fullDay", "shift", "flexible", "remote", "flyInFlyOut"]

class Form(StatesGroup):
    wrote_text = State()
    choosing_experience = State()
    choosing_typemploy = State()
    choosing_schedule = State()

@router.message(Command("Find"))
async def cm_start(message: Message, state: FSMContext):
    await message.answer(text = "Введите название вакансии")
    await state.set_state(Form.wrote_text)

@router.message(Form.wrote_text)
async def text_chosen(message: Message, state: FSMContext):
    await state.update_data(vacancy_name = message.text)
    await message.answer(
        text = "Теперь выберите id опыт работы",
        reply_markup= make_row_keyboard(experience_id)
    )
    await state.set_state(Form.choosing_experience)

@router.message(Form.choosing_experience, F.text.in_(experience_id))
async def experience_chosen(message: Message, state: FSMContext):
    await state.update_data(vacancy_experience = message.text)
    await message.answer(
        text = "Выберите  id занятости:",
        reply_markup= make_row_keyboard(employment_id)
    )
    await state.set_state(Form.choosing_typemploy)

@router.message(StateFilter("Form:choosing_experience"))
async def experience_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого id опыта работы.\n\n"
             "Пожалуйста, выберите один из id из списка ниже:",
        reply_markup=make_row_keyboard(experience_id)
    )

@router.message(Form.choosing_typemploy, F.text.in_(employment_id))
async def employment_chosen(message: Message, state: FSMContext):
    await state.update_data(vacancy_employment = message.text)
    await message.answer(
        text = "Выберите id занятости:",
        reply_markup= make_row_keyboard(schedule_id)
    )
    await state.set_state(Form.choosing_schedule)

@router.message(StateFilter("Form:choosing_typemploy"))
async def employment_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого id занятости.\n\n"
             "Пожалуйста, выберите один id из списка ниже:",
        reply_markup=make_row_keyboard(employment_id)
    )

@router.message(Form.choosing_schedule, F.text.in_(schedule_id))
async def schedule_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text = f"schedule - {message.text}, {user_data['vacancy_name']}, {user_data['vacancy_experience']}, {user_data['vacancy_employment']} ",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()

@router.message(StateFilter("Form:choosing_schedule"))
async def shedule_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого id графика работы.\n\n"
             "Пожалуйста, выберите один id из списка ниже:",
        reply_markup=make_row_keyboard(schedule_id)
    )
'''
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Привет!")
'''