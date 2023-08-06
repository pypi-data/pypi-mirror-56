from minutes.cms.common.views import CMSBaseView
from django.views.generic.base import RedirectView
from django.urls import reverse, reverse_lazy
from minutes.models import Vertical, User


class HomeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        role = "REP"
        try:
            role = User.objects.get(user__username=self.request.user).role
        except User.DoesNotExist:
            pass

        if role == "ADV":
            url = reverse_lazy("minutes:cms:interstitial-list")
            return url
        elif role == "ADM":
            url = reverse_lazy("minutes:cms:home-admin")
            return url
        else:
            # Uncomment and replace when there are more verticals...
            # url = reverse_lazy("minutes:cms:vertical-list")
            # return url

            vertical_id = Vertical.objects.get(slug="2020").id
            url = reverse_lazy(
                "minutes:cms:vertical", kwargs={"vertical": vertical_id}
            )
            return url


class HomeAdminView(CMSBaseView):
    template_name = "home-admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = {
            "home": {"name": "Minutes", "url": reverse("minutes:cms:home")}
        }

        return context
