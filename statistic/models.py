from django.conf import settings
from django.db import models


class Report(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports"
    )
    report_date = models.DateField(auto_now_add=True)
    report_info = models.TextField()

    def __str__(self):
        return f"Report for {self.user.username} on {self.report_date}"
