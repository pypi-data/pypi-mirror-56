from datetime import datetime
import requests
from collections import defaultdict
import numpy as np
from ddmonitoring.utils.constants import DATA_INTERVAL_LONG, DATA_INTERVAL_SHORT, ALERTS_INTERVAL

class MetricsModel(object):
    def __init__(self, check_data, logger):
        self.logger = logger
        self.check_data = check_data
        self.res_data = defaultdict(lambda: np.array([]))
        self.errors = defaultdict(lambda: np.array([]))
        self.codes_so_far = []
        self.MAX_SECONDS = DATA_INTERVAL_LONG

        self.metrics = {self.with_schema(website): {DATA_INTERVAL_LONG: {}, DATA_INTERVAL_SHORT: {}, ALERTS_INTERVAL: {}} for website in self.check_data}
        self.alerts = []

    def make_global_metrics(self, data_interval):
        for website in self.check_data:
            self.make_metrics_for(website, data_interval)

    @staticmethod
    def with_schema(website):
        if not website.startswith("https://") and not website.startswith("http://"):
            website = "http://" + website
        return website

    @staticmethod
    def without_schema(website):
        return website.replace("https://", "").replace("http://", "").replace("www.", "")

    def check(self, website, timeout):
        website  = self.with_schema(website)
        res, call_time, success = self._get(website, timeout)

        if not success:
            self.errors[website] = np.append(self.errors[website], [{
                "call_time": call_time,
                "reason": res
            }])
        else:
            code = str(res.status_code)
            if code not in self.codes_so_far:
                self.codes_so_far.append(code)

            self.res_data[website] = np.append(self.res_data[website], [{
                "call_time": call_time,
                "res_time": round(res.elapsed.total_seconds()*1000, 2), #in ms
                "status": res.status_code
            }])

        now = datetime.now()

        if len(self.res_data[website]) > 0:

            first_call = self.res_data[website][0]["call_time"]

            """ only check oldest element of dict. 
            Ensures a constant maximum number of response data in memory. """

            if (now - first_call).total_seconds() > self.MAX_SECONDS:
                self.res_data[website] = self.res_data[website][1:]

        if len(self.errors[website]) > 0:
            first_error_call = self.errors[website][0]["call_time"]

            if (now - first_error_call).total_seconds() > self.MAX_SECONDS:
                self.errors[website] = self.errors[website][1:]
    
    def make_metrics_for(self, website, data_interval):
        website = self.with_schema(website)
        now = datetime.now()

        self._reset_metric_for(website, data_interval)

        data_considered = [data for data in self.res_data[website] if (now - data["call_time"]).total_seconds() < data_interval]  # could be optimized
        errors_considered = [error for error in self.errors[website] if (now - error["call_time"]).total_seconds() < data_interval]

        metrics_data = self.metrics[website][data_interval]

        n_success_calls = len(data_considered)
        n_errors = len(errors_considered)
        n_total_calls = n_success_calls + n_errors

        max_time = metrics_data["max_res_time"]
        min_time = metrics_data["min_res_time"]
        total_res_time = 0
        metrics_data["code_count"] = defaultdict(int)
        metrics_data["code_count"]["200"] = 0  # for calculating availability
        code_count = metrics_data["code_count"]

        for data in data_considered:
            res_time = data["res_time"]
            total_res_time += res_time
            code_count_string = "{}XX".format(str(data["status"])[0])
            if code_count_string in code_count:
                code_count[code_count_string] += 1
            else:
                code_count[code_count_string] = 1

            max_time = max(max_time, res_time)
            min_time = min(min_time, res_time)

        metrics_data["avg_res_time"] = round(total_res_time/n_success_calls, 2) if n_success_calls > 0 else "unknown"
        metrics_data["max_res_time"] = max_time if n_success_calls > 0 else "unknown"
        metrics_data["min_res_time"] = min_time if n_success_calls > 0 else "unknown"
        metrics_data["total_requests"] = n_total_calls if n_total_calls > 0 else "unknown"
        metrics_data["errors"] = n_errors

        if data_interval == ALERTS_INTERVAL:
            if "prev_av" not in metrics_data:
                metrics_data["prev_av"] = -1
            else:
                metrics_data["prev_av"] = metrics_data["availability"]

        metrics_data["availability"] = round((code_count["2XX"]/n_total_calls)*100, 2) if n_total_calls > 0 else "unknown"

        if data_interval == ALERTS_INTERVAL:
            self._handle_alerts_for(website)

            


    def _get(self, website, timeout):
        success = False
        req_time = datetime.now()
        load_reducer_coefficient = 0.6  # This is to give time for other operations before the next job is run.
        self.logger.debug("requesting " + website)
        try:
            # simulate a request coming from a browser
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            res = requests.get(website, timeout=timeout*load_reducer_coefficient, headers=headers)  # Necessary since only one job of the same interval can run simultaniously.
        except Exception as e:
            res = str(e.__class__)
        else:
            success = True
        return res, req_time, success

    def _reset_metric_for(self, website, data_interval):
        metrics_data = self.metrics[website][data_interval]
        metrics_data["avg_res_time"] = 0
        metrics_data["max_res_time"] = 0
        metrics_data["min_res_time"] = float('inf')
        if "availability" not in metrics_data:
            metrics_data["availability"] = -1
        metrics_data["code_count"] = defaultdict(int)
        metrics_data["total_requests"] = 0
        metrics_data["errors"] = 0

    def _handle_alerts_for(self, website):
        metrics_data = self.metrics[website][ALERTS_INTERVAL]
        if metrics_data["prev_av"] >= 80 and metrics_data["availability"] < 80:
            self.alerts.append(self._make_alert_for(website, "DOWN", metrics_data["availability"]))
        elif metrics_data["prev_av"] < 80 and metrics_data["availability"] >= 80 and metrics_data["prev_av"] != -1:
            self.alerts.append(self._make_alert_for(website, "UP", metrics_data["availability"]))
    
    def _make_alert_for(self, website, status, availability):
        website = self.without_schema(website)
        if len(website) >= 40:
            website = website[:20] + "..." + website[-20:]
        return "{} is {} Availability={}%, time={}".format(website, status, availability, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))