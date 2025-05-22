import os
from .settings import BASE_DIR

LOG_FOLDER = os.path.join(BASE_DIR, "LOGS")

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

CUSTOM_LOGGING_FORMAT = """
-------------------------------------------------------------
{asctime} - {levelname}
-------------------------------------------------------------
Module: {module} | Process: {process:d} | Thread: {thread:d}
-------------------------------------------------------------
{message}
-------------------------------------------------------------
"""

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'custom': {
            'format': CUSTOM_LOGGING_FORMAT,
            'style': '{'
        },
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} | {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_FOLDER, 'Exceptions.log'),
            'formatter': 'custom'
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_FOLDER, 'Debug.log'),
            'formatter': 'custom'
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_FOLDER, 'Info.log'),
            'formatter': 'custom'
        },
        'console_info': {
            'level': 'INFO',
            # 'filters': ['require_debug_true'],
            # 'filename': os.path.join(LOG_FOLDER, 'ConsoleInfo.log'),
            'class': 'logging.StreamHandler',
            'formatter': 'custom'
        },
        'console_debug': {
            'level': 'DEBUG',
            # 'filters': ['require_debug_true'],
            # 'filename': os.path.join(LOG_FOLDER, 'ConsoleDebug.log'),
            'class': 'logging.StreamHandler',
            'formatter': 'custom'
        },
        'console_error': {
            'level': 'ERROR',
            # 'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            # 'filename': os.path.join(LOG_FOLDER, 'ConsoleException.log'),
            'formatter': 'custom'
        },
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'filters': ['custom'],
        #     'email_backend': 'django.core.mail.backends.filebased.EmailBackend',
        # }
    },
    'loggers': {
        'django': {
            'handlers': [
                # 'console_error',
                # 'console_info',
                # 'console_debug',
                'file_error',
                'file_debug',
                'file_info',
                # 'mail_admins'
            ],
            'propagate': True,
            # 'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO')
        },
        'django.request': {
            # , 'console_error',  # 'mail_admins'],
            'handlers': ['file_error'],
            'level': 'ERROR',
            'propagate': False,
        },
        # 'myproject.custom': {
        #     'handlers': ['console', 'mail_admins'],
        #     'level': 'INFO',
        #     'filters': ['special']
        # }
    }
}
