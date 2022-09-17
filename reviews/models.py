from django.contrib import auth
from django.db import models


class Publisher(models.Model):
    """A company that publishes books."""
    name = models.CharField(max_length=50, help_text="name of Publisher.")	# for large text use TextField
    website = models.URLField(help_text="Publisher's website.")			    # validates URL
    email = models.EmailField(help_text="Publisher's email address.")		# validates email format

    def __str__(self):
        return self.name


class Book(models.Model):
    """A published book."""
    title = models.CharField(max_length=70, help_text="title of book.")
    publication_date = models.DateField(verbose_name="Date book was published.")
    isbn = models.CharField(max_length=20, verbose_name="ISBN number of book.")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    contributors = models.ManyToManyField('Contributor', through="BookContributor")
    cover = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    sample = models.FileField(upload_to='book_samples/', null=True, blank=True
                              )
    def __str__(self):
        return f"{self.title} ({self.isbn})"

    def isbn13(self):   # used in class BookAdmin
        """ '9780316769174' => '978-0-31-676917-4' """
        return "{}-{}-{}-{}-{}".format(self.isbn[0:3], self.isbn[3:4], self.isbn[4:6], self.isbn[6:12],
                                       self.isbn[12:13])

class Contributor(models.Model):
    """A contributor to a Book, e.g. author, editor, co-author."""
    first_names = models.CharField(max_length=50, help_text="contributor's first name or names.")
    last_names = models.CharField(max_length=50, help_text="contributor's last name or names.")
    email = models.EmailField(help_text="contact email for contributor.")

    def initialled_name(self):
        """ obj.first_names='Jerome David', obj.last_names='Salinger' => 'Salinger, JD' """
        name = f"{self.last_names}, "
        for word in self.first_names.split():
            name += word[0]
        return name
        # implementation from book
        initials = ''.join([name[0] for name in obj.first_names.split(' ')])
        return "{}, {}".format(obj.last_names, initials)

    def __str__(self):
#        return self.first_names
        return self.initialled_name()

    def number_contributions(self):
        return self.bookcontributor_set.count()

class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):	# subclass - defines set of choices
        AUTHOR = "AUTHOR", "Author"
        CO_AUTHOR = "CO_AUTHOR", "Co-Author"
        EDITOR = "EDITOR", "Editor"

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    role = models.CharField(verbose_name="The role this contributor had in the book.",
                            choices=ContributionRole.choices, max_length=20)

    def __str__(self):
        return "{} {} {}".format(self.contributor.initialled_name(), self.role, self.book.isbn)


class Review(models.Model):
    content = models.TextField(help_text="Review text.")
    rating = models.IntegerField(help_text="rating reviewer has given.")
    date_created = models.DateTimeField(auto_now_add=True, help_text="date and time review was created.")
    date_edited = models.DateTimeField(null=True, help_text="The date and time review was last edited.")
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, help_text="Book that this review is for.")

    def __str__(self):
        return "{} - {}".format(self.creator.username, self.book.title)
