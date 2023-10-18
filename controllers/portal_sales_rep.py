# -*- coding: utf-8 -*-
# try something like
import datetime
import logging
from logging import handlers

# logger = logging.getLogger("portal_sales_rep")
# logger_file_name = 'portal_sales_rep.log'
# logger.setLevel(logging.DEBUG)
# handler = handlers.RotatingFileHandler(f"../MacOS/applications/CRAM/logs/{logger_file_name}", "a", 1000000, 5)
# handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)


@auth.requires(auth.has_membership('sales_rep_1') or auth.has_membership('sales_rep_2'))
def index():
    emp_num = session.auth.user.id
    today_date = datetime.date.today()
    rows = db.executesql('SELECT persons.id, first_name, last_name, c.company_name, persons.employee_id \
                        FROM persons JOIN companies c on c.id = persons.co_id;')
    notes_on_customers = db.executesql('SELECT cn.emp_id, persons.first_name, persons.last_name, \
                                       cn.date_created, cn.time_of_event, cn.contact_note, cn.status , cn.id\
                                        FROM contact_notes cn join persons on persons.id = cn.person_id;')

    return locals()




@auth.requires(auth.has_membership('sales_rep_1') or auth.has_membership('sales_rep_2'))
def add_customer_or_company():
    company_form = SQLFORM(db.companies)
    customer_form = SQLFORM(db.persons)
    if request.vars.msg:
        response.flash = request.vars.msg
    if customer_form.process().accepted:
        response.flash = T('Customer Added')
    else:
        response.flash = T('Please complete the form.')
    return locals()

@auth.requires(auth.has_membership('sales_rep_1') or auth.has_membership('sales_rep_2'))
def submit_customer_and_company():
    try:
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
        else:
            birthday_date = ''
        employee_int = int(request.vars.employee_id)
        #submits to the companies table
        db.companies.insert(company_name=request.vars.company_name, address=request.vars.address, \
                            city=request.vars.city, state_abbr=request.vars.state_abbr, zipcode=request.vars.zipcode, \
                                sic_code=request.vars.sic_code, s_media_link=request.vars.s_media_link)
        new_co_id = db((db.companies.company_name == request.vars.company_name) & \
                       (db.companies.address == request.vars.address)).select(db.companies.id).last()
        db.persons.insert(first_name=request.vars.first_name, last_name=request.vars.last_name, \
                        co_id=int(new_co_id), work_phone_num=request.vars.work_phone_num, \
                        email=request.vars.email, birthday=birthday_date, contact_type=request.vars.contact_type, \
                        referral_source=request.vars.referral_source, employee_id=employee_int, created_on_date=created_date)
        new_customer_id = db((db.persons.last_name == request.vars.last_name) & (db.persons.co_id == new_co_id)).select(db.persons.id)
    except:
        # logger.critical(f"\nsomething broke\n{request.vars}")
        redirect(URL(c='portal_sales_rep', f='add_customer_or_company', vars=dict(msg="Form didn't submit. Please try again.")))
    else:
        # logger.debug("\nSubmitted to everyting")
        redirect(URL(c='portal_sales_rep', f='view_customer', args=[new_customer_id[0].id]))
    return locals()




@auth.requires(auth.has_membership('sales_rep_1') or auth.has_membership('sales_rep_2'))
def add_new_note():
    note_form = SQLFORM(db.contact_notes)
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
    if note_form.process().accepted:
        response.flash = 'Form accepted'
    elif note_form.errors:
        response.flash = 'Form has errors'
    else:
        response.flash = 'Please fill out the form'
    if request.vars:
        return_url = URL('portal_sales_rep','view_customer', args=[request.vars.id]) 
    return locals()

@auth.requires(auth.has_membership('sales_rep_1') or auth.has_membership('sales_rep_2'))
def add_company():
    company_form = SQLFORM(db.companies)
    if company_form.process().accepted:
        response.flash = 'Form accepted'
    elif company_form.errors:
        response.flash = 'Form has errors'
    else:
        response.flash = 'Please fill out the form'
    return locals()

@auth.requires(auth.has_membership('sales_rep_1') or auth.has_membership('sales_rep_2'))
def add_customer():
    customer_form = SQLFORM(db.persons)
    if customer_form.process().accepted:
        response.flash = 'Form accepted'
    elif customer_form.errors:
        response.flash = 'Form has errors'
    else:
        response.flash = 'Please fill out the form'
    return locals()

@auth.requires(auth.has_membership('sales_rep_1') or auth.has_membership('sales_rep_2'))
def view_customer():
    id_num = request.args(0)
    person = db(db.persons.id == id_num).select()
    company_id = person[0].co_id
    person_id = person[0].id
    person_company = db(db.companies.id == person[0].co_id) \
                        .select(db.companies.id, db.companies.company_name, db.companies.address, \
                        db.companies.city, db.states_usa_2.state_abbr, db.companies.zipcode, \
                        db.companies.sic_code, db.companies.s_media_link, \
                        join=[db.states_usa_2.on(db.companies.state_abbr == db.states_usa_2.id)])
    person_notes = db(db.contact_notes.person_id == person_id).select()    
    return locals()


@auth.requires(auth.has_membership('sales_rep_1') or auth.has_membership('sales_rep_2'))
def update_customer():
    persons_id = request.args(0)
    record = db.persons(persons_id) or redirect(URL(''))
    form = SQLFORM(db.persons, record)
    return_url = URL('portal_sales_rep', 'view_customer', args = [record.id])
    if form.process().accepted:
        response.flash = 'Form accepted'
    elif form.errors:
        response.flash = 'Form has errors'
    else:
        response.flash = 'Please fill out the form'
    return locals()




@auth.requires(auth.has_membership('sales_rep_1') or auth.has_membership('sales_rep_2'))
def update_company():
    company_id = request.args(0)
    record = db.companies(company_id) or redirect(URL(''))
    form = SQLFORM(db.companies, record)
    attached_customer = db(db.persons.co_id == record.id).select()
    return_url = URL('portal_sales_rep', 'view_customer', args = [attached_customer[0].id])
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return locals()

@auth.requires(auth.has_membership('sales_rep_1') or auth.has_membership('sales_rep_2'))
def update_note():
    note_id = request.args(0)
    record = db.contact_notes(note_id) or redirect(URL(''))
    form = SQLFORM(db.contact_notes, record)
    return_url = URL('portal_sales_rep', 'view_customer', args = [record.person_id])
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return locals()


@auth.requires(auth.has_membership('sales_rep_1') or auth.has_membership('sales_rep_2'))
def my_companies():
    emp_num = session.auth.user.id
    my_query = db.persons.employee_id == emp_num
    my_companies_ids = db(my_query).select()
    rows_of_companies = []
    for row in my_companies_ids:
        company_row = db(db.companies.id == row.co_id) \
                    .select(db.companies.id, db.companies.company_name, db.companies.address, \
                    db.companies.city, db.states_usa_2.state_abbr, db.companies.zipcode, \
                    db.companies.sic_code, db.companies.s_media_link, \
                    join=[db.states_usa_2.on(db.companies.state_abbr == db.states_usa_2.id)])
        # logger.info(company_row)
        rows_of_companies.append(company_row)
                                
    #logger.info(f"company row:  {rows_of_companies}")
    return locals()

