# -*- coding: utf-8 -*-
# try something like
import logging
from logging import handlers

logger = logging.getLogger("portal_dbadmin")
file_name = 'portal_dbadmin.log'
logger.setLevel(logging.DEBUG)
handler = handlers.RotatingFileHandler(f"../MacOS/applications/CRAM/logs/{file_name}", "a", 1000000, 5)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

@auth.requires_login()
def index(): return dict(message="hello from portal_dbadmin.py")

@auth.requires_login()
def employees():
    grid = SQLFORM.grid(db.auth_user)
    return locals()

@auth.requires_login()
def employees_group():
    grid = SQLFORM.grid(db.auth_group)
    return locals()

@auth.requires_login()
def employees_membership():
    grid = SQLFORM.grid(db.auth_membership)
    return locals()

@auth.requires_login()
def customers():
    grid = SQLFORM.grid(db.persons)
    return locals()

@auth.requires_login()
def companies():
    grid = SQLFORM.grid(db.companies)
    return locals()

@auth.requires_login()
def sic_codes():
    grid = SQLFORM.grid(db.sic_codes)
    return locals()

@auth.requires_login()
def states_usa():
    grid = SQLFORM.grid(db.states_usa)
    return locals()


@auth.requires_login()
def contact_notes():
    grid = SQLFORM.grid(db.contact_notes)
    return locals()

@auth.requires_login()
def catalog():
    grid = SQLFORM.grid(db.catalogs)
    return locals()

@auth.requires_login()
def invoices():
    grid = SQLFORM.grid(db.invoices)
    return locals()

@auth.requires_login()
def invoice_line_items():
    grid = SQLFORM.grid(db.invoice_line_items)
    return locals()
