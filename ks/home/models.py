from django.db import models
from django import forms
from django.shortcuts import redirect
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.models import Page, Orderable, Locale
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, FieldRowPanel
from wagtail.admin.edit_handlers import PageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.search.backends.database.postgres.postgres import PostgresSearchQueryCompiler
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.settings.models import BaseSetting, register_setting

# Partial search bug fix
PostgresSearchQueryCompiler.LAST_TERM_IS_PREFIX = True


@register_snippet
class Topics(models.Model):
    topic_name_ru = models.CharField(max_length=255, verbose_name="Название темы на русском")
    topic_name_en = models.CharField(max_length=255, verbose_name="Название темы на английском")

    panels = [
        FieldPanel('topic_name_ru'),
        FieldPanel('topic_name_en'),
    ]

    def __str__(self):
        return self.topic_name_ru

    class Meta:
        verbose_name_plural = 'Темы публикаций'


@register_snippet
class Components(models.Model):
    component_name_ru = models.CharField(max_length=255, verbose_name="Название раздела на русском")
    component_name_en = models.CharField(max_length=255, verbose_name="Название раздела на английском")

    panels = [
        FieldPanel('component_name_ru'),
        FieldPanel('component_name_en'),
    ]

    def __str__(self):
        return self.component_name_ru

    class Meta:
        verbose_name_plural = 'Основные разделы'


@register_snippet
class Countries(models.Model):
    country_name_ru = models.CharField(max_length=255, verbose_name="Название страны на русском")
    country_name_en = models.CharField(max_length=255, verbose_name="Название страны на английском")

    panels = [
        FieldPanel('country_name_ru'),
        FieldPanel('country_name_en'),
    ]

    def __str__(self):
        return self.country_name_ru

    class Meta:
        verbose_name_plural = 'Страны'

@register_snippet
class Avtors(models.Model):
    avtor_full_name = models.CharField(max_length=250, verbose_name="Имя автора")
    avtor_photo = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    avtor_discription = RichTextField(blank=True, verbose_name="Об авторе")

    search_fields = Page.search_fields + [
        index.SearchField('avtor_full_name'),
        index.SearchField('avtor_discription'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('avtor_full_name', heading='Вначале Фамилия, потом Имя или Инициалы'),
        FieldPanel('avtor_discription'),
        FieldPanel('avtor_photo'),
    ]

    def __str__(self):
        return self.avtor_full_name

    class Meta:
        verbose_name = "Об авторе"


class Authors(Page):
    authors_full_name = models.CharField(max_length=250, verbose_name="Имя автора")
    authors_photo = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    authors_discription = RichTextField(blank=True, verbose_name="Об авторе")

    search_fields = Page.search_fields + [
        index.SearchField('authors_full_name'),
        index.SearchField('authors_discription'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('authors_full_name', heading='Вначале Фамилия, потом Имя или Инициалы'),
        FieldPanel('authors_discription'),
        FieldPanel('authors_photo'),
    ]

    class Meta:
        verbose_name = "Об авторе"


class AuthorsList(Page):
    authors_list_discription = RichTextField(blank=True, verbose_name="Описание списка автров")

    content_panels = Page.content_panels + [
        FieldPanel('authors_list_discription'),
    ]

    class Meta:
        verbose_name = "Список Авторов"


class BestPubList(Orderable):
    """Объединяет категории контента в сортируемый список"""
    # menuitempage ссылка на родителя менюпейдж
    bestpub_parent = ParentalKey('home.HomePage', on_delete=models.CASCADE, related_name='bestpub_list')
    #workcategoryitem ссылка на категорию в снипите
    bestpub_item = models.ForeignKey('pubs.Pubs', on_delete=models.CASCADE, related_name='+')

    class Meta(Orderable.Meta):
        verbose_name = "Список популярных публикаций"

    panels = [
        FieldPanel('bestpub_item', heading='Публикация'),
    ]

    def __str__(self):
        return self.pubs.title


class NewPubList(Orderable):
    """Объединяет категории контента в сортируемый список"""
    # menuitempage ссылка на родителя менюпейдж
    newpub_parent = ParentalKey('home.HomePage', on_delete=models.CASCADE, related_name='newpub_list')
    #workcategoryitem ссылка на категорию в снипите
    newpub_item = models.ForeignKey('pubs.Pubs', on_delete=models.CASCADE, related_name='+')

    class Meta(Orderable.Meta):
        verbose_name = "Список новых публикаций"

    panels = [
        FieldPanel('newpub_item', heading='Новые Публикации'),
    ]

    def __str__(self):
        return self.pubs.title

class HomePage(Page):
    # Поля категорий и фильтров
    main_author = ParentalManyToManyField('home.Authors', blank=True)
    main_avtor = ParentalManyToManyField('home.Avtors', blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('main_author', heading='Популярные авторы'),
                FieldPanel('main_avtor', heading='Популярные авторы 2'),
                InlinePanel('bestpub_list', label="Популярные публикации"),
                InlinePanel('newpub_list', label="Новые публикации"),
            ],
            heading="Новые и популярные публикации, Популярные авторы",
        ),
    ]


class Meta:
    verbose_name = "Главная страница"
