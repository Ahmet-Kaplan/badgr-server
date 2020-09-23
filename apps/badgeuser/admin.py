from django.contrib.admin import ModelAdmin, TabularInline
from django.core.cache import cache
from django.utils import timezone
from django_object_actions import DjangoObjectActions
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.models import ContentType
from django.forms import ModelForm

from externaltools.models import ExternalToolUserActivation
from mainsite.admin import badgr_admin
from mainsite.utils import admin_list_linkify
from mainsite.utils import backoff_cache_key
from staff.models import PermissionedRelationshipBase
from .models import (BadgeUser, EmailAddressVariant,TermsVersion, TermsAgreement, Terms, CachedEmailAddress, UserProvisionment, TermsUrl,
                     UserRecipientIdentifier)


class ExternalToolInline(TabularInline):
    model = ExternalToolUserActivation
    fk_name = 'user'
    fields = ('externaltool',)
    extra = 0


class TermsAgreementInline(TabularInline):
    model = TermsAgreement
    fk_name = 'user'
    extra = 0
    max_num = 0
    can_delete = False
    readonly_fields = ('created_at', 'terms_version')
    fields = ('created_at', 'terms_version')


class EmailAddressInline(TabularInline):
    model = CachedEmailAddress
    fk_name = 'user'
    extra = 0
    fields = ('email', 'verified', 'primary')


class UserRecipientIdentifierInline(TabularInline):
    model = UserRecipientIdentifier
    fk_name = 'user'
    extra = 0
    fields = ('type', 'identifier', 'verified')


class BadgeUserAdmin(UserAdmin):
    readonly_fields = ('email', 'first_name', 'last_name', 'entity_id', 'date_joined', 'last_login', 'username', 'entity_id')
    list_display = ('last_name', 'first_name', 'email', 'is_active', 'is_staff', 'date_joined',
                    admin_list_linkify('institution', 'name'))
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
    search_fields = ('email', 'first_name', 'last_name', 'username', 'entity_id')
    fieldsets = (
        ('Metadata', {'fields': ('entity_id', 'username', 'date_joined',), 'classes': ('collapse',)}),
        (None, {'fields': ('email', 'first_name', 'last_name', 'badgrapp', 'agreed_terms_version', 'marketing_opt_in')}),
        ('Access', {'fields': ('is_active', 'is_staff', 'is_superuser', 'has_usable_password', 'password', 'login_backoff')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
    )
    filter_horizontal = ('groups', 'user_permissions', 'faculty',)
    inlines = [
        EmailAddressInline,
        UserRecipientIdentifierInline,
        ExternalToolInline,
        TermsAgreementInline,
    ]
    change_actions = [
        'clear_login_backoff'
    ]

    def clear_login_backoff(self, request, obj):
        for email in obj.all_verified_recipient_identifiers:
            cache_key = backoff_cache_key(username=email)
            cache.delete(cache_key)
    clear_login_backoff.label = "Clear login backoffs"
    clear_login_backoff.short_description = "Remove blocks created by failed login attempts"

    def login_backoff(self, obj):
        out = []
        for email in obj.all_verified_recipient_identifiers:
            cache_key = backoff_cache_key(username=email)
            backoff = cache.get(cache_key)
            if backoff is not None:
                out.append("<div><strong>{email}</strong>: <span>{until}</span> <span>({count} attempts)</span></div>".format(
                    email=email,
                    until=backoff.get('until').astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%d %H:%M:%S"),
                    count=backoff.get('count')
                ))
        if len(out):
            return "".join(out)
    login_backoff.allow_tags = True

badgr_admin.register(BadgeUser, BadgeUserAdmin)


class EmailAddressVariantAdmin(ModelAdmin):
    search_fields = ('canonical_email', 'email',)
    list_display = ('email', 'canonical_email',)
    raw_id_fields = ('canonical_email',)

badgr_admin.register(EmailAddressVariant, EmailAddressVariantAdmin)


class TermsVersionAdmin(ModelAdmin):
    list_display = ('version','created_at','is_active')
    readonly_fields = ('created_at','created_by','updated_at','updated_by', 'latest_terms_version')
    fieldsets = (
        ('Metadata', {
            'fields': ('created_at','created_by','updated_at','updated_by'),
            'classes': ('collapse',)
        }),
        (None, {'fields': (
            'latest_terms_version', 'is_active','version','short_description',
        )})
    )

    def latest_terms_version(self, obj):
        return TermsVersion.cached.latest_version()
    latest_terms_version.short_description = "Current Terms Version"

badgr_admin.register(TermsVersion, TermsVersionAdmin)


class RecipientIdentifierAdmin(ModelAdmin):
    list_display = ('type', 'identifier', 'user', 'verified')
    list_filter = ('type', 'verified',)
    search_fields = ('identifier', 'user__email')
    raw_id_fields = ('user',)


badgr_admin.register(UserRecipientIdentifier, RecipientIdentifierAdmin)

class TermsInlineForm(ModelForm):
    class Meta:
        model = Terms
        fields = ('terms_type', 'version', 'entity_id')


class TermsInline(TabularInline):
    model = Terms
    extra = 0

    form = TermsInlineForm
    readonly_fields = ('entity_id',)


class TermsUrlInline(TabularInline):
    model = TermsUrl
    extra = 0


class TermsAdmin(ModelAdmin):
    list_display = ('terms_type', admin_list_linkify('institution', 'name'),
                    'version', 'created_at', 'terms_url_count')
    readonly_fields = ('created_at', 'created_by', 'updated_at', 'updated_by', 'entity_id')

    inlines = [TermsUrlInline]

    def terms_url_count(self, obj):
        return len(obj.terms_urls.all())


badgr_admin.register(Terms, TermsAdmin)


class TermsUrlAdmin(ModelAdmin):
    list_display = ('url', 'language', admin_list_linkify('terms', 'terms_type'))


badgr_admin.register(TermsUrl, TermsUrlAdmin)


class UserProvisionmentCreateForm(ModelForm):

    class Meta:
        model = UserProvisionment
        fields = ('email', 'object_id', 'content_type')


class UserProvisionmentAdmin(ModelAdmin):
    form = UserProvisionmentCreateForm
    list_display = ('created_at', 'email', 'type', 'rejected')
    add_form_template = 'admin/custom/userprovisionment_add_form.html'

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.data = PermissionedRelationshipBase.full_permissions()
        obj.for_teacher = True
        obj.type = obj.TYPE_FIRST_ADMIN_INVITATION
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super(UserProvisionmentAdmin, self).get_form(request, obj, **kwargs)
        content_type = ContentType.objects.get(model='institution')
        form.base_fields['content_type'].initial = content_type.id
        form.base_fields['content_type'].disabled = True
        form.base_fields['content_type'].help_text = "This field is not editable"
        form.base_fields['object_id'].help_text = "Set the ID of the institution the invite is for"
        return form


badgr_admin.register(UserProvisionment, UserProvisionmentAdmin)
