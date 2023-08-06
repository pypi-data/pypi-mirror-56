from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin
from django.contrib.admin.options import InlineModelAdmin



class ItemOwnerMixin(BaseModelAdmin):

    owner_field_name = "owner"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        kwargs = {
            self.owner_field_name: request.user,
        }
        queryset = queryset.filter(**kwargs)
        return queryset
