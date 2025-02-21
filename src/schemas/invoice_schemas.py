from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional
from fastapi import Form

class BillingAddress(BaseModel):
    street: Optional[str] = None
    city: str
    state: str
    country: str

    @classmethod
    def as_form(
        cls,
        street: Optional[str] = Form(None),
        city: str = Form(...),
        state: str = Form(...),
        country: str = Form(...)
    ):
        return cls(street=street, city=city, state=state, country=country)

class RecipientInfo(BaseModel):
    name: str
    email: str
    # Billing address is optional. You might handle it as nested or flattened.
    billing_address: Optional[BillingAddress] = None

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        email: str = Form(...),
        street: Optional[str] = Form(None),
        city: Optional[str] = Form(None),
        state: Optional[str] = Form(None),
        country: Optional[str] = Form(None)
    ):
        billing_address = None
        if street or city or state or country:
            billing_address = BillingAddress.as_form(street=street, city=city, state=state, country=country)
        return cls(name=name, email=email, billing_address=billing_address)

class CardDetails(BaseModel):
    card_name: str
    card_number: str
    cvv: str

    @classmethod
    def as_form(
        cls,
        card_name: str = Form(...),
        card_number: str = Form(...),
        cvv: str = Form(...)
    ):
        return cls(card_name=card_name, card_number=card_number, cvv=cvv)

class Product(BaseModel):
    product_name: str
    description: str
    quantity: int
    amount_per_quantity: float

    @classmethod
    def as_form(
        cls,
        product_name: str = Form(...),
        description: str = Form(...),
        quantity: int = Form(...),
        amount_per_quantity: float = Form(...)
    ):
        return cls(
            product_name=product_name,
            description=description,
            quantity=quantity,
            amount_per_quantity=amount_per_quantity
        )

class InvoiceCreate(BaseModel):
    # Recipient Information
    recipient: RecipientInfo
    # Receiving Account Details
    amount: float
    issue_date: date
    due_date: date
    card_details: CardDetails
    # For simplicity, we'll assume one product; you could extend this to a list.
    product: Product
    project_name: str

    @classmethod
    def as_form(
        cls,
        # Recipient fields
        recipient_name: str = Form(...),
        recipient_email: str = Form(...),
        billing_street: Optional[str] = Form(None),
        billing_city: Optional[str] = Form(None),
        billing_state: Optional[str] = Form(None),
        billing_country: Optional[str] = Form(None),
        # Receiving account details
        amount: float = Form(...),
        issue_date: date = Form(...),
        due_date: date = Form(...),
        # Card details
        card_name: str = Form(...),
        card_number: str = Form(...),
        card_cvv: str = Form(...),
        # Product details
        product_name: str = Form(...),
        product_description: str = Form(...),
        product_quantity: int = Form(...),
        product_amount_per_quantity: float = Form(...),
        # Project name
        project_name: str = Form(...)
    ):
        recipient = RecipientInfo.as_form(
            name=recipient_name,
            email=recipient_email,
            street=billing_street,
            city=billing_city,
            state=billing_state,
            country=billing_country,
        )
        card_details = CardDetails.as_form(
            card_name=card_name,
            card_number=card_number,
            cvv=card_cvv,
        )
        product = Product.as_form(
            product_name=product_name,
            description=product_description,
            quantity=product_quantity,
            amount_per_quantity=product_amount_per_quantity,
        )
        return cls(
            recipient=recipient,
            amount=amount,
            issue_date=issue_date,
            due_date=due_date,
            card_details=card_details,
            product=product,
            project_name=project_name
        )

class InvoiceResponse(BaseModel):
    invoice_id: str
    project_name: str
    recipient: RecipientInfo
    product: Product
    issue_date: date
    due_date: date
    total: float
