# from django.test import TestCase
# from .models import ExceptionLog

# class ExceptionTestCase(TestCase):
#     # Go to a page with no exception
#     # Go to a page with exception
    
    
#     # def setUp(self):
#     #     ExceptionLog.objects.create(name="lion", sound="roar")
#     #     ExceptionLog.objects.create(name="cat", sound="meow")

#     def page_with_no_exception(self):
#         """Pages with no exception are ignored by the middleware"""
#         # Preconditions
#         self.assertEqual(ExceptionLog.objects.count(), 0)
        
#     # def page_with_exception(self):
#     #     """Animals that can speak are correctly identified"""
#     #     lion = Animal.objects.get(name="lion")
#     #     cat = Animal.objects.get(name="cat")
#     #     self.assertEqual(lion.speak(), 'The lion says "roar"')
#     #     self.assertEqual(cat.speak(), 'The cat says "meow"')