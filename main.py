import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time


#Class for the paperclip factory
class pclip_factory:
    def __init__(self):
        self.clips = 0
        self.funds = 0.0
        self.inventory = 0

    def update(self,driver):
        self.funds = driver.find_element(By.ID, "funds").text
        print(f"Funds updated to: {self.funds}")




# find the make paperclip button and press it
def click_bt(driver,bt_id):
    bt_loc = driver.find_element(By.ID, bt_id)
    ActionChains(driver).click(bt_loc).perform()

def auto_press_make_bt(driver,event):
    while not event.is_set():
        click_bt(driver,"btnMakePaperclip")

def get_demand(driver):
    demand = driver.find_element(By.ID, "demand").text
    return int(demand)

def adjust_demand(driver,event):
    while not event.is_set():
        demand = get_demand(driver)
        if demand < 100:
            click_bt(driver,"btnLowerPrice")
        if demand > 100:
            click_bt(driver, "btnRaisePrice")

def autoclip_buyer(driver,event):
    while not event.is_set():
        price_autoclip = driver.find_element(By.ID, "clipperCost").text
        amount = driver.find_element(By.ID,"funds").text
        print(f"a:{amount} p:{price_autoclip}")
        if amount > price_autoclip:
            click_bt(driver,"btnMakeClipper")
            print(f"bought autoclipper for {price_autoclip}")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    # Navigate to the game's URL
    driver.get('https://www.decisionproblem.com/paperclips/index2.html')
    time.sleep(1)
    
    #flags
    autoclipper_unlocked = False

    #def threads and events
    #events
    event = threading.Event()
    event_buy_autoclipper = threading.Event()

    #theads
    thread_click_make = threading.Thread(target=auto_press_make_bt, args=(driver, event,))
    # thread_click_make.setDaemon(True)
    thread_adjust_demand = threading.Thread(target=adjust_demand, args=(driver, event,))
    # thread_adjust_demand.setDaemon(True)
    thread_autoclipper = threading.Thread(target=autoclip_buyer, args=(driver, event_buy_autoclipper,))

    #launch all threads
    thread_click_make.start()
    thread_adjust_demand.start()
    thread_autoclipper.start()

    time.sleep(30)
    #set event to stop threads
    event.set()
    #let threads finish
    thread_click_make.join()
    thread_adjust_demand.join()
    thread_autoclipper.join()

    #close the page
    driver.close()

