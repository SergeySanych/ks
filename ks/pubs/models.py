from django.db import models
from django import forms
from wagtail.models import Page, Orderable, Locale
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, PageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel


# Публикации основной класс
class Pubs(Page):
    localize_default_translation_mode = "simple"
    # Основные поля
    pubs_header = models.CharField(verbose_name="Полное название публикации", max_length=250, blank=True)
    pubs_intro = RichTextField(verbose_name="Короткое описание", blank=True)
    pubs_description = RichTextField(verbose_name="Полное описание", blank=True)
    pubs_photo = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    # Поля категорий и фильтров
    pubs_god = models.IntegerField("Год выхода публикации")
    pubs_author = ParentalManyToManyField('home.Authors', blank=True)
    pubs_topics = ParentalManyToManyField('home.Topics', blank=True)
    pubs_components = ParentalManyToManyField('home.Components', blank=True)
    pubs_countries = ParentalManyToManyField('home.Countries', blank=True)

    # Поля для расширенного контента
    pubs_vitrina = models.BooleanField(verbose_name="Показывать витрину", default=False)

    class ColumnBlock(blocks.StructBlock):
        left = blocks.CharBlock()
        right = blocks.RichTextBlock()

        class Meta:
            template = 'column.html'
            icon = 'user'

    class ImageLeftBlock(blocks.StructBlock):
        imgleft = ImageChooserBlock()
        txtright = blocks.RichTextBlock()

        class Meta:
            template = 'imgleft.html'
            icon = 'image'

    class ImageCenterBlock(blocks.StructBlock):
        imgcenter = ImageChooserBlock()
        imgurl = blocks.URLBlock(required=False)
        txtcenter = blocks.RichTextBlock(required=False)

        class Meta:
            template = 'imgcenter.html'
            icon = 'image'

    pubs_body = StreamField([
        ('heading', blocks.CharBlock(form_classname="subtitle")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('leftheader', ColumnBlock()),
        ('imageleft', ImageLeftBlock()),
        ('imagecenter', ImageCenterBlock()),
        ('htmlcode', blocks.RawHTMLBlock()),
    ], use_json_field=True, blank=True)

    pubs_body_bottom = StreamField([
        ('heading', blocks.CharBlock(form_classname="subtitle")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('leftheader', ColumnBlock()),
        ('imageleft', ImageLeftBlock()),
        ('htmlcode', blocks.RawHTMLBlock()),
    ], use_json_field=True, blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)

        childrenpages = self.get_children().all().live().order_by('first_published_at')
        context['childrenpages'] = childrenpages

        return context

    search_fields = Page.search_fields + [
        index.SearchField('pubs_header', partial_match=True),
        index.SearchField('pubs_intro', partial_match=True),
        index.SearchField('pubs_description', partial_match=True),
        index.SearchField('pubs_body', partial_match=True),
        index.SearchField('pubs_body_bottom', partial_match=True),
        index.FilterField('pubs_god'),
        index.FilterField('pubs_author'),
        index.FilterField('pubs_topics'),
        index.FilterField('pubs_components'),
        index.FilterField('pubs_countries'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('pubs_header', heading='Полное название - показывается на странице, заголовок в меню'),
                FieldPanel('pubs_photo', heading='Титульный лист публикации'),
                FieldPanel('pubs_god', heading='Год выхода публикации'),
                InlinePanel('pubs_documents', label="Список документов"),
                FieldPanel('pubs_intro', heading='Короткое описание - показывается в результатах поиска'),
                FieldPanel('pubs_description', heading='Полное описание - показывается на странице публикации'),
            ],
            heading="Общая информация о публикации",
        ),
        MultiFieldPanel(
            [
                FieldPanel('pubs_author', heading='Авторы публикации'),
                FieldPanel('pubs_topics', heading='Темы'),
                FieldPanel('pubs_components', heading='Разделы'),
                FieldPanel('pubs_countries', heading='Страны'),
            ],
            heading="Информация о связанных страницах",
        ),
        MultiFieldPanel(
            [

                FieldPanel('pubs_body', heading="Верхний блок контента"),
                FieldPanel('pubs_body_bottom', heading="Нижний блок контента, после всего"),
                FieldPanel('pubs_vitrina', heading='Показывать дочерние страницы как картинки'),
            ],
            heading="Дополнительные инструменты создания страниц",
            classname="collapsed",
        ),
    ]

    class Meta:
        verbose_name = "Страница публикации"


class PubDocuments(Orderable):
    pubs_doc_key = ParentalKey(Pubs, on_delete=models.CASCADE, related_name='pubs_documents')
    pubs_doc = models.ForeignKey(
        'wagtaildocs.Document', on_delete=models.CASCADE, related_name='+'
    )
    pubs_doc_caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('pubs_doc'),
        FieldPanel('pubs_doc_caption'),
    ]


