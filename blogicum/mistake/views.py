from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, 'mistake/404.html', status=404)

def csrf_failure(request, reason=''):
    return render(request, 'mistake/403csrf.html', status=403)

def tr_handler500(request):
    return render(request, 'mistake/500.html', status=500)
