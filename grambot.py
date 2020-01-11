import sys
import gspread
from pprint import pprint
from selenium import webdriver
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep


class GSheet:
    def __init__(self, creds, sheet):
        self.scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(creds, self.scope)
        client = gspread.authorize(creds)
        self.sheet = client.open(sheet).sheet1


class GramBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(text(), 'Log in')]")\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(2)

    def get_unfollowed(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click()
        following = self._get_names()
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        followers = self._get_names()
        not_following_back = [user for user in following if user not in followers]
        pprint(not_following_back)

    def _get_names(self):
        sleep(2)
        #sugs = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
        #self.driver.execute_script('arguments[0].scrollIntoView()', sugs)
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")

        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button") \
            .click()
        return names

    def get_follower_count(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()
        sleep(2)
        follower_count = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
        return follower_count.text

    def follow_suggested(self):
        self.driver.get("https://www.instagram.com/explore/people/suggested/")
        sleep(2)
        listbox = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[2]/div/div")
        buttons = listbox.find_elements_by_tag_name("button")

        for button in buttons:
            button.click()
            sleep(10)

    def close_browser(self):
        self.driver.quit()


if __name__ == '__main__':

    mysheet = GSheet("private.json", "Geekahol Followers")

    if len(sys.argv) > 1:

        username = sys.argv[1]
        password = sys.argv[2]


        bot = GramBot(username, password)

        #bot.get_unfollowed()

        print(bot.get_follower_count())
        bot.follow_suggested()

        bot.close_browser()

    else:

        print("Specify username and password")
