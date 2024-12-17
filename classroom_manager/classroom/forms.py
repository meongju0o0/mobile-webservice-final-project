from django import forms
from .models import ClassroomPhoto, Lecture

class ClassroomPhotoForm(forms.ModelForm):
    lecture_id = forms.ModelChoiceField(queryset=Lecture.objects.all(), label="Lecture")

    class Meta:
        model = ClassroomPhoto
        fields = ['image', 'number_of_people', 'lecture_id']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.lecture = self.cleaned_data['lecture_id']
        if commit:
            instance.save()
        return instance