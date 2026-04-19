"""
Seeder: Transactions — Rentals, Payments, Reviews
Membuat data rental yang saling berkaitan:
  - Rental (dengan item)
  - Payment (jenis: pembayaran, denda, refund_deposit)
  - Review (ulasan dari customer)

CATATAN: User ID 1 dan 2 dikecualikan dari customer
         (biasanya adalah akun admin/petugas).
"""

import uuid
import random
import datetime
from sqlalchemy.orm import Session

from app.transaction.rentals.models import Rental
from app.transaction.rental_items.models import RentalItem
from app.transaction.payments.models import Payment
from app.transaction.reviews.models import Review
from app.master.items.models import Item
from app.auth.user.models import User


# ─── Komentar ulasan realistis ────────────────────────────────────────────────
COMMENTS = [
    "Kamera dalam kondisi sangat baik, autofokus responsif. Puas banget!",
    "Perlengkapan lengkap dan bersih. Proses penyewaan juga cepat dan mudah.",
    "Kualitas lensa sangat tajam, hasilnya memuaskan untuk foto wedding.",
    "Drone dalam kondisi prima, baterai tahan lama. Sangat direkomendasikan!",
    "Alat foto yang disewa sesuai deskripsi. Pelayanan admin ramah dan cepat.",
    "Gimbal bekerja sempurna sepanjang acara. Pasti balik lagi sewa di sini.",
    "Flash strobe powernya oke untuk studio mini. Terima kasih, sangat membantu.",
    "Memory card kencang banget, tidak ada frame drop saat rekam 4K. Mantap!",
    "Tripod kokoh dan ringan, enak dibawa hiking. Recommended!",
    "Lighting bagus, CRI tinggi, warna foto natural. Pelayanan top markotop.",
    "Lumayan oke, tapi waktu pickup antre sedikit lama.",
    "Kamera sedikit lecet di bagian body tapi fungsi normal. Overall memuaskan.",
    "Harga sewa bersaing, kualitas tidak mengecewakan. Akan kembali lagi.",
    "Drone sangat stabil di udara, footage halus sekali!",
    "Filter ND sangat membantu buat foto long exposure di siang hari.",
    "Kondisi alat seperti baru, pengemasan rapi dan aman.",
    "Proses pengembalian mudah, deposit dikembalikan cepat. Thumbs up!",
    "Sangat puas, alat kamera lengkap dan terawat dengan baik.",
    "Baterai ekstra yang disertakan sangat berguna untuk pemotretan seharian.",
    "Lensa dalam kondisi mulus, tidak ada jamur atau debu. Hasil foto tajam!",
]

FINE_NOTES = [
    "Denda keterlambatan pengembalian 1 hari",
    "Denda keterlambatan pengembalian 2 hari",
    "Denda kerusakan ringan pada body kamera (goresan kecil)",
    "Denda kerusakan lensa (goresan pada elemen optik)",
    "Denda hilangnya tutup lensa",
    "Denda cacat pada gimbal (salah satu arm bengkok)",
    "Denda kotoran berlebih pada sensor kamera",
]

REFUND_NOTES = [
    "Refund deposit setelah alat dikembalikan dalam kondisi baik",
    "Refund deposit — alat dikembalikan tepat waktu dan mulus",
    "Pengembalian deposit penuh sesuai perjanjian sewa",
]


def make_uuid() -> str:
    return str(uuid.uuid4())


def days_ago(n: int) -> datetime.date:
    return datetime.date.today() - datetime.timedelta(days=n)


def dt_ago(days: int, hours: int = 0) -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days, hours=hours)


# ─── Definisi Skenario ────────────────────────────────────────────────────────
# Setiap dict = 1 rental dengan pembayaran & ulasan yang berkaitan.
# start_offset  : berapa hari lalu rental ini dimulai
# duration      : durasi sewa (hari)
# item_count    : jumlah jenis item yang disewa
# status        : status rental akhir
# payment_method: transfer | cod
# payments      : list definisi pembayaran
# has_review    : apakah ada ulasan
# rating        : bintang ulasan (1-5)

