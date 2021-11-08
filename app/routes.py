import logging.config
from app import api
from app.controller.LoginController import Login, Users, Refresh
from app.controller.RoleController import QueryRole, QueryRoleById, CreateRole, UpdateRole, DeleteRole
from app.controller.UserController import QueryUser, QueryUserById, CreateUser, UpdateUser, DeleteUser
from app.controller.FormController import QueryForm, QueryFormById, CreateForm, UpdateForm, DeleteForm
from app.controller.RoleFormController import UpdateRoleForm,QueryRoleFormByRoleId,GetAllRoles
from app.controller.DashBoardController import GetCpuInfo


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

api.add_resource(Refresh, '/account/user/refresh', resource_class_kwargs={
    'logger': logging.getLogger('/users')
})



#角色相關
api.add_resource(QueryRole, '/roles/query', resource_class_kwargs={
    'logger': logging.getLogger('/roles')
})

api.add_resource(QueryRoleById, '/roles/query/id', resource_class_kwargs={
    'logger': logging.getLogger('/roles/query/id')
})

api.add_resource(CreateRole, '/roles/create', resource_class_kwargs={
    'logger': logging.getLogger('/roles/create')
})

api.add_resource(UpdateRole, '/roles/update', resource_class_kwargs={
    'logger': logging.getLogger('/roles/update')
})

api.add_resource(DeleteRole, '/roles/delete', resource_class_kwargs={
    'logger': logging.getLogger('/roles/delete')
})

#帳戶相關

api.add_resource(QueryUser, '/account/query', resource_class_kwargs={
    'logger': logging.getLogger('/account')
})

api.add_resource(QueryUserById, '/account/query/id', resource_class_kwargs={
    'logger': logging.getLogger('/account/query/id')
})

api.add_resource(CreateUser, '/account/create', resource_class_kwargs={
    'logger': logging.getLogger('/account/create')
})

api.add_resource(UpdateUser, '/account/update', resource_class_kwargs={
    'logger': logging.getLogger('/account/update')
})

api.add_resource(DeleteUser, '/account/delete', resource_class_kwargs={
    'logger': logging.getLogger('/account/delete')
})


#表單相關
api.add_resource(QueryForm, '/form/query', resource_class_kwargs={
    'logger': logging.getLogger('/form')
})

api.add_resource(QueryFormById, '/form/query/id', resource_class_kwargs={
    'logger': logging.getLogger('/form/id')
})

api.add_resource(CreateForm, '/form/create', resource_class_kwargs={
    'logger': logging.getLogger('/form/create')
})

api.add_resource(UpdateForm, '/form/update', resource_class_kwargs={
    'logger': logging.getLogger('/form/update')
})

api.add_resource(DeleteForm, '/form/delete', resource_class_kwargs={
    'logger': logging.getLogger('/form/delete')
})

#表單權限功能
api.add_resource(UpdateRoleForm, '/roleForm/update', resource_class_kwargs={
    'logger': logging.getLogger('/roleForm/update')
})

api.add_resource(QueryRoleFormByRoleId, '/roleForm/query/roleId', resource_class_kwargs={
    'logger': logging.getLogger('/roleForm/query/roleId')
})


api.add_resource(GetAllRoles, '/roleForm/getAllRoles', resource_class_kwargs={
    'logger': logging.getLogger('/roleForm/getAllRoles')
})

#DashBoard 資訊功能
api.add_resource(GetCpuInfo, '/dashboard/getCpuInfo', resource_class_kwargs={
    'logger': logging.getLogger('/dashboard/getCpuInfo')
})

