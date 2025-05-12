import threading

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

import utils as ut

class AzSentimentAnalysis:
    _instance = None
    _lock = threading.Lock()
    _key = None
    _endpoint = None

    def __new__(cls):
        # it is necessary to check if _instance is None to guarantee a thread-safe behavior
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AzSentimentAnalysis, cls).__new__(cls)
                    res = ut.load_key('key.api')
                    cls._endpoint, cls._key = res[0][0], res[0][1]
                    print(cls._endpoint, cls._key)
                    cls._instance._init_conn()
        return cls._instance

    def _init_conn(self):
        credential = AzureKeyCredential(self._key)
        self.conn = TextAnalyticsClient(endpoint=self._endpoint, credential=credential)

    def get_conn(self):
        return self.conn
    