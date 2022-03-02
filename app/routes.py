import logging.config
from app import api
from app.controller.LoginController import Login, Users, Refresh
from app.controller.NetworkController import RebootService, TimezoneService, NetworkService, NTPService, \
    ShutdownService, DTMService, GetPortInfo
from app.controller.RoleController import QueryRole, QueryRoleById, CreateRole, UpdateRole, DeleteRole
from app.controller.UserController import QueryUser, QueryUserById, CreateUser, UpdateUser, DeleteUser
from app.controller.FormController import QueryForm, QueryFormById, CreateForm, UpdateForm, DeleteForm
from app.controller.RoleFormController import UpdateRoleForm,QueryRoleFormByRoleId,GetAllRoles
from app.controller.DashBoardController import GetCpuInfo,GetMemoryInfo, GetDiskInfo, GetAllInterface, GetAllInterfaceBytes,GetDetection

from app.controller.ServiceController import GetServiceStatus,StartService,StopService, EnableService, DisableService

from app.controller.LogController import GetDTMLog, GetSuricataLog


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

api.add_resource(GetMemoryInfo, '/dashboard/getMemoryInfo', resource_class_kwargs={
    'logger': logging.getLogger('/dashboard/getMemoryInfo')
})

api.add_resource(GetDiskInfo, '/dashboard/getDiskInfo', resource_class_kwargs={
    'logger': logging.getLogger('/dashboard/getDiskInfo')
})

api.add_resource(GetAllInterface, '/dashboard/getAllInterface', resource_class_kwargs={
    'logger': logging.getLogger('/dashboard/getAllInterface')
})

api.add_resource(GetAllInterfaceBytes, '/dashboard/getAllInterfaceBytes', resource_class_kwargs={
    'logger': logging.getLogger('/dashboard/getAllInterfaceBytes')
})

api.add_resource(GetDetection, '/dashboard/getDetection', resource_class_kwargs={
    'logger': logging.getLogger('/dashboard/getDetection')
})


#Service 功能
api.add_resource(GetServiceStatus, '/service/getServiceStatus', resource_class_kwargs={
    'logger': logging.getLogger('/service/getServiceStatus')
})

api.add_resource(StartService, '/service/startService', resource_class_kwargs={
    'logger': logging.getLogger('/service/startService')
})

api.add_resource(StopService, '/service/stopService', resource_class_kwargs={
    'logger': logging.getLogger('/service/startService')
})

api.add_resource(EnableService, '/service/enableService', resource_class_kwargs={
    'logger': logging.getLogger('/service/enableService')
})

api.add_resource(DisableService, '/service/disableService', resource_class_kwargs={
    'logger': logging.getLogger('/service/disableService')
})

#取出Log功能
api.add_resource(GetDTMLog, '/log/dtm', resource_class_kwargs={
    'logger': logging.getLogger('/log/dtm')
})

api.add_resource(GetSuricataLog, '/log/suricata', resource_class_kwargs={
    'logger': logging.getLogger('/log/suricata')
})

#network

api.add_resource(RebootService, '/service/reboot', resource_class_kwargs={
    'logger': logging.getLogger('/service/reboot')
})

api.add_resource(ShutdownService, '/service/shutdown', resource_class_kwargs={
    'logger': logging.getLogger('/service/shutdown')
})

api.add_resource(TimezoneService, '/service/timezone', resource_class_kwargs={
    'logger': logging.getLogger('/service/timezone')
})

api.add_resource(NetworkService, '/service/network', resource_class_kwargs={
    'logger': logging.getLogger('/service/network')
})

api.add_resource(NTPService, '/service/ntp', resource_class_kwargs={
    'logger': logging.getLogger('/service/ntp')
})

api.add_resource(DTMService, '/service/dtm', resource_class_kwargs={
    'logger': logging.getLogger('/service/dtm')
})

api.add_resource(GetPortInfo, '/service/portInfo', resource_class_kwargs={
    'logger': logging.getLogger('/service/dtm')
})

