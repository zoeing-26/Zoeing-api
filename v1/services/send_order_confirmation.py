"""
send_order_confirmation.py

Drop-in replacement for your plain-string send_mail().
Renders templates/emails/order_confirmation.html with real order data
and sends HTML + plain-text fallback in one email.

Adjust the field names under "order.<field>" / "item.<field>" to match
your actual Order / OrderItem models.
"""

from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import configs as cfg
from v1.utils import send_email
from itertools import zip_longest

def send_order_confirmation_email(order):
    """ Get details from enquiry and send confirmation mail to user """

    context = {
        # --- company / sender info: pull from settings so it's not hardcoded ---
        "company_name": cfg.COMPANY_NAME,
        "company_address_rows" : list(zip_longest(cfg.COMPANY_ADDRESS_UAE,cfg.COMPANY_ADDRESS_INDIA,fillvalue="")),
        # "company_logo_url": settings.COMPANY_LOGO_URL,
        # "company_po_box": settings.COMPANY_PO_BOX,
        # "company_address_line1": cfg.COMPANY_ADDRESS_LINE1,
        # "company_address_line2": cfg.COMPANY_ADDRESS_LINE2,
        # "company_city": cfg.COMPANY_CITY,
        # "company_country": cfg.COMPANY_COUNTRY,
        "company_phone": cfg.COMPANY_PHONE,
        # "company_fax": settings.COMPANY_FAX,
        "company_email": cfg.DEFAULT_FROM_EMAIL,
        "company_website": cfg.COMPANY_WEBSITE,
        "current_year": datetime.now().year,

        # --- dynamic customer / order info ---
        "customer_name": order['user_name'],
        "customer_company" : order.get('company_name',""),
        "customer_phone" : order['phone_number'],
        "customer_email" : order['email'],
        # "order_view_url": f"{settings.SITE_URL}/orders/{order.id}/",
        # "order_reference": order.reference,
        # "order_date": order.created_at.strftime("%d-%m-%Y"),
        # "order_total": order.total,

        # "shipping_company": order.shipping_address.company,
        # "shipping_address_line1": order.shipping_address.line1,
        # "shipping_postal_code": order.shipping_address.postal_code,
        # "shipping_city": order.shipping_address.city,
        # "shipping_state": order.shipping_address.state,
        # "shipping_country": order.shipping_address.country,
        # "shipping_phone": order.shipping_address.phone,

        # "order_items": [
        #     {
        #         "quantity": item.quantity,
        #         "item_number": item.item_number,
        #         "description": item.description,
        #         "unit_price": item.unit_price,
        #         "line_total": item.line_total,
        #     }
        #     for item in order.items.all()
        # ],
        "order_items": [
        {
            "material_name": material["name"],
            "product_code": material["product_code"],
            "quantity": material["quantity"],
        }
        for material in order["materials"]
    ],
    }

    html_content = render_to_string("emails/order_confirmation.html", context)
    text_content = strip_tags(html_content)  # plain-text fallback for clients that block HTML

    subject = f"Order Confirmation" # - {order.reference}"

    # msg = EmailMultiAlternatives(
    #     subject=subject,
    #     body=text_content,
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     to=[order.customer.email],
    # )
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()

    send_email(
        subject=subject,
        body=html_content,
        sender = cfg.SENDER,
        recipients=[order['email']],
        password= cfg.SALES_PASSWORD
    )

def receive_order_confirmation_mail(order):

    """ Get details from enquiry and send new order to sales mail"""

    context = {

        "customer_name": order['user_name'],
        "customer_company_name" : order.get('company_name',""),
        "customer_phone" : order['phone_number'],
        "customer_email" : order['email'],

        "company_email": cfg.DEFAULT_FROM_EMAIL,
        "company_website": cfg.COMPANY_WEBSITE,
        "current_year": datetime.now().year,
        

        "order_items": [
                {
                    "material_name": material["name"],
                    "product_code": material["product_code"],
                    "quantity": material["quantity"],
                }
                for material in order["materials"]
            ],
    }

    html_content = render_to_string("emails/receive_order_confirmation.html", context)
    text_content = strip_tags(html_content)  # plain-text fallback for clients that block HTML

    subject = f"New Order Received " 

    send_email(
            subject=subject,
            body=html_content,
            sender = cfg.SENDER,
            recipients=[cfg.SENDER],
            password= cfg.SALES_PASSWORD
        )
    