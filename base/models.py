from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from django.db.models import Count


from ckeditor.fields import RichTextField



class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
    

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_locations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

class UserRole(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.role


class UserType(models.Model):
    type =  models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type}"
    

class Status(models.Model):
    status =  models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.status}"


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    email       = models.EmailField(blank=True, default='', unique=True)
    name        = models.CharField(max_length=255, blank=True, default='')
    is_active   = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff    = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login  = models.DateTimeField(blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    company     = models.ForeignKey(Company,   on_delete=models.CASCADE, related_name='user_company')
    user_type   = models.ForeignKey(UserType,   on_delete=models.CASCADE, related_name='user_type')
    user_role   = models.ForeignKey(UserRole,   on_delete=models.CASCADE, related_name='user_role', blank=True, null=True)
    location    = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='user_locations',blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name or self.email.split('@')[0]
    
    def __str__(self):
        return f"{self.name}"


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_departments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"





    

class Ticket(models.Model):
    order_id    = models.CharField(max_length=15)
    description = models.TextField('Description', blank=True, null=True)
    post_image  = models.ImageField(upload_to='image/post' ,blank=True, null=True,)
    location    = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='ticket_locations')
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ticket')
    status      = models.ForeignKey(Status,   on_delete=models.CASCADE, related_name='tickt_status', default="6")
    tag         = models.ForeignKey(Tag,   on_delete=models.CASCADE, related_name='tickt_tag',  blank=True, null=True)
    department  = models.ForeignKey(Department,   on_delete=models.CASCADE, related_name='tickt_department', blank=True, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='assigend_to',  blank=True, null=True)
    created_at  = models.DateTimeField(default=timezone.now)
    updated_at  = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        '''
            Function to set time zone for created at and updated at
        '''
        self.updated_at = timezone.now()
        if not self.created_at:
            self.created_at = self.updated_at
        return super().save(*args, **kwargs)


    @staticmethod
    def get_status_counts():
        """
        Returns a dictionary with the count of tickets for each status.
        """
        status_counts = Ticket.objects.values('status__status').annotate(count=Count('status'))
        # Convert the queryset result to a dictionary for easy access
        status_count_dict = {item['status__status']: item['count'] for item in status_counts}
        return status_count_dict

    def __str__(self):
        return f"{self.order_id}"
    
    class Meta:
        ordering = ['-updated_at', ]

    def log_update(self, user, message):
        TicketLog.objects.create(ticket=self, user=user, message=message)

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    comment = RichTextField(blank=False, null=False)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    comment_image= models.ImageField(upload_to='image/comment' ,blank=True, null=True,)

    class Meta:
        ordering = ['modified', ]

    def __str__(self):
        return "%s" % (self.ticket.id)
    

class TicketLog(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.message} At {self.timestamp}"

