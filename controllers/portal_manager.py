# -*- coding: utf-8 -*-
# try something like
import datetime
import logging
from logging import handlers

logger = logging.getLogger("portal_manager")
logger.setLevel(logging.DEBUG)
handler = handlers.RotatingFileHandler("../MacOS/applications/CRAM/logs/portal_manager.log", "a", 1000000, 5)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

@auth.requires_login()
def index():
    man_num = session.auth.user.id
    man_group = list(session.auth.user_groups.keys())
    if man_num == 4:
        emp_group = db.executesql(f'SELECT am.group_id, au.id, au.last_name, au.first_name\
                        FROM auth_membership am \
                        JOIN auth_user au ON am.user_id = au.id \
                        WHERE am.group_id = "6";', as_dict=True)
    else:
        emp_group = db.executesql(f'SELECT am.group_id, au.id, au.last_name, au.first_name\
                        FROM auth_membership am \
                         JOIN auth_user au ON am.user_id = au.id \
                        WHERE am.group_id = "7";', as_dict=True)
    logger.info(f'\nmanager group number: {man_group}\nemployee group: {emp_group}')
    return locals()

@auth.requires_login()
def employee_view():
    emp_num = int(request.args(0))
    today_date = datetime.date.today()
    employee_details = db(db.auth_user.id == emp_num).select()
    rows = db.executesql('SELECT persons.id, first_name, last_name, c.company_name, persons.employee_id \
                        FROM persons JOIN companies c on c.id = persons.co_id;')
    notes_on_customers = db.executesql('SELECT cn.emp_id, persons.first_name, persons.last_name, \
                                       cn.date_created, cn.time_of_event, cn.contact_note, cn.status , cn.id\
                                        FROM contact_notes cn join persons on persons.id = cn.person_id;')
    return locals()




@auth.requires_login()
def add_customer_or_company():
    company_form = SQLFORM(db.companies)
    customer_form = SQLFORM(db.persons)
    if request.vars:
        response.flash = msg
    if customer_form.process().accepted:
        response.flash = T('Customer Added')
    else:
        response.flash = T('Please complete the form.')
    man_group = list(session.auth.user_groups.keys())[0]
    if man_group == 4:
        # ids of related employees and collect employee ids
        employees = db(db.auth_membership.group_id == 6).select(db.auth_user.id, join=[db.auth_user.on(db.auth_membership.user_id == db.auth_user.id)])
        employees_list = []
        for x in employees:
            employees_list.append(x.id)
    else:
        # ids of related employees and collect employee ids
        employees = db(db.auth_membership.group_id == 7).select(db.auth_user.id, join=[db.auth_user.on(db.auth_membership.user_id == db.auth_user.id)])
        employees_list = []
        for x in employees:
            employees_list.append(x.id)
    logger.info(f"employee id list: {employees_list}")
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
    else:
        birthday_date = ''
    employee_int = int(request.vars.employee_id)
    #submits to the companies table
    try:
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
        logger.critical(f"\nsomething broke\n{request.vars}")
        redirect(URL(c='portal_sales_rep', f='add_customer_or_company'), vars=dict(msg="Form didn't submit. Please try again."))
    else:
        logger.debug("\nSubmitted to everyting")
        redirect(URL(c='portal_sales_rep', f='view_customer', args=[new_customer_id[0].id]))
    return locals()




