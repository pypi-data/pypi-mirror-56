import time

import bqplot.pyplot as plt
import bqplot
import numpy as np
import psutil


class CpuUsage(object):
    def __init__(self, df, clear=False, interactive=False, throttle_time=0.05):
        self.xlist = []
        self.ylist = []
        self.throttle_time = throttle_time
        self.interactive = interactive

        self.scales = {'x': bqplot.LinearScale(min=0, max=1), 'y': bqplot.LinearScale(min=0, max=100)}
        self.fig = plt.figure(scales=self.scales)
        self.lines = plt.plot(x=[0, 1], y=[0, 2], stroke_width=0.5, line_style='dotted', scales=self.scales)
        self.line_mean = plt.plot(x=[0, 1], y=[0, 2], colors=["red"], line_style="solid", scales=self.scales)
        if clear:
            df.executor.signal_begin.callbacks.clear()

        @df.executor.signal_begin.connect
        def begin():
            psutil.cpu_percent(0.0, True)
            self.xlist.clear()
            self.ylist.clear()
            self.last_time = time.time()
            return True

        if clear:
            df.executor.signal_progress.callbacks.clear()
        @df.executor.signal_progress.connect
        def progress(f):
            current_time = time.time()
            if (current_time - self.last_time) > self.throttle_time or f in [0, 1]:
                self.last_time = current_time
                self.xlist.append(f)
                self.ylist.append(psutil.cpu_percent(0.0, True))
                if self.interactive:
                    self.update_plot()
            return True

        if clear:
            df.executor.signal_end.callbacks.clear()
        @df.executor.signal_end.connect
        def end():
            if self.ylist:
                self.update_plot()
            return True
    
    def update_plot(self):
        if self.ylist:
            y = np.array(self.ylist)
            x = np.array(self.xlist)
            self.lines.x = x
            self.lines.y = y.T
            self.line_mean.x = x
            self.line_mean.y = np.mean(y, axis=1)
