import vk_api
from get_token import token2, token
from pprint import pprint
from vk_api import VkTools
import requests
import time


vk_session = vk_api.VkApi(token=token2)
api = vk_session.get_api()


def get_photo(user_id, info, final_dict):
    photo = {}
    url = 'https://api.vk.com/method/photos.get'
    params = {'owner_id': user_id, 'album_id': 'profile', 'photo_sizes': 1, 'access_token': token2, 'v': '5.131',
              'extended': 1}
    response = requests.get(url=url, params=params)
    if response.status_code == 200:
        result = response.json()
        for all_info in result['response']['items']:
            likes = all_info['likes']['count']
            comments = all_info['comments']['count']
            url = all_info['sizes'][-1]['url']
            x = {int(likes) + int(comments): {'name': info['name'], 'user_link': info['user_link'], 'user_id': user_id,
                                              'url': url}}
            photo.update(x)
        try:
            count = 0
            max_count = 3
            while count < max_count:
                max_val = max(photo.keys())
                result = {k: v for k, v in photo.items() if k == max_val}
                final_dict.update(result)
                count += 1
                photo.pop(max_val)
        except ValueError:
            pass
    # pprint(final_dict)
    return final_dict


def search_id(search_params):
    rs = VkTools(api).get_all(method='users.search', max_count=1000, values=search_params)
    ids_dict = {}
    for ids in rs['items']:
        if ids['is_closed'] is False:
            info = {ids['id']: {'name': ids['first_name'], 'user_link': f'vk.com/id{ids["id"]}'}}
            ids_dict.update(info)
        else:
            continue
    return ids_dict


def info_filter(final_count, search_params, history_user_id):
    count = 0
    final_dict = {}
    si = search_id(search_params)
    for user_id, info in si.items():
        if count < final_count and user_id not in history_user_id:
            get_photo(user_id, info, final_dict)
            count += 1
            history_user_id.append(user_id)
            time.sleep(0.5)
        else:
            continue
    return [final_dict, history_user_id]