# Публикации по разделам
class PubsComponents(Page):

    def get_context(self, request):
        # Filter by cat
        comp = request.GET.get('comp')
        if comp:
            pubs = Pubs.objects.filter(pubs_components__component_name_ru=comp)
            if pubs:
                pubs_comp = pubs.first().pubs_components.filter(component_name_ru=comp)
                if self.locale.language_code == "en":
                    filter_header = 'Component: ' + pubs_comp[0].component_name_en
                else:
                    filter_header = 'Раздел: ' + pubs_comp[0].component_name_ru
            else:
                filter_header = 'Publications not found'
        else:
            pubs = Pubs.objects.all()
            if self.locale.language_code == "en":
                filter_header = 'All publications'
            else:
                filter_header = 'Все публикации'
        # Update template context

        context = super().get_context(request)
        context['pubs'] = pubs
        context['filter'] = 'comp'
        print('заголовок - ')
        print(filter_header)
        context['filter_header'] = filter_header
        return context


# Публикации по темам
class PubsTopics(Page):
    def get_context(self, request):
        # Filter by cat
        topic = request.GET.get('topic')
        if topic:
            pubs = Pubs.objects.filter(pubs_topics__topic_name_ru=topic)
            if pubs:
                pubs_topic = pubs.first().pubs_topics.filter(topic_name_ru=topic)
                if self.locale.language_code == "en":
                    filter_header = 'Topic: ' + pubs_topic[0].topic_name_en
                else:
                    filter_header = 'Тема: ' + pubs_topic[0].topic_name_ru
            else:
                filter_header = 'Publications not found'
        else:
            pubs = Pubs.objects.all()
            if self.locale.language_code == "en":
                filter_header = 'All publications'
            else:
                filter_header = 'Все публикации'
        # Update template context

        context = super().get_context(request)
        context['pubs'] = pubs
        context['filter'] = 'topic'
        print('заголовок - ')
        print(filter_header)
        context['filter_header'] = filter_header
        return context


# Публикации по странам
class PubsCountries(Page):
    def get_context(self, request):
        # Filter by cat
        country = request.GET.get('country')
        if country:
            pubs = Pubs.objects.filter(pubs_countries__country_name_ru=country)
            if pubs:
                pubs_country = pubs.first().pubs_countries.filter(country_name_ru=country)
                if self.locale.language_code == "en":
                    filter_header = 'Country: ' + pubs_country[0].country_name_en
                else:
                    filter_header = 'Страна: ' + pubs_country[0].country_name_ru
            else:
                filter_header = 'Publications not found'
        else:
            pubs = Pubs.objects.all()
            if self.locale.language_code == "en":
                filter_header = 'All publications'
            else:
                filter_header = 'Все публикации'
        # Update template context

        context = super().get_context(request)
        context['pubs'] = pubs
        context['filter'] = 'country'
        print('заголовок - ')
        print(filter_header)
        context['filter_header'] = filter_header
        return context
