from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login ,logout
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.sessions.models import Session

search_form = ProductSearchForm()

# Trang Chủ 
def home(request):
    customer = Customer.objects.get(user=request.user)  # Lấy thông tin khách hàng dựa trên người dùng hiện tại
    user_id = request.user.id if request.user.is_authenticated else None
    products = Product.objects.all()
    cart = None
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Xử lý trường hợp người dùng chưa đăng nhập
        # Ví dụ: Bạn có thể không tạo giỏ hàng cho khách truy cập ẩn danh
        pass

    items = cart.cartitem_set.all() if cart else []
    total_quality = sum(item.quantity for item in items)

    context = {
        'customer':customer,
        'user': request.user,
        'products': products,
        'total_quality': total_quality,
        'search_form': search_form,
        'user_id': user_id,

    }
    return render(request, "home.html", context)
# Sản Phẩm 
def product(request):
    customer = Customer.objects.get(user=request.user)  # Lấy thông tin khách hàng dựa trên người dùng hiện tại
    products = Product.objects.all()
    cart = None
    items = []
    total_quality = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.cartitem_set.all()
        for item in items:
            total_quality += item.quantity
    context = {
        'customer':customer,
        'user': request.user,
        'products': products,
        'total_quality': total_quality,
        'search_form': search_form,
    }
    return render(request, "product.html", context)
# Chi tiết sản phẩm 
def product_detail(request, product_id):
    customer = Customer.objects.get(user=request.user)  # Lấy thông tin khách hàng dựa trên người dùng hiện tại
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    total_quality = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.cartitem_set.all()
        for item in items:
            total_quality += item.quantity

    context = {
        'customer':customer,
        'user': request.user,
        'product': product,
        'reviews': reviews,
        'form': form,
        'search_form': search_form,
        'total_quality': total_quality,
    }
    return render(request, 'product_detail.html', context)
# Đánh giả sản phẩm
def product_reviews(request, product_id):
    customer = Customer.objects.get(user=request.user)  # Lấy thông tin khách hàng dựa trên người dùng hiện tại
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    
    return render(request, 'product_detail.html', {'product': product, 'reviews': reviews,'customer':customer})
# Tạo đánh giá sản phẩm 
@login_required
def create_review(request, product_id):
    customer = Customer.objects.get(user=request.user)  # Lấy thông tin khách hàng dựa trên người dùng hiện tại
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            if review.image:
                review.image = request.FILES['image']
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'product_detail.html', {'form': form, 'product': product,'customer':customer})
# Tìm sản phẩm 
def search_products(request):
    customer = Customer.objects.get(user=request.user)  # Lấy thông tin khách hàng dựa trên người dùng hiện tại
    products = Product.objects.all()
    if request.method == 'GET':
        search_form = ProductSearchForm(request.GET)
        if search_form.is_valid():
            search_item = search_form.cleaned_data['search_item']
            products = Product.objects.filter(name__icontains=search_item)
        else:
            products = Product.objects.none()  # Hoặc trả về tất cả sản phẩm nếu muốn
    else:
        search_form = ProductSearchForm()
        products = Product.objects.none()
    total_quality = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.cartitem_set.all()
        for item in items:
            total_quality += item.quantity

    context = {
        'total_quality':total_quality,
        'customer':customer,
        'user': request.user,
        'products': products,
        'search_form': search_form,
    }
    return render(request, 'product.html', context)
#Phân loại sản phẩm 
# Giỏ hàng 
def cart(request):
    customer = Customer.objects.get(user=request.user)  # Lấy thông tin khách hàng dựa trên người dùng hiện tại
    if request.user.is_authenticated:

        if request.method == 'POST':
            action = request.POST.get('action')
            product_id = request.POST.get('product_id')
            cart_item = get_object_or_404(CartItem, id=product_id)
            
            if action == 'minus':
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                elif cart_item.quantity == 1:
                    cart_item.delete() 
            if action == 'plus':
                cart_item.quantity += 1
                cart_item.save()
            elif action == 'delete':
                cart_item.delete()
                
            return redirect('cart_detail')
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.cartitem_set.all()
        total_price = 0
        total_quality = 0
        discount = 0
        for item in items:
            total_price += item.product.price * item.quantity
            total_quality += item.quantity
            if total_quality >= 5 :
                discount = 10
                total_price = (total_price*0.9)
        context = {
            'customer':customer,

            'items': items,
            'total_price': total_price,
            'total_quality':total_quality,
            'discount':discount,
            'search_form' : search_form,

        }
        return render(request, 'cart.html', context)
    else:
        messages.error(request, "Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng.")
        return redirect('/login')
# Thêm vào giỏ hàng
def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)

        # Tạo hoặc lấy giỏ hàng của người dùng
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Tạo hoặc lấy mục giỏ hàng cho sản phẩm
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

        # Nếu mục giỏ hàng đã tồn tại, tăng số lượng lên 1
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()

        messages.success(request, "Thêm sản phẩm vào giỏ hàng thành công!")
        return redirect('/product')
    else:
        messages.error(request, "Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng.")
        return redirect('/login')  
