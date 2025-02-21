import random
import string
from datetime import date
from ..database import invoices_collection  # Ensure this is defined in your database.py
from ..schemas.invoice_schemas import InvoiceCreate, InvoiceResponse

def generate_invoice_id() -> str:
    # Generate a 9-character alphanumeric string
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    return f"INV#{random_str}"

async def create_invoice(invoice_data: InvoiceCreate, user_email: str) -> InvoiceResponse:
    # Calculate the total from the product (for simplicity, assuming one product)
    total = invoice_data.product.quantity * invoice_data.product.amount_per_quantity
    invoice_id = generate_invoice_id()

    invoice_dict = invoice_data.dict()
    invoice_dict["invoice_id"] = invoice_id
    invoice_dict["total"] = total
    # Tie the invoice to the authenticated user:
    invoice_dict["created_by"] = user_email

    # Insert into MongoDB
    inserted = await invoices_collection.insert_one(invoice_dict)
    saved_invoice = await invoices_collection.find_one({"_id": inserted.inserted_id})

    return InvoiceResponse(**saved_invoice)
