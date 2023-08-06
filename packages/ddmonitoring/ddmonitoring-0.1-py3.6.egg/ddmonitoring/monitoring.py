import requests

from datetime import datetime
import numpy as np

from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

class MonitoringBot:
    def __init__(self, url, check_intervals, logger):
        self.logger = logger
        self.check_intervals = []
        self.url = url
        self.metrics = {}
        self.res_data = np.array([])
        self.MAX_SECONDS = 30
        self.ALERT_INTERVAL = 60
        self.alerts = []
        
    def get_call(self):
        url = self.url
        req_time = datetime.now()
        if not url.startswith("https://www.") and not url.startswith("http://www."):
            url = "http://" + url
        # print("requesting", url)
        res = requests.get(url)
        resp_time = res.elapsed.total_seconds()
        return res, req_time

    def update_res_data(self):
        res, call_time = self.get_call()
        MAX_SECONDS = self.MAX_SECONDS

        self.res_data = np.append(self.res_data, [{
            "call_time": call_time,
            "resp_time": round(res.elapsed.total_seconds()*1000, 2), #in ms
            "status": res.status_code
        }])

        now = datetime.now()
        call_time = self.res_data[0]["call_time"]

        """ only check oldest element of dict. 
        Ensures a constant maximum number of response data in memory. """

        if (now - call_time).total_seconds()//MAX_SECONDS >= 1:
            self.res_data = self.res_data[1:]

    def make_metrics(self, interval_s):

        now = datetime.now()

        self._init_metric_interval(interval_s)

        data_considered = [data for data in self.res_data if (now - data["call_time"]).total_seconds() <= interval_s]  # could be optimized

        metrics = self.metrics[interval_s]
        n_calls = len(data_considered)
        max_time = metrics["max_resp_time"]
        min_time = metrics["min_resp_time"]
        total_res_time = 0
        metrics["200_count"] = 0

        for data in data_considered:
            resp_time = data["resp_time"]
            total_res_time += resp_time  #TODO: avoid integer overflow
            code_count_string = "{}_count".format(data["status"])
            if code_count_string in metrics:
                metrics[code_count_string] += 1
            else:
                metrics[code_count_string] = 1
            max_time = max(max_time, resp_time)
            min_time = min(min_time, resp_time)

        metrics["avg_resp_time"] = round(total_res_time/n_calls, 2)
        metrics["max_resp_time"] = max_time
        metrics["min_resp_time"] = min_time
        metrics["total_requests"] = n_calls

        if interval_s == self.ALERT_INTERVAL:
            self.handle_alerts()

        metrics["availability"] = round((metrics["200_count"]/n_calls)*100, 2)

    def handle_alerts(self):  #TODO: test
        metrics = self.metrics[self.ALERT_INTERVAL]
        if metrics["prev_availability"] == -1 and metrics["availability"] == -1:
            return
        elif metrics["prev_availability"] == -1:
            metrics["prev_availability"] = metrics["availability"]
            return
        elif metrics["prev_availability"] > 80 and metrics["availability"] < 80:
            self.alerts.append(self.make_alert("DOWN"))
        elif metrics["prev_availability"] < 80 and metrics["availability"] > 80:
            self.alerts.append(self.make_alert("UP"))

    def make_alert(self, status):
        return "{} is {} @ {}".format(self.url, status, datetime.now().isoformat())

    def _init_metric_interval(self, interval_s):
        self.metrics[interval_s] = {
            "avg_resp_time": 0,
            "max_resp_time": 0,
            "min_resp_time": float('inf'),
            "availability": -1,
            "200_count": 0,
            "total_requests": 0
        }

        if interval_s == self.ALERT_INTERVAL:
            self.metrics[interval_s]["prev_availability"] = -1

    def show_metrics(self, interval_s):
        self.logger.info(self.metrics[interval_s])
        if self.alerts:
            self.logger.info(self.alerts)
        else:
            self.logger.info("no alerts to show")