"""
Seeder: Item Categories (Alat Foto)
Mengisi tabel rental.item_categories dengan kategori perlengkapan fotografi.
"""

from sqlalchemy.orm import Session
from app.master.item_categories.models import ItemCategory


CATEGORIES = [
  {
    "id": 1,
    "name": "Kamera",
    "description": "Body kamera digital, mirrorless, dan DSLR untuk keperluan fotografi dan videografi.",
    "is_active": True,
  },
  {
    "id": 2,
    "name": "Lensa",
    "description": "Berbagai jenis lensa kamera mulai dari lensa wide, standard, telefoto, hingga macro.",
    "is_active": True,
  },
  {
    "id": 3,
    "name": "Tripod & Stabilizer",
    "description": "Tripod, monopod, gimbal, dan stabilizer untuk hasil foto/video yang stabil.",
    "is_active": True,
  },
  {
    "id": 4,
    "name": "Lighting",
    "description": "Peralatan pencahayaan seperti flash eksternal, softbox, LED panel, dan reflektor.",
    "is_active": True,
  },
  {
    "id": 5,
    "name": "Drone",
    "description": "Drone kamera untuk aerial photography dan videografi.",
    "is_active": True,
  },
  {
    "id": 6,
    "name": "Aksesori Kamera",
    "description": "Perlengkapan tambahan seperti filter, battery grip, memory card, dan tas kamera.",
    "is_active": True,
  },
]


def run(db: Session):
  print("  [ItemCategories] Seeding kategori alat foto...")

  for cat_data in CATEGORIES:
    existing = db.query(ItemCategory).filter(ItemCategory.id == cat_data["id"]).first()
    if existing:
      print(f"    - Kategori ID {cat_data['id']} '{cat_data['name']}' sudah ada, dilewati.")
      continue

    category = ItemCategory(
      id=cat_data["id"],
      name=cat_data["name"],
      description=cat_data["description"],
      is_active=cat_data["is_active"],
      created_by="seeder",
    )
    db.add(category)
    print(f"    + Kategori '{cat_data['name']}' ditambahkan.")

  db.commit()
  print("  [ItemCategories] Selesai.\n")
