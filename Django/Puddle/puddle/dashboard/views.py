from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from item.models import Item

@login_required
def index(request):
    # Get all items created by the logged-in user
    items = Item.objects.filter(created_by=request.user)

    return render(request, 'dashboard/index.html', {
        'items': items,
    })
