import os
import sys

def debug():
  sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
  
  from app.auth.permission.models import Permission
  from app.auth.role.models import Role, RolePermission
  from app.auth.user_role.models import UserRole
  from app.auth.user.models import User
  from db.database import Session

  db = Session()

  print("=" * 80)
  print("CHECKING PERMISSIONS DATABASE STATE")
  print("=" * 80)

  # Check Permissions
  print("\n1. PERMISSIONS TABLE:")
  permissions = db.query(Permission).all()
  print(f"Total permissions: {len(permissions)}")
  for p in permissions:
    print(f"  ID: {p.id}, App: {p.app}, Name: {p.name}")

  # Check Roles
  print("\n2. ROLES TABLE:")
  roles = db.query(Role).all()
  print(f"Total roles: {len(roles)}")
  for r in roles:
    print(f"  ID: {r.id}, Name: {r.name}")

  # Check Role Permissions
  print("\n3. ROLE PERMISSIONS TABLE:")
  for r in roles:
    role_perms = db.query(RolePermission).filter(RolePermission.role_id == r.id).all()
    print(f"\n  Role: {r.name} (ID: {r.id})")
    print(f"  Total permissions: {len(role_perms)}")
    if role_perms:
      # Show first 5
      for rp in role_perms[:5]:
        perm = db.query(Permission).filter(Permission.id == rp.permission_id).first()
        print(f"    Permission: {perm.app}/{perm.name} - Browse:{rp.browse} Read:{rp.read} Create:{rp.create} Update:{rp.update} Delete:{rp.delete} Restore:{rp.restore}")
      if len(role_perms) > 5:
        print(f"    ... and {len(role_perms) - 5} more")
    else:
      print(f"    NO PERMISSIONS ASSIGNED!")

  # Check Users and their roles
  print("\n4. USERS AND THEIR ROLES:")
  users = db.query(User).all()
  for u in users:
    user_roles = db.query(UserRole).filter(UserRole.user_id == u.id).all()
    role_names = []
    for ur in user_roles:
      role = db.query(Role).filter(Role.id == ur.role_id).first()
      if role:
        role_names.append(role.name)
    print(f"  User: {u.username} ({u.email}) - Roles: {', '.join(role_names) if role_names else 'NO ROLES'}")

  # Check admin specifically
  print("\n5. ADMIN DETAILED CHECK:")
  admin_user = db.query(User).filter(User.username == 'admin').first()
  if admin_user:
    print(f"  Admin User ID: {admin_user.id}")
    admin_roles = db.query(UserRole).filter(UserRole.user_id == admin_user.id).all()
    print(f"  Admin Roles: {[r.role_id for r in admin_roles]}")
    
    for ur in admin_roles:
      role = db.query(Role).filter(Role.id == ur.role_id).first()
      if role:
        print(f"\n  Role: {role.name}")
        role_perms = db.query(RolePermission).filter(RolePermission.role_id == role.id).all()
        print(f"  Total permissions in this role: {len(role_perms)}")
        
        # Check specifically for auth/users
        auth_users_perm = db.query(Permission).filter(Permission.app == 'identity', Permission.name == 'auth/users').first()
        if auth_users_perm:
          auth_users_rp = db.query(RolePermission).filter(RolePermission.role_id == role.id, RolePermission.permission_id == auth_users_perm.id).first()
          if auth_users_rp:
            print(f"  auth/users permission: Browse:{auth_users_rp.browse} Read:{auth_users_rp.read} Create:{auth_users_rp.create} Update:{auth_users_rp.update} Delete:{auth_users_rp.delete}")
          else:
            print(f"  auth/users permission: NOT ASSIGNED!")
        else:
          print(f"  auth/users permission: NOT FOUND IN PERMISSIONS TABLE!")
  else:
    print("  ADMIN USER NOT FOUND!")

  db.close()
  print("\n" + "=" * 80)

if __name__ == "__main__":
  debug()
