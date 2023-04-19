from browsermobproxy import Server

# Path to browsermob-proxy-2.1.4/bin
BROWSERMOB_PROXY_PATH = "/usr/local/bin/browsermob-proxy-2.1.4/bin/browsermob-proxy"


class BrowserProxy:
    def __init__(self):
        self.server = None
        self.proxy = None

    def start(self):
        self.server = Server(BROWSERMOB_PROXY_PATH)
        self.server.start()
        self.proxy = self.server.create_proxy()
        self.new_har({
            'captureContent': True,
            'captureHeaders': True
        })

    def new_har(self, options):
        self. proxy.new_har(options=options)

    def get_entries(self):
        try:
            return self.proxy.har['log']['entries']
        except Exception as e:
            print(f"Error retrieving entries from proxy: {e}")
        return []

    @property
    def har(self):
        return {}
