import requests
from tinydb import TinyDB, Query
from operator import itemgetter
from tinydb.operations import set

#  There you can take vk token https://badcode.ru/vk-api-osnovy-poluchieniie-tokiena/#vkcom
TOKEN = 'HERE MUST BE YOUR TOKEN'
VERSION = 5.74
#  There must be your id or public id
OWNER_ID = 'PUBLIC OR YOUR ID'
db = TinyDB('./db.json')
Post = Query()


def posting_on_vk(message_text):
    """ Publishes a post on the vk wall.
    Published posts id and text save in database.
    :param message_text: here your text for the wall
    :return:
    """
    data = {
        'access_token': TOKEN,
        'from_group': 1,
        'message': message_text,
        'signed': 0,
        'v': VERSION}
    r = requests.post('https://api.vk.com/method/wall.post', data).json()
    data = r.get('response')
    data.update({'text': message_text})
    db.insert(data)


def get_last_post_id():
    """ Get last post id.

    :return: (int) last post id
    """
    last_post = db.all()[-1]
    return last_post['post_id']


def edit_post_on_vk(massage_text, post_id):
    """ Edit post.

    Updates your text with a new one.
    :param massage_text: edited text.
    :param post_id: id of the post you want to edit
    :return:
    """
    data = {
        'access_token': TOKEN,
        'from_group': 1,
        'message': massage_text,
        'signed': 0,
        'v': VERSION,
        'owner_id': OWNER_ID,
        'post_id': post_id,
    }
    r = requests.post('https://api.vk.com/method/wall.edit', data).json()
    db.update(set('text', massage_text), Post.post_id == int(post_id))


def delete_post_on_vk(post_id):
    """ Delete post by id.


    :param post_id: id of the post you want to delete.
    :return:
    """
    data = {
        'access_token': TOKEN,
        'from_group': 1,
        'signed': 0,
        'v': VERSION,
        'owner_id': OWNER_ID,
        'post_id': post_id,
    }
    r = requests.post('https://api.vk.com/method/wall.delete', data).json()


def get_all_id():
    """ Get all id

    :return: list of id
    """
    all_id = db.all()
    result = list(map(itemgetter('post_id'), all_id))
    return result


def choice():
    """ This is a CLI.

    :return:
    """
    user_choice = input('\n'
                        'Введите:\n'
                        ' 1 - чтобы опубликовать пост\n'
                        ' 2 - чтобы редактировать пост(требуется id)\n'
                        ' 3 - чтобы получить список id постов\n'
                        ' 4 - чтобы удалить пост(требуется id)\n'
                        '--> '
                        )
    if user_choice.isnumeric() and int(user_choice) == 1:
        user_text = input('Введите текст: ')
        posting_on_vk(user_text)
        print('Пост успешно опубликован!')
    else:
        if user_choice.isnumeric() and int(user_choice) == 2:
            post_id = input('Чтобы редактировать введите id поста:'
                            '\n'
                            '--> ')
            edition_text = input('Напишите пост в исправленном виде: ')
            edit_post_on_vk(edition_text, post_id)
            print('Пост успешно отредактирован!')
        else:
            if user_choice.isnumeric() and int(user_choice) == 3:
                a = get_all_id()
                print(a)
            else:
                if user_choice.isnumeric() and int(user_choice) == 4:
                    post_id_for_delete = input('Введите id поста: '
                                     '\n'
                                     '--> ')
                    delete_post_on_vk(post_id_for_delete)
                    print('Пост успешно удален!')
                else:
                    print('Введите числовое значение')
    choice()


if __name__ == '__main__':
    choice()


