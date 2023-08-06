# Filename for the patch to apply on top of a snapshot, if the project is using git.
COMMIT_PATCH_BASENAME = 'anyscale-patch'

ENDPOINTS = {
    "project_create": "/project/create",
    "project_list": "/project/list",
    "project_sessions": "/project/sessions",
    "session_list": "/session/list",
    "session_create": "/session/create",
    "session_describe": "/session/describe",
    "session_commands": "/session/commands",
    "session_execute": "/session/execute",
    "session_stop": "/session/stop",
    "session_execution_log": "/session/execution_log",
    "session_startup_log": "/session/startup_log",
    "session_sync": "/session/sync",
    "snapshot_list": "/snapshot/list",
    "snapshot_describe": "/snapshot/describe",
    "snapshot_create": "/snapshot/create",
    "snapshot_delete": "/snapshot/delete",
    "snapshot_get": "/snapshot/get",
    "user_info": "/user/info",
    "user_login": "/user/login",
    "user_register": "/user/register",
    "user_server_session_token": "/user/server_session_token",
}
