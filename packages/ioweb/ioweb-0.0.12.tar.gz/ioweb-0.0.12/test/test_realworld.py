from ioweb.session import Session


def test_yandex():
    sess = Session()
    res = sess.request('https://yandex.ru/robots.txt')
    assert '# yandex.ru' in res.text
