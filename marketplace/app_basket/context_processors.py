from .cart import CartService

def cart(request):
    if request.user.is_superuser:
        return {'cart': []}
    else:
        print(request.user)
        return {'cart': CartService(request)}