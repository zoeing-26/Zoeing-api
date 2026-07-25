
INTERNAL_MAIL_SUBJECT = "New order has placed"
INTERNAL_BODY = '''
Hi Team,

    New enquery has been placed by {mail}.
    Here is the list of orders,
    
{materials}
    
    Please verify the orders and get back to the client as soon as possible.
    
Regards,
Zo Products
'''



USER_MAIL_SUBJECT  = "Regarding Order"

USER_BODY = '''
Hi User,
    Thank you for your enquiry! Your order has been placed successfully. 
    Our team will contact you shortly.

Order Summary:
---------------   
{materials}

Regards,
Zo products

'''


SUCCESS_RESPONSE = "Successfull"
ERROR_RESPONSE = "Unsuccessfull"\

GUEST_USER = "Guest User created"
REGISTERED_USER = "User created successfully"
