from random import randrange

import vk_api
from vk_api import VkTools
from vk_api.longpoll import VkLongPoll, VkEventType

import DataBase
from settings import token, token2
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from help_menu import Help_menu
from search_users import info_filter


vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
keyboard = VkKeyboard()
session = vk_api.VkApi(token=token2)
api = session.get_api()
history_user_id = []
search_params = {}
SEX = {
    'Female': 1,
    'Male': 2,
    'Not specified': 0
}


def write_msg(user_id, message, keyboard=None):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message,
                                        'keyboard': keyboard.get_keyboard(), 'random_id': randrange(10 ** 7)})


class SearchInfo:
    def get_city(self) -> str:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                request = event.text.capitalize()
                if request:
                    city = request
                    city_id = VkTools(api).get_all(method='database.getCities', values={'country_id': 1, 'q': city},
                                                   max_count=1)
                    for ids in city_id['items']:
                        if ids['title'] == city:
                            get_id = ids['id']
                            info = {'city': get_id}
                            search_params.update(info)
                    return city

    def get_sex(self) -> int:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                request = event.text.capitalize()
                if request in SEX.keys():
                    sex = SEX.get(request)
                    info = {'sex': sex}
                    search_params.update(info)
                    return sex

    def get_age_from(self) -> int:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                request = event.text
                if request:
                    age_from = request
                    info = {'age_from': int(age_from)}
                    search_params.update(info)
                    return age_from

    def get_age_to(self) -> int:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                request = event.text
                if request:
                    age_to = request
                    info = {'age_to': int(age_to)}
                    search_params.update(info)
                    return age_to

    def get_count(self) -> int:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                request = event.text
                final_count = int(request)
                return final_count


sp = SearchInfo()
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text.capitalize()

            if request == 'Hello' or request == 'Hi':
                keyboard.add_button('Help menu', color=VkKeyboardColor.SECONDARY)
                keyboard.add_button('Search', color=VkKeyboardColor.SECONDARY)
                keyboard.add_button('Good bye', color=VkKeyboardColor.POSITIVE)
                write_msg(event.user_id, f'Hello, {event.user_id}', keyboard)
                DataBase.create_db()
            elif request == 'Help menu':
                write_msg(event.user_id, f'{Help_menu}', keyboard)
            elif request == 'Search':
                write_msg(event.user_id, 'Enter search city: ', keyboard)
                sp.get_city()
                write_msg(event.user_id, 'Enter gender people: ', keyboard)
                sp.get_sex()
                write_msg(event.user_id, 'Enter age from for you search: ', keyboard)
                sp.get_age_from()
                write_msg(event.user_id, 'Enter age to for you search: ', keyboard)
                sp.get_age_to()
                write_msg(event.user_id, 'How many peoples you need to find? ', keyboard)
                final_count = sp.get_count()
                print(search_params)
                write_msg(event.user_id, 'Thank you my friend, the data was accepted. Start searching ...', keyboard)
                write_msg(event.user_id, 'It will take some time ...', keyboard)
                answer_for_user = info_filter(final_count, search_params, history_user_id)
                for key, values in answer_for_user[0].items():
                    name = values['name']
                    user_link = values['user_link']
                    photo_url = values['url']
                    write_msg(event.user_id, name, keyboard)
                    write_msg(event.user_id, user_link, keyboard)
                    write_msg(event.user_id, photo_url, keyboard)
                write_msg(event.user_id, 'Search is done!', keyboard)
                DataBase.add_info(answer_for_user[0])
            elif request == 'Good bye':
                write_msg(event.user_id, 'Good bye, my friend((', keyboard)
                history_user_id.clear()
                DataBase.delete_db()
                write_msg(event.user_id, 'You search history was deleted!'
                                         '\n If you want to start again, just say "hi" or "hello".'
                                         '\n GOOD LUCK!', keyboard)
            else:
                write_msg(event.user_id, 'I did not understand you...please repeat', keyboard)
