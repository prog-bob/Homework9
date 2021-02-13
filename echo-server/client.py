from http.client import HTTPConnection

if __name__ == '__main__':
    connection = HTTPConnection('localhost', 7777, timeout=10)
    connection.request("POST", 'localhost', headers={"Header1": "Hello!"})
    response = connection.getresponse()
    print(response.status)
    print(f"От сервера получен код ответа: {response.getcode()}")
    print(f"Сообщение: {response.reason}")

