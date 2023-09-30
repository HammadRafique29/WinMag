import _scripts.action_calls as func

create_action_functions = func._CREATE_ACTION_FUNCTIONS()

# _Actions = {
#     "create": {
#         "file": create_action_functions.create_file,
#         "folder": create_action_functions._CREATE_FOLDER,
#     }
# }
_Actions = {"create": ['file', 'folder']}

_Action_Func = {'file':create_action_functions._CREATE_FILE,
                "folder": create_action_functions._CREATE_FOLDER,
                }