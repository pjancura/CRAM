# -*- coding: utf-8 -*-
# try something like
import datetime

@auth.requires_login()
def index():
    emp_num = session.auth.user.id
    today_date = datetime.date.today()
    rows = db.executesql('SELECT persons.id, first_name, last_name, c.company_name, persons.employee_id \
                        FROM persons JOIN companies c on c.id = persons.co_id;')
    notes_on_customers = db.executesql('SELECT cn.emp_id, persons.first_name, persons.last_name, cn.date_created, cn.time_of_event, cn.contact_note, cn.completed \
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
    person_company = db(db.companies.id == person[0].co_id).select()
    person_notes = db(db.contact_notes.person_id == person[0].id).select()
    return locals()

@auth.requires_login()
def update_company():
    company_id = request.args(0)
    record = db.companies(company_id) or redirect(URL(''))
    form = SQLFORM(db.companies, record)
    if form.process().accepted:
        response.flash = T('Record Updated')
    else:
        response.flash = T('Please complete the form.')
    return locals()