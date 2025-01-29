from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic,Message
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm,LoginForm



# View for rendering the homepage
def home(request):
    
    # Get the search query from the GET request, default to an empty string if not provided
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    # Filter rooms based on the topic name that matches the search query (case-insensitive)
    rooms = Room.objects.filter(
       Q(topic__name__icontains=q) |  # Match if the topic name contains the query
       Q(name__icontains=q) |        # Match if the room name contains the query
       Q(description__icontains=q)   # Match if the room description contains the query
    )
    
    # Get all topics for displaying in the template
    topics = Topic.objects.all()[0:5]
    room_count=rooms.count()

    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    

    # Message to display if no rooms are found
    message = None
    if not rooms:
        message = "No rooms available."

    # Render the 'home.html' template with the rooms, message, and topics data
    return render(request, 'base/home.html', {'rooms': rooms, 'message': message, 'topics': topics,'room_count':room_count,'room_messages':room_messages})

# View for rendering a specific room's details
def room(request, pk):
        room = Room.objects.get(id=pk)
        room_messages=room.message_set.all()
        participants=room.participants.all()

        #accept form
        if request.method=='POST':
            message=Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body')
            )
            room.participants.add(request.user)
            return redirect('room',pk=room.id)
        
        

        return render(request, 'base/room.html', {'room': room,'room_messages':room_messages,'participants':participants})
        
# View for creating a new room
@login_required(login_url='login')  # Ensure the user is logged in before accessing this view
def createroom(request):
    # Create an instance of the RoomForm to display an empty form
    form = RoomForm()
    # Fetch all available topics from the database
    topics = Topic.objects.all()
    
    # Check if the request method is POST (i.e., when the form is submitted)
    if request.method == 'POST':
        # Get the topic name submitted from the form
        topic_name = request.POST.get('topic')
        # Get or create a new Topic instance based on the submitted topic name
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        # Create a new Room instance using the submitted data
        Room.objects.create(
            host=request.user,  # Assign the currently logged-in user as the host
            topic=topic,  # Associate the room with the selected or newly created topic
            name=request.POST.get('name'),  # Get the room name from the form data
            description=request.POST.get('description')  # Get the description from the form data
        )
        

          #Djangos def form-> Jo maine pehle banaya tha
        # If the request method is POST, populate the form with the submitted data
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room=form.save(commit=False)
        #     room.host=request.user
        #     room.save()
         


        # Redirect the user to the home page after successfully creating the room
        return redirect('home')
    
    # Render the 'room_form.html' template with the form and topics context
    return render(request, 'base/room_form.html', {'form': form, 'topics': topics})



# View for updating an existing room
@login_required(login_url='login')
def updateroom(request, pk):
    # Fetch the room to be updated using the primary key (ID)
    room = Room.objects.get(id=pk)
    # Fetch all available topics
    topics = Topic.objects.all()
    # Pre-fill the form with the room's current data
    form = RoomForm(instance=room)

    # Check if the request method is POST (i.e., form submission)
    if request.method == 'POST':
        # Get the topic name submitted from the form
        topic_name = request.POST.get('topic')
        # Get or create a new Topic instance based on the submitted topic name
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        # Update the room instance with the submitted data
        room.name = request.POST.get('name')  # Update the room name
        room.description = request.POST.get('description')  # Update the room description
        room.topic = topic  # Update the topic
        room.save()  # Save the updated room instance to the database


        #PURANI WALI DJANGO KA DEFAULT FORM
        # if request.method == 'POST':
        # # If the request method is POST, update the form with the submitted data
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     # If the form is valid, save the updated room to the database
        #     form.save()
        #     # Redirect to the home page after successful update
        #     return redirect('home')

        
        # Redirect to the home page after successful update
        return redirect('home')

    # Render the 'room_form.html' template with the pre-filled form and topics context
    return render(request, 'base/room_form.html', {'form': form, 'topics': topics, 'room': room})






# View for deleting an existing room
@login_required(login_url='login')
def delete(request, pk):
    # Fetch the room to be deleted using the primary key (ID)
    room = Room.objects.get(id=pk) 
    if request.method == 'POST':
        # If the request method is POST, delete the room from the database
        room.delete()
        # Redirect to the home page after successful deletion
        return redirect('home')

    # Render the 'delete.html' template for user confirmation before deletion
    return render(request, 'base/delete.html', {'room': room})


def Loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    page='login'
    
    context={'page':page}

    if request.method=='POST':
        username = request.POST.get('username').lower() 
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)

        except:
            messages.error(request, 'Username not exist')
          # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If user exists, log them in
            login(request, user)
            return redirect('home')  # Redirect to the home page
        else:
            # If credentials are invalid, show an error message
            messages.error(request, 'Invalid username or password.')
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()  # Create an empty form instance
    
    if request.method == 'POST':  # Handle form submission
        form = UserCreationForm(request.POST)  # Bind form with POST data
        if form.is_valid():  # Check if the form is valid
            user = form.save(commit=False)  # Save user but don't commit to DB yet
            user.username = user.username.lower()  # Normalize username to lowercase
            user.save()  # Save user to the database
            login(request, user)  # Log the user in after successful registration
            messages.success(request, 'Account created successfully!')  # Show success message
            return redirect('home')  # Redirect to the home page
        else:
            messages.error(request, 'An error occurred during registration. Please try again.')  # Show error message

    return render(request, 'base/login_register.html', {'form': form})

@login_required(login_url='login')
def deletemessage(request, pk):
    # Fetch the room to be deleted using the primary key (ID)
    message = Message.objects.get(id=pk) 

    if request.user!=message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        # If the request method is POST, delete the room from the database
        message.delete()
        # Redirect to the home page after successful deletion
        return redirect('home')

    # Render the 'delete.html' template for user confirmation before deletion
    return render(request, 'base/delete.html', {'message': message})

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages = user.message_set.all()  # Fetch messages related to the user
    topics=Topic.objects.all()
    
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)

#Update user
@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)

    if request.method == 'POST':
        form=form=UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)

    return render(request,'base/update-user.html',{'form':form})

def topicsPage(request):
       # Get the search query from the GET request, default to an empty string if not provided
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics=Topic.objects.filter(name__icontains=q)
    return render(request,'base/topics.html',{'topics':topics})

def activityPage(request):
    room_messages=Message.objects.all()
    return render(request,'base/activity.html',{'room_messages':room_messages})