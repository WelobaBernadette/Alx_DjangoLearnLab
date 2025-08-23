from django import forms
from .models import Post, Tag

class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Comma-separated tags")

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

    def save(self, commit=True, *args, **kwargs):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        tags_str = self.cleaned_data.get('tags', '')
        if tags_str:
            tag_names = [t.strip() for t in tags_str.split(',')]
            instance.tags.clear()
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                instance.tags.add(tag)
        return instance
