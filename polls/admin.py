from django.contrib import admin

from polls.models import (
    Poll,
    Option,
    Vote
)

admin.site.register(Poll)
admin.site.register(Option)
admin.site.register(Vote)

