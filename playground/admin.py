from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "amount",
        "currency",
        "status",
        "tx_ref",
        "created_at",
    )

    list_filter = (
        "status",
        "currency",
        "created_at",
    )

    search_fields = (
        "tx_ref",
        "user__email",
        "user__username",
    )

    readonly_fields = (
        "tx_ref",
        "created_at",
    )

    ordering = ("-created_at",)

    date_hierarchy = "created_at"

    list_per_page = 25