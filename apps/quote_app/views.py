
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import *

###############################################################

# LOGIN / REGISTRATION

###############################################################
def index(request):
    return render(request, 'quote_app/index.html')

## Success always redirects whether you successfully register/login- Double checks to see if request.session['user_id'] is set before navigating to the main quotes page ###
def success(request):
    try:
        request.session['user_id']
        return redirect('/quotes')

    except:
        return redirect('/')

def registration(request):
    errors = User.objects.basic_validation(request.POST)

    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    else:
        user = User.objects.new_user(request.POST)
        request.session['user_id'] = user.id
        return redirect('/success')
        

def login(request):
    result = User.objects.login_validation(request.POST)

    if type(result) is list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['user_id'] = result.id
        return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')

###############################################################

# END OF LOGIN / REGISTRATION

###############################################################    



###############################################################

# EVERYTHING ABOUT THE QUOTESSSSS

###############################################################
def quote(request):
    user = User.objects.get(id=request.session['user_id'])
    quotes = Quote.objects.all()
    ## Below lists out all the favorite quotes by the user in session ###
    favorites = user.user_favorites.all()

    ## Filtered_quotes returns all the quotes not in the user's favorites
    filtered_quotes = Quote.objects.exclude(favorite = user)
    print filtered_quotes

    ### Favorites quotes ###
    favorite = Quote.objects.filter(favorite = user)
    print quotes

    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'quotes': filtered_quotes,
        'favorites': favorite
    }

    return render(request, 'quote_app/quotes.html', context)


def add_quote(request, user_id):
    errors = Quote.objects.quote_validation(request.POST)

    if errors:
        for error in errors:
            messages.error(request, error)

            return redirect('/quotes')
    else: 
        user = User.objects.get(id = user_id)
        Quote.objects.create(author = request.POST['author'], quote = request.POST['quote'], user = user)
        messages.success(request, "Success quote contribution")

        return redirect('/quotes')

def user_info(request, user_id):
    user = User.objects.get(id = user_id)
    quote_count = Quote.objects.filter(user = user).count()
    quotes = Quote.objects.filter(user = user)

    context = {
        'user': user,
        'quote_count': quote_count,
        'quotes': quotes
    }

    return render(request, 'quote_app/user_info.html', context)

def add_favorite(request, quote_id):
    this_user = User.objects.get(id = request.session['user_id'])
    this_quote = Quote.objects.get(id = quote_id)
    ## Below adds the specific quote to the user's favorites ##
    this_quote.favorite.add(this_user)

    return redirect('/quotes')

def remove_favorite(request, quote_id):
    this_user = User.objects.get(id = request.session['user_id'])
    this_quote = Quote.objects.get(id = quote_id)
    this_quote.favorite.remove(this_user)

    return redirect('/quotes')

###############################################################

# END OF THE QUOOOTEEEESSSS

###############################################################