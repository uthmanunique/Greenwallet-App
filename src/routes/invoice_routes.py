from fastapi import APIRouter, HTTPException, Depends
from ..schemas.invoice_schemas import InvoiceCreate, InvoiceResponse
from ..services.invoice_services import create_invoice
from ..utils.jwt_utils import verify_jwt_token  # This should return the user's email from the token

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