@auth.requires_login()
def add_new_note():
    note_form = SQLFORM(db.contact_notes)
    man_group = list(session.auth.user_groups.keys())[0]
    rows_customers = db(db.persons).select(db.persons.id, db.persons.first_name, db.persons.last_name, \
                                           db.companies.company_name, db.persons.work_phone_num, db.persons.email, \
                                            db.persons.birthday, db.persons.contact_type, db.persons.referral_source, \
                                            db.persons.employee_id, db.persons.created_on_date, \
                                            join=[db.companies.on(db.companies.id == db.persons.co_id)])
    if man_group == 4:
        # ids of related employees and collect employee ids
        employees = db(db.auth_membership.group_id == 6).select(db.auth_user.id, join=[db.auth_user.on(db.auth_membership.user_id == db.auth_user.id)])
        employees_list = []
        for x in employees:
            employees_list.append(x.id)
        # collect rows of companies
        relevant_customers = []
        for row in rows_customers:
            if row.persons.employee_id in employees_list:
                logger.info(f"employee_id: {row.persons.id}  \t {row.persons.employee_id}")
                relevant_customers.append(row.persons.id)
            else:
                continue
    else:
        # ids of related employees and collect employee ids
        employees = db(db.auth_membership.group_id == 7).select(db.auth_user.id, join=[db.auth_user.on(db.auth_membership.user_id == db.auth_user.id)])
        employees_list = []
        for x in employees:
            employees_list.append(x.id)
        # collect rows of companies 
        relevant_customers = []
        for row in rows_customers:
            if row.persons.employee_id in employees_list:
                relevant_customers.append(row.persons.id)
            else:
                continue
    list_customer_ids = []
    for x in relevant_customers:
        s_id = str(x)
        r_1 = s_id.replace("(","")
        r_2 = r_1.replace(")","")
        r_3 = r_2.replace(",","")
        i = int(r_3)
        list_customer_ids.append(i)
    if note_form.process().accepted:
        response.flash = 'form accepted'
    elif note_form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    if request.vars:
        return_url = URL('portal_sales_rep','view_customer', args=[request.vars.id]) 
    return locals()

@auth.requires_login()
def add_company():
    company_form = SQLFORM(db.companies)
    if company_form.process().accepted:
        response.flash = 'form accepted'
    elif company_form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return locals()

@auth.requires_login()
def add_customer():
    customer_form = SQLFORM(db.persons)
    if customer_form.process().accepted:
        response.flash = 'form accepted'
    elif customer_form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    man_group = list(session.auth.user_groups.keys())[0]
    if man_group == 4:
        # ids of related employees and collect employee ids
        employees = db(db.auth_membership.group_id == 6).select(db.auth_user.id, join=[db.auth_user.on(db.auth_membership.user_id == db.auth_user.id)])
        employees_list = []
        for x in employees:
            employees_list.append(x.id)
    else:
        # ids of related employees and collect employee ids
        employees = db(db.auth_membership.group_id == 7).select(db.auth_user.id, join=[db.auth_user.on(db.auth_membership.user_id == db.auth_user.id)])
        employees_list = []
        for x in employees:
            employees_list.append(x.id)
    logger.info(f"employee id list: {employees_list}")
    return locals()

@auth.requires_login()
def view_customer():
    id_num = request.args(0)
    person = db(db.persons.id == id_num).select()
    company_id = person[0].co_id
    person_id = person[0].id
    person_company = db(db.companies.id == person[0].co_id) \
                        .select(db.companies.id, db.companies.company_name, db.companies.address, \
                        db.companies.city, db.states_usa.state_abbr, db.companies.zipcode, \
                        db.companies.sic_code, db.companies.s_media_link, \
                        join=[db.states_usa.on(db.companies.state_abbr == db.states_usa.id)])
    person_notes = db(db.contact_notes.person_id == person_id).select()    
    return locals()


@auth.requires_login()
def update_customer():
    persons_id = request.args(0)
    record = db.persons(persons_id) or redirect(URL(''))
    form = SQLFORM(db.persons, record)
    return_url = URL('portal_sales_rep', 'view_customer', args = [record.id])
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return locals()




@auth.requires_login()
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

@auth.requires_login()
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


