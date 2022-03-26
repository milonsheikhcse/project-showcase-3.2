from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login
from user.models import Buyer, Seller
from product.models import Product
from . import validator, code, auth_app
from user.forms import BuyerForm, SellerForm
from order.forms import OrderForm
from order.models import OrderItem, Order
from cart.cart import Cart
from .file_upload import UploadFile

# done
def is_buyer(request):
    user_obj = User.objects.get(username=request.user)
    return user_obj.groups.filter(name__in=['Buyer']).exists()

# done
def is_seller(request):
    user_obj = User.objects.get(username=request.user)
    return user_obj.groups.filter(name__in=['Seller']).exists()

# done
def create_buyer(request):
    # get data
    data = request.POST
    data = data.dict()

    # check if buyer related data are ok
    form = BuyerForm(request.POST, request.FILES)
    if not form.is_valid():
        return {'status': 'error', 'msg': 'Enter valid data!'}

    # check if email is valid
    email = auth_app.EmailObject(data['email'])
    if not email.is_valid():
        return {'status': 'error', 'msg': 'Email is not valid!'}

    # check if email exists
    if email.exists():
        return {'status': 'error', 'msg': 'Email already exists!'}

    # check password
    response = validator.password_validator(data['password'], data['confirm'])
    if response != True:
        return response

    # check phone
    phone = auth_app.PhoneObject(data['phone'])
    if not phone.is_valid():
        return {'status': 'error', 'msg': 'Phone number is not valid!'}

    # create user 
    try:
        username = code.id_generate()
        new_user = User(username=username, email=data['email'])
        new_user.set_password(data['password'])
        new_user.save()
    except Exception as e:
        # print(str(e))
        return {'status': 'error', 'msg': 'Error occured!'}
    
    # create buyer 
    try:
        buyer_obj = form.save()
        buyer_obj.user = new_user
        buyer_obj.save()
    except Exception as e:
        # print(str(e))
        new_user = User.objects.get(email=data['email'])
        new_user.delete()
        return {'status': 'error', 'msg': 'Error occured!'}

    # add to group
    try:
        group_obj = Group.objects.get(name='Buyer')
        user_obj = User.objects.get(email=data['email'])
        group_obj.user_set.add(user_obj)
    except Exception as e: 
        # print(str(e))
        new_user = User.objects.get(email=data['email'])
        new_user.delete()
        return {'status': 'error', 'msg': 'Error occured!'}

    # upload image to firebase
    try:
        upload_obj = UploadFile(request, filename='photo')
        
        status = upload_obj.is_valid()
        if not status == True:
            return status            
        
        firebase_url = upload_obj.upload()
        if firebase_url == False:
            return {'status': 'error', 'msg': 'Error occured!'}
        buyer_obj.firebase_url = firebase_url
        buyer_obj.save()
    except Exception as e:
        # print(e)
        new_user = User.objects.get(email=data['email'])
        new_user.delete()
        return {'status': 'error', 'msg': 'Error occured!'}


    return {'status': 'success', 'msg': 'Successfully created account!\nLogin to continue.'}

# done
def create_seller(request):
    # get data
    data = request.POST
    data = data.dict()

    # check if seller related data are ok
    form = SellerForm(request.POST, request.FILES)
    if not form.is_valid():
        return {'status': 'error', 'msg': 'Enter valid data!'}

    # check if email is valid
    email = auth_app.EmailObject(data['email'])
    if not email.is_valid():
        return {'status': 'error', 'msg': 'Email is not valid!'}

    # check if email exists
    if email.exists():
        return {'status': 'error', 'msg': 'Email already exists!'}

    # check password
    response = validator.password_validator(data['password'], data['confirm'])
    if response != True:
        return response

    # check phone
    phone = auth_app.PhoneObject(data['phone'])
    if not phone.is_valid():
        return {'status': 'error', 'msg': 'Phone number is not valid!'}

    # check shop phone
    shop_phone = auth_app.PhoneObject(data['shop_phone'])
    if not shop_phone.is_valid():
        return {'status': 'error', 'msg': 'Shop phone number is not valid!'}

    # create user 
    try:
        username = code.id_generate()
        new_user = User(username=username, email=data['email'])
        new_user.set_password(data['password'])
        new_user.save()
    except Exception as e:
        # print(str(e))
        return {'status': 'error', 'msg': 'Error occured!'}

    # create seller 
    try:
        seller_obj = form.save()
        seller_obj.user = new_user
        seller_obj.save()
    except Exception as e:
        # print(str(e))
        new_user = User.objects.get(email=data['email'])
        new_user.delete()
        return {'status': 'error', 'msg': 'Error occured!'}

    # add to group
    try:
        group_obj = Group.objects.get(name='Seller')
        user_obj = User.objects.get(email=data['email'])
        group_obj.user_set.add(user_obj)
    except Exception as e: 
        # print(str(e))
        new_user = User.objects.get(email=data['email'])
        new_user.delete()
        return {'status': 'error', 'msg': 'Error occured!'}

    # upload image to firebase
    try:
        upload_obj = UploadFile(request, filename='photo')
        
        status = upload_obj.is_valid()
        if not status == True:
            return status   
        
        firebase_url = upload_obj.upload()
        if firebase_url == False:
            return {'status': 'error', 'msg': 'Error occured!'}
        seller_obj.firebase_url = firebase_url
        seller_obj.save()
    except Exception as e:
        # print(e)
        new_user = User.objects.get(email=data['email'])
        new_user.delete()
        return {'status': 'error', 'msg': 'Error occured!'}

    return {'status': 'success', 'msg': 'Successfully created account!\nLogin to continue.'}

