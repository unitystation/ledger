from django.contrib import admin

from django.contrib import admin
from .models import Movement, MovementTemplate
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.utils.html import format_html

@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    readonly_fields = ('balance_after',)
    list_display = ('description', 'type', 'amount_usd', 'balance_after', 'created_at')

    def get_changeform_initial_data(self, request):
        return {
            key: request.GET.get(key) for key in ['type', 'description', 'notes', 'amount_usd']
            if key in request.GET
        }

@admin.register(MovementTemplate)
class MovementTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'use_button',  'type', 'description', 'amount_usd')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'use/<int:pk>/',
                self.admin_site.admin_view(self.use_recurrent_movement),
                name='use-recurrent-movement',
            ),
        ]
        return custom_urls + urls

    def use_button(self, obj):
        url = reverse('admin:use-recurrent-movement', args=[obj.pk])
        return format_html('<a class="button" href="{}">Use</a>', url)
    use_button.short_description = "Use"
    use_button.allow_tags = True

    def use_recurrent_movement(self, _, pk):
        recurrent = MovementTemplate.objects.get(pk=pk)
        add_url = (
                reverse("admin:transactions_movement_add") +
                f"?type={recurrent.type}&description={recurrent.description}"
                f"&notes={recurrent.notes or ''}&amount_usd={recurrent.amount_usd}"
        )
        return HttpResponseRedirect(add_url)