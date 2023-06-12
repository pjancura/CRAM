# -*- coding: utf-8 -*-
# try something like
import datetime
import logging
from logging import handlers

logger = logging.getLogger("portal_sales_rep")
logger.setLevel(logging.DEBUG)
handler = handlers.RotatingFileHandler("../MacOS/applications/CRAM/logs/portal_sales_rep.log", "a", 1000000, 5)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

@auth.requires_login()
def index():
    emp_num = session.auth.user.id
    today_date = datetime.date.today()
    rows = db.executesql('SELECT persons.id, first_name, last_name, c.company_name, persons.employee_id \
                        FROM persons JOIN companies c on c.id = persons.co_id;')
    invoices = db.executesql('SELECT invoices.id, purchase_date, p_id, due_date, invoice_total, credit, \
                             payment_total FROM invoices WHERE;', as_dict=True)
    notes_on_customers = db.executesql('SELECT cn.emp_id, persons.first_name, persons.last_name, cn.date_created, cn.time_of_event, cn.contact_note, cn.status \
                                        FROM contact_notes cn join persons on persons.id = cn.person_id;')

    return locals()


@auth.requires_login()
def add_customer_or_company():
    customer_form = SQLFORM(db.persons).process()
    company_form = SQLFORM(db.companies).process()
    return locals()

@auth.requires_login()
def add_new_note():
    note_form = SQLFORM(db.contact_notes).process()
    emp_num = session.auth.user.id
    relevant_customers = db.executesql(f'SELECT persons.id \
                                        FROM persons \
                                        WHERE persons.employee_id = {emp_num};')
    list_customer_ids = []
    for x in relevant_customers:
        s_id = str(x)
        r_1 = s_id.replace("(","")
        r_2 = r_1.replace(")","")
        r_3 = r_2.replace(",","")
        i = int(r_3)
        list_customer_ids.append(i)
    return locals()

@auth.requires_login()
def add_company():
    company_form = SQLFORM(db.companies).process()
    return locals()

@auth.requires_login()
def view_customer():
    id_num = request.args(0)
    person = db(db.persons.id == id_num).select()
    person_company = db(db.companies.id == person[0].co_id).select(db.companies.id, db.companies.company_name, db.companies.address, db.companies.city, db.states_usa.state_abbr, db.companies.zipcode, db.companies.sic_code, db.companies.s_media_link, join=[db.states_usa.on(db.companies.state_abbr == db.states_usa.id)])
    person_notes = db(db.contact_notes.person_id == person[0].id).select()    
    return locals()

@auth.requires_login()
def update_customer():
    persons_id = request.args(0)
    record = db.persons(persons_id) or redirect(URL(''))
    form = SQLFORM(db.persons, record)
    return_url = URL('portal_sales_rep', 'view_customer', args = [record.id])
    if form.process().accepted:
        response.flash = T('Record Updated')
    else:
        response.flash = T('Please complete the form.')
    return locals()




@auth.requires_login()
def update_company():
    company_id = request.args(0)
    record = db.companies(company_id) or redirect(URL(''))
    form = SQLFORM(db.companies, record)
    attached_customer = db(db.persons.co_id == record.id).select()
    return_url = URL('portal_sales_rep', 'view_customer', args = [attached_customer[0].id])
    if form.process().accepted:
        response.flash = T('Record Updated')
    else:
        response.flash = T('Please complete the form.')
    return locals()

@auth.requires_login()
def update_note():
    note_id = request.args(0)
    record = db.contact_notes(note_id) or redirect(URL(''))
    form = SQLFORM(db.contact_notes, record)
    return_url = URL('portal_sales_rep', 'view_customer', args = [record.person_id])
    if form.process().accepted:
        response.flash = T('Record Updated')
    else:
        response.flash = T('Please complete the form.')
    return locals()


#work on this##########################
@auth.requires_login()
def my_companies():
    emp_num = session.auth.user.id
    my_query = db.persons.employee_id == emp_num
    my_companies_ids = db(my_query).select()
    rows_of_companies = []
    for row in my_companies_ids:
        company_row = db(db.companies.id == row.co_id).select(db.companies.id, db.companies.company_name, db.companies.address, db.companies.city, db.states_usa.state_abbr, db.companies.zipcode, db.companies.sic_code, db.companies.s_media_link, join=[db.states_usa.on(db.companies.state_abbr == db.states_usa.id)])
        rows_of_companies.append(company_row)
                                
    return locals()

@auth.requires_login()
def my_invoices():
    emp_num = session.auth.user.id
    my_query = db.invoices.p_id == emp_num
    my_customers_invoices = db(my_query).select()
    rows_of_invoices = []
    for row in my_customers_invoices:
        {{if row.p_id == }}
        invoice_row = db(db.invoices.id == row.co_id).select(db.companies.id, db.companies.company_name, db.companies.address, db.companies.city, db.states_usa.state_abbr, db.companies.zipcode, db.companies.sic_code, db.companies.s_media_link, join=[db.states_usa.on(db.companies.state_abbr == db.states_usa.id)])
        rows_of_companies.append(company_row)
                                
    return locals()


