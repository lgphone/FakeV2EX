import os
import random
from uuid import uuid4
from v2ex.settings import AVATAR_FILE_PATH


def gender_topic_sn():
    topic_sn = str(uuid4()).split("-")[0]
    return topic_sn


def gender_random_code():
    random_code = str(uuid4()).split("-")[0]
    return random_code


def gender_random_balance():
    min_balance = 1
    max_balance = 80
    return random.randint(min_balance, max_balance)


def save_avatar_file(file):
    # file_con = file.content_type
    random_code = gender_random_code()
    file_type = file.name.split('.')[-1]
    save_file_name = random_code + '.' + file_type
    file_path = os.path.join(AVATAR_FILE_PATH, save_file_name)
    # print(file_path)
    with open(file_path, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    return '/static/img/' + save_file_name
