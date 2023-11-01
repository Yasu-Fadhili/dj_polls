from django.contrib import admin
from polls.models import Poll, Option, Vote, Comment

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1

class VoteInline(admin.TabularInline):
    model = Vote
    extra = 1

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'expiry_date', 'visibility', 'created_at', 'updated_at')
    list_filter = ('visibility',)
    search_fields = ('question', 'created_at')
    inlines = [OptionInline, CommentInline, VoteInline]

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('option', 'poll', 'created_at', 'updated_at')
    list_filter = ('poll',)
    search_fields = ('option', 'poll__question')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'poll', 'author', 'created_at', 'updated_at')
    list_filter = ('poll',)
    search_fields = ('content', 'poll__question')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('author', 'poll', 'option', 'created_at', 'updated_at')
    list_filter = ('poll', 'option')
    search_fields = ('author__username', 'poll__question', 'option__option')

admin.site.site_header = "My Polls Admin"
admin.site.site_title = "My Polls Admin"
