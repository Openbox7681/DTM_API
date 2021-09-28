import logging.config
from app import api
from app.controller.LoginController import Login, Users
from app.controller.RoleController import QueryRole, QueryRoleById


logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "info_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": "info.log",
                "maxBytes": 10485760,
                "backupCount": 50,
                "encoding": "utf8",
            },
            "error_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "simple",
                "filename": "errors.log",
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8",
            },
            "debug_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": "debug.log",
                "maxBytes": 10485760,
                "backupCount": 50,
                "encoding": "utf8",
            },
        },
        "loggers": {
            "my_module": {"level": "ERROR", "handlers": ["console"], "propagate": "no"}
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["error_file_handler", "debug_file_handler"],
        },
    }
)


#登入相關
api.add_resource(Login, '/account/user/login', resource_class_kwargs={
    'logger': logging.getLogger('/account/user/ogin')
})

api.add_resource(Users, '/users', resource_class_kwargs={
    'logger': logging.getLogger('/users')
})

#角色相關
api.add_resource(QueryRole, '/roles/query', resource_class_kwargs={
    'logger': logging.getLogger('/roles')
})

api.add_resource(QueryRoleById, '/roles/query/id', resource_class_kwargs={
    'logger': logging.getLogger('/roles/query/id')
})


