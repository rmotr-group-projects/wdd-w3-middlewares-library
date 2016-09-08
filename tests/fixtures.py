import factory
from factory.fuzzy import FuzzyInteger, FuzzyDecimal

from entries.models import Blog, Author, Entry, COUNTRY_CHOICES


class BlogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Blog

    name = factory.Sequence(lambda n: 'Blog {0}'.format(n + 1))
    tagline = 'Some tagline'


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Faker('name')
    email = factory.Sequence(lambda n: 'author{0}@example.com'.format(n))
    nationality = COUNTRY_CHOICES[0][1]


class EntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Entry

    blog = factory.SubFactory(BlogFactory)
    headline = 'Some headline'
    body_text = 'Some body text'
    number_comments = FuzzyInteger(100)
    scoring = FuzzyDecimal(0.00, 9.99)
