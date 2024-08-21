import sys

import structlog

import standardize_repo_settings


def add_custom_info(logger, method_name, event_dict):
    event_dict["version"] = standardize_repo_settings.__version__
    return event_dict


def setup_logging():
    shared_processors = [
        add_custom_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
    ]

    if sys.stderr.isatty():
        # If we're in a terminal, pretty print the logs.
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(),
        ]
    else:
        # Otherwise, output logs in JSON format
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]

    structlog.configure(
        processors=processors,
        cache_logger_on_first_use=True,
    )
