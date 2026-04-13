"""
Seeder: Items (Alat Foto)
Mengisi tabel rental.items dengan data perlengkapan fotografi yang siap disewa.
"""

from sqlalchemy.orm import Session
from app.master.items.models import Item


# Catatan: category_id merujuk ke data di item_categories_seeder.py
# 1 = Kamera | 2 = Lensa | 3 = Tripod & Stabilizer
# 4 = Lighting | 5 = Drone | 6 = Aksesori Kamera

ITEMS = [
  # ── KAMERA ─────────────────────────────────────────────
  {
    "code": "CAM-001",
    "category_id": 1,
    "name": "Sony Alpha A7 III",
    "brand": "Sony",
    "description": (
      "Kamera mirrorless full-frame 24.2MP dengan autofokus fase hybrid 693 titik. "
      "Cocok untuk fotografi portrait, landscape, dan videografi 4K."
    ),
    "condition": "baik",
    "stock_total": 3,
    "stock_available": 3,
    "price_per_day": 350_000,
    "deposit_amount": 1_500_000,
    "is_active": True,
  },
  {
    "code": "CAM-002",
    "category_id": 1,
    "name": "Canon EOS R6 Mark II",
    "brand": "Canon",
    "description": (
      "Kamera mirrorless full-frame 24.2MP dengan IBIS 8-stop dan video 4K 60fps. "
      "Sangat andal untuk event photography dan videografi dinamis."
    ),
    "condition": "baik",
    "stock_total": 2,
    "stock_available": 2,
    "price_per_day": 375_000,
    "deposit_amount": 1_500_000,
    "is_active": True,
  },
  {
    "code": "CAM-003",
    "category_id": 1,
    "name": "Nikon Z6 II",
    "brand": "Nikon",
    "description": (
      "Kamera mirrorless full-frame 24.5MP, dual card slot, dan autofokus low-light -4.5EV. "
      "Pilihan solid untuk street photography dan low-light shooting."
    ),
    "condition": "baik",
    "stock_total": 2,
    "stock_available": 2,
    "price_per_day": 325_000,
    "deposit_amount": 1_500_000,
    "is_active": True,
  },
  {
    "code": "CAM-004",
    "category_id": 1,
    "name": "Fujifilm X-T5",
    "brand": "Fujifilm",
    "description": (
      "Kamera mirrorless APS-C 40.2MP dengan film simulation khas Fujifilm. "
      "Bobot ringan, ideal untuk foto travel dan street."
    ),
    "condition": "baik",
    "stock_total": 2,
    "stock_available": 2,
    "price_per_day": 300_000,
    "deposit_amount": 1_200_000,
    "is_active": True,
  },
  {
    "code": "CAM-005",
    "category_id": 1,
    "name": "GoPro Hero 12 Black",
    "brand": "GoPro",
    "description": (
      "Action camera 5.3K waterproof dengan HyperSmooth 6.0 stabilization. "
      "Sempurna untuk aktivitas outdoor, olahraga, dan vlogging."
    ),
    "condition": "baik",
    "stock_total": 5,
    "stock_available": 5,
    "price_per_day": 150_000,
    "deposit_amount": 500_000,
    "is_active": True,
  },

  # ── LENSA ──────────────────────────────────────────────
  {
    "code": "LNS-001",
    "category_id": 2,
    "name": "Sony FE 85mm f/1.4 GM",
    "brand": "Sony",
    "description": (
      "Lensa portrait prime 85mm dengan aperture f/1.4. "
      "Bokeh creamy nan indah, ideal untuk foto wedding dan portrait profesional."
    ),
    "condition": "baik",
    "stock_total": 2,
    "stock_available": 2,
    "price_per_day": 200_000,
    "deposit_amount": 2_000_000,
    "is_active": True,
  },
  {
    "code": "LNS-002",
    "category_id": 2,
    "name": "Sony FE 16-35mm f/2.8 GM",
    "brand": "Sony",
    "description": (
      "Lensa wide-angle zoom 16-35mm f/2.8 dengan kualitas G Master. "
      "Terbaik untuk landscape, arsitektur, dan interior."
    ),
    "condition": "baik",
    "stock_total": 2,
    "stock_available": 2,
    "price_per_day": 225_000,
    "deposit_amount": 2_500_000,
    "is_active": True,
  },
  {
    "code": "LNS-003",
    "category_id": 2,
    "name": "Canon RF 50mm f/1.2L USM",
    "brand": "Canon",
    "description": (
      "Lensa prime 50mm f/1.2 dengan autofokus cepat dan tajam. "
      "Serbaguna untuk portrait, street, dan foto sehari-hari."
    ),
    "condition": "baik",
    "stock_total": 2,
    "stock_available": 2,
    "price_per_day": 200_000,
    "deposit_amount": 2_000_000,
    "is_active": True,
  },
  {
    "code": "LNS-004",
    "category_id": 2,
    "name": "Tamron 70-200mm f/2.8 Di III VXD",
    "brand": "Tamron",
    "description": (
      "Lensa telefoto zoom 70-200mm f/2.8 untuk Sony E-mount. "
      "Sempurna untuk olahraga, satwa liar, dan event photography."
    ),
    "condition": "baik",
    "stock_total": 2,
    "stock_available": 2,
    "price_per_day": 175_000,
    "deposit_amount": 1_800_000,
    "is_active": True,
  },
  {
    "code": "LNS-005",
    "category_id": 2,
    "name": "Laowa 15mm f/2 Zero-D",
    "brand": "Laowa",
    "description": (
      "Lensa ultra wide-angle 15mm dengan distorsi nol. "
      "Ideal untuk astrofotografi, interior, dan landscape dramatis."
    ),
    "condition": "baik",
    "stock_total": 1,
    "stock_available": 1,
    "price_per_day": 150_000,
    "deposit_amount": 1_500_000,
    "is_active": True,
  },

  # ── TRIPOD & STABILIZER ────────────────────────────────
  {
    "code": "TRP-001",
    "category_id": 3,
    "name": "Joby GorillaPod 5K",
    "brand": "Joby",
    "description": (
      "Tripod fleksibel dengan kaki yang bisa dilekukkan untuk berbagai permukaan. "
      "Kapasitas hingga 5kg, cocok untuk kamera mirrorless dan aksesoris."
    ),
    "condition": "baik",
    "stock_total": 4,
    "stock_available": 4,
    "price_per_day": 50_000,
    "deposit_amount": 200_000,
    "is_active": True,
  },
  {
    "code": "TRP-002",
    "category_id": 3,
    "name": "Benro Mach3 Carbon Fiber TMA38CL",
    "brand": "Benro",
    "description": (
      "Tripod carbon fiber ringan dengan ball head presisi tinggi. "
      "Tinggi maksimum 185cm, kapasitas 18kg, sangat stabil untuk long exposure."
    ),
    "condition": "baik",
    "stock_total": 3,
    "stock_available": 3,
    "price_per_day": 75_000,
    "deposit_amount": 500_000,
    "is_active": True,
  },
  {
    "code": "TRP-003",
    "category_id": 3,
    "name": "DJI RS 3 Pro Gimbal",
    "brand": "DJI",
    "description": (
      "Gimbal 3-axis untuk kamera mirrorless/DSLR hingga 4.5kg. "
      "Fitur Force Mobile, OLED display, dan native vertical shooting."
    ),
    "condition": "baik",
    "stock_total": 2,
    "stock_available": 2,
    "price_per_day": 175_000,
    "deposit_amount": 800_000,
    "is_active": True,
  },
  {
    "code": "TRP-004",
    "category_id": 3,
    "name": "Zhiyun Smooth 5S Gimbal",
    "brand": "Zhiyun",
    "description": (
      "Gimbal smartphone 3-axis dengan motor brushless terkuat di kelasnya. "
      "Kompatibel dengan iOS & Android, cocok untuk vlog dan konten kreator."
    ),
    "condition": "baik",
    "stock_total": 3,
    "stock_available": 3,
    "price_per_day": 100_000,
    "deposit_amount": 400_000,
    "is_active": True,
  },

  # ── LIGHTING ───────────────────────────────────────────
  {
    "code": "LGT-001",
    "category_id": 4,
    "name": "Godox AD200Pro Flash Strobe",
    "brand": "Godox",
    "description": (
      "Flash strobe portabel 200Ws dengan TTL dan HSS 1/8000s. "
      "Dilengkapi dua flash head (bulb & bare), baterai isi ulang."
    ),
    "condition": "baik",
    "stock_total": 4,
    "stock_available": 4,
    "price_per_day": 100_000,
    "deposit_amount": 600_000,
    "is_active": True,
  },
  {
    "code": "LGT-002",
    "category_id": 4,
    "name": "Godox SL-60W LED Video Light",
    "brand": "Godox",
    "description": (
      "LED video light 60W dengan suhu warna 5600K dan CRI>95. "
      "Dilengkapi softbox 60x60cm, cocok untuk studio home dan YouTube."
    ),
    "condition": "baik",
    "stock_total": 4,
    "stock_available": 4,
    "price_per_day": 75_000,
    "deposit_amount": 400_000,
    "is_active": True,
  },
  {
    "code": "LGT-003",
    "category_id": 4,
    "name": "Profoto B10X Plus Flash",
    "brand": "Profoto",
    "description": (
      "Off-camera flash 500Ws dengan TTL dan HSS, baterai lithium built-in. "
      "Solusi lighting profesional paling ringkas di kelasnya."
    ),
    "condition": "baik",
    "stock_total": 2,
    "stock_available": 2,
    "price_per_day": 250_000,
    "deposit_amount": 2_000_000,
    "is_active": True,
  },
  {
    "code": "LGT-004",
    "category_id": 4,
    "name": "Aputure 300D Mark II LED",
    "brand": "Aputure",
    "description": (
      "LED daylight 300W dengan Bowens mount dan kontrol wireless. "
      "Standar industri untuk set film, TVC, dan pemotretan fashion."
    ),
    "condition": "baik",
    "stock_total": 2,
    "stock_available": 2,
    "price_per_day": 200_000,
    "deposit_amount": 1_500_000,
    "is_active": True,
  },

  # ── DRONE ──────────────────────────────────────────────
  {
    "code": "DRN-001",
    "category_id": 5,
    "name": "DJI Mini 4 Pro",
    "brand": "DJI",
    "description": (
      "Drone 4K HDR ultra-ringan (<249g) dengan omnidirectional obstacle sensing. "
      "Tidak perlu SIM drone, cocok untuk pemula hingga kreator konten."
    ),
    "condition": "baik",
    "stock_total": 2,
    "stock_available": 2,
    "price_per_day": 400_000,
    "deposit_amount": 3_000_000,
    "is_active": True,
  },
  {
    "code": "DRN-002",
    "category_id": 5,
    "name": "DJI Air 3",
    "brand": "DJI",
    "description": (
      "Drone dual-camera (wide + 3x telefoto) dengan video 4K/60fps. "
      "Waktu terbang 46 menit, ideal untuk sinematik dan foto aerial profesional."
    ),
    "condition": "baik",
    "stock_total": 1,
    "stock_available": 1,
    "price_per_day": 550_000,
    "deposit_amount": 4_000_000,
    "is_active": True,
  },

  # ── AKSESORI KAMERA ────────────────────────────────────
  {
    "code": "ACC-001",
    "category_id": 6,
    "name": "Filter Variable ND 2-400 (77mm)",
    "brand": "K&F Concept",
    "description": (
      "Filter ND variabel 2-400 stop diameter 77mm dengan lapisan nano anti-refleksi. "
      "Wajib untuk foto long exposure dan video di kondisi terang."
    ),
    "condition": "baik",
    "stock_total": 5,
    "stock_available": 5,
    "price_per_day": 35_000,
    "deposit_amount": 150_000,
    "is_active": True,
  },
  {
    "code": "ACC-002",
    "category_id": 6,
    "name": "Sony NP-FZ100 Battery + Charger",
    "brand": "Sony",
    "description": (
      "Baterai original Sony NP-FZ100 kapasitas 2280mAh kompatibel dengan A7 III, A7R IV, A9 II. "
      "Termasuk charger BC-QZ1."
    ),
    "condition": "baik",
    "stock_total": 8,
    "stock_available": 8,
    "price_per_day": 25_000,
    "deposit_amount": 100_000,
    "is_active": True,
  },
  {
    "code": "ACC-003",
    "category_id": 6,
    "name": "SanDisk Extreme Pro 256GB V90",
    "brand": "SanDisk",
    "description": (
      "Memory card CFexpress Type A / SD 256GB dengan kecepatan tulis 800MB/s. "
      "Mendukung rekaman video RAW 4K dan burst shooting cepat."
    ),
    "condition": "baik",
    "stock_total": 10,
    "stock_available": 10,
    "price_per_day": 20_000,
    "deposit_amount": 75_000,
    "is_active": True,
  },
  {
    "code": "ACC-004",
    "category_id": 6,
    "name": "Tas Kamera Lowepro ProTactic 450 AW II",
    "brand": "Lowepro",
    "description": (
      "Tas ransel kamera modular kapasitas besar, kompatibel untuk 2 body + 6 lensa. "
      "Raincover bawaan, padding tebal, akses samping cepat."
    ),
    "condition": "baik",
    "stock_total": 4,
    "stock_available": 4,
    "price_per_day": 40_000,
    "deposit_amount": 200_000,
    "is_active": True,
  },
]


def run(db: Session):
  print("  [Items] Seeding alat foto rental...")

  for item_data in ITEMS:
    existing = db.query(Item).filter(Item.code == item_data["code"]).first()
    if existing:
      print(f"    - Item '{item_data['code']} - {item_data['name']}' sudah ada, dilewati.")
      continue

    item = Item(
      code=item_data["code"],
      category_id=item_data["category_id"],
      name=item_data["name"],
      brand=item_data.get("brand"),
      description=item_data.get("description"),
      condition=item_data.get("condition", "baik"),
      stock_total=item_data.get("stock_total", 1),
      stock_available=item_data.get("stock_available", 1),
      price_per_day=item_data["price_per_day"],
      deposit_amount=item_data.get("deposit_amount", 0),
      is_active=item_data.get("is_active", True),
      images=None,
      created_by="seeder",
    )
    db.add(item)
    print(f"    + Item '{item_data['code']} - {item_data['name']}' ditambahkan.")

  db.commit()
  print("  [Items] Selesai.\n")
