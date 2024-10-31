from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash 
from django.contrib import messages
from django.http import Http404
from .forms import TopicForm, EntryForm
from .forms import UserUpdateForm, ProfileForm, UserPasswordChangeForm
from .models import Topic, Entry

# Create your views here.


def index(request):
    """The home page for Learning Log."""
    return render(request, "learning_logs/index.html")

@login_required
def topics(request):
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {"topics": topics}
    return render(request, "learning_logs/topics.html", context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by("-date_added")
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)

@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != "POST":
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)  # Don't save to the database yet
            new_topic.owner = request.user  # Assign the current user as the owner
            new_topic.save()  # Save the Topic instance
            return redirect("learning_logs:topics")
    # Display a blank or invalid form
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)

    if request.method != "POST":
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect("learning_logs:topic", topic_id=topic_id)
    # Display a blank or invalid form.
    context = {"topic": topic, "form": form}
    return render(request, "learning_logs/new_entry.html", context)


def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect("learning_logs:topic", topic_id=topic.id)
    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)

@login_required
def profile(request):
    """Display the profile page with user information."""
    return render(request, 'learning_logs/profile.html', {'profile': request.user.profile})

@login_required
def update_profile(request):
    """Handle updating user profile and redirect upon successful update."""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        password_form = UserPasswordChangeForm(request.user, request.POST)

        if u_form.is_valid() and p_form.is_valid():
            # Save user and profile information
            u_form.save()
            p_form.save()

            # Save password if the form is valid
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Keep the user logged in after password change

            # Provide a success message
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('learning_logs:profile')  # Redirect to the profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)
        password_form = UserPasswordChangeForm(request.user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'password_form': password_form,
    }

    return render(request, 'learning_logs/update_profile.html', context)