from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from . import models, forms


# Create your views here.


def signup(request):
    if request.method == "POST":
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('dashboard')

    else:
        form = forms.CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})


def login_user(request):
    user = request.user

    if request.POST:
        
        form = forms.UserForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = forms.UserForm()
        return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('../login')

def update_user(request):
    if request.user.is_authenticated:
        current_user = models.User.objects.get(id=request.user.id)
        form = forms.CustomUserCreationForm(request.POST or None, instance=current_user)
        return render(request, 'profile.html', {'form': form})
    else:
        return redirect('../login')

def profile(request):
    if request.user.is_authenticated:
        current_user = models.User.objects.get(id=request.user.id)
        form = forms.UserProfileForm(request.POST or None, instance=current_user)
        return render(request, 'profile.html', {'form': form})
    else:
        return redirect('../login')


def dashboard(request):
    if request.user.is_authenticated:
        current_user = models.User.objects.get(id=request.user.id)
        lead_list = models.Lead.objects.filter(creator=request.user)
        
        # Prefilled and editable forms for existing leads using lead_list
        # method objects.getid created to return lead id easily

        form_list = []
        for lead in lead_list:
            # for every lead in above lead list we need to initialize a form with its info

            #Stores Lead ID
            id = models.Lead.getid(lead)
            #then we need to store the initialized form into a variable and append it to the form_list and display to template
            testlead_form = forms.LeadForm(initial = {'id':id, 'first_name':lead.first_name, 
            'last_name':lead.last_name, 'email':lead.email, 'contact_num':lead.contact_num})
            form_list.append(testlead_form)
            #in the template we need to loop through the form list with the lead id in a hidden input so we can catch the id in POST
                # and update the lead which the id belongs to
        print(form_list)

        """
        user_board_list = []
        
        boards = models.Board.objects.filter(user=request.user).order_by('id')
        for board in boards:
            board_lead_list = []
            board_leads = models.Lead.objects.filter(creator=request.user, board=board).order_by('id')
            for lead in board_leads:
                lead_id = models.Lead.getid(lead)
                board_lead_form = forms.LeadForm(initial = {'id':lead_id, 'first_name':lead.first_name, 
                    'last_name':lead.last_name, 'email':lead.email, 'contact_num':lead.contact_num})
                board_lead_list.append(board_lead_form)
            user_board_list.append(board_lead_list)

        

        #for board in user_board_list:
            #print(board)
            #for lead in board:
                #print(lead)
                    
        """
                            



        

        lead_form = forms.LeadForm()
        

        if request.POST:
            if "edit_lead" in request.POST: # Allows user to edit an exisiting lead
                
                form = forms.LeadForm(request.POST)
                if form.is_valid():
                    lead_id = request.POST['id']
                    lead_obj = models.Lead.objects.get(id=lead_id)
                    lead_obj.first_name = request.POST['first_name']
                    lead_obj.last_name = request.POST['last_name']
                    lead_obj.email = request.POST['email']
                    lead_obj.contact_num = request.POST['contact_num']
                    lead_obj.save()
                    return redirect('dashboard')

            if "new_lead" in request.POST: #Allows user to add a new lead
                
                form = forms.LeadForm(request.POST)
                if form.is_valid():
                    lead = form.save(commit=False)
                    print(lead.id)
                    lead.creator = request.user
                    lead.save()
                    return redirect('dashboard')

            if "delete_lead" in request.POST: #Allows user to delete an exisiting entry

                lead_id = request.POST['id']
                lead_obj = models.Lead.objects.get(id=lead_id)
                lead_obj.delete()
                return redirect('dashboard')



        context = {'lead_form':lead_form, 'first_name': request.user.first_name, 
        'lead_list':lead_list, 'form_list':form_list,}
        return render(request, 'dashboard.html', context)
    else:
        return redirect('../login')