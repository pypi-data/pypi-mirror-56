import time
import sched
import random
import threading
import traceback
from atatus.utils.logging import get_logger
from .transport import BaseTransport
from .layer import Layer

import atatus


class Txn(Layer):
    def __init__(self, type, kind, duration):
        super(Txn, self).__init__(type, kind, duration)
        self.spans = {}

    def add_span(self, span_name, type, kind, duration):
        if span_name not in self.spans:
            self.spans[span_name] = Layer(type, kind, duration)
        else:
            self.spans[span_name].aggregate(duration)


class Collector(object):
    def __init__(self, config, metadata):
        self._config = config
        cls = self.__class__
        self._error_logger = get_logger("atatus.errors")
        self._logger = get_logger("%s.%s" % (cls.__module__, cls.__name__))

        if not self._config.app_name and not self._config.license_key:
            self._error_logger.error("Error: Atatus configuration app_name and license_key are missing!")
        elif not self._config.license_key:
            self._error_logger.error("Error: Atatus configuration license_key is missing!")
        elif not self._config.app_name:
            self._error_logger.error("Error: Atatus configuration app_name is missing!")

        self._spans = {}
        self._txns_lock = threading.Lock()
        self._txns_agg = {}
        self._traces_agg = []
        self._error_metrics_agg = {}
        self._error_requests_agg = []

        self._errors_lock = threading.Lock()
        self._errors_agg = []

        self._metrics_lock = threading.Lock()
        self._metrics_agg = []

        self._transport = BaseTransport(config, metadata)
        self._collect_counter = 0

        self._scheduler = None
        self._start_time = int(time.time() * 1000)
        self._worker = None
        self._closed = False
        self.start_collector_thread()

    def start_collector_thread(self):
        if (not self._worker or not self._worker.is_alive()) and not self._closed:
            try:
                self._worker = threading.Thread(target=self._worker_thread, name="Atatus Collector Worker")
                self._worker.setDaemon(True)
                self._worker_exit = threading.Event()
                self._worker.start()
            except RuntimeError:
                pass

    def close(self):
        if self._closed:
            return
        self._closed = True
        self._worker_exit.set()
        if self._worker.is_alive():
            self._worker.join(10)

    def _worker_timefunc(self):
        if self._worker_exit.isSet():
            return float("inf")
        return time.time()

    def _worker_thread(self):
        self._scheduler = sched.scheduler(self._worker_timefunc, self._worker_exit.wait)
        self._start_time = int(time.time() * 1000)
        self._scheduler.enter(60.0, 1, self._collect)
        try:
            self._scheduler.run()
        except Exception as e:
            self._error_logger.error("Atatus worker failed with exception: %r", e)
            self._error_logger.error(traceback.format_exc())

    def _collect(self):
        start_time = self._start_time

        if not self._worker_exit.isSet():
            self._start_time = int(time.time() * 1000)
            self._scheduler.enter(60.0, 1, self._collect)

        end_time = int(time.time() * 1000)

        if not self._config.app_name or not self._config.license_key:
            if not self._config.app_name and not self._config.license_key:
                self._error_logger.error("Error: Atatus configuration app_name and license_key are missing!")
            elif not self._config.license_key:
                self._error_logger.error("Error: Atatus configuration license_key is missing!")
            elif not self._config.app_name:
                self._error_logger.error("Error: Atatus configuration app_name is missing!")
            return

        with self._txns_lock:
            txn_data = self._txns_agg
            self._txns_agg = {}

            trace_data = self._traces_agg
            self._traces_agg = []

            error_metrics_data = self._error_metrics_agg
            self._error_metrics_agg = {}

            error_requests_data = self._error_requests_agg
            self._error_requests_agg = []

        with self._errors_lock:
            error_data = self._errors_agg
            self._errors_agg = []

        with self._metrics_lock:
            metrics_data = self._metrics_agg
            self._metrics_agg = []

        try:
            if txn_data:
                self._transport.txns(start_time, end_time, txn_data)

            if trace_data:
                self._transport.traces(start_time, end_time, trace_data)

            if error_metrics_data:
                self._transport.error_metrics(start_time, end_time, error_metrics_data, error_requests_data)

            if error_data:
                self._transport.errors(start_time, end_time, error_data)

            if metrics_data:
                self._transport.metrics(start_time, end_time, metrics_data)

            if self._collect_counter % 30 == 0:
                self._transport.hostinfo(start_time)
                self._collect_counter = 0
            self._collect_counter += 1

        except Exception as e:
            self._error_logger.error("Atatus collect failed with exception: %r" % e)
            self._error_logger.error(traceback.format_exc())

    def add_error(self, error):

        with self._errors_lock:
            if len(self._errors_agg) < 20:
                self._errors_agg.append(error)
            else:
                i = random.randrange(20)
                self._errors_agg[i] = error

    def add_metricset(self, metricset):
        if "samples" not in metricset:
            return
        s = metricset["samples"]

        if not all(k in s for k in ("system.cpu.total.norm.pct", "system.memory.actual.free", "system.memory.total", "system.process.cpu.total.norm.pct", "system.process.memory.size", "system.process.memory.rss.bytes")):
            return

        if not all("value" in s[k] for k in ("system.cpu.total.norm.pct", "system.memory.actual.free", "system.memory.total", "system.process.cpu.total.norm.pct", "system.process.memory.size", "system.process.memory.rss.bytes")):
            return

        metric = {
            "system.cpu.total.norm.pct": s["system.cpu.total.norm.pct"]["value"],
            "system.memory.actual.free": s["system.memory.actual.free"]["value"],
            "system.memory.total": s["system.memory.total"]["value"],
            "system.process.cpu.total.norm.pct": s["system.process.cpu.total.norm.pct"]["value"],
            "system.process.memory.size": s["system.process.memory.size"]["value"],
            "system.process.memory.rss.bytes": s["system.process.memory.rss.bytes"]["value"]
        }

        with self._metrics_lock:
            self._metrics_agg.append(metric)

    def add_span(self, span):
        if not all(k in span for k in ("transaction_id", "name", "type", "subtype", "duration")):
            return

        span_id = span["transaction_id"]
        if span_id not in self._spans:
            self._spans[span_id] = [span]
        else:
            self._spans[span_id].append(span)

    def add_txn(self, txn):
        if not all(k in txn for k in ("name", "id", "duration")):
            return
        txn_name = txn["name"]
        if not txn_name:
            return

        with self._txns_lock:
            if txn_name not in self._txns_agg:
                if self._config.framework_name:
                    txn_type = self._config.framework_name
                else:
                    txn_type = atatus.PYTHON_AGENT
                self._txns_agg[txn_name] = Txn(txn_type, atatus.PYTHON_AGENT, txn["duration"])
            else:
                self._txns_agg[txn_name].aggregate(txn["duration"])

            spans_present = False

            txn_id = txn["id"]
            if txn_id in self._spans:
                for span in self._spans[txn_id]:
                    if not all(k in span for k in ("name", "type", "subtype", "duration")):
                        continue
                    span_name = span["name"]
                    if span_name not in self._txns_agg[txn_name].spans:
                        kind = Layer.kinds_dict.get(span["type"], span["type"])
                        type = Layer.types_dict.get(span["subtype"], span["subtype"])
                        self._txns_agg[txn_name].spans[span_name] = Layer(type, kind, span["duration"])
                    else:
                        self._txns_agg[txn_name].spans[span_name].aggregate(span["duration"])
                spans_present = True

            if spans_present:
                # if txn["duration"] >= self._config.trace_threshold:
                if txn["duration"] >= 0:
                    trace_txn = txn
                    trace_txn["spans"] = self._spans[txn_id]

                    if len(self._traces_agg) < 5:
                        self._traces_agg.append(trace_txn)
                    else:
                        i = random.randrange(5)
                        self._traces_agg[i] = trace_txn

            if spans_present:
                del self._spans[txn_id]

            if "context" in txn and \
               "response" in txn["context"] and \
               "status_code" in txn["context"]["response"]:

                status_code = txn["context"]["response"]["status_code"]

                if status_code >= 400 and status_code != 404:
                    if txn_name not in self._error_metrics_agg:
                        self._error_metrics_agg[txn_name] = {status_code: 1}
                    else:
                        if status_code not in self._error_metrics_agg[txn_name]:
                            self._error_metrics_agg[txn_name][status_code] = 1
                        else:
                            self._error_metrics_agg[txn_name][status_code] += 1

                    if len(self._error_requests_agg) < 20:
                        self._error_requests_agg.append({"name": txn_name, "context": txn["context"]})
                    else:
                        i = random.randrange(20)
                        self._error_requests_agg[i] = {"name": txn_name, "context": txn["context"]}
