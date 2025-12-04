from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from item.models import Item
from conversation.models import Conversation
from conversation.forms import ConversationMessageForm


@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('dashboard:index')

    conversations = Conversation.objects.filter(item=item, members=request.user)
    if conversations.exists():
        return redirect('conversation:detail', pk=conversations.first().pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user, item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('conversation:detail', pk=conversation.pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html', {'form': form})


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members=request.user)
    return render(request, 'conversation/inbox.html', {'conversations': conversations})


@login_required
def detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, members=request.user)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })



    
    return render(request, 'conversation/detail.html', {'conversation': conversation})
