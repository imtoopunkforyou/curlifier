from curlifier import __version__ as vers


def test_const():
    assert vers.NAME == 'curlifier'
    assert isinstance(vers.VERSION, str)
    assert vers.AUTHOR == 'Timur Valiev'
    assert vers.AUTHOR_EMAIL == 'cptchunk@yandex.ru'
    assert vers.LICENSE == 'MIT'


def test_get_package_information():
    pkg_info = vers.get_package_information()

    assert pkg_info == {
        'name': vers.NAME,
        'version': vers.VERSION,
        'author': vers.AUTHOR,
        'author_email': vers.AUTHOR_EMAIL,
        'license': vers.LICENSE,
    }
