# -*- coding: utf-8 -*-
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth
from pydal import DAL, Field
import datetime

db.define_table('states_usa',
                Field('state_name', type='string', notnull=True, unique=True),
                Field('state_abbr', type='string', notnull=True, unique=True)
                )

db.define_table('sic_codes',
                Field('sic_code',type="integer", notnull=True, unique=True),
                Field('office', type='string', notnull=True, unique=True),
                Field('industry_title', type ='string', notnull=True, unique=True)
                )

db.define_table('companies',
                Field('company_name', type = 'string', notnull=True),
                Field('address', type = 'string', notnull=True),
                Field('city', type = 'string', notnull=True),
                Field('state_abbr', type = 'string', notnull=True),
                Field('zipcode', type = 'string', requires = IS_LENGTH(5), notnull=True),
                Field('sic_code', type = 'string', requires = IS_LENGTH(5), notnull=True),
                Field('s_media_link', type = 'string', requires = IS_URL(), notnull=True, unique=True)
                )



#creates foreign key references for table(companies)
db.companies.state_abbr.requires = IS_IN_DB(db, db.states_usa.id, '%(state_abbr)s')
db.companies.sic_code.requires = IS_IN_DB(db, db.sic_codes.sic_code, '%(sic_code)s   %(industry_title)s')

db.define_table('persons',
                Field('first_name', type = 'string', notnull=True),
                Field('last_name', type = 'string', notnull=True),
                Field('co_id', type = 'integer', notnull=True),
                Field('work_phone_num', type = 'string', notnull=True),
                Field('email', type = 'string', notnull=True, unique=True),
                Field('birthday', type = 'date', default = "", requires = IS_DATE()),
                Field('contact_type', type = 'string', requires = IS_IN_SET(['customer', 'vendor']), notnull=True),
                Field('referral_source', type = 'string', requires = IS_IN_SET(['cold call', 'email', 'event', 'newsletter', 'referred by customer'])),
                Field('employee_id', type = 'integer', notnull=True),
                Field('created_on_date', type='date', requires=IS_DATE(), notnull=True)
                )

#creates foreign key reference for table(persons)
db.persons.co_id.requires = IS_IN_DB(db, db.companies.id, '%(company_name)s')
db.persons.employee_id.requires = IS_IN_DB(db, db.auth_user.id, '%(first_name)s %(last_name)s %(id)s')


# time data must in military and formatted HH:MM   with optional :SS 
db.define_table('contact_notes',
                Field('emp_id', type = 'integer', notnull=True),
                Field('date_created', type = 'date', requires=IS_DATE()),
                Field('time_of_event', type = 'time', requires=IS_TIME(), default='12:00 AM'),
                Field('person_id', type = 'integer', notnull=True),
                Field('contact_note', type = 'text', notnull=True),
                Field('status', type='text', requires=IS_IN_SET(['complete', 'incomplete', 'ongoing']), default='incomplete', notnull=True)
                )

#creates foreign key reference for table(persons)
db.contact_notes.emp_id.requires= IS_IN_DB(db, db.auth_user.id, '%(first_name)s %(last_name)s')
db.contact_notes.person_id.requires= IS_IN_DB(db, db.persons.id, '%(id)s %(first_name)s %(last_name)s')



db.define_table('product_images',
                Field('image_name',type='string'),
                Field('pic_file',type='upload'))

db.define_table('catalogs',
                Field('product_name', type = 'string', unique=True, notnull=True),
                Field('description', type = 'text'),
                Field('price', type = 'integer', notnull=True),
                Field('category', type = 'string', requires = IS_IN_SET(['meat', 'fruits and veggies', 'beverage', 'grain']), notnull=True),
                Field('mass_kg', type='decimal(20,2)', notnull=True),
                Field('shelf_life_yrs', type = 'decimal(20,2)', notnull=True),
                Field('ingredient_list', type = 'text', notnull=True),
                Field('allergens', type = 'string'),
                Field('vendor_id', type = 'integer', notnull=True),
                Field('img_id', type = 'string')
                )

db.catalogs.requires = IS_IN_DB(db, db.product_images.id, '%(image_name)s')



db.define_table('invoice_line_items',
                Field('invoice_id', type = 'integer'),
                Field('prod_id', type = 'integer'),                
                Field('prod_quantity', type = 'integer')
                )



#creates foreign key reference for table(invoice_line_items)
db.invoice_line_items.prod_id.requires=IS_IN_DB(db, db.catalogs.id, '%(product_name)s')



db.define_table('invoices',
                Field('purchase_date', type = 'date', requires=IS_DATE(), notnull=True),
                Field('p_id', type = 'integer', notnull=True),
                Field('company_id', type = 'integer'),
                Field('due_date', type = 'date', compute=lambda r: r['purchase_date'] + datetime.timedelta(days=30)),
                Field('invoice_total', type = 'decimal(20,2)', notnull=True),
                Field('credit', type = 'decimal(20,2)', default=0),
                Field('payment_total', type = 'decimal(20,2)', default=0),
                )

#creates foreign key reference for table(invoices)
db.invoices.p_id.requires=IS_IN_DB(db, db.persons.id, '%(first_name)s %(last_name)s %(co_id)s')
db.invoices.company_id.requires=IS_IN_DB(db, db.companies.id, '%(company_name)s %(id)s')




#########################    This is a test element for the invoice calculations


db.define_table('fake_line_items',
                Field('invoice_id', type = 'integer'),
                Field('prod_id', type = 'integer'),                
                Field('prod_quantity', type = 'integer'),
                Field('total_item_price', type = 'decimal(20,2)'),
                Field('total_mass_kg', type = 'decimal(20,2)'),
                Field('shipping', type = 'decimal(20,2)'),
                Field('total_cost', type = 'decimal(20,2)')
                )



db.invoice_line_items.prod_id.requires=IS_IN_DB(db, db.catalogs.id, '%(product_name)s')


db.define_table('fake_invoices',
                Field('purchase_date', type = 'date', requires=IS_DATE(), notnull=True),
                Field('p_id', type = 'integer', notnull=True),
                Field('due_date', type = 'date', compute=lambda r: r['purchase_date'] + datetime.timedelta(days=30)),
                Field('invoice_total', type = 'decimal(20,2)', notnull=True),
                Field('credit', type = 'decimal(20,2)', default=0),
                Field('payment_total', type = 'decimal(20,2)', default=0),
                )

db.invoices.p_id.requires=IS_IN_DB(db, db.persons.id, '%(first_name)s %(last_name)s %(co_id)s')









######################################      WORK SPACE / SAVE FOR LATER
