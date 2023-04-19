import time
from modules.browser_proxy import BrowserProxy
from modules.firefox_driver import FirefoxDriver
from modules.proxy_listener import ProxyListener
from modules.skip_ad import AdSkipper
from utils.video_url_helper import get_last_mime_url_by_entries
from utils.convert_webm_helper import convert_mp3_and_delete_temp_file, download_to_temp_folder
from utils.yotube_dom_helper import get_video_title

# Callback function


def on_entries_change(new_entry):
    # do something with the new entries
    entry = new_entry
    formatted_entry = {}
    if isinstance(entry, dict):

        formatted_entry['method'] = entry['request']['method'] if 'request' in entry and 'method' in entry['request'] else ''
        formatted_entry['url'] = entry['request']['url'][:80] + \
            '...' if 'request' in entry and 'url' in entry['request'] and len(
            entry['request']['url']) > 80 else ''
        formatted_entry['status'] = entry['response']['status'] if 'response' in entry and 'status' in entry['response'] else ''
        formatted_entry['time'] = entry['time'] if 'time' in entry else ''

    # print(formatted_entry)


# Create a new instance of the Firefox driver
firefoxDriver = FirefoxDriver()
# Start the BrowserMob Proxy server
browserProxy = BrowserProxy()
listener = ProxyListener(browserProxy, on_entries_change)


try:
    browserProxy.start()

    firefoxDriver.set_proxy(browserProxy.proxy)

    # Start the instance of the Firefox driver
    firefoxDriver.start()
    # Navigate to the URL
    firefoxDriver.driver.get(
        'https://www.youtube.com/watch?app=desktop&v=yGoHsTV6QrE')

    # Wait for the page to load
    firefoxDriver.driver.implicitly_wait(10)

    listener.start()

    # while AdSkipper.check_ad_existence(firefoxDriver.driver):
    #     print('ad exists')
    #     AdSkipper.wait_and_skip_ads(firefoxDriver.driver, 10)
    #     firefoxDriver.driver.implicitly_wait(2)
    #     time.sleep(2)

    AdSkipper.wait_and_skip_ads(firefoxDriver.driver, 60)

    new_url = get_last_mime_url_by_entries(browserProxy.get_entries(), 'audio')
    listener.stop()
    print(new_url)
    title = get_video_title(firefoxDriver.driver)
    tempPath = download_to_temp_folder(new_url)
    convert_mp3_and_delete_temp_file(tempPath, 'output/' + title + '.mp3')

finally:
    if browserProxy:
        browserProxy.proxy.close()
        browserProxy.server.stop()
    if firefoxDriver:
        firefoxDriver.driver.quit()
