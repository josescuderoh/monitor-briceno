from rolepermissions.roles import AbstractUserRole


class Administrador(AbstractUserRole):
    available_permissions = {
        'create_users': True,
        'view_all_projects': True,
        'edit_all_projects': True,
        'view_projects': True,
        'create_projects': True,
    }


class Consulta(AbstractUserRole):
    available_permissions = {
        'view_all_projects': True,
        'view_projects': True,
    }


class Entidad(AbstractUserRole):
    available_permissions = {
        'create_projects': True,
        'view_projects': True,
    }
