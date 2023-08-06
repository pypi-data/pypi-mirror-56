""" Import functions and methods. """
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.views.generic import (ListView, DetailView, CreateView,
UpdateView, DeleteView, FormView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
""" import from local app. """
from .models import CategoryModelScheme, ArticleModelScheme
from .forms import CategoryFormScheme, ArticleFormScheme


""" Password protected view, Dashboard view for apptwo app. """
# ArticleListDashboard view returns the list of articles.
class ArticleListDashboard(LoginRequiredMixin, ListView):
    template_name = 'djangoadmin/djangoarticle/article_list_dashboard.html'
    context_object_name = 'article_filter'

    def get_queryset(self):
        article_filter = ArticleModelScheme.objects.by_author(self.request.user)
        query = self.request.GET.get("query")
        if query:
            article_match = ArticleModelScheme.objects.by_author(self.request.user).filter(Q(title__icontains=query))
            if article_match:
                return article_match
            else:
                return article_filter
        else:
            return article_filter
        return article_filter


""" Password protected view, manage category view for apptwo app. """
# CategoryListDashboard returns the list of category
class CategoryListDashboard(LoginRequiredMixin, ListView):
    template_name = 'djangoadmin/djangoarticle/category_list_dashboard.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        category_list = CategoryModelScheme.objects.all()
        query = self.request.GET.get("query")
        if query:
            category_match = CategoryModelScheme.objects.by_author(self.request.user).filter(Q(title__icontains=query))
            if category_match:
                return category_match
            else:
                return category_list
        else:
            return category_list
        return category_list


# Djangoarticle Home view.
class ArticleListView(ListView):
    template_name = 'djangoadmin/djangoarticle/article_list_view.html'
    context_object_name = 'article_filter'

    def get_queryset(self):
        return ArticleModelScheme.objects.filter_publish().filter(is_promote=False)

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['is_promoted'] = ArticleModelScheme.objects.filter_promoted()
        context['is_trending'] = ArticleModelScheme.objects.filter_trending()
        return context


# Djangoarticle Category view.
class CategoryDetailView(ListView):
    template_name = 'djangoadmin/djangoarticle/category_detail_view.html'
    slug_url_kwarg = 'category_slug'
    context_object_name = 'article_filter'

    def get_queryset(self):
        self.category_detail = get_object_or_404(CategoryModelScheme, slug=self.kwargs['category_slug'])
        return ArticleModelScheme.objects.filter(category=self.category_detail)

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['category_detail'] = self.category_detail
        return context


""" Start a full featured ArticleDetailView for GET method. """
class ArticleDetailView(DetailView):
    model = ArticleModelScheme
    template_name = 'djangoadmin/djangoarticle/article_detail_view.html'
    context_object_name = 'article_detail'
    slug_url_kwarg = 'article_slug'

    def get_object(self, **kwargs):
        object = super(ArticleDetailView, self).get_object(**kwargs)
        object.total_views += 1
        object.save()
        return object


""" Password protected view, category create view for apptwo app. """
class CategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CategoryFormScheme
    template_name = 'djangoadmin/djangoarticle/category_create_view_form.html'
    success_url = reverse_lazy('djangoarticle:category_list_dashboard')
    success_message = "Category created successfully."

    def get_success_message(self, cleaned_data):
        return "{0} {1}".format(cleaned_data["title"], self.success_message)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(CategoryCreateView, self).form_valid(form)

    def form_invalid(self, form):
        message = f"{form.instance.title} category not created! Please try some different keywords."
        messages.add_message(self.request, messages.WARNING, message)
        return redirect("djangoarticle:category_list_dashboard")

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['category_form'] = context['form']
        return context


""" Password protected view, category update view for apptwo app. """
class CategoryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CategoryModelScheme
    form_class = CategoryFormScheme
    template_name = 'djangoadmin/djangoarticle/category_create_view_form.html'
    success_url = reverse_lazy('djangoarticle:category_list_dashboard')
    slug_url_kwarg = 'category_slug'
    success_message = "Category updated successfully."

    def get_success_message(self, cleaned_data):
        return "{} {}".format(cleaned_data["title"], self.success_message)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(CategoryUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        message = f"Sorry! {form.instance.title} category not updated."
        messages.add_message(self.request, messages.WARNING, message)
        return redirect("djangoarticle:category_list_dashboard")

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['category_form'] = context['form']
        return context


""" Password protected view, category delete view for apptwo app. """
class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = CategoryModelScheme
    context_object_name = 'category_detail'
    template_name = 'djangoadmin/djangoarticle/category_delete_view_form.html'
    success_url = reverse_lazy('djangoarticle:category_list_dashboard')
    slug_url_kwarg = 'category_slug'
    success_message = "category deleted successfully."

    def delete(self, request, *args, **kwargs):
        message = f"{kwargs['category_slug']} {self.success_message}"
        messages.add_message(self.request, messages.WARNING, message)
        return super(CategoryDeleteView, self).delete(request, *args, **kwargs)


""" Password protected view, article create view for apptwo app. """
class ArticleCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = ArticleFormScheme
    template_name = 'djangoadmin/djangoarticle/article_create_view_form.html'
    success_url = reverse_lazy('djangoarticle:article_list_dashboard')
    success_message = "article created successfully."

    def get_success_message(self, cleaned_data):
        return f"{cleaned_data['title']} {self.success_message}"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(ArticleCreateView, self).form_valid(form)

    def form_invalid(self, form):
        message = f"{form.instance.title} article not created! Please try some different keywords."
        messages.add_message(self.request, messages.WARNING, message)
        return redirect("djangoarticle:article_list_dashboard")

    def get_context_data(self, **kwargs):
        context = super(ArticleCreateView, self).get_context_data(**kwargs)
        context['article_form'] = context['form']
        return context


""" Password protected view, article update view for apptwo app. """
class ArticleUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ArticleModelScheme
    form_class = ArticleFormScheme
    template_name = 'djangoadmin/djangoarticle/article_create_view_form.html'
    success_url = reverse_lazy('djangoarticle:article_list_dashboard')
    slug_url_kwarg = 'article_slug'
    success_message = "article updated successfully."

    def get_success_message(self, cleaned_data):
        return f"{cleaned_data['title']} {self.success_message}"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(ArticleUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        message = f"{form.instance.title} article not updated! Please try some different keywords."
        messages.warning(self.request, message)
        return redirect("djangoarticle:article_list_dashboard")

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdateView, self).get_context_data(**kwargs)
        context['article_form'] = context['form']
        return context


""" Password protected view, article delete view for apptwo app. """
class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = ArticleModelScheme
    context_object_name = 'article_detail'
    template_name = 'djangoadmin/djangoarticle/article_delete_view_form.html'
    success_url = reverse_lazy('djangoarticle:article_list_dashboard')
    slug_url_kwarg = 'article_slug'
    success_message = "article deleted successfully."

    def delete(self, request, *args, **kwargs):
        message = f"{kwargs['article_slug']} {self.success_message}."
        messages.warning(self.request, message)
        return super(ArticleDeleteView, self).delete(request, *args, **kwargs)