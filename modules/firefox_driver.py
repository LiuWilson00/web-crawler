from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Proxy


class FirefoxDriver:
    def __init__(self, ):
        self.driver = None
        self.proxy = None
        self.proxy_settings = None
        self.firefox_options = Options()

    def set_proxy(self, proxy):
        self.proxy = proxy

    def start(self):

        self.firefox_options.headless = True

        # Create a Proxy object using the BrowserMob proxy server
        if self.proxy:
            self.proxy_settings = Proxy({
                "httpProxy": self.proxy.proxy,
                "sslProxy": self.proxy.proxy
            })
            self.firefox_options.proxy = self.proxy_settings

        # Create a new instance of the Firefox driver
        self.driver = webdriver.Firefox(options=self.firefox_options)