SCENARIOS = [
    # 1 ─ Selesai, transfer, ulasan bintang 5
    {
        "rental_code": "RNT10001",
        "start_offset": 30, "duration": 3, "item_count": 2,
        "payment_method": "transfer", "status": "selesai",
        "payments": [
            {"type": "pembayaran", "status": "terverifikasi", "paid_offset_days": 29},
        ],
        "has_review": True, "rating": 5,
    },
    # 2 ─ Selesai, denda keterlambatan, ulasan bintang 4
    {
        "rental_code": "RNT10002",
        "start_offset": 20, "duration": 2, "item_count": 1,
        "payment_method": "transfer", "status": "selesai",
        "payments": [
            {"type": "pembayaran", "status": "terverifikasi", "paid_offset_days": 19},
            {"type": "denda",      "status": "terverifikasi", "paid_offset_days": 17,
             "amount_override": 150_000, "notes": FINE_NOTES[0]},
        ],
        "has_review": True, "rating": 4,
    },
    # 3 ─ Aktif sekarang, COD, belum ada ulasan
    {
        "rental_code": "RNT10003",
        "start_offset": 2, "duration": 5, "item_count": 1,
        "payment_method": "cod", "status": "aktif",
        "payments": [
            {"type": "pembayaran", "status": "terverifikasi", "paid_offset_days": 2},
        ],
        "has_review": False,
    },
    # 4 ─ Menunggu verifikasi pembayaran
    {
        "rental_code": "RNT10004",
        "start_offset": 1, "duration": 3, "item_count": 1,
        "payment_method": "transfer", "status": "menunggu_verif",
        "payments": [
            {"type": "pembayaran", "status": "menunggu", "paid_offset_days": 0},
        ],
        "has_review": False,
    },
    # 5 ─ Selesai, refund deposit, ulasan bintang 5
    {
        "rental_code": "RNT10005",
        "start_offset": 45, "duration": 4, "item_count": 2,
        "payment_method": "transfer", "status": "selesai",
        "payments": [
            {"type": "pembayaran",     "status": "terverifikasi", "paid_offset_days": 44},
            {"type": "refund_deposit", "status": "terverifikasi", "paid_offset_days": 40,
             "notes": REFUND_NOTES[0]},
        ],
        "has_review": True, "rating": 5,
    },
    # 6 ─ Selesai, denda kerusakan, ulasan bintang 3
    {
        "rental_code": "RNT10006",
        "start_offset": 60, "duration": 2, "item_count": 1,
        "payment_method": "transfer", "status": "selesai",
        "payments": [
            {"type": "pembayaran", "status": "terverifikasi", "paid_offset_days": 59},
            {"type": "denda",      "status": "terverifikasi", "paid_offset_days": 56,
             "amount_override": 300_000, "notes": FINE_NOTES[3]},
        ],
        "has_review": True, "rating": 3,
    },
    # 7 ─ Dibatalkan
    {
        "rental_code": "RNT10007",
        "start_offset": 10, "duration": 1, "item_count": 1,
        "payment_method": "cod", "status": "dibatalkan",
        "payments": [],
        "has_review": False,
    },
    # 8 ─ Menunggu bayar (baru dibuat)
    {
        "rental_code": "RNT10008",
        "start_offset": 0, "duration": 2, "item_count": 1,
        "payment_method": "transfer", "status": "menunggu_bayar",
        "payments": [],
        "has_review": False,
    },
    # 9 ─ Selesai, COD, ulasan bintang 4
    {
        "rental_code": "RNT10009",
        "start_offset": 15, "duration": 2, "item_count": 2,
        "payment_method": "cod", "status": "selesai",
        "payments": [
            {"type": "pembayaran", "status": "terverifikasi", "paid_offset_days": 14},
        ],
        "has_review": True, "rating": 4,
    },
    # 10 ─ Selesai, denda + refund deposit, ulasan bintang 4
    {
        "rental_code": "RNT10010",
        "start_offset": 75, "duration": 3, "item_count": 2,
        "payment_method": "transfer", "status": "selesai",
        "payments": [
            {"type": "pembayaran",     "status": "terverifikasi", "paid_offset_days": 74},
            {"type": "denda",          "status": "terverifikasi", "paid_offset_days": 70,
             "amount_override": 200_000, "notes": FINE_NOTES[2]},
            {"type": "refund_deposit", "status": "terverifikasi", "paid_offset_days": 69,
             "notes": REFUND_NOTES[1]},
        ],
        "has_review": True, "rating": 4,
    },
    # 11 ─ Diproses (sedang disiapkan staf)
    {
        "rental_code": "RNT10011",
        "start_offset": 0, "duration": 3, "item_count": 1,
        "payment_method": "transfer", "status": "diproses",
        "payments": [
            {"type": "pembayaran", "status": "terverifikasi", "paid_offset_days": 1},
        ],
        "has_review": False,
    },
    # 12 ─ Selesai, ulasan bintang 5 tanpa denda
    {
        "rental_code": "RNT10012",
        "start_offset": 90, "duration": 5, "item_count": 3,
        "payment_method": "transfer", "status": "selesai",
        "payments": [
            {"type": "pembayaran",     "status": "terverifikasi", "paid_offset_days": 89},
            {"type": "refund_deposit", "status": "terverifikasi", "paid_offset_days": 83,
             "notes": REFUND_NOTES[2]},
        ],
        "has_review": True, "rating": 5,
    },
    # 13 ─ Selesai, terlambat 2 hari, ulasan bintang 2
    {
        "rental_code": "RNT10013",
        "start_offset": 50, "duration": 2, "item_count": 1,
        "payment_method": "cod", "status": "selesai",
        "payments": [
            {"type": "pembayaran", "status": "terverifikasi", "paid_offset_days": 48},
            {"type": "denda",      "status": "terverifikasi", "paid_offset_days": 46,
             "amount_override": 250_000, "notes": FINE_NOTES[1]},
        ],
        "has_review": True, "rating": 2,
    },
    # 14 ─ Aktif, transfer, 3 item
    {
        "rental_code": "RNT10014",
        "start_offset": 1, "duration": 7, "item_count": 3,
        "payment_method": "transfer", "status": "aktif",
        "payments": [
            {"type": "pembayaran", "status": "terverifikasi", "paid_offset_days": 1},
        ],
        "has_review": False,
    },
    # 15 ─ Selesai, bintang 5, refund deposit
    {
        "rental_code": "RNT10015",
        "start_offset": 40, "duration": 3, "item_count": 1,
        "payment_method": "transfer", "status": "selesai",
        "payments": [
            {"type": "pembayaran",     "status": "terverifikasi", "paid_offset_days": 39},
            {"type": "refund_deposit", "status": "terverifikasi", "paid_offset_days": 35,
             "notes": REFUND_NOTES[0]},
        ],
        "has_review": True, "rating": 5,
    },
    # 16 ─ Menunggu bayar, COD
    {
        "rental_code": "RNT10016",
        "start_offset": 0, "duration": 1, "item_count": 1,
        "payment_method": "cod", "status": "menunggu_bayar",
        "payments": [],
        "has_review": False,
    },
    # 17 ─ Selesai, denda + bintang 3
    {
        "rental_code": "RNT10017",
        "start_offset": 110, "duration": 4, "item_count": 2,
        "payment_method": "transfer", "status": "selesai",
        "payments": [
            {"type": "pembayaran", "status": "terverifikasi", "paid_offset_days": 109},
            {"type": "denda",      "status": "terverifikasi", "paid_offset_days": 105,
             "amount_override": 175_000, "notes": FINE_NOTES[4]},
        ],
        "has_review": True, "rating": 3,
    },
    # 18 ─ Selesai, bintang 4, COD
    {
        "rental_code": "RNT10018",
        "start_offset": 65, "duration": 2, "item_count": 2,
        "payment_method": "cod", "status": "selesai",
        "payments": [
            {"type": "pembayaran", "status": "terverifikasi", "paid_offset_days": 63},
        ],
        "has_review": True, "rating": 4,
    },
    # 19 ─ Menunggu verif, transfer
    {
        "rental_code": "RNT10019",
        "start_offset": 0, "duration": 3, "item_count": 1,
        "payment_method": "transfer", "status": "menunggu_verif",
        "payments": [
            {"type": "pembayaran", "status": "menunggu", "paid_offset_days": 0},
        ],
        "has_review": False,
    },
    # 20 ─ Selesai, bintang 5, 3 items, refund
    {
        "rental_code": "RNT10020",
        "start_offset": 120, "duration": 6, "item_count": 3,
        "payment_method": "transfer", "status": "selesai",
        "payments": [
            {"type": "pembayaran",     "status": "terverifikasi", "paid_offset_days": 119},
            {"type": "refund_deposit", "status": "terverifikasi", "paid_offset_days": 112,
             "notes": REFUND_NOTES[2]},
        ],
        "has_review": True, "rating": 5,
    },
]


