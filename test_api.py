import requests
import yaml
import logging

with open('/testdata.yaml', encoding='utf-8') as f:
    testdata = yaml.safe_load(f)

S = requests.Session()


def test_step1(user_login, post_title):
    try:
        logging.info("Test test_step1 Starting")
        result = S.get(url=testdata['address'], headers={'X-Auth-Token': user_login}, params={'owner': 'notMe'}).json()['data']
        result_title = [i['title'] for i in result]
        assert post_title in result_title, 'test_step1 FAIL'
    except Exception as e:
        logging.error(f"test_step1 failed with error: {str(e)}")
        raise e


# Новый тест для создания и проверки нового поста
def test_create_and_check_new_post(user_login, new_post_data):
    try:
        logging.info("Test test_create_and_check_new_post Starting")
        # Создаем новый пост
        response = S.post(
            url=testdata['address'],
            headers={'X-Auth-Token': user_login},
            data=new_post_data
        )
        assert response.status_code == 200, 'Failed to create a new post'

        # Получаем описание нового поста
        new_post_description = new_post_data['description']

        # Проверяем, есть ли созданный пост на сервере по полю "описание"
        result = S.get(url=testdata['address'], headers={'X-Auth-Token': user_login}).json()['data']
        result_descriptions = [i['description'] for i in result]
        assert new_post_description in result_descriptions, 'New post not found'
    except Exception as e:
        logging.error(f"test_create_and_check_new_post failed with error: {str(e)}")
        raise e
