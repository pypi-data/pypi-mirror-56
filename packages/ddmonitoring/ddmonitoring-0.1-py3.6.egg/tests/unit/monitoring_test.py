# from ddmonitoring.app.metrics_model import MetricsModel
# import logging
# from datetime import datetime

# model = MetricsModel({"google.com": [1]}, logging.getLogger(__name__))

# def test_internet_ok():
#     for website in model.check_data:
#         response, time = model._get(website)
#         assert response.status_code==200

# def test_res_data_ok():
#     for website in model.check_data:
#         model.check(website)
#     for website in model.check_data:
#         data = model.res_data[website][0]
#         call_time = data["call_time"]
#         res_time = data["res_time"]
#         status = data["status"]
#         assert type(call_time) == type(datetime.now())
#         assert type(res_time) == type(float()) 
#         assert type(status) == type(int())

# def test_metrics_ok():
#     google = "http://google.com"
#     model.metrics = {website: {} for website in [google, "dummy"]}
#     model.check(google)
#     model.make_metrics_for(google, 5)
#     metrics = model.metrics[google][5]
#     assert "avg_res_time" in metrics
#     assert "max_res_time" in metrics
#     assert "min_res_time" in metrics
#     assert "availability" in metrics
#     assert "200_count" in metrics
#     assert "total_requests" in metrics
#     model.metrics["dummy"] = {}
#     model._init_metric_for("dummy", 5)
#     assert model.metrics["dummy"][5] != metrics

# def test_alerts_ok():
#     website = "dummy"
#     alert_message_template = "{} is {}"
#     model.metrics = {website: {}}
#     model._init_metric_for("dummy", model.ALERT_INTERVAL)
#     metrics = model.metrics[website][model.ALERT_INTERVAL]
#     metrics["prev_availability"] = 82.0
#     metrics["availability"] = 79.9999
#     model._handle_alerts_for(website)
#     assert model.alerts[0].startswith(alert_message_template.format(website, "DOWN"))
#     metrics["prev_availability"] = 42
#     metrics["availability"] = 81
#     model._handle_alerts_for(website)
#     assert model.alerts[1].startswith(alert_message_template.format(website, "UP"))
