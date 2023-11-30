from django.shortcuts import render, get_object_or_404,redirect
from .models import Discussion,Message,Like
from django.views.generic import CreateView,UpdateView,DetailView,ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


class ModdView(View):
    template_name = "modd.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class index(ListView):
    model = Discussion
    template_name = 'index.html'  
    context_object_name = 'Discussions'
    paginate_by = 10
    def get_queryset(self):
        discussions = Discussion.objects.annotate(num_likes=Count('like')).order_by('-num_likes')[:5]
        return discussions

class DiscussionCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Discussion
    template_name = "form.html"
    fields = ["title","description",]
    success_message = "Discussion Started!"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Start Discussion'
        return context
    def form_valid(self,form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('Message_list', kwargs={'discussion_id': self.object.id})


    


class DiscussionUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Discussion
    template_name = "form.html"
    fields = ["title","description",]
    success_message = "Discussion was successfully Updated!"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Discussion'
        return context
    def form_valid(self,form):
        form.instance.creator = self.request.user
        return super().form_valid(form)  
    def get_success_url(self):
        return reverse('Message_list', kwargs={'discussion_id': self.object.id})

  
    
class DiscussionListView(ListView):
    model = Discussion
    context_object_name = "Discussions"
    paginate_by = 10
    template_name = "Discussion_list.html"
    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        queryset = Discussion.objects.all().order_by('-created_at')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_discussions_by_user = Discussion.objects.values('creator__username').annotate(total_discussions=Count('id')).order_by('-total_discussions')[:10]
        context['top_discussions_by_user'] = top_discussions_by_user

        return context    

    
class MessageCreateView(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    model = Message
    template_name = "form.html"
    fields = ["body"]
    success_message = "Message Successfull!"
    def form_valid(self,form):
        discussion = get_object_or_404(Discussion, pk=self.kwargs['pk'])
        form.instance.discussion = discussion
        form.instance.creator = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('Message_list', kwargs={'discussion_id': self.kwargs['pk']})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Message"
        return context
    

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "Message_list.html"
    context_object_name = "Messages"
    paginate_by = 10

    def get_queryset(self):
        discussion_id = self.kwargs.get('discussion_id')
        if discussion_id:
            return Message.objects.filter(discussion__id=discussion_id).order_by('-created_at')
        else:
            return Message.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        discussion_id = self.kwargs.get('discussion_id')
        if discussion_id:
            discussion = get_object_or_404(Discussion, pk=discussion_id)
            context['discussion'] = discussion
            total_likes = Like.objects.filter(discussion=discussion).count()
            context['total_likes'] = total_likes
            user_has_liked = Like.objects.filter(discussion=discussion, user=self.request.user).exists()
            context['user_has_liked'] = user_has_liked
            participants = Message.objects.filter(discussion=discussion).values('creator__username').annotate(count=Count('creator')).order_by('-count')
            context['participants'] = participants

        return context


class ToggleLikeView(View):
    def get(self, request, *args, **kwargs):
        discussion_id = kwargs.get('discussion_id')
        discussion = get_object_or_404(Discussion, pk=discussion_id)
        user = request.user
        existing_like = Like.objects.filter(discussion=discussion, user=user)
        if existing_like.exists():
            existing_like.delete()
        else:
            Like.objects.create(discussion=discussion, user=user)

        return redirect('Message_list', discussion_id=discussion_id)