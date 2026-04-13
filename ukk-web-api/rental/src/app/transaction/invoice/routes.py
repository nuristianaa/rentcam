from typing import Annotated

from app.auth.oauth2 import get_cred_with_permission
from db.database import get_db
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from utils.repo.queries import BrowseSchema, browse_query
from utils.responses import res_success

from .service import RentalInvoiceService

path = "transaction/rental-invoices"
router = APIRouter(prefix=f"/v1/{path}", tags=[path])


# BROWSE
@router.get("")
def browse(
  browse_queries: Annotated[BrowseSchema, Depends(browse_query)],
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("browse"))],
):
  service = RentalInvoiceService(db=db, cred=cred)
  data = service.get_index(browse_queries)
  return res_success(data=data)


# READ
@router.get("/{id}")
def get_id(
  id: str,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("read"))],
):
  service = RentalInvoiceService(db=db, cred=cred)
  data = service.get_id(id)
  return res_success(data=data)


# Semua invoice sebuah rental
@router.get("/by-rental/{rental_id}")
def get_by_rental(
  rental_id: str,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("read"))],
):
  service = RentalInvoiceService(db=db, cred=cred)
  data = service.get_by_rental(rental_id)
  return res_success(data=data)


# Trigger manual generate invoice dari payment (admin)
@router.post("/generate-from-payment/{payment_id}")
def generate_from_payment(
  payment_id: str,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("create"))],
):
  service = RentalInvoiceService(db=db, cred=cred)
  data = service.create_from_payment(payment_id=payment_id)
  return res_success(data=data, db=db)


# PREVIEW PDF — inline di browser
@router.get("/{id}/preview-pdf")
def preview_pdf(
  id: str,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("read"))],
):
  service = RentalInvoiceService(db=db, cred=cred)
  pdf_bytes, filename = service.generate_pdf_bytes(id)
  return StreamingResponse(
    iter([pdf_bytes]),
    media_type="application/pdf",
    headers={
      "Content-Disposition": f'inline; filename="{filename}"',
      "Content-Length": str(len(pdf_bytes)),
    },
  )


# DOWNLOAD PDF — paksa download
@router.get("/{id}/download-pdf")
def download_pdf(
  id: str,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred_with_permission("read"))],
):
  service = RentalInvoiceService(db=db, cred=cred)
  pdf_bytes, filename = service.generate_pdf_bytes(id)
  return StreamingResponse(
    iter([pdf_bytes]),
    media_type="application/pdf",
    headers={
      "Content-Disposition": f'attachment; filename="{filename}"',
      "Content-Length": str(len(pdf_bytes)),
    },
  )