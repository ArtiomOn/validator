import random
import string

import requests


class TempMail:
    def __init__(self):
        self.url = 'https://www.1secmail.com/api/v1/'

    def get_all_domains(self):
        suffix = '?action=getDomainList'
        response = requests.get(self.url + suffix)
        if response.ok:
            return {"email_domain": response.json()}

    @staticmethod
    def generate_random_user_name():
        name = string.ascii_lowercase + string.digits
        username = ''.join(random.choice(name) for _ in range(10))
        return username

    def check_mailbox(self, username, domain):
        notification_objects = {}
        suffix = f"?action=getMessages&login={username}&domain={domain}"
        request = requests.get(self.url + suffix)
        if not request.ok:
            return request.json()
        req_length = len(request.json())
        if not req_length:
            return notification_objects
        email_ids = [request.json()[i]['id'] for i in range(req_length)]
        notification_objects[f"{username}@{domain}"] = []
        for email_id in email_ids:
            suffix = f"?action=readMessage&login={username}&domain={domain}&id={email_id}"
            request = requests.get(self.url + suffix)
            if not request.ok:
                return request.json()
            notification_object = {
                "id": request.json()['id'],
                "from": request.json()['from'],
                "subject": request.json()['subject'],
                "body": request.json()['textBody'],
                "date": request.json()['date'],
            }
            notification_objects[f"{username}@{domain}"].append(notification_object)
        return notification_objects
