from src.pages.browser_manager import Browser


class BasePage(object):
   
    def __init__(self, expected_title, expected_url):
        self.expected_title = expected_title
        self.expected_url = expected_url
     
    def open_new_tab(self):
        Browser.open_new_tab()
        
        
           
    def switch_to(self):
        Browser.switch_to_latest_active_window()
    
    def close_window(self):
        Browser.close_current_active_window()
    
    def get_actual_url(self):
        return Browser.get_driver().current_url
    
    def get_actual_title(self):
        return Browser.get_driver().title

    def open(self):
        Browser.get_driver().get(self.expected_url)
        return self
    
    def open_url(self, url):
        Browser.get_driver().get(url)
        return url
    
    def maximize(self):
        Browser.get_driver().maximize_window()
    
    def refresh_page(self):
        Browser.get_driver().refresh()   
    
    def get_browser_console_log(self):
        return Browser.get_browser_console_log()
        
    def validate_console_log(self):
        Browser.get_browser_console_log()
        
    def close_current_tab(self):
        Browser.close_current_active_window()