from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from .forms import AssignmentDocumentForm,AssignmentEditForm
from .models import Assignments
from .filters import AssignmentFilter
from payments.models import UserMembership
from authentication.models import Notification

# Create your views here.
def AssignmentCategoryView(request):
    return render(request,'search.html')


def AssignmentSearchView(request):
    return render(request,'job-search.html')


def AssignmentDetailView(request):
    return render(request,'job-single.html')

def assignment_upload(request):
    if request.method == 'POST':
        form=AssignmentDocumentForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Assignment has successfully uploaded')
            return redirect('assignments:search')
    else:
        form=AssignmentDocumentForm()
    return render(request,'upload.html',{
        'form':form
    })



def delete_assignment(request,pk):
    if request.method=='POST':
        assignment=Assignments.objects.get(pk=pk)
        assignment.delete()
    return redirect('assignments:search')

def edit_assignment(request,pk):
    # update view for details 
    context ={} 
  
    # fetch the object related to passed id 
    obj = Assignments.objects.get(id=pk)
  
    # pass the object as instance in form 
    form = AssignmentEditForm(request.POST or None, instance = obj) 
  
    # save the data from the form and 
    # redirect to detail_view 
    if form.is_valid(): 
        form.save() 
        return redirect("index")
  
    # add form dictionary to context 
    context["form"] = form 
  
    return render(request, "assignment_update.html", context) 



# after updating it will redirect to detail_View 
def assignment_detail(request, pk): 
    # dictionary for initial data with  
    # field names as keys 
    context ={} 
   
    # add the dictionary during initialization
    data = Assignments.objects.get(id = pk)
    
    user_membership=UserMembership.objects.filter(user=request.user).first()
    # if user_membership:
    # if user_membership is not None:
    # import pdb; pdb.set_trace()
    user_membership_type=user_membership.membership.membership_type

    assignment_allowed_memberships=data.allowed_memberships.all() 

    context["data"] = None
    # if user_membership_type is not None

    if assignment_allowed_memberships.filter(membership_type=user_membership_type).exists():
        context['data'] = data


    if request.POST.get('status') == 'approve':
        data.is_approved=True
        data.save()
    elif request.POST.get('status') == 'complete':
        data.is_completed=True
        data.save()
    elif request.POST.get('status') == 'revise':
        data.revise=True
        data.save()
    else:
        data.save()

    
           
    return render(request, "assignment_detail.html", context) 
  

def search_assignment(request):
    assignment_list = Assignments.objects.all()
    assignment_filter = AssignmentFilter(request.GET, queryset=assignment_list)

    data = Assignments.objects.all().first()
    
    user_membership=UserMembership.objects.filter(user=request.user).first()
    # if user_membership:
    # if user_membership is not None:
    # import pdb; pdb.set_trace()
    user_membership_type=user_membership.membership.membership_type

    assignment_allowed_memberships=data.allowed_memberships.all() 

    data = None
    # if user_membership_type is not None

    if assignment_allowed_memberships.filter(membership_type=user_membership_type).exists():
        data = data

    if request.user.is_authenticated:
        notifications=Notification.objects.filter(user=request.user,viewed=False)
    return render(request, 'assignment_detail.html', {'data': data,'filter':assignment_filter,'notifications':notifications})
        