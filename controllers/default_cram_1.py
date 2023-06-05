# -*- coding: utf-8 -*-
# try something like
def index(): return (dict(message = 'This is index_prime test'))

def about_us(): return locals()

def index_prime():
    if session.flash == None:
        pass
    else: 
        user_f_l = f"{str(session.auth.user.first_name)} {str(session.auth.user.last_name)}"
        user_role_id = f"{list(session.auth.user_groups.keys())[0]}"
    return locals()


def employees():
    rows = db.executesql('Select auth_user.id, auth_user.first_name, auth_user.last_name, auth_user.email, auth_group.role \
                        From auth_user \
                        Join auth_membership ON auth_membership.user_id = auth_user.id \
                        Join auth_group ON auth_group.id = auth_membership.group_id \
                        Order by auth_membership.group_id;')
    return locals()