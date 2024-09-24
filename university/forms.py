from django import forms

PROGRAM_CATEGORIES = [
    ('Engineering', 'Engineering'),
    ('Computer Science', 'Computer Science'),
    ('Arts', 'Arts'),
    ('Business', 'Business'),
    ('Law', 'Law'),
    ('Social Sciences', 'Social Sciences'),
    ('Health Sciences', 'Health Sciences'),
    ('Education', 'Education'),
    ('Science', 'Science'),
    ('Technology', 'Technology'),
    ('Mathematics', 'Mathematics'),
    ('Physics', 'Physics'),
    ('Chemistry', 'Chemistry'),
    ('Biology', 'Biology'),
    ('Geology', 'Geology'),
    ('Other', 'Other'),
]

RECOMMENDATION_MODE_CHOICES = [
    ('academic', 'Based on Academic Interests'),
    ('location', 'Based on Location'),
]

class RecommendationForm(forms.Form):
    mode = forms.ChoiceField(
        choices=RECOMMENDATION_MODE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label="Recommendation Mode"
    )
    academic_interests = forms.MultipleChoiceField(
        choices=PROGRAM_CATEGORIES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    preferred_location = forms.CharField(
        max_length=255,
        required=False,
        help_text="Enter your preferred city or area."
    )

    def clean(self):
        cleaned_data = super().clean()
        mode = cleaned_data.get('mode')
        academic_interests = cleaned_data.get('academic_interests')
        preferred_location = cleaned_data.get('preferred_location')

        if mode == 'academic' and not academic_interests:
            self.add_error('academic_interests', 'Please select at least one academic interest.')

        if mode == 'location' and not preferred_location:
            self.add_error('preferred_location', 'Please enter a preferred location.')