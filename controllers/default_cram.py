# -*- coding: utf-8 -*-
# try something like
import datetime
import logging
from logging import handlers

# logger = logging.getLogger("default_cram")
# logger_file_name = 'default_cram.log'
# logger.setLevel(logging.DEBUG)
# handler = handlers.RotatingFileHandler(f"../MacOS/applications/CRAM/logs/{logger_file_name}", "a", 1000000, 5)
# handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)


def index(): 
    state_counts = db.executesql('SELECT states_usa_2.state_name, COUNT(companies.state_abbr) AS state_count, states_usa_2.state_abbr\
                                FROM companies\
                                JOIN states_usa_2 ON states_usa_2.id = companies.state_abbr \
                                GROUP BY companies.state_abbr;', as_dict=True)
    state_count = []
    state_name = []
    state_abbr = []
    for item in state_counts:
        state_count.append(int(item['state_count']))
        state_name.append(str(item['state_name']))
        state_abbr.append(str(item['state_abbr']))

    recent_customer = db.executesql('SELECT p.id, p.first_name, p.last_name, c.company_name, states.state_name, MAX(p.created_on_date) AS most_recent_date\
                                    FROM persons p \
                                    JOIN companies c ON c.id = p.co_id \
                                    JOIN states_usa_2 states ON states.id = c.state_abbr;', as_dict=True)
    emp_customer_count = db.executesql('SELECT auth_user.first_name, auth_user.last_name, COUNT(persons.employee_id) as customer_count\
                                            FROM auth_user \
                                            JOIN persons ON auth_user.id = persons.employee_id \
                                            GROUP BY persons.employee_id;', as_dict=True)
    cc_employee_names = []
    cc_customer_counts = []
    for item in emp_customer_count:
        complete_name = f"{str(item['first_name'])} {str(item['last_name'])}"
        cc_employee_names.append(complete_name)
        cc_customer_counts.append(int(item['customer_count']))
    emp_with_most_customers = db.executesql('SELECT au.id, au.first_name, au.last_name, COUNT(p.employee_id) AS customer_count\
                                            FROM auth_user au \
                                            JOIN persons p ON au.id = p.employee_id \
                                            GROUP BY p.employee_id \
                                            ORDER BY customer_count DESC \
                                            LIMIT 1;', as_dict=True)
    # logger.debug(f"\n{state_name}")
    return locals()

def about_us(): 
    return locals()

def team_bio():
    return locals()

def pert_careers():
    return locals()

def pert_investors():
    return locals()

def pert_products():
    return locals()

def pert_suppliers():
    return locals()

def pert_sustainability():
    return locals()

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


def display_all_catalogs():
    rows = db(db.catalogs).select(db.catalogs.id, db.catalogs.product_name, db.catalogs.description, db.catalogs.price, \
                                db.catalogs.category, db.catalogs.mass_kg, db.catalogs.shelf_life_yrs, db.catalogs.ingredient_list, \
                                db. catalogs.allergens, db.product_images.id, db.product_images.image_name, db.product_images.pic_file, \
                                join=[db.product_images.on(db.product_images.id == db.catalogs.img_id)],orderby=db.catalogs.id)
    
    return locals()


def download():
    return response.download(request, db)