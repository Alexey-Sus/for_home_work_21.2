# Импорт встроенной библиотеки для работы веб-сервера
import tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import os

# Для начала определим настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """Специальный класс, который отвечает за обработку входящих запросов от клиентов"""

    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """

        if self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/html_content")
            self.end_headers()
        elif self.path == "/html_content":

            remote_file_url = "https://raw.githubusercontent.com/Alexey-Sus/for_DataBase_project/develop/src/file.html"

            try:
                response = requests.get(remote_file_url)
                response.raise_for_status()

                with tempfile.NamedTemporaryFile(mode='w+t', delete=False,
                                                 encoding='utf-8') as tmp_file:
                    tmp_file.write(response.text)
                    tmp_file_path = tmp_file.name

                    try:
                        with open(tmp_file_path, 'r', encoding='utf-8') as f:

                            html_content = f.read()
                            self.send_response(200)
                            self.send_header("Content-type", "text/html")
                            self.end_headers()
                            self.wfile.write(html_content.encode("utf-8"))
                    finally:
                        os.remove(tmp_file_path)

            except requests.exceptions.RequestException as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write((f"Ошибка при получении удаленного файла: {e}".encode("utf-8")))

            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Внутренняя ошибка сервера: {e}".encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")


if __name__ == "__main__":

    # Инициализация веб-сервера, который будет по заданным параметрах в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")git