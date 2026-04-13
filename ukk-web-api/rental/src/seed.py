import os
import sys

# Pastikan direktori src ada di path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from db.database import Session
from seeders import item_categories_seeder, items_seeder


def init():
  print("=" * 50)
  print("  RENTAL SEEDER - Alat Foto")
  print("=" * 50)

  db = Session()
  try:
    # 1. Seed kategori dahulu (karena items butuh category_id)
    item_categories_seeder.run(db)

    # 2. Seed item alat foto
    items_seeder.run(db)

    print("=" * 50)
    print("  Seeding selesai!")
    print("=" * 50)

  except Exception as e:
    db.rollback()
    print(f"\n[ERROR] Seeding gagal: {e}")
    raise
  finally:
    db.close()


if __name__ == "__main__":
  init()
