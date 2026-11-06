# TaskFlow

Навчальний PWA-менеджер завдань на Vue 3, Framework7 і Vite.

## Запуск

```sh
npm install
npm run dev
```

Production-збірка: `npm run build`; локальний перегляд: `npm run preview`.

## Можливості

- Головна зі статистикою (10 / 3 у роботі / 3 виконано / 4 заплановано) та прогресом 30%.
- Повторно використовувані TaskCard, StatusBadge, PriorityBadge та TaskCounter.
- Спільне реактивне сховище; зміна статусу і пріоритету через Props та Emits.
- Поєднані фільтри, сортування пріоритету, вибір завдання з переглядом деталей.
- Адаптивний інтерфейс, фіксована навігація, сторінки About/Help.
- PWA manifest і service worker у production-збірці.

Стан зберігається у пам’яті й скидається після перезавантаження (відповідно до методички).

## Практична робота № 4 (2-6.pdf)

- Створення й редагування через TaskForm, локальна копія та скасування.
- Валідація у формі та сховищі, попередній перегляд, повідомлення про збереження.
- Усі 7 додаткових завдань: категорії, перевірка дати, залишок символів, очищення, доступність, живий пошук, унікальність нових назв.
- Звіт: [PDF](output/pdf/TaskFlow_forms_report.pdf), [текст](reports/practice4/report.md), [перевірки T1-T8](reports/practice4/verification.json).
- Початкових записів 10. Стару дату можна залишити при редагуванні; нова дата має бути не в минулому.

Повторення перевірок: запустіть `npm run dev`, встановіть Playwright окремо (`npm install --no-save --package-lock=false playwright`), використайте встановлений Google Chrome, потім `node scripts/verify-practice4.mjs` і `node scripts/verify-practice4-store.mjs`. PDF можна повторно створити командою `python3 scripts/generate-practice4-report.py` за наявності reportlab і Pillow та шрифтів Arial у macOS.


## Звіт і перевірки

- [PDF-звіт](output/pdf/TaskFlow_report.pdf)
- [Текст звіту](reports/report.md)
- [Контрольні запитання](reports/answers.md)
- [Результати браузерних перевірок](reports/verification.json)
- [Скріншоти](reports/screenshots)

Виконано всі шість додаткових завдань із методичних вказівок «2-5.pdf».
Збірка проходить; Vite попереджає про розмір JS-пакета понад 500 kB.
