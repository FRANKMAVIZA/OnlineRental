from django.shortcuts import render
from django.views.generic import (TemplateView, DetailView,
                                    ListView, CreateView,
                                    UpdateView,DeleteView,FormView,)
from .models import Cities, Apartment, Comment
from django.urls import reverse_lazy
from .forms import CommentForm,ReplyForm, ApartmentForm
from django.http import HttpResponseRedirect



class CitiesListView(ListView):
    context_object_name = 'cities'
    model = Cities
    template_name = 'onlinerental/standard_list_view.html'


class ApartmentListView(DetailView):
    context_object_name = 'cities'
    model = Cities
    template_name = 'onlinerental/lesson_list_view.html'

class ApartmentDetailView(DetailView, FormView):
    context_object_name = 'cities'
    model = Apartment
    template_name = 'onlinerental/lesson_detail_view.html'
    form_class = CommentForm
    second_form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super(ApartmentDetailView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(request=self.request)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(request=self.request)
        # context['comments'] = Comment.objects.filter(id=self.object.id)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'

        form = self.get_form(form_class)
        # print("the form name is : ", form)
        # print("form name: ", form_name)
        # print("form_class:",form_class)

        if form_name=='form' and form.is_valid():
            print("comment form is returned")
            return self.form_valid(form)
        elif form_name=='form2' and form.is_valid():
            print("reply form is returned")
            return self.form2_valid(form)


    def get_success_url(self):
        self.object = self.get_object()
        cities = self.object.Cities
        return reverse_lazy('onlinerental:lesson_detail', kwargs={'cities':cities.slug,

                                                             'slug':self.object.slug})
    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.lesson_name = self.object.comments.name
        fm.lesson_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        fm.save()
        return HttpResponseRedirect(self.get_success_url())


class ApartmentCreateView(CreateView):
    # fields = ('lesson_id','name','position','image','video','ppt','Notes')
    form_class = ApartmentForm
    context_object_name = 'apartment'
    model = Cities
    template_name = 'onlinerental/lesson_create.html'

    def get_success_url(self):
        self.object = self.get_object()
        cities = self.object.cities
        return reverse_lazy('onlinerental:lesson_list',kwargs={'cities':cities.slug,
                                                             'slug':self.object.slug})


    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.Cities = self.object.cities
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

class ApartmentUpdateView(UpdateView):
    fields = ('name','position','video','ppt','Notes')
    model = Apartment
    template_name = 'onlinerental/lesson_update.html'
    context_object_name = 'apartment'

class ApartmentDeleteView(DeleteView):
    model = Apartment
    context_object_name = 'apartment'
    template_name = 'onlinerental/lesson_delete.html'

    def get_success_url(self):
        print(self.object)
        cities = self.object.Cities

        return reverse_lazy('onlinerental:lesson_list',kwargs={'cities':cities.slug})
