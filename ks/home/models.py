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
        FieldPanel('authors_full_name'),
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


class HomePage(Page):
    pass
