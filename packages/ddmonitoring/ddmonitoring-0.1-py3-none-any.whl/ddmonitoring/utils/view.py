import os
import time
from collections import defaultdict
from asciimatics.widgets import Frame, Layout, MultiColumnListBox, Label, TextBox, Divider
from asciimatics.screen import Screen
from ddmonitoring.utils.constants import DATA_INTERVAL_SHORT, DATA_INTERVAL_LONG,\
    REFRESH_LONG, REFRESH_SHORT


class UIInfo:
    """Class to hold UI data"""
    def __init__(
            self,
            last_frames,
            last_refreshes,
            headers,
            interval,
            displayed_codes,
            base_titles,
            columns):

        self.last_frames = last_frames
        self.last_refreshes = last_refreshes
        self.headers = headers
        self.interval = interval
        self.displayed_codes = displayed_codes
        self.titles = base_titles + self.displayed_codes
        self.columns = columns

class MonitorFrame(Frame):
    """This class details the 'window' to be drawn into the terminal"""
    def __init__(self, screen, model):
        super(MonitorFrame, self).__init__(
            screen,
            screen.height,
            screen.width,
            has_border=True,
            title="DD-MONITORING"
        )
        # Internal state required for doing periodic updates
        now = time.time()
        self._last_frame = 0
        self._ui_info = UIInfo(
            last_frames=defaultdict(int),
            last_refreshes=defaultdict(lambda: now),
            headers={
                "LONG": "Past hour - ",
                "SHORT": "Past 10 minutes -",
                "ALERTS": "Alerts [2min.]"
                },
            interval=DATA_INTERVAL_SHORT,
            displayed_codes=["1XX", "2XX", "3XX", "4XX", "5XX"],
            base_titles=[
                "URL",
                "Availability",
                "MAX.(ms)",
                "AVG.(ms)",
                "MIN.(ms)",
                "Req.",
                "Failed"
            ],
            columns=[35, 15, 10, 10, 10, 7, 13, 5, 5, 5, 5, 5]
        )
        self._model = model
        self._metrics_data_short, _ = self.get_metrics(self._ui_info.interval)

        self._metrics_data_long, self._alerts_data = self.get_metrics(self._ui_info.interval)

        # Create the basic form layout...
        layout = Layout([1], fill_frame=True)

        self._alerts_header = TextBox(height=1, as_string=True)
        self._alerts_header.disabled = True
        self._alerts_header.custom_colour = "label"
        self._alerts_header.value = self._ui_info.headers["ALERTS"]

        self._metrics_h_short = TextBox(height=1, as_string=True)
        self._metrics_h_short.disabled = True
        self._metrics_h_short.custom_colour = "label"

        self._metrics_h_long = TextBox(height=1, as_string=True)
        self._metrics_h_long.disabled = True
        self._metrics_h_long.custom_colour = "label"

        self._metrics_short = MultiColumnListBox(
            height=screen.height//3 -3,
            columns=self._ui_info.columns,
            options=[],
            titles=self._ui_info.titles,
            name="Metrics Short")

        self._metrics_long = MultiColumnListBox(
            height=screen.height//3 -3,
            columns=self._ui_info.columns,
            options=[],
            titles=self._ui_info.titles,
            name="Metrics Long")

        self._alerts = MultiColumnListBox(
            height=screen.height//3 -3,
            columns=[100],
            options=[],
            titles=["Message"],
            name="Alerts"
        )
        self.add_layout(layout)
        layout.add_widget(self._metrics_h_short)
        layout.add_widget(self._metrics_short)
        layout.add_widget(Divider())
        layout.add_widget(self._metrics_h_long)
        layout.add_widget(self._metrics_long)
        layout.add_widget(Divider())
        layout.add_widget(self._alerts_header)
        layout.add_widget(self._alerts)
        layout.add_widget(Divider())
        layout.add_widget(Label('Press `Ctrl+{0}` to exit, `Tab` to switch focus,\
            Arrow Keys to scroll.'.format('Break' if os.name == 'nt' else 'C')))
        self.fix()

        # Add my own colour palette
        self.palette = defaultdict(
            lambda: (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLACK)
        )
        self.palette["selected_focus_field"] = (
            Screen.COLOUR_CYAN, Screen.A_BOLD, Screen.COLOUR_BLACK
        )
        self.palette["label"] = (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK)
        self.palette["title"] = (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_WHITE)
        self.palette["borders"] = (Screen.COLOUR_MAGENTA, Screen.A_BOLD, Screen.COLOUR_BLACK)

    def get_metrics(self, data_interval):
        """Method to retrieve all the metrics corresponding to the specified data interval"""

        metrics = []

        for i, url in enumerate(self._model.metrics):
            metrics_data = self._model.metrics[url][data_interval]
            row_data = [
                self._model.without_schema(url),
                str(metrics_data["availability"]),
                str(metrics_data["max_res_time"]),
                str(metrics_data["avg_res_time"]),
                str(metrics_data["min_res_time"]),
                str(metrics_data["total_requests"]),
                str(metrics_data["errors"]),
            ]
            row_data += [str(metrics_data["code_count"][code]) for code in self._ui_info.displayed_codes]
            row = (row_data, i)
            metrics.append(row)

        alerts = [([alert], i) for i, alert in enumerate(self._model.alerts)]

        return metrics, alerts

    def _update(self, frame_no):
        if frame_no - self._last_frame >= self.frame_update_count or self._last_frame == 0:
            now = time.time()

            last_start_short = self._metrics_short.start_line
            last_start_long = self._metrics_long.start_line

            last_sel_short = self._metrics_short.value
            last_sel_long = self._metrics_long.value

            last_start_a = self._alerts.start_line
            last_sel_a = self._alerts.value

            self._last_frame = frame_no

            if frame_no - self._ui_info.last_frames["LONG"] >= REFRESH_LONG * self.frame_update_count:
                self._ui_info.last_frames["LONG"] = frame_no
                self._ui_info.last_refreshes["LONG"] = now
                self._ui_info.interval = DATA_INTERVAL_LONG
                self._metrics_data_long, self._alerts_data = self.get_metrics(DATA_INTERVAL_LONG)


            if frame_no - self._ui_info.last_frames["SHORT"] >= REFRESH_SHORT * self.frame_update_count or self._last_frame == 0:
                self._ui_info.last_frames["SHORT"] = frame_no
                self._ui_info.last_refreshes["SHORT"] = now
                self._ui_info.interval = DATA_INTERVAL_SHORT
                self._metrics_data_short, self._alerts_data = self.get_metrics(DATA_INTERVAL_SHORT)

            # self._metrics_h_short.value = (self._base_h_short + "refreshing in:
            # " + str(int(round((self._last_refresh_short + REFRESH_SHORT - now)))))
            self.make_refresh_header(
                base_header=self._ui_info.headers["SHORT"],
                header=self._metrics_h_short,
                refresh=REFRESH_SHORT,
                last_refresh=self._ui_info.last_refreshes["SHORT"],
                now=now)

            self.make_refresh_header(
                base_header=self._ui_info.headers["LONG"],
                header=self._metrics_h_long,
                refresh=REFRESH_LONG,
                last_refresh=self._ui_info.last_refreshes["LONG"],
                now=now)

            self._metrics_short.options = self._metrics_data_short
            self._metrics_short.value = last_sel_short
            self._metrics_short.start_line = last_start_short

            self._metrics_long.options = self._metrics_data_long
            self._metrics_long.value = last_sel_long
            self._metrics_long.start_line = last_start_long

            self._alerts.options = self._alerts_data
            self._alerts.value = last_sel_a
            self._alerts.start_line = last_start_a

        # Now redraw as normal
        super(MonitorFrame, self)._update(frame_no)

    @property
    def frame_update_count(self):
        # Refresh once every second by default.
        return 20

    @staticmethod
    def make_refresh_header(base_header, header, refresh, last_refresh, now):
        """Updates the header with the 'refresh in' message"""

        header.value = (base_header + "refreshing in: " \
            + str(int(round(last_refresh + refresh - now))))
