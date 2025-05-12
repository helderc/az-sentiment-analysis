import threading

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

import streamlit as st

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
                    # the try-except is just to accomodate local/remote doployment
                    try:
                        # try to load the local key/endpoint
                        # just one pair endpoint-key, so [0]
                        res = ut.load_key('key.api')[0]
                        endpoint, key = res[0], res[1]
                    except:
                        # if it fails it means we are running on streamlit servers
                        st.secrets["endpoint"]
                        st.secrets["key"]
                    cls._endpoint, cls._key = endpoint, key
                    print(cls._endpoint, cls._key)
                    cls._instance._init_conn()
        return cls._instance

    def _init_conn(self):
        credential = AzureKeyCredential(self._key)
        self.conn = TextAnalyticsClient(endpoint=self._endpoint, credential=credential)

    def get_conn(self):
        return self.conn
    