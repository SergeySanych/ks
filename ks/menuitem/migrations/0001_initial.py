# Generated by Django 4.1.7 on 2023-03-28 09:24

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0083_workflowcontenttype'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('menupage_header', models.CharField(blank=True, max_length=250)),
                ('menupage_date', models.DateField(verbose_name='Дата публикации')),
                ('menupage_vitrina', models.BooleanField(default=False, verbose_name='Показывать витрину')),
                ('menupage_left', models.BooleanField(default=False, verbose_name='Показывать слева')),
                ('menupage_slider', models.BooleanField(default=False, verbose_name='НЕ показывать слайдер сверху')),
                ('menupage_body', wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='subtitle')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('leftheader', wagtail.blocks.StructBlock([('left', wagtail.blocks.CharBlock()), ('right', wagtail.blocks.RichTextBlock())])), ('imageleft', wagtail.blocks.StructBlock([('imgleft', wagtail.images.blocks.ImageChooserBlock()), ('txtright', wagtail.blocks.RichTextBlock())])), ('imagecenter', wagtail.blocks.StructBlock([('imgcenter', wagtail.images.blocks.ImageChooserBlock()), ('imgurl', wagtail.blocks.URLBlock(required=False)), ('txtcenter', wagtail.blocks.RichTextBlock(required=False))])), ('htmlcode', wagtail.blocks.RawHTMLBlock())], blank=True, use_json_field=True)),
                ('menupage_body_bottom', wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='subtitle')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('leftheader', wagtail.blocks.StructBlock([('left', wagtail.blocks.CharBlock()), ('right', wagtail.blocks.RichTextBlock())])), ('imageleft', wagtail.blocks.StructBlock([('imgleft', wagtail.images.blocks.ImageChooserBlock()), ('txtright', wagtail.blocks.RichTextBlock())])), ('htmlcode', wagtail.blocks.RawHTMLBlock())], blank=True, use_json_field=True)),
            ],
            options={
                'verbose_name': 'Страница для пукнта меню',
                'verbose_name_plural': 'Страницы в пункте меню',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='MenuPageGalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('menupage_image_caption', models.CharField(blank=True, max_length=250)),
                ('menupage_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.image')),
                ('menupage_key', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='menupage_gallery_images', to='menuitem.menupage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
