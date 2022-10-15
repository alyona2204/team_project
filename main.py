import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from pprint import pprint


with open('token_for_search.txt') as file_object:
    token_for_search = file_object.read().strip()
with open('token_for_bot.txt') as file_object:
    token_for_bot = file_object.read().strip()
version = '5.126'

class VkUser_Search:
    url = 'https://api.vk.com/method/'
    version = '5.126'
    def __init__(self):
        self.token = token_for_search
        self.params = {
            'access_token': self.token,
            'v': version
        }

    def favorites(self):
        url = 'https://api.vk.com/method/'
        vk = vk_api.VkApi(token=token_for_bot)
        longpoll = VkLongPoll(vk)
        # Основной цикл
        for event in longpoll.listen():
            # Если пришло новое сообщение
            if event.type == VkEventType.MESSAGE_NEW:
                # Если оно имеет метку для меня(то есть бота)
                if event.to_me:
                    # Сообщение от пользователя
                    request = event.text.lower()
                    id = event.user_id
                    if request == "hi":
                        self.params = {
                            'user_ids': id,
                            'owner_id': id,
                            'access_token': self.token,
                            'v': version,
                            'album_id': 'profile',
                            'extended': 1,
                            'fields': 'bdate, city, sex'
                        }

                        profile = requests.get(self.url + 'users.get', self.params).json()['response'][0]
                        profile_city = profile['city']['id']
                        profile_first_name = profile['first_name']
                        profile_last_name = profile['last_name']
                        profile_bdate = profile['bdate']
                        profile_sex = profile['sex']
                        profile_year = profile_bdate[-4:]
                        print(profile_first_name, profile_last_name, profile_bdate, profile_sex)
                        if profile_sex == 1:
                            favorites_sex = 2
                        else:
                            favorites_sex = 1
                        params_favorites = {
                            'user_ids': id,
                            'sort': 0,
                            'count': 2,
                            'city': profile_city,
                            'status': 6,
                            'sex': favorites_sex,
                            'birth_year': profile_year,
                            'fields': 'bdate, city',
                            'has_photo': 1,
                            'owner_id': id,
                            'access_token': self.token,
                            'v': version,
                            'album_id': 'profile',
                            'extended': 1
                        }

                        favorites_people = requests.get(url + 'users.search', params_favorites).json()['response']['items']
                        for el in favorites_people:
                            id_favorites = el['id']
                            name = el['first_name'] + ' ' + el['last_name']
                            url_favorites = f'https://vk.com/id{id_favorites}'
                            print(name, url_favorites)


vk_client = VkUser_Search()
vk_client.favorites()