
import requests


base_url = "http://localhost:8000/api"


# test /conversation

session = requests.Session()

user_input = { "text" : "hello my bot"}

resp = session.put(base_url + "/conversation",json = user_input)

try:
    resp.raise_for_status()
except requests.HTTPError as exc:
    print("error : {}".format(exc))

print(resp)