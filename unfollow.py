import sys
from selenium import webdriver
from time import sleep
from pprint import pprint


white_list = [
 'theminiaturesvault',
 'siegestudios',
 'miniwargaming',
 'warhammerofficial',
 'immersive_world_crafter',
 'toadtimemachine',
 'gatwickgames',
 'nonzerosumgames',
 'tarsasnavigator.hu',
 'nemonovaart',
 'the_pickled_dragon',
 'chadwickboseman',
 'therock',
 'clarkgregg',
 'kevinhart4real',
 'looperhq',
 'vancityreynolds',
 'igndotcom',
 'thatkevinsmith',
 'rottentomatoes',
 'comicbook',
 'mcu_direct',
 'tessamaethompson',
 'prattprattpratt',
 'hamillhimself',
 'evangelinelillyofficial',
 'starwars',
 'chrishemsworth',
 'dccomics',
 'jonfavreau',
 'samuelljackson',
 'thehughjackman',
 'karengillan',
 'therealstanlee',
 'robertdowneyjr',
 'tomholland2013',
 'markruffalo',
 'renner4real',
 'marvel',
 'therussobrothers',
 'marvelstudios',
 'iamfires',
 'darrenlatham',
]


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
        to_unfollow = [user for user in not_following_back if user not in white_list]
        return to_unfollow

    def _get_names(self):
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

    def unfollow_users(self, list_of_users):
        for user in list_of_users:
            print("\n\n" + user)
            self.driver.get("https://www.instagram.com/" + user)
            sleep(2)

            is_verified = self.driver.find_elements_by_class_name("coreSpriteVerifiedBadge")
            pprint(is_verified)

            if is_verified:
                print(user + " has checkmark!!")
            else:
                self.driver.find_element_by_xpath('//button[text()="Following"]') \
                    .click()
                self.driver.find_element_by_xpath('//button[text()="Unfollow"]') \
                    .click()
                print(" *Unfollowed* ")
                sleep(20)

    def close_browser(self):
        self.driver.quit()


if __name__ == '__main__':

    if len(sys.argv) > 1:

        username = sys.argv[1]
        password = sys.argv[2]

        # log in
        bot = GramBot(username, password)

        # find unfollowers
        to_unfollow = bot.get_unfollowed()

        # unfollow those not on white list
        bot.unfollow_users(to_unfollow)

        # close selenium
        bot.close_browser()

    else:

        print("Specify username and password")
