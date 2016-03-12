# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################
@auth.requires_login()
def gridd():
    if not auth.user.retailer:
        session.flash="Permission Denied"
        redirect(URL('main_page'))
    else:
        g=SQLFORM.grid(db.store.created_by==auth.user_id,csv=False,paginate=10)
        try:
             for x in g.elements('span.buttontext'):
                 if x.components[0] == "Edit":
                    x.components[0] = "Update"
                 if x.components[0] == "View":
                    x.components[0] = "View"
                 if x.components[0] == "Delete":
                    x.components[0] = "Remove"
        except:
            pass
    return locals()


def index():
    rows=db().select(db.auth_user.ALL)
    fl=0
    for i in rows:
        if(i.id==auth.user_id):
            fl=1
            c=i
            break
    if fl==1:
        if c.retailer==True:
            redirect(URL('gridd'))
        else:
            redirect(URL('main_page'))
    else:
        redirect(URL('main_page'))
    return dict()


def user():
    ##exposes:
        #127.0.0.1:8000/form/default/user/login
        #http://..../[app]/default/user/logout
        #http://..../[app]/default/user/register
        #http://..../[app]/default/user/profile
        #http://..../[app]/default/user/retrieve_password
        #http://..../[app]/default/user/change_password
        #http://..../[app]/default/user/manage_users (requires membership in
        #use @auth.requires_login()
        #@auth.requires_membership('group name')
        #@auth.requires_permission('read','table name',record_id)
    #to decorate functions that need access control
    #"""
     return dict(form=auth())


#@cache.action()
#def download():
 #   """
  #  allows downloading of uploaded files
   # http://..../[app]/default/download/[filename]
    #"""
    #return response.download(request, db)


#def call():
 #   """
  #  exposes services. for example:
   # http://..../[app]/default/call/jsonrpc
    #decorate with @services.jsonrpc the functions to expose
    #supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    #"""
    #return service()


#@auth.requires_login() 
#def api():
 #   """
  #  this is example of API with access control
   # WEB2PY provides Hypermedia API (Collection+JSON) Experimental
   # """
    #from gluon.contrib.hypermedia import Collection
    #rules = {
     #   '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
      #  }
    #return Collection(db).process(request,response,rules)
@auth.requires_login()
def payment():
    form=SQLFORM.factory(Field('pay_option',requires=IS_IN_SET(['cash_on_delivery','online_payment']))).process()
    if(form.accepted):
        if form.vars.pay_option=='cash_on_delivery':
            session.flash='Thanks for shopping'
            redirect(URL('sold'))
        else:
            redirect(URL('online'))
    return dict(form=form)
def sold():
    #ids=db().select(db.solditem.user_id,db.solditem.product_id)
    for i in range(len(session.cart)):
        row=db(db.store.id==session.cart[i]).select()
        d=row[0].qty
        try:
            rows=db((db.solditem.user_id==auth.user.id )& (db.solditem.product_id==row[0].P_id)).select()
            #d=row[0].qty
            s=rows[0].qty
        except:
                            db.solditem.insert(user_id=auth.user.id,product_id=row[0].P_id,category=row[0].category,price=row[0].price,image=row[0].image,title=row[0].title)
        else:
            db((db.solditem.user_id==auth.user.id) & (db.solditem.product_id==row[0].P_id)).update(qty=s+1)
        db(db.store.id==session.cart[i]).update(qty=d-1)
    session.cart=[]
    session.flash='payment accepted , thank you for shopping with us'
    redirect(URL('sendmail'))
def online():
    session.flash='proceed for online payment'
    redirect(URL('creditcard'))
    return dict()


def creditcard():
    form = SQLFORM.factory(
                Field('creditcard',default='4427802641004797',requires=IS_NOT_EMPTY()),
                Field('expiration',default='12/2012',requires=IS_MATCH('\d{2}/\d{4}')),
                Field('cvv',default='123',requires=IS_MATCH('\d{3}')),
                Field('shipping_address',requires=IS_NOT_EMPTY()),
                Field('shipping_city',requires=IS_NOT_EMPTY()),
                Field('shipping_state',requires=IS_NOT_EMPTY()),
                Field('shipping_zip_code',requires=IS_MATCH('\d{5}(\-\d{4})?')))
    if form.process().accepted:
        redirect(URL('sold'))
    return dict(form=form)

