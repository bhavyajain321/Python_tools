import requests
from bs4 import BeautifulSoup #BeautifulSoup is used to parse any data(element) from html page
import urlparse

def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "http://192.168.0.123/mutillidae/index.php?page=dns-lookup.php"
response = request(target_url)

parsed_html = BeautifulSoup(response.content, "html.parser")
forms_list = parsed_html.findAll("form")

for form in forms_list:
    action = form.get("action")
    post_url = urlparse.urljoin(target_url, action)
    # print(post_url)
    method = form.get("method")
    # print(method)

    input_lists = form.findAll("input")
    post_data= {}
    for input in input_lists:
        input_name = input.get("name")
        # print(input_name)
        input_type = input.get("type")
        input_value = input.get("value")
        if input_type == "text":
            input_value = "test"
        post_data[input_name] = input_value
    result = requests.post(post_url, data=post_data)
    print(result.content)