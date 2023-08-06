# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Base class for all loggers."""
from abc import ABC, abstractmethod
from os import getenv
import uuid

from azureml.telemetry.log_scope import LogScope as _LogScope

try:
    from azureml._base_sdk_common import _ClientSessionId
    _telemetry_session_id = _ClientSessionId
except ImportError:
    _telemetry_session_id = str(uuid.uuid4())


class AbstractEventLogger(ABC):
    """Abstract event logger class."""

    @abstractmethod
    def log_event(self, telemetry_event):
        """
        Log event.

        :param telemetry_event: the event to be logged
        :type telemetry_event: TelemetryObjectBase
        :return: Event GUID.
        :rtype: str
        """
        raise NotImplementedError()

    @abstractmethod
    def log_metric(self, telemetry_metric):
        """
        Log metric.

        :param telemetry_metric: the metric to be logged
        :type telemetry_metric: TelemetryObjectBase
        :return: Metric GUID.
        :rtype: str
        """
        raise NotImplementedError()

    @abstractmethod
    def flush(self):
        """Flush the telemetry client."""
        raise NotImplementedError()

    SESSION_ID = "SessionId"
    SAMPLE_NOTEBOOK_NAME = "SampleNotebookName"

    @staticmethod
    def _fill_props_with_context(telemetry_entry):
        """Fill telemetry props with context info.

        :param telemetry_entry: event or metric
        :type telemetry_entry: TelemetryObjectBase
        :return properties with context info
        :rtype: dict
        """
        props = telemetry_entry.get_all_properties()
        ctx = _LogScope.get_current()
        props = props if ctx is None else ctx.get_merged_props(props)  # merge values from parent scope if any

        props[AbstractEventLogger.SESSION_ID] = _telemetry_session_id  # set global session id
        # set SampleNotebookName if any
        sample_notebook_name = getenv(AbstractEventLogger.SAMPLE_NOTEBOOK_NAME)
        if sample_notebook_name:
            props[AbstractEventLogger.SAMPLE_NOTEBOOK_NAME] = sample_notebook_name

        return props
