# -*- coding: utf-8 -*-
# try something like
import datetime
import json
import logging
from logging import handlers

logger = logging.getLogger("default_cram")
logger_file_name = 'default_cram.log'
logger.setLevel(logging.DEBUG)
handler = handlers.RotatingFileHandler(f"../MacOS/applications/CRAM/logs/{logger_file_name}", "a", 1000000, 5)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


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
    orderby_var = ''
    where_var = ''
    if request.vars.filters:
        if "highToLow" in request.vars.filters:
            orderby_var = 'ORDER BY catalogs.price DESC'
        if "lowToHigh" in request.vars.filters:
            orderby_var = 'ORDER BY catalogs.price'
        if "zToA" in request.vars.filters:
            orderby_var = 'ORDER BY catalogs.product_name DESC'
        if "aToZ" in request.vars.filters:
            orderby_var = 'ORDER BY catalogs.product_name'
        if len(request.vars.filters) > 0:
            if "grains" in request.vars.filters:
                if where_var == '':
                    where_var = 'WHERE catalogs.category = "grain" '
                else:
                    where_var += 'OR catalogs.category = "grain" '
            if "meats" in request.vars.filters:
                if where_var == '':
                    where_var = 'WHERE catalogs.category = "meat" '
                else:
                    where_var += 'OR catalogs.category = "meat" '
            if "beverages" in request.vars.filters:
                if where_var == '':
                    where_var = 'WHERE catalogs.category = "beverage" '
                else:
                    where_var += 'OR catalogs.category = "beverage" '
            if "fruitsAndVegetables" in request.vars.filters:
                if where_var == '':
                    where_var = 'WHERE catalogs.category = "fruits and veggies" '
                else:
                    where_var += 'OR catalogs.category = "fruits and veggies" '
    sql_query = f'SELECT catalogs.id, catalogs.product_name, catalogs.description, catalogs.price, catalogs.category, \
                        catalogs.mass_kg, catalogs.shelf_life_yrs, catalogs.ingredient_list, \
                        catalogs.allergens, product_images.image_name, product_images.pic_file \
                        FROM catalogs \
                        JOIN product_images ON product_images.id = catalogs.img_id {where_var} {orderby_var}'
    # logger.debug(sql_query)
    sql = db.executesql(sql_query, as_dict=True)
    pages_total = len(sql)
    pages = []
    on_page = -1
    for i in range(len(sql)):
        if i % 15 == 0:
            pages.append([])
            on_page += 1
        pages[on_page].append(sql[i])
    if request.args:
        logger.debug(f'd_a_c: {request.args[0]}')
        logger.debug(f'results for page 1: {pages[int(request.args[0]) - 1]}')
        sql = pages[int(request.args[0]) - 1]
    else:
        sql = pages[0]



    return locals()

                        # catalogs.allergens, product_images.id, product_images.image_name, product_images.pic_file \

def download():
    return response.download(request, db)



def catalog_sort():
    filters = []
    if request.vars:
        for prop in request.vars:
            filters.append({prop: request.vars[prop]})
        logger.debug(filters)
    redirect(URL(c='default_cram', f='display_all_catalogs', vars=dict(filters=json.dumps(filters))))
    return locals()

def catalog_pages():
    if request.vars:
        logger.debug(f'vars: {request.vars}')
    if request.args:
        logger.debug(f'args {request.args}')
    redirect(URL(c='default_cram', f='display_all_catalogs', args=request.args, vars=request.vars))
    return locals()