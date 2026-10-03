from django import forms
from .models import Student
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name", "email", "age", "course",]

    def clean_age(self):
        age = self.cleaned_data["age"]

        if age < 17 or age > 100:
            raise forms.ValidationError(
                "Age must be between 17 and 100."
            )
        return age