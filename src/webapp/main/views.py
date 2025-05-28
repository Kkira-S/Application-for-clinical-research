from django.shortcuts import render, redirect
from django.db.models import Avg
from django.db import IntegrityError
from .forms import MeasurementForm
from .models import Trials, Measurements, Patients

def index(request):
    trials = Trials.objects.all()

    if request.method == "POST":
        form = MeasurementForm(request.POST)

        if form.is_valid():
            try:
                measurement = form.save(commit=False)
                measurement.trial = form.cleaned_data['trial']
                measurement.drug = form.cleaned_data['drug']
                measurement.save()

                print(f"✅ Данные сохранены: {measurement}")

                avg_score = Measurements.objects.filter(
                    trial=measurement.trial, drug=measurement.drug
                ).aggregate(Avg('condition_score'))['condition_score__avg']

                print(f"📊 Среднее значение: {avg_score}")

                if avg_score is not None:
                    lower_bound = avg_score * 0.9
                    upper_bound = avg_score * 1.1
                    in_range = lower_bound <= measurement.condition_score <= upper_bound

                    message = (
                        "✅ Ваше самочувствие в норме."
                        if in_range else "⚠ Ваше самочувствие выходит за пределы нормы."
                    )
                else:
                    message = "❌ Недостаточно данных для анализа."

                return render(request, "main/result.html", {"message": message})

            except IntegrityError as e:
                print(f"❌ Ошибка базы данных: {e}")
                form.add_error(None, "❌ Ошибка базы данных. Попробуйте снова.")
        else:
            print("❌ Ошибки формы:", form.errors)

    else:
        form = MeasurementForm()

    return render(request, "main/index.html", {"form": form, "trials": trials})