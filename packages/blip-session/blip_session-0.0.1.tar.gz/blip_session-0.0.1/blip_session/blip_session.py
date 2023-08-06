from requests import Session
from time import sleep
from uuid import uuid4

IRIS_URL_BASE = 'https://msging.net'
COMMANDS_URL = '/commands'
MESSAGES_URL = '/messages'
ID_KEY = 'id'


class BlipSession:

    def __init__(self, authorization):
        self.session = Session()
        self.session.headers = {
            'Authorization': authorization
        }

    def process_command(self, command):
        if ID_KEY not in command:
            command[ID_KEY] = str(uuid4())
        try:
            command_res = self.session.post(
                f'{IRIS_URL_BASE}{COMMANDS_URL}',
                json=command
            )

            command_res = command_res.json()
            return command_res
        except:
            return None

    def send_command(self, command):
        self.process_command(command)

    def force_command(self, command, attempts=5, cooldown_time=1.0):
        attempt = 0
        command_res = None
        while attempt < attempts and command_res is None:
            command_res = self.process_command(command)
            if command_res is None:
                attempt += 1
                sleep(cooldown_time)
        return command_res

    def send_message(self, message):
        session = self.session
        if ID_KEY not in message:
            message[ID_KEY] = str(uuid4())
        session.post(
            f'{IRIS_URL_BASE}{MESSAGES_URL}',
            json=message
        )
