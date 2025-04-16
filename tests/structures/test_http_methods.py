from curlifier.structures.http_methods import HttpMethodsEnum


def test_http_methods_enum():
    all_methods = HttpMethodsEnum.get_methods_without_body() + HttpMethodsEnum.get_methods_with_body()
    assert len(all_methods) == len(tuple(method for method in HttpMethodsEnum))
