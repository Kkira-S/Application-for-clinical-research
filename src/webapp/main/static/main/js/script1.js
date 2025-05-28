document.addEventListener("DOMContentLoaded", function () {
    // Пример данных исследований (можно заменить на данные с сервера)
    const studies = [
        "Исследование 1: Эффективность препарата X",
        "Исследование 2: Влияние плацебо на здоровье",
        "Исследование 3: Новый метод лечения Y"
    ];

    const studySelect = document.getElementById("study");

    // Заполняем список исследований
    studies.forEach(study => {
        const option = document.createElement("option");
        option.value = study;
        option.textContent = study;
        studySelect.appendChild(option);
    });

    // Обработка отправки формы
    const form = document.getElementById("medicalForm");
    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Предотвращаем отправку формы

        // Собираем данные формы
        const userId = document.getElementById("userId").value;
        const study = document.getElementById("study").value;
        const wellness = document.getElementById("wellness").value;
        const medication = document.getElementById("medication").value;

        // Выводим данные в консоль (можно отправить на сервер)
        console.log("Идентификатор пользователя:", userId);
        console.log("Исследование:", study);
        console.log("Оценка самочувствия:", wellness);
        console.log("Препарат:", medication);

        alert("Данные успешно отправлены!");
        form.reset(); // Очищаем форму
    });
});