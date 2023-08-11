import requests
from datetime import datetime
import json


class VK:
    API_BASE_URL = 'https://api.vk.com/method'
    url_path_yandex = 'https://cloud-api.yandex.net'

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_profile_photos(self, x=5):
        params = {
            'access_token': self.token,
            'count': x,
            'v': '5.131'
        }
        params.update({'owner_id': self.id, 'album_id': 'wall', 'extended': 1})
        response = requests.get(f'{self.API_BASE_URL}/photos.get', params=params)
        return response.json()

    def create_a_folder(self, yandex_token, name_dir):
        headers = {"Authorization": f'OAuth {yandex_token}'}
        params = {'path': name_dir}
        response = requests.put(f'{self.url_path_yandex}/v1/disk/resources', params=params, headers=headers)
        if 199 < response.status_code < 300:
            print("Папка создана")
        else:
            print("Произошла ошибка!")

    def copy_of_image(self, yandex_token, name_dir):
        result_list = []
        list_photo_name = []
        count_ = 0
        headers = {"Authorization": f'OAuth {yandex_token}'}
        for i in photos_json['response']['items']:
            if f'{i["likes"]["count"]}.jpg' in list_photo_name:
                date = i["date"]
                dateTime = datetime.fromtimestamp(date)
                path_name_ph = f'{i["likes"]["count"]} {dateTime.strftime("%d %b %Y")}.jpg'
            else:
                path_name_ph = f'{i["likes"]["count"]}.jpg'
            params = {
                'path': f'{name_dir}/{path_name_ph}',
                'url': f'{i["sizes"][-1]["url"]}'
            }
            response = requests.post(f'{self.url_path_yandex}/v1/disk/resources/upload/', params=params, headers=headers)
            if 199 < response.status_code < 300:
                count_ += 1
                print(f'{count_} из {count_photo} изображений загружено')
                list_photo_name.append(f'{i["likes"]["count"]}.jpg')
                result_list.append({"file_name": path_name_ph, "size": i["sizes"][-1]["type"]})
                if count_ == count_photo_var:
                    break
            else:
                print("Произошла ошибка!")
        print("Загрузка завершена!")
        return result_list

    def get_json_file(self, name_json, result_list):
        with open(f'{name_json}.json', "w") as file:
            json.dump(result_list, file, indent=2)
        print("json-файл сформирован")


access_token = ""
user_id = input("Введите ID в вконтакте:")
vk = VK(access_token, user_id)
photos_json = vk.get_profile_photos(1000)

count_photo = photos_json['response']['count']

yandex_token = input("Введите токен Яндекс Диска: ")
name_dir = input("Введите название папки: ")
vk.create_a_folder(yandex_token, name_dir)

print(f"Вы можете сохранить {count_photo} изображение(ий)")
count_photo_var = int(input("Введите желаемое количество сохраняемых фотографий: "))
result_list = vk.copy_of_image(yandex_token, name_dir)

name_json = input("Введите название json-файла: ")
vk.get_json_file(name_json, result_list)
