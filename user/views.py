from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from user.forms import MyLoginForm, MySignupForm
from .models import UserProfile

@login_required
def profile(request):
  cur_user = request.user
  
  if request.method == 'POST':
      language = request.POST.get('language')
      if language:
          # Get or create the UserProfile associated with the current user
          profile, created = UserProfile.objects.get_or_create(
              user=cur_user,
              defaults={'language': language}
          )
          # Update the language field
          profile.language = language
          profile.save()
          return redirect('profile')

  try:
    user_profile = UserProfile.objects.get(user=cur_user)
    lang = user_profile.language
    if (lang == 'en'):
       lang = 'English'
    if (lang == 'hi'):
       lang = 'Hindi'
    if (lang == 'bn'):
       lang = 'Bengali'
    if (lang == 'as'):
       lang = 'Assamese'
    if (lang == 'np'):
       lang = 'Nepali'
    if (lang == 'gj'):
       lang = 'Gujarati'
    
    return render(request, 'profile.html', context={'language' : lang})
  except Exception as e:
    return render(request, 'profile.html')

def signup(request):
  url='/accounts/signup/'
  return redirect(url)

def login(request):
  url='/accounts/login/'
  return redirect(url)

def account(request):
    context = {
        'login_form': MyLoginForm(), 
        'signup_form': MySignupForm()
    }
    return render(request, 'account/signup.html', context)

def verification_sent(request):
   return render(request, 'account/vertification_sent.html')

def logout(request):
  if request.method == 'POST':
    django_logout(request)
    return redirect('/')
  return render(request, 'account/logout.html')

# def signup(request):
#     return render(request, 'account/signup.html', context={'signup_form' : MySignupForm()})

# def profile(request):
#   if request.method == 'POST':
#     language = request.POST.get('language')
#     if language:
#         profile, created = User.objects.update_or_create(
#             user=request.user,
#             defaults={'language': language}
#         )
#         # Redirect the user to the profile page or any other page
#         return redirect('profile')

#   return render(request, 'profile.html')