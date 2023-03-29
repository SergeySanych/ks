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


class MenuPage(Page):
    localize_default_translation_mode = "simple"

    menupage_header = models.CharField(max_length=250, blank=True)
    menupage_date = models.DateField("Дата публикации")
    menupage_vitrina = models.BooleanField(verbose_name="Показывать витрину", default=False)
    menupage_left = models.BooleanField(verbose_name="Показывать слева", default=False)
    menupage_slider = models.BooleanField(verbose_name="НЕ показывать слайдер сверху", default=False)

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

    menupage_body = StreamField([
        ('heading', blocks.CharBlock(form_classname="subtitle")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('leftheader', ColumnBlock()),
        ('imageleft', ImageLeftBlock()),
        ('imagecenter', ImageCenterBlock()),
        ('htmlcode', blocks.RawHTMLBlock()),
    ], use_json_field=True, blank=True)

    menupage_body_bottom = StreamField([
        ('heading', blocks.CharBlock(form_classname="subtitle")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('leftheader', ColumnBlock()),
        ('imageleft', ImageLeftBlock()),
        ('htmlcode', blocks.RawHTMLBlock()),
    ], use_json_field=True, blank=True)

    def main_image(self):
        gallery_item = self.menupage_gallery_images.first()
        if gallery_item:
            return gallery_item.menupage_image
        else:
            return None

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)

        childrenpages = self.get_children().all().live().order_by('first_published_at')
        context['childrenpages'] = childrenpages

        return context

    search_fields = Page.search_fields + [
        index.SearchField('menupage_header', partial_match=True),
        index.SearchField('menupage_body', partial_match=True),
        index.SearchField('menupage_body_bottom', partial_match=True),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('menupage_header', heading='Расширенный заголовок - показывается на странице, заголовок в меню'),
                FieldPanel('menupage_date'),
            ],
            heading="Общая информация о странице",
            classname="collapsed",
        ),

        FieldPanel('menupage_body', heading="Верхний блок контента"),
        FieldPanel('menupage_body_bottom', heading="Нижний блок контента, после всего"),
        InlinePanel('menupage_gallery_images', label="Фото галерея"),
        FieldRowPanel(
            [
                FieldPanel('menupage_vitrina', heading='Показывать дочерние страницы как проекты'),
                FieldPanel('menupage_left', heading='Показывать ссылки на дочерние страницы в левой колонке'),
                FieldPanel('menupage_slider', heading='НЕ показывать слайдер'),
            ],
            heading="Отображение элементов страницы",
        ),
    ]

    class Meta:
        verbose_name = "Страница для пукнта меню"
        verbose_name_plural = "Страницы в пункте меню"


class MenuPageGalleryImage(Orderable):
    menupage_key = ParentalKey(MenuPage, on_delete=models.CASCADE, related_name='menupage_gallery_images')
    menupage_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    menupage_image_caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('menupage_image'),
        FieldPanel('menupage_image_caption'),
    ]
