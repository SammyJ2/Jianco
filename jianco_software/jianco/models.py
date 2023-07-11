from django.db import models

class Inches(models.Model):
    gallons = models.DecimalField(primary_key=True, max_digits=10, decimal_places=2)
    inches = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'inches'

class MNR(models.Model):
    dayDay = models.IntegerField(unique=True)
    start_inventory = models.IntegerField()
    gallons_delivered = models.IntegerField(blank=True, null=True)
    gallons_pumped = models.IntegerField(blank=True, null=True)
    book_inventory = models.IntegerField(blank=True, null=True)
    inches = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gallons = models.IntegerField(blank=True, null=True)
    daily = models.IntegerField(blank=True, null=True)
    initials = models.CharField(max_length=2)
    number = models.IntegerField()
    regular = models.IntegerField()
    super = models.IntegerField()
    premium = models.IntegerField()
    day = models.IntegerField(blank=True, null=True)
    start_inventory_p = models.IntegerField()
    gallons_delivered_p = models.IntegerField(blank=True, null=True)
    gallons_pumped_p = models.IntegerField(blank=True, null=True)
    book_inventory_p = models.IntegerField(blank=True, null=True)
    inches_p = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gallons_p = models.IntegerField(blank=True, null=True)
    Dailyy = models.IntegerField(blank=True, null=True)
    initials_p = models.CharField(max_length=2)

    class Meta:
        db_table = 'mnr'

    def save(self, *args, **kwargs):
        # Fetch the nearest Inches value from the 'inches' table for inches
        inches_row = Inches.objects.order_by(models.functions.Abs(models.F('gallons') - self.gallons)).first()
        if inches_row is not None:
            self.inches = inches_row.inches
        else:
            self.inches = 0.0

        # Fetch the nearest Inches value from the 'inches' table for inches_p
        inches_p_row = Inches.objects.order_by(models.functions.Abs(models.F('gallons') - self.gallons_p)).first()
        if inches_p_row is not None:
            self.inches_p = inches_p_row.inches
        else:
            self.inches_p = 0.0

        # Set the dayDay field as 1 plus the number of existing rows
        if not self.dayDay:
            self.dayDay = MNR.objects.count() + 1

        super().save(*args, **kwargs)
