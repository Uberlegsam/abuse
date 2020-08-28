from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from .models import (
    Articles,
    Page,
    Block,
    Main_Cat,
    Organizations,
    City,
    ServicesType,
    PageType,
    OrganizationServices
)


def main_page(request):
    all_cats = Main_Cat.objects.filter(is_active=True)
    down_cats = all_cats.filter(header_menu='down')
    up_cats = all_cats.filter(header_menu='up')
    return render(
        request,
        template_name='main_page.html',
        context={'down_cats': down_cats,
                 'up_cats': up_cats,
                 })


def articles_by_cat(request, slug, choosed_city=None, choosed_type=None):
    if Main_Cat.objects.get(slug=slug).org_widget:
        orgs = Organizations.objects.all().prefetch_related('organizationservices_set')
        org_widget_flag = True
    else:
        orgs = None
        org_widget_flag = False

    category_number = Main_Cat.objects.get(slug=slug).id
    all_cites = City.objects.filter()
    all_types = ServicesType.objects.filter()
    all_cats = Main_Cat.objects.filter(is_active=True)
    down_cats = all_cats.filter(header_menu='down')
    up_cats = all_cats.filter(header_menu='up')

    articles = Articles.objects.filter(category__id=category_number)
    return render(
        request,
        template_name='Main_Article.html',
        context={'articles': articles,
                 'orgs': orgs,
                 'org_widget_flag': org_widget_flag,
                 'all_cites': all_cites,
                 'all_types': all_types,
                 'all_cats': all_cats,
                 'down_cats': down_cats,
                 'up_cats': up_cats,
                 })


def org_info(request, slug):
    org = Organizations.objects.get(slug=slug)

    return render(
        request,
        template_name='organizations.html',
        context={'org': org}
    )


def news_view(request):
    news_type = PageType.objects.get(type='Новость')
    news = Page.objects.filter(type=news_type)

    return render(
        request,
        template_name='news.html',
        context={
            'news': news,
        }
    )

# https://stackoverflow.com/questions/29758558/inlineformset-factory-create-new-objects-and-edit-objects-after-created
from .forms import OrgForm, OrgServsForm
from django.forms import inlineformset_factory
def add_new_org(request):  # https://stackoverflow.com/questions/1113047/creating-a-model-and-related-models-with-inline-formsets
    if request.method == 'POST':
        org_form = OrgForm(request.POST)
        ServFormset = inlineformset_factory(Organizations, OrganizationServices, exclude=[])
        # formset = ServFormset(request.POST)
        if org_form.is_valid():
            new_org = org_form.save(commit=False)
            new_org.slug = request.POST['title']
            formset = ServFormset(request.POST, instance=new_org)
            if formset.is_valid():
                new_org.save()
                formset.save()
                return HttpResponse('kkk')
        else:
            return HttpResponse(1341)
    else:
        form = OrgForm()
        OrgFomset = inlineformset_factory(Organizations, OrganizationServices, exclude=(), extra=5)
        formset = OrgFomset()
        return render(
            request,
            template_name='add_new_org.html',
            context={
                'form': form,
                'formset': formset,
            }
        )
