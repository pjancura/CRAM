# -*- coding: utf-8 -*-
# try something like
import datetime
import logging
from logging import handlers

logger = logging.getLogger("portal_sales_rep")
logger.setLevel(logging.DEBUG)
handler = handlers.RotatingFileHandler("../MacOS/applications/CRAM/logs/portal_sales_rep.log", "a", 1000000, 5)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


@auth.requires(auth.has_membership('sales_rep_1') or auth.has_membership('sales_rep_2'))
def index():
    emp_num = session.auth.user.id
    today_date = datetime.date.today()
    
    # Retrieve the list of orders and their due dates
    orders = db.executesql('SELECT order_id, due_date FROM orders;')
    
    # Iterate over the orders and check if each order is past due
    for order in orders:
        order_id = order[0]
        due_date = order[1]
        
        # Check if the order is past due
        if due_date < today_date:
            # Update the order status or add a CSS class to change the color
            db.executesql(f'UPDATE orders SET status="Past Due" WHERE order_id={order_id};')
    
    rows = db.executesql('SELECT persons.id, first_name, last_name, c.company_name, persons.employee_id \
                        FROM persons JOIN companies c on c.id = persons.co_id;')
    notes_on_customers = db.executesql('SELECT cn.emp_id, persons.first_name, persons.last_name, \
                                       cn.date_created, cn.time_of_event, cn.contact_note, cn.status , cn.id\
                                        FROM contact_notes cn join persons on persons.id = cn.person_id;')
    
    return locals()


@auth.requires(auth.has_membership('sales_rep_1') or auth.has_membership('sales_rep_2'))
def add_customer_or_company():
    # Function code...
    return locals()

# Rest of your functions...

@auth.requires(auth.has_membership('sales_rep_1') or auth.has_membership('sales_rep_2'))
def my_companies():
    # Function code...
    return locals()

