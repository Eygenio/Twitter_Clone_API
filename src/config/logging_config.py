from uvicorn.logging import DefaultFormatter


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        # Цветные логи для приложения
        "color": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            "log_colors": {
                "DEBUG": "blue",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
        # Форматтер для uvicorn
        "uvicorn": {
            "()": DefaultFormatter,
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": True,
        },
    },

    "handlers": {
        # Консоль для логов
        "console_color": {
            "class": "logging.StreamHandler",
            "formatter": "color",
            "level": "INFO",
        },
        # Консоль для uvicorn
        "uvicorn_console": {
            "class": "logging.StreamHandler",
            "formatter": "uvicorn",
            "level": "INFO",
        },
    },

    "loggers": {
        # uvicorn логгеры
        "uvicorn": {
            "handlers": ["uvicorn_console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["uvicorn_console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["uvicorn_console"],
            "level": "INFO",
            "propagate": False,
        },

        # Логи приложения
        "src": {
            "handlers": ["console_color"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
