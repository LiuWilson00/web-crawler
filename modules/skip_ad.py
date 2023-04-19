from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from utils.yotube_dom_helper import save_html
AD_MODULE_SELECTOR = ".ytp-ad-module"
SKIP_AD_BUTTON_SELECTOR = ".ytp-ad-skip-button-container .ytp-ad-skip-button"

# ytp-ad-preview-container ytp-ad-preview-container-larger-bottom 
# ytp-ad-text ytp-ad-preview-text
class AdSkipper:

    @staticmethod
    def wait_and_skip_ads(driver: WebDriver, timeout=60):
        """
        Wait for ads and skip them when the skip ad button appears.
        :param driver: WebDriver instance
        :param timeout: Maximum time to wait for the skip ad button (in seconds)
        """
        print("等待廣告出現")
        save_html(driver)
        # 等待出現廣告
        ad_exists = AdSkipper._wait_for_element(
            driver, By.CSS_SELECTOR, AD_MODULE_SELECTOR, timeout)

        if not ad_exists:
            return

        # 等待出現跳過廣告
        skip_ad_button_exists = AdSkipper._wait_for_element(
            driver, By.CSS_SELECTOR, SKIP_AD_BUTTON_SELECTOR, timeout)

        if skip_ad_button_exists:
            # 點擊跳過廣告按鈕
            skip_ad_button = driver.find_element_by_css_selector(
                SKIP_AD_BUTTON_SELECTOR)
            skip_ad_button.click()
            print("已跳過廣告")

    @staticmethod
    def _wait_for_element(driver: WebDriver, by, value, timeout):
        """
        Wait for an element to be visible on the page.
        :param driver: WebDriver instance
        :param by: Selenium By object
        :param value: Selector value
        :param timeout: Maximum time to wait (in seconds)
        :return: True if the element is found, False otherwise
        """
        try:
            WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except Exception:
            return False

    @staticmethod
    def check_ad_existence(driver: WebDriver):
        """
        Check if there is an ad in the browser.
        :param driver: WebDriver instance
        :return: True if an ad is found, False otherwise
        """
        ad_module_elements = driver.find_elements_by_css_selector(
            AD_MODULE_SELECTOR)

        if not ad_module_elements:
            return False

        ad_module_element = ad_module_elements[0]
        return len(ad_module_element.find_elements_by_xpath("./*")) > 0
