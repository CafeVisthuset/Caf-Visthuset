from django.shortcuts import render
from django.http.response import HttpResponse


def CleanIndexView(request):
    return render(request, 'cleaning/CleanIndex.html')

def Results(request):
    return HttpResponse("Du har nu angett temperaturen")

'''

register = template.Library()
@register.inclusion_tag('cleaning/_name.html')
def get_cold_unit(related_object):
    related_object_type = ContentType.objects.get_for_model(related_object)
    clean = Clean.objects.filter(
        content_type__pk=related_object_type.id,
        object_id=related_object.id,
        ).first()
    return {'clean': clean}
'''