# done
def verify_admin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    # check if blank
    if len(email) == 0 or len(password) == 0:
        return {'status': 'error', 'msg': 'Fields cannot be empty!'}

    email_obj = auth_app.EmailObject(email)
    if not email_obj.is_valid():
        return {'status': 'error', 'msg': 'Email is not valid!'}

    try:
        # check if user exists
        user_obj = User.objects.get(email=email)
        # check if user is staff
        print(user_obj.is_staff)
        if user_obj.is_staff:
            # check if authentic
            authentic_user = authenticate(request, username=user_obj, password=password)
            if authentic_user:
                login(request, authentic_user)
                return {'status': 'success', 'msg': 'Welcome Back!'}
            else:
                return {'status': 'error', 'msg': 'Email and password did not match!'}
        else:
            return {'status': 'error', 'msg': 'You are not a staff!'}
    except Exception as e:
        # print(str(e))
        return {'status': 'error', 'msg': 'Email does not exists!'}

    return {}

# done
def verify_buyer(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    # check if blank
    if len(email) == 0 or len(password) == 0:
        return {'status': 'error', 'msg': 'Fields cannot be empty!'}

    email_obj = auth_app.EmailObject(email)
    if not email_obj.is_valid():
        return {'status': 'error', 'msg': 'Email is not valid!'}
    
    try:
        # check if user exists
        user_obj = User.objects.get(email=email)
        # check if user is buyer
        if user_obj.groups.filter(name__in=['Buyer']).exists():
            # check if authentic
            authentic_user = authenticate(request, username=user_obj, password=password)
            if authentic_user:
                login(request, authentic_user)
                return {'status': 'success', 'msg': 'Welcome Back!'}
            else:
                return {'status': 'error', 'msg': 'Email and password did not match!'}
        else:
            return {'status': 'error', 'msg': 'You are not a buyer!'}
    except Exception as e:
        # print(str(e))
        return {'status': 'error', 'msg': 'Email does not exists!'}

    return {}

# done
def verify_seller(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    
    # check if blank
    if len(email) == 0 or len(password) == 0:
        return {'status': 'error', 'msg': 'Fields cannot be empty!'}

    email_obj = auth_app.EmailObject(email)
    if not email_obj.is_valid():
        return {'status': 'error', 'msg': 'Email is not valid!'}
    
    try:
        # check if user exists
        user_obj = User.objects.get(email=email)
        # check if user is buyer
        if user_obj.groups.filter(name__in=['Seller']).exists():
            # check if authentic
            authentic_user = authenticate(request, username=user_obj, password=password)
            if authentic_user:
                login(request, authentic_user)
                return {'status': 'success', 'msg': 'Welcome Back!'}
            else:
                return {'status': 'error', 'msg': 'Email and password did not match!'}
        else:
            return {'status': 'error', 'msg': 'You are not a seller!'}
    except Exception as e:
        # print(str(e))
        return {'status': 'error', 'msg': 'Email does not exist!'}

    return {}

# done
def create_order(request):
    form = OrderForm(request.POST)
    if not form.is_valid():
        return {'status': 'error', 'msg': 'Enter valid data!'}

    # print(form.cleaned_data)

    bill_contact = auth_app.PhoneObject(form.cleaned_data['bill_contact'])
    if not bill_contact.is_valid():
        return {'status': 'error', 'msg': 'Billing phone number is not valid!'}

    ship_contact = form.cleaned_data['ship_contact']
    if ship_contact is not None:
        ship_contact = auth_app.PhoneObject(ship_contact)
        if not ship_contact.is_valid():
            return {'status': 'error', 'msg': 'Shipping phone number is not valid!'}
    
    try:
        order = form.save()
        cart = Cart(request)

        for item in cart:
            product_obj = Product.objects.get(pk=item['id'])

            OrderItem.objects.create(
                order=order, 
                shop=Seller.objects.get(pk=item['shop']),
                product=product_obj,
                price=item['price'],
                quantity=item['quantity']
            )
            # clear the cart
            cart.clear()

    except Exception as e:
        # print(e)
        return {'status': 'error', 'msg': 'Error occured!'}

    return {'status': 'success', 'msg': 'Successfully Placed Order!'}

def is_owner(request, products_id):
    user_obj = User.objects.get(username=request.user)
    seller_obj = Seller.objects.get(user_name=user_obj)
    
    product_obj = Product.objects.filter(pk=products_id, shop=seller_obj)
    if len(product_obj) == 0:
        return False
    else:
        return True