#work on this##########################
@auth.requires_login()
def my_companies():
    emp_num = session.auth.user.id
    my_query = db.persons.employee_id == emp_num
    my_companies_ids = db(my_query).select()
    rows_of_companies = []
    for row in my_companies_ids:
        company_row = db(db.companies.id == row.co_id) \
                    .select(db.companies.id, db.companies.company_name, db.companies.address, \
                    db.companies.city, db.states_usa.state_abbr, db.companies.zipcode, \
                    db.companies.sic_code, db.companies.s_media_link, \
                    join=[db.states_usa.on(db.companies.state_abbr == db.states_usa.id)])
        rows_of_companies.append(company_row)
                                
    return locals()

@auth.requires_login()
def all_employee_customers():
    # get manager id number
    man_group = list(session.auth.user_groups.keys())[0]
    rows_customers = db(db.persons).select(db.persons.id, db.persons.first_name, db.persons.last_name, \
                                           db.companies.company_name, db.persons.work_phone_num, db.persons.email, \
                                            db.persons.birthday, db.persons.contact_type, db.persons.referral_source, \
                                            db.persons.employee_id, db.persons.created_on_date, \
                                            join=[db.companies.on(db.companies.id == db.persons.co_id)])
    if man_group == 4:
        # ids of related employees and collect employee ids
        employees = db(db.auth_membership.group_id == 6).select(db.auth_user.id, join=[db.auth_user.on(db.auth_membership.user_id == db.auth_user.id)])
        employees_list = []
        for x in employees:
            employees_list.append(x.id)
        # collect rows of companies
        employee_rows_customers = []
        for row in rows_customers:
            if row.persons.employee_id in employees_list:
                logger.info(f"employee_id: {row.persons.id}  \t {row.persons.employee_id}")
                employee_rows_customers.append(row)
            else:
                continue
    else:
        # ids of related employees and collect employee ids
        employees = db(db.auth_membership.group_id == 7).select(db.auth_user.id, join=[db.auth_user.on(db.auth_membership.user_id == db.auth_user.id)])
        employees_list = []
        for x in employees:
            employees_list.append(x.id)
        # collect rows of companies 
        employee_rows_customers = []
        for row in rows_customers:
            if row.persons.employee_id in employees_list:
                employee_rows_customers.append(row)
            else:
                continue
    return locals()

@auth.requires_login()
def all_employee_companies():
    # get manager id number
    man_group = list(session.auth.user_groups.keys())[0]
    rows_customers = db(db.persons).select()
    rows_companies = db(db.companies) \
                    .select(db.companies.id, db.companies.company_name, db.companies.address, \
                    db.companies.city, db.states_usa.state_abbr, db.companies.zipcode, \
                    db.companies.sic_code, db.companies.s_media_link, \
                    join=[db.states_usa.on(db.companies.state_abbr == db.states_usa.id)])
    if man_group == 4:
        # ids of related employees and collect employee ids
        employees = db(db.auth_membership.group_id == 6).select(db.auth_user.id, join=[db.auth_user.on(db.auth_membership.user_id == db.auth_user.id)])
        employees_list = []
        for x in employees:
            employees_list.append(x.id)
        # collect rows of companies
        customer_co_ids = []
        for row in rows_customers:
            if row.employee_id in employees_list:
                logger.info(f"employee_id: {row.id}  \t {row.employee_id}")
                customer_co_ids.append(row.co_id)
            else:
                continue
        employee_rows_companies = []
        for row in rows_companies:
            if row.companies.id in customer_co_ids:
                employee_rows_companies.append(row)
            else:
                continue
    else:
        # ids of related employees and collect employee ids
        employees = db(db.auth_membership.group_id == 7).select(db.auth_user.id, join=[db.auth_user.on(db.auth_membership.user_id == db.auth_user.id)])
        employees_list = []
        for x in employees:
            employees_list.append(x.id)
        # collect rows of companies 
        customer_co_ids = []
        for row in rows_customers:
            if row.employee_id in employees_list:
                customer_co_ids.append(row.co_id)
            else:
                continue
        employee_rows_companies = []
        for row in rows_companies:
            if row.companies.id in customer_co_ids:
                employee_rows_companies.append(row)
            else:
                continue
    return locals()
