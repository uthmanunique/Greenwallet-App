from typing import List
from fastapi import APIRouter, HTTPException, Depends
from ..schemas.invoice_schemas import InvoiceCreate, InvoiceResponse
from ..services.invoice_services import create_invoice
from ..utils.jwt_utils import verify_jwt_token  # This should return the user's email from the token
from ..database import invoices_collection  # Ensure this is defined in your database.py


router = APIRouter()

@router.post("/create", response_model=InvoiceResponse)
async def create_invoice_route(
    invoice: InvoiceCreate = Depends(InvoiceCreate.as_form),
    user_email: str = Depends(verify_jwt_token)
):
    try:
        new_invoice = await create_invoice(invoice, user_email)
        return new_invoice
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(invoice_id: str, user_email: str = Depends(verify_jwt_token)):
    invoice = await invoices_collection.find_one({"invoice_id": invoice_id, "created_by": user_email})
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return InvoiceResponse(**invoice)

@router.get("/", response_model=List[InvoiceResponse])
async def list_invoices(user_email: str = Depends(verify_jwt_token)):
    invoices_cursor = invoices_collection.find({"created_by": user_email})
    invoices = await invoices_cursor.to_list(length=100)  # Adjust the limit as needed
    return [InvoiceResponse(**inv) for inv in invoices]

