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


@auth.requires_login()
def index():
    emp_num = session.auth.user.id
    today_date = datetime.date.today()
    rows = db.executesql('SELECT persons.id, first_name, last_name, c.company_name, persons.employee_id \
                        FROM persons JOIN companies c on c.id = persons.co_id;')
    notes_on_customers = db.executesql('SELECT cn.emp_id, persons.first_name, persons.last_name, cn.date_created, cn.time_of_event, cn.contact_note, cn.status \
                                        FROM contact_notes cn join persons on persons.id = cn.person_id;')

    return locals()




@auth.requires_login()
def add_customer_or_company():
    company_form = SQLFORM(db.companies)
    customer_form = SQLFORM(db.persons)
    if customer_form.process().accepted:
        response.flash = T('Customer Added')
    else:
        response.flash = T('Please complete the form.')
    return locals()

@auth.requires_login()
def submit_customer_and_company():
    #cast each variable to the correct data type
    full_year = int(request.vars.created_on_date[:4])
    full_month = int(request.vars.created_on_date[5:7])
    full_day = int(request.vars.created_on_date[8:10])
    created_date = datetime.date(full_year, full_month, full_day)
    if request.vars.birthday:
        b_full_year = int(request.vars.birthday[:4])
        b_full_month = int(request.vars.birthday[5:7])
        b_full_day = int(request.vars.birthday[8:10])
        birthday_date = datetime.date(b_full_year, b_full_month, b_full_day)
    employee_int = int(request.vars.employee_id)
    #submits to the companies table
    try:
        db.companies.insert(company_name=request.vars.company_name, address=request.vars.address, city=request.vars.city, state_abbr=request.vars.state_abbr, zipcode=request.vars.zipcode, sic_code=request.vars.sic_code, s_media_link=request.vars.s_media_link)
    except:
        logger.critical("\nDidn't Insert to Companies")
    else:
        logger.debug("\nsubmitted to table: companies")
    #get id of new company information
    try:
        new_co_id = db((db.companies.company_name == request.vars.company_name) & (db.companies.address == request.vars.address)).select(db.companies.id).last()
    except:
        logger.critical("\nCould not get new Company ID")
    else:
        logger.info(f'\nNew Company ID:  {new_co_id}\n')
    # submits to the persons table the company info
    try:
        db.persons.insert(first_name=request.vars.first_name, last_name=request.vars.last_name, co_id=int(new_co_id), work_phone_num=request.vars.work_phone_num, email=request.vars.email, birthday=birthday_date, contact_type=request.vars.contact_type, referral_source=request.vars.referral_source, employee_id=employee_int, created_on_date=created_date)
    except:
        logger.critical("\nCould not submit to table:  persons")
    else:
        new_customer_id = db((db.persons.last_name == request.vars.last_name) & (db.persons.co_id == new_co_id)).select(db.persons.id)
        logger.debug("\nSubmitted to table: persons")
        redirect(URL(c='portal_sales_rep', f='view_customer', args=[new_customer_id[0].id]))
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
    if company_form.process().accepted:
        response.flash = T('Record Updated')
    else:
        response.flash = T('Please complete the form.')
    return locals()

@auth.requires_login()
def add_customer():
    customer_form = SQLFORM(db.persons).process()
    if customer_form.process().accepted:
        response.flash = T('Record Updated')
    else:
        response.flash = T('Please complete the form.')
    return locals()

@auth.requires_login()
def view_customer():
    id_num = request.args(0)
    person = db(db.persons.id == id_num).select()
    company_id = person[0].co_id
    person_id = person[0].id
    person_company = db(db.companies.id == company_id).select(db.companies.id, db.companies.company_name, db.companies.address, db.companies.city, db.states_usa.state_abbr, db.companies.zipcode, db.companies.sic_code, db.companies.s_media_link, join=[db.states_usa.on(db.companies.state_abbr == db.states_usa.id)])
    person_notes = db(db.contact_notes.person_id == person_id).select()    
    return locals()

# def test():
    # id_num = request.args(0)
    #person = db(db.persons.id == 76).select()
    # company_id = person[0].co_id
    # person_id = person[0].id
    #person_company = db(db.companies.id == 79).select(db.companies.id, db.companies.company_name, db.companies.address, db.companies.city, db.states_usa.state_abbr, db.companies.zipcode, db.companies.sic_code, db.companies.s_media_link, join=[db.states_usa.on(db.companies.state_abbr == db.states_usa.id)])
    # person_notes = db(db.contact_notes.person_id == person_id).select()
    #return locals()


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

