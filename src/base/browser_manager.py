import os
import platform
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager                            
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Browser:

    CHROME = 1
    __DRIVER_MAP = {}
    
    @staticmethod
    def create_new_driver(driver_id):

        thread_object = threading.currentThread()
        print(os.getcwd())
        
        def get_driver():
            # PROXY = 'http://127.0.0.1:24000'

            # from selenium.webdriver.common.proxy import *
            # myProxy = "86.111.144.194:3128"
            # proxy = Proxy({
            #     'proxyType': ProxyType.MANUAL,
            #     'httpProxy': myProxy,
            #     'ftpProxy': myProxy,
            #     'sslProxy': myProxy,
            #     'noProxy': ''})
            
            if Browser.CHROME == driver_id:
                options = Options()
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                options.add_argument("--mute-audio")
                #options.add_argument('log-level=1')
                options.add_argument('--start-maximized')
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--auto-open-devtools-for-tabs")
                # options.add_argument('--proxy-server='+PROXY)
                #options.add_argument("--no-sandbox")
                caps = DesiredCapabilities.CHROME
                caps['goog:loggingPrefs'] = {'browser': 'SEVERE'}
                
                
                
                # options.add_argument("--mute-audio")
                # options.add_argument('--lang=en-US')
                # options.add_argument('--enable-logging')
                work_folder = os.getcwd() 
                #.split("automation_tests_web")[0]
                #driver = webdriver.Chrome("/Users/Karyna/Documents/automation_tests_web/chromedriver")
                if platform.system() == "Darwin":
                    driver = webdriver.Chrome(desired_capabilities=caps, executable_path=ChromeDriverManager().install())
                    # driver = webdriver.Chrome(desired_capabilities=caps,
                    #                           executable_path=work_folder + "/src/chromedriver") #, options=options)
                                              #, options=options, desired_capabilities=d)
                if platform.system() == "Linux":
                    driver = webdriver.Chrome(desired_capabilities=caps,
                                              executable_path=work_folder + "/src/chromedriver_linux", options=options)
            
            else:
                raise Exception("There is no support for driver_id:" + str(driver_id))
            return driver

        Browser.__map(thread_object, get_driver())
        return Browser.get_driver()

    @staticmethod
    def get_console_errors():
        logs = Browser.get_driver().get_log("browser")
        return logs
    
    @staticmethod
    def get_server_errors():
        logs = Browser.get_driver().get_log("server")
        return logs
    
    @staticmethod
    def get_driver():
        # print "Getting  driver for thread: {}".format(threading.currentThread())
        return Browser.__DRIVER_MAP[threading.current_thread()]["driver"]

    @staticmethod
    def shutdown():

        Browser.get_driver().quit()

    @staticmethod
    def __map(thread, driver):

        Browser.__DRIVER_MAP[thread] = {"driver": driver}

    @staticmethod
    def get_driver_map():
        return Browser.__DRIVER_MAP

    @staticmethod
    def back():

        Browser.get_driver().back()

    @staticmethod
    def forward():

        Browser.get_driver().forward()
        
    @staticmethod
    def refresh():
        
        Browser.get_driver().refresh()
            

    @staticmethod
    def open_new_tab():
        Browser.get_driver().execute_script("window.open('');")
        #Browser.get_driver().find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')

    
    @staticmethod
    def switch_to_window(window):
        Browser.get_driver().switch_to.window(window)

    @staticmethod
    def switch_to_latest_active_window():
        windows = Browser.get_driver().window_handles
        if len(windows) == 1:
            Browser.get_driver().switch_to.window(windows[0])
            return
        for index in range(1, len(windows)):
            Browser.get_driver().switch_to.window(windows[-index])
            return
 
    @staticmethod
    def close_current_active_window():
        windows = Browser.get_driver().window_handles
        if len(windows) == 1:
            return
        for index in range(1, len(windows)):
            Browser.get_driver().close()
            Browser.switch_to_latest_active_window()
            return

    @staticmethod
    def hash_it(path):
        with open(path, 'rb') as f:
            hasher = hashlib.md5()
            hasher.update(f.read())
            return hasher.hexdigest()    
    
    
    @staticmethod
    def check_errors_console_log(self):
        current_console_log_errors = []
        log_errors = []
        new_errors = []
        log = self.get_browser_console_log()
        print("Console Log: ", log)
        for entry in log:
            if entry['level'] =='SEVERE':
                log_errors.append(entry['message'])

            if current_console_log_errors != log_errors:
                new_errors = list(set(log_errors) - set(current_console_log_errors))
                current_console_log_errors = log_errors

            if len(new_errors) > 0:
                print("\nBrowser console error on url: %s\nConsole error(s):%s"%(self.driver.current_url,'\n----'.join(new_errors)))
                
    @staticmethod        
    def get_browser_console_log():
        try:
            time.sleep(10)
            log = Browser.get_driver().get_log('browser')
            return log
        except Exception as e:
            print("Exception when reading Browser Console log")
            print(str(e))
            
            
if "__main__" == __name__:

    urls = ["https://www.hackerrank.com/dashboard",
            "https://www.hackerrank.com/contests",
            "https://www.hackerrank.com/jobs/search",
            "https://www.hackerrank.com/leaderboard"]

    threads = []

    def get_url(_url):
        Browser.create_new_driver(Browser.CHROME)
        Browser.get_driver().get(_url)
        print("URL:"+str(Browser.get_driver().current_url))  
        for each in Browser.get_driver().get_log("browser"):
            print(each)  
        Browser.shutdown()

    for url in urls:
        thread = threading.Thread(target=get_url, args=(url,))
        thread.name = "[Thread: {}]".format(urls.index(url))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
