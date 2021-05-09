import time
from selenium import webdriver


class Actor_bot:
    def __init__(self, name):
        self.name = name
        self.line_numbers = []
        self.browser = webdriver.Chrome(r'chatbot/chromedriver_2')
        self.password = "helloworld"

    def enter_chatroom(self, room):
        url = "http://127.0.0.1:5000/"
        self.browser.get(url)

        create_account = self.browser.find_element_by_id("createacc")
        create_account.click()
        time.sleep(1)

        username_field = self.browser.find_element_by_id("username")
        username_field.send_keys(self.name)

        username_field = self.browser.find_element_by_id("password")
        username_field.send_keys(self.password)

        create_account = self.browser.find_element_by_id("startchatbutton")
        create_account.click()
        time.sleep(1)

        back_to_login = self.browser.find_element_by_id("createacc")
        back_to_login.click()
        time.sleep(1)

        username_field = self.browser.find_element_by_id("username")
        username_field.send_keys(self.name)

        username_field = self.browser.find_element_by_id("password")
        username_field.send_keys(self.password)

        time.sleep(1)
        room_field = self.browser.find_element_by_id("room")
        room_field.send_keys(room)
        time.sleep(1)

        start_chat_button = self.browser.find_element_by_id("startchatbutton")
        start_chat_button.click()
        time.sleep(1)

    def read_line(self, line, last_line):
        enter_message_field = self.browser.find_element_by_id("text")
        enter_message_field.send_keys(line)
        send_message_button = self.browser.find_element_by_id("send")
        if last_line:
            send_message_button.click()

    def end_scene(self):
        while True:
            try:
                leave_message_button = self.browser.find_element_by_id("leave")
                leave_message_button.click()
                self.browser.close()
                break
            except:
                pass





