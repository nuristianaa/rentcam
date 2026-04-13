import io

import fitz
from sqlalchemy.orm import Session
from utils.audit_trail import define_datalog, logs
from utils.repo.queries import BrowseSchema
from utils.responses import BadRequest400, NotFound404
from utils.std_service import StdService

from app.transaction.rentals_histories.repo import RentalHistoryRepo
from .models import RentalInvoice as Model
from .models import tbl_select
from .repo import RentalInvoiceRepo


class RentalInvoiceService(StdService):
  def __init__(self, db: Session, cred: dict | None) -> None:
    self.repo         = RentalInvoiceRepo(db=db)
    self.history_repo = RentalHistoryRepo(db=db)
    super().__init__(db, cred, self.repo)

  # ─────────────────────────────────────────
  # CREATE — dipanggil dari PaymentService setelah payment terverifikasi
  # ─────────────────────────────────────────

  def create_from_payment(self, payment_id: str) -> dict:
    """
    Buat invoice dari payment yang sudah terverifikasi.
    Dipanggil oleh PaymentService — bukan langsung dari endpoint.
    """
    # Guard: jangan buat duplikat
    existing = self.repo.get_by_payment(payment_id=payment_id)
    if existing:
      raise BadRequest400(f"Invoice untuk payment ini sudah ada: {existing.invoice_code}")

    # Ambil data payment
    from app.transaction.payments.models import Payment
    payment = self.db.query(Payment).filter(
      Payment.id == payment_id,
      Payment.deleted_at.is_(None),
    ).first()
    if not payment:
      raise BadRequest400("Payment tidak ditemukan.")
    if payment.status != "terverifikasi":
      raise BadRequest400("Invoice hanya bisa dibuat untuk payment yang sudah terverifikasi.")

    # Ambil data rental
    from app.transaction.rentals.models import Rental
    rental = self.db.query(Rental).filter(Rental.id == payment.rental_id).first()
    if not rental:
      raise BadRequest400("Rental tidak ditemukan.")

    # Ambil data customer & verifikator
    from app.auth.user.models import User
    customer = self.db.query(User).filter(User.id == rental.customer_id).first()
    verifier = None
    if payment.verified_by:
      verifier = self.db.query(User).filter(User.id == payment.verified_by).first()

    # Snapshot items dan biaya harus disesuaikan berdasarkan tipe payment.
    from app.transaction.rental_items.models import RentalItem
    from app.master.items.models import Item
    rental_items = (
      self.db.query(RentalItem)
      .filter(RentalItem.rental_id == rental.id, RentalItem.deleted_at.is_(None))
      .all()
    )
    rental_items_snapshot = []
    for ri in rental_items:
      item = self.db.query(Item).filter(Item.id == ri.item_id).first()
      rental_items_snapshot.append({
        "item_id":        ri.item_id,
        "item_code":      item.code if item else None,
        "item_name":      item.name if item else None,
        "quantity":       ri.quantity,
        "price_per_day":  ri.price_per_day,
        "deposit_amount": ri.deposit_amount,
        "duration_days":  rental.duration_days,
        "subtotal":       ri.subtotal,
      })

    payment_type = (payment.type or '').lower()
    if payment_type == 'denda':
      items_snapshot = [{
        "item_id":        None,
        "item_code":      'Denda',
        "item_name":      'Denda rental',
        "quantity":       1,
        "price_per_day":  payment.amount or 0,
        "deposit_amount": 0,
        "duration_days":  0,
        "subtotal":       payment.amount or 0,
      }]
      subtotal = 0
      deposit_total = 0
      fine_total = float(payment.amount or 0)
    elif payment_type == 'refund_deposit':
      items_snapshot = [{
        "item_id":        None,
        "item_code":      'Refund Deposit',
        "item_name":      'Refund Deposit',
        "quantity":       1,
        "price_per_day":  payment.amount or 0,
        "deposit_amount": 0,
        "duration_days":  0,
        "subtotal":       payment.amount or 0,
      }]
      subtotal = 0
      deposit_total = float(payment.amount or 0)
      fine_total = 0
    else:
      items_snapshot = rental_items_snapshot
      subtotal = rental.subtotal
      deposit_total = rental.deposit_total
      fine_total = 0

    try:
      invoice_code = self.repo.generate_code()
      values = {
        "rental_id":        str(rental.id),
        "payment_id":       str(payment.id),
        "invoice_code":     invoice_code,
        "type":             payment.type,

        # Snapshot customer
        "customer_id":      customer.id if customer else None,
        "customer_name":    customer.name if customer else None,
        "customer_email":   customer.email if customer else None,
        "customer_phone":   customer.phone if customer else None,

        # Snapshot periode
        "rental_code":      rental.rental_code,
        "start_date":       rental.start_date,
        "end_date":         rental.end_date,
        "duration_days":    rental.duration_days,

        # Snapshot items
        "items_snapshot":   items_snapshot,

        # Snapshot biaya
        "subtotal":         subtotal,
        "deposit_total":    deposit_total,
        "fine_total":       fine_total,
        "grand_total":      payment.amount,

        # Snapshot pembayaran
        "payment_method":   rental.payment_method,
        "bank_name":        payment.bank_name,
        "account_number":   payment.account_number,
        "paid_at":          payment.paid_at,
        "verified_at":      payment.verified_at,
        "verified_by_name": verifier.name if verifier else None,

        "pdf_status":       "pending",
        "created_by":       self.username,
      }
      data = self.repo.create(values=values)

      # Catat di rental_histories
      # FIX: tambah created_by agar konsisten dengan create di modul lain
      self.history_repo.create(values={
        "rental_id":  str(rental.id),
        "event":      "invoice_generated",
        "payment_id": str(payment.id),
        "actor":      self.username,
        "actor_id":   self.cred.get("user_id") if self.cred else None,
        "data":       {"invoice_code": invoice_code, "pdf_status": "pending"},
        "created_by": self.username,
      })

      logs(
        type="create", model=Model, cred=self.cred,
        data=define_datalog(name=invoice_code, after=data),
        schema="transaction"
      )
      return data
    except BadRequest400:
      raise
    except Exception as e:
      raise BadRequest400(str(e), e)

  # ─────────────────────────────────────────
  # UPDATE PDF STATUS — dipanggil background job setelah PDF selesai di-generate
  # ─────────────────────────────────────────

  def update_pdf(self, id: str, pdf_file_id: int, pdf_url: str) -> dict:
    """
    Tandai invoice bahwa PDF sudah berhasil di-generate.
    Dipanggil oleh background job, bukan endpoint langsung.
    """
    data = self.repo.get_id(id=id)
    if data.pdf_status == "generated":
      raise BadRequest400("PDF invoice ini sudah pernah di-generate.")

    try:
      return self.repo.update(
        values={
          "pdf_file_id": pdf_file_id,
          "pdf_url":     pdf_url,
          "pdf_status":  "generated",
          "updated_by":  self.username,
        },
        data=data,
      )
    except Exception as e:
      raise BadRequest400(str(e), e)

  def mark_pdf_failed(self, id: str, reason: str = "") -> dict:
    """Tandai generate PDF gagal — untuk retry logic di background job."""
    data = self.repo.get_id(id=id)
    try:
      return self.repo.update(
        values={
          "pdf_status": "failed",
          "notes":      reason or data.notes,
          "updated_by": self.username,
        },
        data=data,
      )
    except Exception as e:
      raise BadRequest400(str(e), e)

  def generate_pdf_bytes(self, id: str) -> tuple[bytes, str]:
    invoice = self.repo.get_id(id=id)
    if not invoice:
      raise BadRequest400("Invoice tidak ditemukan.")

    def fmt_idr(value):
      try:
        return f"Rp {int(value or 0):,}".replace(",", ".")
      except Exception:
        return "Rp 0"

    def fmt_date(value):
      if not value:
        return "-"
      try:
        return value.strftime("%d/%m/%Y %H:%M")
      except Exception:
        return str(value)

    def item_label(item):
      name = item.get("item_name") or item.get("item_code") or "-"
      return name.replace("\n", " ")[:32]

    def payment_label(value):
      if not value:
        return "-"
      mapping = {
        "transfer": "Transfer Bank",
        "cod": "Cash on Delivery",
      }
      return mapping.get(value, value)

    lines = [
      "========================================",
      "                RENTCAM                 ",
      "           rental alat photo            ",
      "========================================",
      "            STRUK PEMBAYARAN            ",
      "----------------------------------------",
      f"Invoice      : {invoice.invoice_code or '-'}",
      f"Rental       : {invoice.rental_code or '-'}",
      f"Pelanggan    : {invoice.customer_name or '-'}",
      f"Email        : {invoice.customer_email or '-'}",
      f"Telepon      : {invoice.customer_phone or '-'}",
      "----------------------------------------",
      f"Periode      : {invoice.start_date or '-'} s.d. {invoice.end_date or '-'}",
      f"Durasi       : {invoice.duration_days or 0} hari",
      f"Tipe Invoice : {payment_label(invoice.type)}",
      "----------------------------------------",
      "Detail Alat",
    ]

    if invoice.items_snapshot:
      for item in invoice.items_snapshot:
        lines.append(item_label(item))
        lines.append(
          f"  {item.get('quantity', 0)} x {fmt_idr(item.get('price_per_day', 0)):>13} x {item.get('duration_days', 0):>2} hari = {fmt_idr(item.get('subtotal', 0)):>13}"
        )
        if item.get('deposit_amount') is not None and item.get('deposit_amount', 0) > 0:
          lines.append(
            f"    Deposit/item: {fmt_idr(item.get('deposit_amount', 0))}"
          )
    else:
      lines.append("- Tidak ada detail alat")

    lines.extend([
      "----------------------------------------",
      f"Subtotal     : {fmt_idr(invoice.subtotal)}",
      f"Deposit      : {fmt_idr(invoice.deposit_total)}",
      f"Denda        : {fmt_idr(invoice.fine_total)}",
      f"Total Tagihan: {fmt_idr((invoice.subtotal or 0) + (invoice.deposit_total or 0) + (invoice.fine_total or 0))}",
      f"Total Bayar  : {fmt_idr(invoice.grand_total)}",
      "----------------------------------------",
      f"Metode Bayar : {payment_label(invoice.payment_method)}",
      f"Bank         : {invoice.bank_name or '-'}",
      f"No. Rekening : {invoice.account_number or '-'}",
      f"Tgl Bayar    : {fmt_date(invoice.paid_at)}",
      f"Tgl Verif    : {fmt_date(invoice.verified_at)}",
      f"Diverifikasi : {invoice.verified_by_name or '-'}",
      "----------------------------------------",
      "Terima kasih atas kepercayaan Anda.",
      "Semoga acara pemotretan berjalan lancar.",
    ])

    text = "\n".join(lines)
    doc = fitz.open()
    page = doc.new_page(width=450, height=900)
    rect = fitz.Rect(20, 20, 430, 880)
    page.insert_textbox(rect, text, fontsize=10, fontname="courier", align=0)
    buffer = io.BytesIO()
    doc.save(buffer)
    doc.close()
    pdf_bytes = buffer.getvalue()

    if invoice.pdf_status != "generated":
      self.repo.update(
        values={
          "pdf_status": "generated",
          "updated_by": self.username,
        },
        data=invoice,
      )

    filename = f"{invoice.invoice_code or 'invoice'}.pdf"
    return pdf_bytes, filename

  # ─────────────────────────────────────────
  # READ
  # ─────────────────────────────────────────

  def get_index(self, browse_queries: BrowseSchema) -> dict:
    try:
      model = tbl_select()
      return self.repo.browse(browse_queries=browse_queries, model=model)
    except Exception as e:
      raise BadRequest400(str(e), e) from e

  def get_id(self, id: str) -> Model:
    try:
      return self.repo.get_id(id=id)
    except NotFound404:
      raise
    except Exception as e:
      raise BadRequest400(str(e), e) from e

  def get_by_rental(self, rental_id: str) -> list:
    try:
      return self.repo.get_by_rental(rental_id=rental_id)
    except Exception as e:
      raise BadRequest400(str(e), e) from e