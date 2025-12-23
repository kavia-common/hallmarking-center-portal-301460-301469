from django.db import models

# PUBLIC_INTERFACE
class CenterInfo(models.Model):
    """
    Model representing hallmarking center information.
    Maps to existing 'center_info' table in the database.
    """
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    address = models.TextField()
    contact_email = models.TextField()
    contact_phone = models.TextField()

    class Meta:
        db_table = 'center_info'
        managed = False  # Don't let Django manage this table

    def __str__(self):
        return self.name


# PUBLIC_INTERFACE
class Service(models.Model):
    """
    Model representing hallmarking services offered by the center.
    Maps to existing 'services' table in the database.
    """
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'services'
        managed = False  # Don't let Django manage this table

    def __str__(self):
        return self.name


# PUBLIC_INTERFACE
class Certification(models.Model):
    """
    Model representing certifications held by the hallmarking center.
    Maps to existing 'certifications' table in the database.
    """
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    description = models.TextField()
    issued_date = models.DateField()
    certificate_number = models.TextField()
    services = models.ManyToManyField(
        Service,
        through='ServiceCertification',
        related_name='certifications'
    )

    class Meta:
        db_table = 'certifications'
        managed = False  # Don't let Django manage this table

    def __str__(self):
        return self.title


# PUBLIC_INTERFACE
class ServiceCertification(models.Model):
    """
    Junction table linking services to certifications.
    Maps to existing 'service_certifications' table in the database.
    """
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        db_column='service_id'
    )
    certification = models.ForeignKey(
        Certification,
        on_delete=models.CASCADE,
        db_column='certification_id'
    )

    class Meta:
        db_table = 'service_certifications'
        managed = False  # Don't let Django manage this table
        unique_together = ('service', 'certification')

    def __str__(self):
        return f"{self.service.name} - {self.certification.title}"
