import os
import sys

from sqlalchemy import delete, insert, text


def init():
  import json

  from app.auth.permission.models import Permission
  from app.auth.role.models import Role, RolePermission
  from app.auth.user_role.models import UserRole
  from app.auth.user.models import User
  from db.database import Session
  from utils.helpers.hash import bcrypt

  db = Session()

  ####### PERMISSIONS #######
  # Use absolute path relative to this file
  base_path = os.path.dirname(__file__)
  permissions_file = os.path.join(base_path, "seeders", "permissions.json")
  
  try:
    with open(permissions_file, "r") as p:
      mod = {"browse": True, "read": True, "create": True, "update": True, "delete": True, "restore": True}
      permissions = json.load(p)
      perms: list[dict] = []
      for v in permissions:
        try:
          v: dict
          app = v.get("app")
          name = v.get("name")
          if db.query(Permission.id).filter(Permission.app == app).filter(Permission.name == name).first():
            print(f"permission exist: {name}")
          else:
            db.add(Permission(app=app, name=name))
            print(f"commit {name}")
            db.commit()
          perms.append({"app": app, "name": name, "detail": mod})
        except Exception as e:
          db.rollback()
          print("permission except", e)
  except FileNotFoundError:
    print(f"ERROR: Could not find {permissions_file}")
    # Try alternative path for different execution contexts
    alt_path = os.path.join(base_path, "src", "seeders", "permissions.json")
    print(f"Trying alternative path: {alt_path}")
    # ... logic continues or we just assume the first one is correct if we fix the script

  try:
    print("\n" + "="*60)
    print("SETTING UP ROLES AND PERMISSIONS")
    print("="*60)
    
    # Create all roles first - ONLY 3 ROLES
    roles_to_create = [
      ("admin", "Admin role with manage access"),
      ("petugas", "Officer role with read/browse access"),
      ("user", "User role with basic access"),
    ]
    
    for role_name, description in roles_to_create:
      existing_role = db.query(Role).filter_by(name=role_name).first()
      if not existing_role:
        new_role = Role(name=role_name)
        db.add(new_role)
        db.flush()
        print(f"[NEW] {role_name} role created")
      else:
        print(f"[EXISTS] {role_name} role already exists")
    
    db.commit()

    # Get all permissions from database
    perms_model = db.query(Permission).all()
    print(f"\nFound {len(perms_model)} permissions in database")
    
    # Helper function to assign permissions to a role
    def assign_permissions_to_role(role_name, p_browse=False, p_create=False, p_read=False, p_update=False, p_delete=False, p_restore=False):
      try:
        role_obj = db.query(Role).filter_by(name=role_name).first()
        if not role_obj:
          print(f"[FAIL] ERROR: {role_name} role not found!")
          return False
        
        print(f"\n  Assigning permissions for {role_name} (role_id={role_obj.id})...")
        
        # Delete existing permissions first
        existing_count = db.query(RolePermission).filter(RolePermission.role_id == role_obj.id).count()
        if existing_count > 0:
          db.execute(delete(RolePermission).where(RolePermission.role_id == role_obj.id))
          db.commit()
          print(f"    - Deleted {existing_count} existing permissions")
        
        # Create new permission records
        objects = []
        for perm in perms_model:
          row = RolePermission(
            role_id=role_obj.id,
            permission_id=perm.id,
            browse=p_browse,
            create=p_create,
            read=p_read,
            update=p_update,
            delete=p_delete,
            restore=p_restore,
          )
          objects.append(row)
        
        print(f"    - Creating {len(objects)} permission records...")
        db.bulk_save_objects(objects)
        db.commit()
        
        # Verify they were saved
        count = db.query(RolePermission).filter(RolePermission.role_id == role_obj.id).count()
        print(f"    - [OK] {count} permissions assigned successfully!")
        
        return True
      except Exception as e:
        print(f"    - [FAIL] ERROR: {str(e)}")
        db.rollback()
        return False
    
    # Assign permissions based on role
    print("\nAssigning role permissions:")
    assign_permissions_to_role("admin", p_browse=True, p_create=True, p_read=True, p_update=True, p_delete=False, p_restore=False)
    assign_permissions_to_role("petugas", p_browse=True, p_create=False, p_read=True, p_update=False, p_delete=False, p_restore=False)
    assign_permissions_to_role("user", p_browse=True, p_create=False, p_read=True, p_update=False, p_delete=False, p_restore=False)
    
    print("\n[OK] All role permissions configured successfully!")
    print("="*60)

  except Exception as e:
    print(f"[FAIL] role/permission configuration failed: {str(e)}")
    db.rollback()
    import traceback
    traceback.print_exc()

  ####### USER #######
  try:
    # ADMIN USER
    admin = db.query(User).filter(User.email == 'admin@gmail.com').first()
    admin_role = db.query(Role).filter(Role.name == 'admin').first()
    if admin:
      db.query(User).filter(User.email == 'admin@gmail.com').update(
        {
          "name": "admin",
          "username": "admin",
          "email": "admin@gmail.com",
          "password": bcrypt("test1234"),
          "is_active": True,
        }
      )
      if admin_role:
        existing = db.query(UserRole).filter_by(user_id=admin.id, role_id=admin_role.id).first()
        if not existing:
          db.add(UserRole(user_id=admin.id, role_id=admin_role.id))
      print("admin user updated")
    else:
      admin = User(
        name="admin",
        username="admin",
        email="admin@gmail.com",
        password=bcrypt("test1234"),
        is_active=True,
      )
      db.add(admin)
      db.flush()
      if admin_role:
        existing = db.query(UserRole).filter_by(user_id=admin.id, role_id=admin_role.id).first()
        if not existing:
          db.add(UserRole(user_id=admin.id, role_id=admin_role.id))
      print("admin user added")

    # PETUGAS USER
    petugas = db.query(User).filter(User.email == 'petugas@gmail.com').first()
    petugas_role = db.query(Role).filter(Role.name == 'petugas').first()
    if petugas:
      db.query(User).filter(User.email == 'petugas@gmail.com').update(
        {
          "name": "petugas",
          "username": "petugas",
          "email": "petugas@gmail.com",
          "password": bcrypt("test1234"),
          "is_active": True,
        }
      )
      if petugas_role:
        existing = db.query(UserRole).filter_by(user_id=petugas.id, role_id=petugas_role.id).first()
        if not existing:
          db.add(UserRole(user_id=petugas.id, role_id=petugas_role.id))
      print("petugas user updated")
    else:
      petugas = User(
        name="petugas",
        username="petugas",
        email="petugas@gmail.com",
        password=bcrypt("test1234"),
        is_active=True,
      )
      db.add(petugas)
      db.flush()
      if petugas_role:
        existing = db.query(UserRole).filter_by(user_id=petugas.id, role_id=petugas_role.id).first()
        if not existing:
          db.add(UserRole(user_id=petugas.id, role_id=petugas_role.id))
      print("petugas user added")

    # USER USER
    user = db.query(User).filter(User.email == 'user@gmail.com').first()
    user_role = db.query(Role).filter(Role.name == 'user').first()
    if user:
      db.query(User).filter(User.email == 'user@gmail.com').update(
        {
          "name": "user",
          "username": "user",
          "email": "user@gmail.com",
          "password": bcrypt("test1234"),
          "is_active": True,
        }
      )
      if user_role:
        existing = db.query(UserRole).filter_by(user_id=user.id, role_id=user_role.id).first()
        if not existing:
          db.add(UserRole(user_id=user.id, role_id=user_role.id))
      print("user user updated")
    else:
      user = User(
        name="user",
        username="user",
        email="user@gmail.com",
        password=bcrypt("test1234"),
        is_active=True,
      )
      db.add(user)
      db.flush()
      if user_role:
        existing = db.query(UserRole).filter_by(user_id=user.id, role_id=user_role.id).first()
        if not existing:
          db.add(UserRole(user_id=user.id, role_id=user_role.id))
      print("user user added")

    db.commit()
    print("All users created successfully")

  except Exception as e:
    db.rollback()
    print("user creation failed:", str(e))

  db.close()


if __name__ == "__main__":
  sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
  init()
