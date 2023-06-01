# -*- coding: utf-8 -*-
# try something like
@auth.requires_login()
def index(): 
    return dict(message=T('Welcome to web2py!'))


#######   USING DB(????)  WILL RETURN A DICTIONARY FOR EACH ROW
def display_all_persons():
    rows = db(db.persons).select(orderby=db.persons.id)
    return locals()

def display_all_companies():
    rows = db(db.companies).select(orderby=db.companies.id)
    return locals()


###### USING DB.EXECUTESQL(?????) WILL RETURN A LIST OF TUPLES
@auth.requires_membership('database_admin')
def display_all_employees():
    rows = db.executesql('Select auth_user.id, auth_user.first_name, auth_user.last_name, auth_user.email, auth_group.role \
                        From auth_user \
                        Join auth_membership ON auth_membership.user_id = auth_user.id \
                        Join auth_group ON auth_group.id = auth_membership.group_id \
                        Order by auth_membership.group_id;')
    return locals()

def display_all_invoices():
    rows = db(db.contact_notes).select(orderby=db.contact_notes.id)
    return locals()

def display_all_catalogs():
    rows = db(db.catalogs).select(orderby=db.catalogs.id)
    return locals()

