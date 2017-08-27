from django.contrib import admin

# Register your models here.

from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import IndexPage, Category,Project, ProjectPhoto, \
                    ContactPerson, ContactPhone, ContactEmail, ProjectCommentatorSecret, ProjectComment

class WysiwygAdmin(admin.ModelAdmin):

    class Meta:
        wysiwyg_fields = ('description', 'body')

    #class Media:
    #    js = ('%stiny_mce/tiny_mce.js' % settings.STATIC_URL,
    #          '%sjs/wysiwyg.js' % settings.STATIC_URL,)

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(WysiwygAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in self.Meta.wysiwyg_fields:
            # field.widget.attrs['class'] = 'wysiwyg %s' % field.widget.attrs.get('class', '')
            #field.widget = TinyMCE(attrs={'cols': 100, 'rows': 20})
            field.widget = CKEditorUploadingWidget()  # CKEditorWidget()
        return field

class ProjectPhotoAdmin(admin.TabularInline):
    model = ProjectPhoto
    extra = 0


class ProjectAdmin(WysiwygAdmin):
    model = Project
    inlines = [ProjectPhotoAdmin]

admin.site.register(Project, ProjectAdmin)

class IndexPageAdmin(WysiwygAdmin):
    model = IndexPage

admin.site.register(IndexPage, IndexPageAdmin)

admin.site.register(Category)
# admin.site.register(Segment)

# class WorkerAdmin(WysiwygAdmin):
#     model = Worker

# admin.site.register(Worker, WorkerAdmin)

# class JobCategoryAdmin(WysiwygAdmin):
#     model = JobCategory
#
# admin.site.register(JobCategory, JobCategoryAdmin)
#
# class JobAdmin(WysiwygAdmin):
#     model = Job
#
# admin.site.register(Job, JobAdmin)

class ContactPhoneAdmin(admin.TabularInline):
    model = ContactPhone

class ContactEmailAdmin(admin.TabularInline):
    model = ContactEmail

class ContactPersonAdmin(admin.ModelAdmin):
    model = ContactPerson
    inlines = [ContactPhoneAdmin, ContactEmailAdmin]

admin.site.register(ContactPerson, ContactPersonAdmin)

admin.site.register(ProjectCommentatorSecret)
admin.site.register(ProjectComment)