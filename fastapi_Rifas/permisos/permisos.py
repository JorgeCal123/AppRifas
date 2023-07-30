# permissions.py

from fastapi_permissions import Allow, Deny, IsAuthenticated, Everyone, Authenticated, All
from fastapi_permissions import Permission


# Permiso para editar datos
# Permitir a usuarios autenticados con permiso 'edit_data'],
    # Si ningún permiso coincide, se aplicará Deny a todos los demás usuarios
    # Esto niega automáticamente el acceso a los usuarios no autenticados

edit_permission = Permission(rules=[(Allow, Authenticated, 'edit_data'),],  default=Deny)

# Rol de administrador con todos los permisos
# Permitir a todos los usuarios con todos los permisos
admin_role = Permission(rules=[(Allow, Everyone, All),  ])

# Asignar un permiso específico a un rol (por ejemplo, solo lectura)
 # Permitir a todos los usuarios con permiso 'read_only'
read_only_role = Permission(rules=[(Allow, Everyone, 'read_only'), ])
