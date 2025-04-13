from django.contrib import messages
from django.shortcuts import render
from ecommerceapp.models import Product
from math import ceil

def index(request):
    allProds = []
    # Get all unique categories
    categories = Product.objects.values_list('category', flat=True).distinct()
    
    for cat in categories:
        # Get all products in this category
        products = Product.objects.filter(category=cat)
        n = len(products)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        # Now we'll include the category in each group
        allProds.append({
            'category': cat,
            'products': products,
            'range': range(1, nSlides),
            'nSlides': nSlides
        })

    params = {'allProds': allProds}
    return render(request, "index.html", params)

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        desc = request.POST.get("desc")
        pnumber = request.POST.get("pnumber")
        
        # Create and save contact entry
        myquery = Contact(name=name, email=email, desc=desc, phonenumber=pnumber)
        myquery.save()
        
        # Send success message
        messages.info(request, "We will get back to you soon...")
        return render(request, "contact.html")
    
    # GET request or other methods
    return render(request, "contact.html")

def about(request):
    return render(request,"contact.html")