# Thanh Toán 
def oder(request):
    customer = Customer.objects.get(user=request.user)  # Lấy thông tin khách hàng dựa trên người dùng hiện tại
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.all()
    total_price = 0
    total_quality = 0
    discount = 0
    for item in items:
        total_price += item.product.price * item.quantity
        total_quality += item.quantity
        if total_quality >= 5 :
            discount = 10
            total_price = (total_price*0.9)

    context = {
        'customer':customer,
        'items': items,
        'total_price': total_price,
        'total_quality':total_quality,
        'discount':discount,
        'search_form' : search_form,
    }
    return render(request,'oder.html',context)
#Kiểm tra giỏ hàng 
def check_item(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitem_set.all()

    total_quality = 0
    for item in items:
        total_quality += item.quantity

    if total_quality > 0:
        return redirect('oder')
    elif total_quality == 0:
        messages.error(request, "Không có sản phẩm")
        return redirect('/cart/')

# Đặt hàng 
def clear_cart(request):
    # Xóa tất cả các sản phẩm trong giỏ hàng
    CartItem.objects.all().delete()
    # Chuyển hướng người dùng đến trang giỏ hàng hoặc trang khác
    return redirect('home')  # Thay 'cart' bằng tên đúng của view giỏ hàng của bạn
# Đăng Ký
def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            # Lấy thông tin từ form đăng ký
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(username=username, email=email, password=password)  # Tạo tài khoản người dùng mới
            
            # Tạo Customer liên kết với người dùng
            customer = Customer.objects.create(user=user)
            user.customer = customer
            user.save()
            messages.success(request, 'Đăng ký thành công!')  # Gửi thông báo thành công
            login(request, user)  # Đăng nhập người dùng mới tạo
            return redirect('create_customer')  # Điều hướng đến trang tạo khách hàng
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

# Điền thông tin 
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            # Lấy thông tin từ form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            # Lấy người dùng đã đăng nhập
            user = request.user
            # Kiểm tra xem người dùng đã có đối tượng Customer tương ứng chưa
            customer, created = Customer.objects.get_or_create(user=user, defaults={
                'name': name,
                'email': email,
                'phone': phone,
                'address': address,
            })
            if not created:
                # Nếu đối tượng Customer đã tồn tại, cập nhật thông tin
                customer.name = name
                customer.email = email
                customer.phone = phone
                customer.address = address
                customer.save()

            return redirect('home')  # Chuyển hướng đến trang chủ hoặc trang khác tùy ý
    else:
        form = CustomerForm()

    return render(request, 'create_customer.html', {'form': form})

# Đăng Nhập
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Lấy thông tin từ form đăng nhập
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            # Xác thực thông tin đăng nhập
            user = authenticate(request, username=username, password=password1)
            if user is not None:
                # Đăng nhập thành công
                login(request, user)
                
                # Lấy thông tin khách hàng liên quan
                customer = user.customer
                return redirect('/')  # Điều hướng đến trang chủ sau khi đăng nhập thành công
            else:
                # Thông báo lỗi nếu thông tin đăng nhập không hợp lệ
                messages.error(request, 'Tên người dùng hoặc mật khẩu không hợp lệ.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
# Đăng xuất
def logout_user(request) :
    logout(request)
    return redirect("login")
# Cập nhật thông tin
def user_detail(request):
    customer, created = Customer.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Lấy dữ liệu từ biểu mẫu
        username = request.POST['username']
        name = request.POST.get('name', '')
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.POST['address']
        
        # Kiểm tra xem khách hàng đã tồn tại hay chưa
        if request.user.is_authenticated:
            user = request.user
            customer, created = Customer.objects.get_or_create(user=user)
            if 'name' in request.GET:
                    name = request.GET['name'] 
            customer.phone = phone
            customer.email = email
            customer.address = address
            customer.save()
        else:
            # Tạo một đối tượng User mới
            user = User(username=username)
            user.save()
            
            # Tạo một đối tượng Customer mới và liên kết với User mới
            customer = Customer(user=user,name = name , phone=phone, email=email, address=address)
            customer.save()

        # Chuyển hướng sau khi đã lưu thông tin thành công
        return redirect('user_profile')

    total_quality = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.cartitem_set.all()
        for item in items:
            total_quality += item.quantity

    context = {
        'user': request.user,
        'search_form': search_form,
        'total_quality': total_quality,
        'customer':customer,

    }
    return render(request , 'user_detail.html', context)
#Lưu thông tin
def user_profile(request):
    customer = Customer.objects.get(user=request.user)  # Lấy thông tin khách hàng dựa trên người dùng hiện tại

    total_quality = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.cartitem_set.all()
        for item in items:
            total_quality += item.quantity
    context = {
        'customer':customer,
        'user': request.user,
        'search_form': search_form,
        'total_quality': total_quality,
    }
    return render(request, 'user_profile.html', context)