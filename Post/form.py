from django import forms


class CreatePostForm(forms.Form):
    title = forms.CharField(label="Title of the Post", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Title of the Post'}))
    content = forms.CharField(label="Content of the post", required=True,
                              widget=forms.Textarea(attrs={'class': 'form-control'}))
    published = forms.BooleanField(initial=True)


class EditPostForm(forms.Form):
    title = forms.CharField(label="Title of the Post", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Title of the Post'}))
    content = forms.CharField(label="Content of the post", required=True,
                              widget=forms.Textarea(attrs={'class': 'form-control'}))