def run(db: Session):
    print("  [Transactions] Seeding rentals, payments & reviews...")

    # ── Ambil data pengguna (EXCLUDE id 1 dan 2 = admin/petugas) ───────────
    all_users = db.query(User).filter(
        User.deleted_at.is_(None),
        User.is_active == True,
        User.id.notin_([1, 2])
    ).all()

    # Petugas: ambil user id 1 atau 2 untuk verifikasi pembayaran
    petugas = db.query(User).filter(User.id.in_([1, 2])).first()
    if not petugas:
        # Fallback: gunakan user pertama yang ada
        petugas = db.query(User).filter(User.deleted_at.is_(None)).first()

    items = db.query(Item).filter(Item.deleted_at.is_(None), Item.is_active == True).all()

    if not all_users:
        print("    [SKIP] Tidak ada user (selain id 1 & 2) di database. Daftarkan user customer terlebih dahulu.")
        return

    if not items:
        print("    [SKIP] Tidak ada item di database. Jalankan items_seeder terlebih dahulu.")
        return

    created_count = 0

    for idx, scenario in enumerate(SCENARIOS):
        # Rotasi customer dari daftar user (bukan admin)
        customer = all_users[idx % len(all_users)]

        rental_code = scenario["rental_code"]

        # Cek duplikat
        existing = db.query(Rental).filter(Rental.rental_code == rental_code).first()
        if existing:
            print(f"    - Rental '{rental_code}' sudah ada, dilewati.")
            continue

        # Pilih item secara acak
        item_count  = scenario["item_count"]
        chosen_items = random.sample(items, min(item_count, len(items)))

        start_date = days_ago(scenario["start_offset"])
        duration   = scenario["duration"]
        end_date   = start_date + datetime.timedelta(days=duration - 1)

        subtotal      = sum(i.price_per_day * duration for i in chosen_items)
        deposit_total = sum((i.deposit_amount or 0) for i in chosen_items)
        grand_total   = subtotal + deposit_total

        rental_id = make_uuid()

        # ── Rental ────────────────────────────────────────────────────────
        rental = Rental(
            id=rental_id,
            rental_code=rental_code,
            customer_id=customer.id,
            petugas_id=petugas.id if petugas else None,
            start_date=start_date,
            end_date=end_date,
            duration_days=duration,
            subtotal=subtotal,
            deposit_total=deposit_total,
            grand_total=grand_total,
            payment_method=scenario["payment_method"],
            status=scenario["status"],
            notes=f"Data seeder — {rental_code}",
            created_by="seeder",
            created_at=dt_ago(scenario["start_offset"] + 1),
        )
        db.add(rental)
        db.flush()

        # ── RentalItems ───────────────────────────────────────────────────
        for item in chosen_items:
            db.add(RentalItem(
                id=make_uuid(),
                rental_id=rental_id,
                item_id=item.id,
                quantity=1,
                price_per_day=item.price_per_day,
                deposit_amount=item.deposit_amount or 0,
                subtotal=item.price_per_day * duration,
                created_by="seeder",
            ))

        # ── Payments ──────────────────────────────────────────────────────
        for pay_def in scenario.get("payments", []):
            pay_type    = pay_def["type"]
            pay_status  = pay_def["status"]
            paid_offset = pay_def.get("paid_offset_days", scenario["start_offset"])

            if "amount_override" in pay_def:
                amount = pay_def["amount_override"]
            elif pay_type == "pembayaran":
                amount = grand_total
            elif pay_type == "refund_deposit":
                amount = deposit_total
            else:
                amount = 150_000

            paid_at      = dt_ago(paid_offset)
            verified_at  = dt_ago(paid_offset - 1) if pay_status == "terverifikasi" else None
            is_transfer  = scenario["payment_method"] == "transfer"

            db.add(Payment(
                id=make_uuid(),
                rental_id=rental_id,
                verified_by=petugas.id if (pay_status == "terverifikasi" and petugas) else None,
                amount=amount,
                type=pay_type,
                status=pay_status,
                bank_name="BCA" if is_transfer else None,
                account_number="1234567890" if is_transfer else None,
                notes=pay_def.get("notes"),
                paid_at=paid_at,
                verified_at=verified_at,
                created_by="seeder",
            ))

        # ── Reviews ───────────────────────────────────────────────────────
        if scenario.get("has_review") and scenario["status"] == "selesai":
            for item in chosen_items:
                db.add(Review(
                    id=make_uuid(),
                    rental_id=rental_id,
                    item_id=item.id,
                    customer_id=customer.id,
                    rating=scenario.get("rating", random.randint(3, 5)),
                    comment=random.choice(COMMENTS),
                    is_visible=True,
                    created_by=customer.username or "seeder",
                ))

        print(f"    + {rental_code} | status={scenario['status']} | customer_id={customer.id} | items={[i.code for i in chosen_items]}")
        created_count += 1

    db.commit()
    print(f"  [Transactions] Selesai. {created_count} rental berhasil dibuat.\n")
