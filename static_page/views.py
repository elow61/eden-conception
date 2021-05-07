""" All views in the frontend web application """
from django.shortcuts import render
from django.views import View


class IndexView(View):
    """ Homepage view """

    template_name = 'static_page/index.html'

    def get(self, request):
        return render(request, self.template_name)


# class LegalNoticeView(View):
#     """ Legal Notice view """

#     template_name = 'static_page/legal_notice.html'

#     def get(self, request):
#         return render(request, self.template_name)
