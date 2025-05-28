from django import forms
from .models import Measurements, Trials, Patients

class MeasurementForm(forms.ModelForm):
    trial = forms.ModelChoiceField(
        queryset=Trials.objects.all(),
        label="Выберите исследование",
        empty_label="-- Выберите исследование --"
    )
    drug = forms.ChoiceField(label="Принимаемый препарат")

    class Meta:
        model = Measurements
        fields = ['patient', 'trial', 'condition_score']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # По умолчанию добавляем "Плацебо"
        self.fields['drug'].choices = [("placebo", "Плацебо")]

        # Если форма загружена с данными (POST), подставляем препарат из Trials
        if 'trial' in self.data:
            try:
                trial_id = int(self.data.get('trial'))
                trial = Trials.objects.get(pk=trial_id)
                self.fields['drug'].choices.append((trial.med, trial.med))  # Добавляем препарат из Trials
            except (ValueError, Trials.DoesNotExist):
                pass  # Если исследования нет, оставляем только "Плацебо"




    #condition_score = forms.IntegerField(min_value=0, max_value=100, label="Оценка самочувствия")
    #user_id = forms.IntegerField(min_value=0, label="ID пользователя")
    #trial_name = forms.ChoiceField(choices=[(s, s) for s in STUDIES], label="Исследование")
    #health_score = forms.IntegerField(min_value=0, max_value=100, label="Оценка самочувствия")
    #drug = forms.ChoiceField(choices=DRUG_CHOICES, label="Принимаемый препарат")
