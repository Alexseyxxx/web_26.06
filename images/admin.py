from django.contrib import admin

from images.models import Images, Gallery, Avatar


admin.site.register([Images, Gallery, Avatar])