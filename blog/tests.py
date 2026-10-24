from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Post


class BlogTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Тестові дані: створюються в окремій тимчасовій базі, твою базу не чіпають
        user = User.objects.create_user(username='tester',
                                        password='test-pass')
        cls.published = Post.objects.create(
            title='Опублікований пост',
            slug='published',
            body='Текст опублікованого поста',
            author=user,
            status=Post.Status.PUBLISHED,
        )
        cls.draft = Post.objects.create(
            title='Чернетка',
            slug='draft',
            body='Текст чернетки',
            author=user,
            status=Post.Status.DRAFT,
        )

    def test_post_str(self):
        """Пост показує свій заголовок як назву"""
        self.assertEqual(str(self.published), 'Опублікований пост')

    def test_list_page_opens(self):
        """Головна сторінка відкривається"""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)

    def test_list_shows_only_published(self):
        """На головній є опублікований пост, а чернетки немає"""
        response = self.client.get(reverse('blog:post_list'))
        self.assertContains(response, 'Опублікований пост')
        self.assertNotContains(response, 'Чернетка')

    def test_detail_page_opens(self):
        """Сторінка опублікованого поста відкривається"""
        response = self.client.get(
            reverse('blog:post_detail', args=[self.published.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Текст опублікованого поста')

    def test_draft_returns_404(self):
        """Чернетку не можна відкрити за посиланням (помилка 404)"""
        response = self.client.get(
            reverse('blog:post_detail', args=[self.draft.id]))
        self.assertEqual(response.status_code, 404)

    def test_admin_login_page_opens(self):
        """Сторінка входу в адмінку відкривається"""
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)