def main_page():
    return dict()
def womenclothing():
    return dict()
def menclothing():
    return dict()
def showitems():
    rows=db(db.store.id==request.args(0)).select()
    return dict(data=rows)

def book():
    rows=db(db.store.category=='book').select()
    return dict(records=rows)
def sarees():
    rows=db(db.store.category=='sarees').select()
    return dict(records=rows)
def download():
    return response.download(request,db)
def jumpsuit():
    rows=db(db.store.category=='jumpsuit').select()
    return dict(records=rows)
def kurti():
    rows=db(db.store.category=='kurti').select()
    return dict(records=rows)
def footwear():
   rows=db(db.store.category=='footwear').select() 
   return dict(records=rows)
def salwar_kameez():
    rows=db(db.store.category=='salwar_kameez').select()
    return dict(records=rows)
def tops_tunic():
    rows=db(db.store.category=='tops_tunic').select()
    return dict(records=rows)
def dresses():
    rows=db(db.store.category=='dresses').select()
    return dict(records=rows)
def tshirts():
    rows=db(db.store.category=='tshirts').select()
    return dict(records=rows)
def trousers():
    rows=db(db.store.category=='trousers').select()
    return dict(records=rows)
def shorts():
    rows=db(db.store.category=='shorts').select()
    return dict(records=rows)
def ethnic():
    rows=db(db.store.category=='ethnic').select()
    return dict(records=rows)
def jeans():
    rows=db(db.store.category=='jeans').select()
    return dict(records=rows)
def formal():
    rows=db(db.store.category=='formal').select()
    return dict(records=rows)
def suits():
    rows=db(db.store.category=='suits').select()
    return dict(records=rows)
if not session.cart:
    session.cart=[]
@auth.requires_login()
def add_to_cart():
    if request.args(0) not in session.cart:
        session.cart.append(request.args(0))
    else:
        session.flash='already in cart'
    redirect(URL('main_page'))
    return dict()

@auth.requires_login()
def show_cart():
    cartitems=[]
    for i in range(len(session.cart)):
        row=db(db.store.id==session.cart[i]).select()
        cartitems.append(row)
    return dict(cartitems=cartitems)

@auth.requires_login()
def delete():
    session.cart.remove(request.args(0))
    redirect(URL('show_cart'))
    return dict()

@auth.requires_login()
def checkout():
    if len(session.cart)==0:
        session.flash='cart is empty'
        redirect(URL('main_page'))
    else:
        cartitems=[]
        for i in range(len(session.cart)):
            row=db(db.store.id==session.cart[i]).select()
            if row[0].qty<=0:
                session.flash='item out of stock. Delete the item and proceed'
                redirect(URL('show_cart'))
            cartitems.append(row)
    return dict(cartitems=cartitems)
if not session.total:
    session.total=0

@auth.requires_login()
def previous_buys():
    rows=db(db.solditem.user_id==auth.user.id ).select()
    return dict(records=rows)

from gluon.tools import Mail
mail = Mail()

mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'chewinggum.tyagi@gmail.com'
mail.settings.login = 'chewinggum.tyagi@gmail.com:tanyatyagi'
#mail.settings.server = 'logging'


@auth.requires_login()
def sendmail():
    if mail:
        if mail.send(to=[auth.user.email],
            subject="shopping at shoppy",
            message="Thank you for shopping with us.\n\nYour total bill is " +str(session.total)
        ):
            session.flash = 'email sent sucessfully.'
            redirect(URL('main_page'))
        else:
            session.flash = 'fail to send email sorry!'
            redirect(URL('main_page'))
    else:
        session.flash = 'Unable to send the email : email parameters not defined'
        redirect(URL('main_page'))
    return dict()


def shipping():
    return dict()

def helpp():
     return dict()

def contact():
     return dict()
