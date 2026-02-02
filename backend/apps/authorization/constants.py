from typing import Literal

READ_PERMISSION = 'read_permission'
READ_ALL_PERMISSION = 'read_all_permission'
CREATE_PERMISSION = 'create_permission'
UPDATE_PERMISSION = 'update_permission'
UPDATE_ALL_PERMISSION = 'update_all_permission'
DELETE_PERMISSION = 'delete_permission'
DELETE_ALL_PERMISSION = 'delete_all_permission'

PERMISSIONS_LITERAL = Literal[
    READ_PERMISSION,
    CREATE_PERMISSION,
    UPDATE_PERMISSION,
    DELETE_PERMISSION,
    READ_ALL_PERMISSION,
    UPDATE_ALL_PERMISSION,
    DELETE_ALL_PERMISSION,
]
