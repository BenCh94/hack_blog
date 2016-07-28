from django.test import TestCase
from django.shortcuts import render_to_response
from django.core.urlresolvers import resolve
from .views import post_list, post_details
from .models import Post
from .forms import BlogPostForm
from django import forms
from django.conf import settings

# Create your tests here.
class SimpleTest(TestCase):
    def test_add_two_numbers(self):
        self.assertEqual(1+2, 3)

    def test_add_not_equal(self):
        self.assertNotEqual(2+3, 10)

    def test_home_page_view(self):
        home_page = resolve('/')
        self.assertEqual(home_page.func, post_list)

    def test_post_detail_view(self):
        post_detail = resolve('/blog/5/')
        self.assertEqual(post_detail.func, post_details)

    def test_home_page_status_code_is_good(self):
        home_page = self.client.get('/')
        self.assertEqual(home_page.status_code, 200)


    def test_check_content_is_correct(self):
        post_list_page = self.client.get('/')
        self.assertTemplateUsed(post_list_page, 'blogposts.html')
        post_list_template_output = render_to_response('blogposts.html', {'posts': Post.objects.all()}).content
        self.assertEqual(post_list_page.content, post_list_template_output)


class HomePageTest(TestCase):
    fixtures = ['posts', 'users']
    def test_check_content_is_correct(self):
        post_detail_page = self.client.get('/blog/1/')
        self.assertTemplateUsed(post_detail_page, 'postdetail.html')

        thePost = Post.objects.get(id=1)
        post_detail_template_output = render_to_response('postdetail.html', {'post': thePost}).content
        self.assertEqual(post_detail_page.content, post_detail_template_output)


class CustomUserTest(TestCase):

    def test_blogPost_form(self):
        form = BlogPostForm({
            'title': 'Test Title',
            'content': 'Test Content',
            'image': None,
            'tag': 'Test Tag'
        })

        self.assertTrue(form.is_valid())

    def test_blogPost_form_fails_without_title(self):
        form = BlogPostForm({
            'content': 'Test Content',
            'image': None,
            'tag': 'Test Tag'
        })

        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError,
                                 'please enter a title',
                                 form.full_clean())
