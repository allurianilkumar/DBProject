from django.core.validators import MinLengthValidator, RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.db.models.functions import Length
from django.db import models

class AuthorAllManager(models.Manager):
    def get_queryset(self):
        #return super().get_queryset().all()
        return super().get_queryset().first()
        #return self.all() # RecursionError: maximum recursion depth
    def name_starts_with(self, prefix):
        # Filter authors whose names start with the given prefix
        return super().get_queryset().filter(name__startswith=prefix)

class AuthorMatchManager(models.Manager):
    def name_starts_with(self, prefix):
        # Filter authors whose names start with the given prefix
        return self.filter(name__startswith=prefix)
    '''
    If useed get_queryset(self): not working self. directly
    '''
    # def get_queryset(self):
    #     #return super().get_queryset().all()
    #     return super().get_queryset().first()


class AuthorQuerySet(models.QuerySet):
    def with_name_length(self, min_length):
        return self.annotate(name_length=Length('name')).filter(name_length__gte=min_length)

def validate_email_domain(value):
    if not value.endswith('@example.com'):
        raise ValidationError('Email must end with @example.com.')
   
class Author(models.Model):
    name = models.CharField(
            max_length=100,
            blank=False,  # Presence validation
            validators=[
            RegexValidator(r'^[A-Za-z\s]+$', 'Name must contain only letters and spaces.')
        ]
    )
    email = models.EmailField(
        unique=True,
         validators=[
            MinLengthValidator(2, 'Email must be at least 2 characters long.'),  # Length validation
            EmailValidator('Enter a valid email address.'),  # Email format validation
            validate_email_domain,  # Custom domain validation
        ]
    )
    def clean(self):
        super().clean()  # Always call the parent clean() method

        # Additional validation in clean()
        if self.email and 'admin' in self.email:
            raise ValidationError({'email': 'Email cannot contain the word "admin".'})
    
    # objects = models.Manager()  # Default manager
    objects = AuthorQuerySet.as_manager() # long_name_authors = Author.objects.with_long_names()

    # objects = AuthorAllManager()  # Custom manager
    match = AuthorMatchManager()  # Custom manager
    '''
    authors_all = Author.objects.all_authors()
    print(authors_all)
    '''

    @staticmethod # print(Author.is_valid_name("JK"))  # Outputs: False
    def is_valid_name(name):
        return len(name) > 2
    @property
    def has_email(self): # print(author.has_email)  # Outputs: True or False
        return bool(self.email)
    # Overriding Model Methods
    def save(self, *args, **kwargs):
        self.name = self.name.title()  # Capitalize name before saving
        super().save(*args, **kwargs)
    
    # Example Function: Full Details
    def full_details(self):
        return f"Author Name: {self.name}"

    # Example Function: Uppercase Name
    def uppercase_name(self):
        return self.name.upper()

    # Example Function: Address Check
    def show_email(self):
        return f"Author Email: {self.email}"

    def __str__(self):
        return self.name

# Child model
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def clean(self):
        super().clean()
        if not self.title.istitle():
            raise ValidationError({'title': 'Book title must be in title case.'})

    def __str__(self):
        return self.title

class Profile(models.Model):
    author = models.OneToOneField(Author, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField()
    date_of_birth = models.DateField()

    def __str__(self):
        return f"Profile of {self.author.name}"

class Genre(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name="genres")

    def __str__(self):
        return self.name
    

# Raw SQL to filter by name length
authors = Author.objects.raw(
    "SELECT id, name FROM your_app_author WHERE LENGTH(name) >= %s", [10]
)

#from django.db.models.functions import Length
#from your_app.models import Author
# Filter directly using Length
#authors = Author.objects.filter(name__length__gte=10)
