from django.forms.models import inlineformset_factory
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from apps.rsvp.forms import GroupForm
from apps.rsvp.models import Group, Guest


def rsvp(request):
    query = request.GET.get('q', '').upper()

    if query:
        groups = Group.objects.filter(code=query, invitation_required=True)
    else:
        groups = []

    template_name = 'rsvp/rsvp.html'
    context = {
        'groups': groups,
        'query': query,
    }
    return render_to_response(
        template_name,
        context,
        context_instance=RequestContext(request)
        )


def rsvp_detail(request, **kwargs):
    code = kwargs.get('code', None).upper()
    group = get_object_or_404(Group, code=code)

    template_name = 'rsvp/rsvp_detail.html'
    context = {
        'group': group,
    }
    return render_to_response(
        template_name,
        context,
        context_instance=RequestContext(request)
        )


def rsvp_edit(request, **kwargs):
    code = kwargs.get('code', None).upper()
    group = get_object_or_404(Group, code=code)

    GuestInlineFormSet = inlineformset_factory(Group, Guest,
            extra=group.number_guests, max_num=group.number_guests)
    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        formset = GuestInlineFormSet(request.POST, instance=group)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect(group.get_absolute_url())
    else:
        form = GroupForm(instance=group)
        formset = GuestInlineFormSet(instance=group)

    template_name = 'rsvp/rsvp_edit.html'
    context = {
        'form': form,
        'formset': formset,
        'group': group,
    }
    return render_to_response(
        template_name,
        context,
        context_instance=RequestContext(request)
        )


def stats(request):

    if not request.user.is_staff:
        raise Http404

    template_name = 'rsvp/stats.html'
    context = {
        'bride_no_response_num': Guest.objects.filter(group__party=0, group__response=0).count(),
        'bride_no_response': Group.objects.filter(party=0, response=0).count(),
        'bride_attending_num': Guest.objects.filter(group__party=0, group__response=1).count(),
        'bride_attending': Group.objects.filter(party=0, response=1).count(),
        'bride_not_attending_num': Guest.objects.filter(group__party=0, group__response=2).count(),
        'bride_not_attending': Group.objects.filter(party=0, response=2).count(),

        'groom_no_response_num': Guest.objects.filter(group__party=1, group__response=0).count(),
        'groom_no_response': Group.objects.filter(party=1, response=0).count(),
        'groom_attending_num': Guest.objects.filter(group__party=1, group__response=1).count(),
        'groom_attending': Group.objects.filter(party=1, response=1).count(),
        'groom_not_attending_num': Guest.objects.filter(group__party=1, group__response=2).count(),
        'groom_not_attending': Group.objects.filter(party=1, response=2).count(),

        'meat': Guest.objects.filter(group__response=1, meal=0).count(),
        'fish': Guest.objects.filter(group__response=1, meal=1).count(),
        'veggie': Guest.objects.filter(group__response=1, meal=2).count(),
    }
    return render_to_response(
        template_name,
        context,
        context_instance=RequestContext(request)
        )


