from pathlib import Path
import json
from xml.sax.saxutils import escape
from PIL import Image as PILImage
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,PageBreak,Preformatted,Table,TableStyle
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'reports/practice5';OUT=ROOT/'output/pdf/TaskFlow_list_report.pdf'
FONT=Path('/System/Library/Fonts/Supplemental')
for name,file in [('TNR','Times New Roman.ttf'),('TNRBold','Times New Roman Bold.ttf'),('Code','Courier New.ttf')]:pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
pdfmetrics.registerFontFamily('TNR',normal='TNR',bold='TNRBold',italic='TNR',boldItalic='TNRBold')
styles=getSampleStyleSheet()
for name,font,size,leading,space in [('BodyUA','TNR',14,21,10),('HeadingUA','TNRBold',17,22,15),('CaptionUA','TNR',11,15,10),('CellUA','TNR',11,15,0),('AnswerUA','TNR',13,19.5,10),('CodeUA','Code',9,13,12)]:
 styles.add(ParagraphStyle(name=name,fontName=font,fontSize=size,leading=leading,spaceAfter=space))
styles.add(ParagraphStyle(name='TitleUA',fontName='TNRBold',fontSize=22,leading=28,alignment=TA_CENTER,spaceAfter=22))
story=[];md=[]
def p(t):story.append(Paragraph(t,styles['BodyUA']));md.append(t+'\n')
def h(t):story.append(Paragraph(t,styles['HeadingUA']));md.append('## '+t+'\n')
def page():story.append(PageBreak())
def code(t):story.append(Preformatted(t,styles['CodeUA']));md.append('```js\n'+t+'\n```\n')
def pic(name,caption,maxh=300,width=480):
 path=BASE/'screenshots'/f'{name}.png';w,hh=PILImage.open(path).size;scale=min(width/w,maxh/hh)
 story.append(Image(str(path),width=w*scale,height=hh*scale,hAlign='CENTER'));story.append(Spacer(1,6));story.append(Paragraph(caption,styles['CaptionUA']));md.append(f'![{caption}](screenshots/{name}.png)\n')
def crop(name,height):
 path=BASE/'screenshots'/f'{name}.png';im=PILImage.open(path);im.crop((0,0,im.width,min(height,im.height))).save(BASE/'screenshots'/f'{name}-fragment.png')
for n,height in [('all-tasks',1100),('sort-before',470),('sort-after',470),('after-delete',1100)]:crop(n,height)
results=json.loads((BASE/'verification.json').read_text())['results']
def tests(rows):
 data=[[Paragraph('<b>№</b>',styles['CellUA']),Paragraph('<b>Фактичний результат</b>',styles['CellUA']),Paragraph('<b>Оцінка</b>',styles['CellUA'])]]
 for r in rows:
  data.append([Paragraph(r['id'],styles['CellUA']),Paragraph(escape(r['observed']),styles['CellUA']),Paragraph('Успішно',styles['CellUA'])]);md.append(f"- {r['id']}: {r['observed']} Успішно.\n")
 table=Table(data,colWidths=[28,390,64],hAlign='LEFT')
 table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#edf2f8')),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#cbd5e1')),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]));story.append(table);story.append(Spacer(1,14))
story.append(Paragraph('Звіт з практичної роботи № 5',styles['TitleUA']));md.append('# Звіт з практичної роботи № 5\n')
p('TaskFlow • Управління списком завдань у PWA-застосунку')
p('Дата виконання: 06.11.2026. Методичні вказівки: «2-8.pdf».')
h('1. Тема, мета та вихідні умови')
p('Тема: видалення, пошук, комбінована фільтрація, сортування та зміна станів завдань у Vue 3. Мета: керувати реактивним масивом, будувати похідні списки через computed, використовувати Props та Emits і синхронізувати дані між сторінками.')
p('Після роботи № 4 проєкт уже містив 10 початкових завдань, картки, статистику, форму створення й редагування, категорії, валідацію та попередній перегляд. Попередню роботу зафіксовано й надіслано до origin/main: коміт 9e1fb7a.')
h('2. Теоретичні відомості')
p('<b>ref()</b> зберігає пошуковий рядок і вибрані умови. <b>computed()</b> кешує похідний список та перераховує його при зміні залежностей. <b>filter()</b> повертає новий масив, тоді як <b>sort()</b> сортує масив на місці, тому застосовується до результату filter, а не до taskState.tasks.')
p('<b>findIndex()</b> знаходить індекс запису за ID; <b>splice(index, 1)</b> видаляє один елемент. Зміна спільного reactive-сховища автоматично оновлює картки, лічильники й головну сторінку.')
page()
h('3. Структура та передавання подій')
code('src/\n  components/TaskListControls.vue  # новий, Props + Events\n  components/TaskCard.vue          # подія delete\n  components/TaskForm.vue          # опис 500, дата необов’язкова\n  pages/TasksPage.vue              # фільтри, сортування, діалог\n  pages/HelpPage.vue               # актуальна довідка\n  store/tasks.js                  # deleteTask, перевірка даних\n  css/task-list.css               # новий, адаптивні стилі\nreports/practice5/                 # скріншоти та результати\noutput/pdf/TaskFlow_list_report.pdf')
p('TaskListControls отримує search, status, priority, sort та incomplete через Props. Події update:* повертають нові значення батьківській сторінці через іменовані v-model; reset скидає всі умови. Компонент не зберігає масив завдань.')
p('TaskCard надсилає status-change, priority-change, task-select, edit і delete. TasksPage обробляє події та звертається до сховища. Власник рішення про видалення - сторінка: картка тільки повідомляє ID.')
code('const filteredTasks = computed(() => {\n  const result = taskState.tasks.filter(task =>\n    matchesText(task) && matchesStatus(task) &&\n    matchesPriority(task) && matchesIncomplete(task))\n  return result.sort(compareTasks)\n})\n\nconst index = taskState.tasks.findIndex(task => task.id === id)\nif (index === -1) return false\ntaskState.tasks.splice(index, 1)')
p('Фрагмент фільтрації скорочено для пояснення. Повна реалізація міститься у src/pages/TasksPage.vue. Сортування дат окремо обробляє порожні значення, залишаючи їх наприкінці в обох напрямках.')
page()
h('4. Усі завдання та пошук')
p('Початковий режим - «Спочатку нові». Лічильник показує кількість знайдених із загальної кількості та частку виконаних у поточній вибірці.')
pic('all-tasks-fragment','Рис. 1. Поля керування й початок повного списку з 10 записів.',maxh=270)
p('Пошук перевіряє назву та опис після trim і приведення до нижнього регістру української локалі.')
pic('search-description','Рис. 2. Слово Navbar міститься тільки в описі знайденого завдання.',maxh=210)
page()
h('5. Фільтрація та сортування')
pic('combined-filters','Рис. 3. Статус «Виконано» та високий пріоритет застосовані одночасно.',maxh=245)
p('Доступні новіші ID першими, назва А-Я, пріоритет, дата у двох напрямах, статус, а також попередні режими низького пріоритету й порядку додавання.')
pic('sort-before-fragment','Рис. 4. Початок списку до сортування: новіші ID першими.',maxh=145)
pic('sort-after-fragment','Рис. 5. Той самий список після сортування за назвою А-Я.',maxh=145)
page()
h('6. Підтвердження та результат видалення')
p('Реалізовано модальний HTML-діалог із назвою завдання. Початковий фокус - на «Скасувати»; Escape також скасовує дію. До підтвердження сховище залишається без змін.')
pic('delete-confirmation','Рис. 6. Підтвердження видалення обраного запису.',maxh=230)
pic('after-delete-fragment','Рис. 7. Після підтвердження: 9 записів замість 10.',maxh=220)
p('Якщо видаляється запис, відкритий у формі чи деталях, відповідний перегляд закривається. Головна статистика також зменшується без перезавантаження.')
page()
h('7. Тести 01-07: пошук і впорядкування')
tests(results[:7])
p('Перевірки виконано у Google Chrome через Playwright. Для сортування додатково порівняно порядок ID у сховищі до та після зміни режиму: вихідний масив не переставляється.')
p('Порожні терміни перевірено на окремому записі, створеному через інтерфейс. Така картка завжди остання при зростанні й спаданні дат.')
page()
h('8. Тести 08-14: дії зі списком')
tests(results[7:14])
p('<b>Production-збірка:</b> npm run build завершилася успішно. Створено manifest, service worker та production bundle. Є попередження Vite про JS-пакет понад 500 kB. Воно не блокує збірку.')
p('Runtime-помилок не виявлено. Повні результати: reports/practice5/verification.json. Лог збірки: reports/practice5/build.txt. Скрипт: scripts/verify-practice5.mjs.')
page()
h('9. Результати додаткових завдань')
p('1. <b>Тільки невиконані:</b> швидкий фільтр поєднується з текстом, статусом і пріоритетом. Суперечливі умови дають порожній результат.')
p('2. <b>Статуси:</b> порядок «У роботі» → «Заплановано» → «Виконано», при рівності - новіші ID першими.')
p('3. <b>Частка виконаних:</b> поруч із лічильником відображається відсоток для поточної вибірки; для порожньої - 0%.')
p('4. <b>Очистити пошук:</b> кнопка видима тільки за наявності тексту, очищує лише пошук і зберігає решту умов.')
p('5. <b>Порожній список:</b> після видалення всіх записів показано окреме пояснення та кнопку створення першого завдання.')
p('6. <b>Зворотні дати:</b> додано режим «найпізніший перший»; записи без дати залишаються внизу.')
pic('all-deleted','Рис. 8. Стан після видалення всіх завдань.',maxh=245)
page()
h('10. Адаптивність та сумісність')
p('На екрані 390 px поля розміщено в одну колонку, кнопки переносяться, горизонтального переповнення немає. Діалог має підпис, опис та керування клавіатурою.')
pic('mobile-controls','Рис. 9. Керування списком на мобільній ширині 390 px.',maxh=230,width=210)
pic('mobile-dialog','Рис. 10. Мобільний діалог підтвердження.',maxh=230,width=210)
p('Збережено категорії, деталі, лічильники символів, очищення форми й попередній перегляд. За новою методичкою опис допускає до 500 символів, дата стала необов’язковою. Якщо дату вводять, діє перевірка календарної коректності й правила попередньої роботи щодо минулої дати.')
page()
h('11. Контрольні запитання: 1-8')
answers=[
('Яке призначення ref() у Vue 3?','Створює реактивне значення для пошуку, фільтрів, режиму сортування та стану форми.'),
('Коли computed() кращий за звичайну функцію?','Коли потрібне похідне значення з кешуванням, яке оновлюється при зміні реактивних залежностей.'),
('Чим filter() відрізняється від find()?','filter повертає масив усіх збігів; find - перший знайдений елемент або undefined.'),
('Чому не слід сортувати спільний масив у computed()?','sort змінює масив на місці. Це неочікувано переставляє спільні дані; потрібно сортувати копію чи результат filter.'),
('Як працює пошук у назві та описі?','Назва й опис об’єднуються в рядок, приводяться до нижнього регістру, після чого перевіряється includes для нормалізованого запиту.'),
('Як поєднуються умови фільтрації?','Через логічне І: запис має одночасно задовольняти текст, статус, пріоритет та швидкий фільтр.'),
('Навіщо localeCompare() для українських назв?','Він порівнює рядки за правилами заданої локалі, забезпечуючи коректний алфавітний порядок.'),
('Що відбувається із записами без терміну?','Окрема умова компаратора залишає їх наприкінці і при прямому, і при зворотному порядку дат.'),
('Яка роль defineEmits()?','Оголошує події компонентів: картка повідомляє про дії, а TaskListControls - про нові значення полів керування.'),
('Чому видалення обробляє сторінка?','Сторінка координує підтвердження, сховище, форму та деталі. Картка залишається повторно використовуваним компонентом відображення.'),
('Чим findIndex() відрізняється від indexOf()?','findIndex використовує предикат, наприклад порівняння ID; indexOf шукає конкретне значення або посилання. За відсутності обидва повертають -1.'),
('Як splice() впливає на відображення?','Змінює реактивний масив; Vue відстежує видалення та оновлює список, лічильники й статистику.'),
('Для чого :key у v-for?','Надає стабільну ідентичність карткам під час перестановки й видалення. Використовується task.id.'),
('Чому змінюються обидві сторінки?','HomePage та TasksPage імпортують один спільний reactive-об’єкт taskState.'),
('Чому записи повертаються після reload?','Стан зберігається тільки в оперативній пам’яті, а після перезавантаження модуль копіює src/data/tasks.js.'),
('Що вирішуватимуть Pinia та IndexedDB?','Pinia структурує спільний стан і дії; IndexedDB дає постійне локальне зберігання та основу офлайн-роботи.')]
for i,(q,a) in enumerate(answers,1):
 if i==9:page();h('12. Контрольні запитання: 9-16')
 story.append(Paragraph(f'<b>{i}. {q}</b> {a}',styles['AnswerUA']));md.append(f'**{i}. {q}** {a}\n')
page()
h('13. Висновки та обмеження')
p('Розширено наявний TaskFlow пошуком у назві та описі, поєднаними фільтрами, кількома режимами сортування та підтвердженим видаленням. Компонент керування використовує Props і події update:*, а сторінка обчислює видимий список без зміни порядку спільного масиву.')
p('Виконано всі 14 основних сценаріїв і шість додаткових завдань. Перевірено синхронізацію статистики після зміни статусу та видалення, редагування без зміни ID, коректну обробку порожніх дат, мобільне компонування та відновлення демонстраційних записів після reload.')
p('Дані залишаються в пам’яті: після повного перезавантаження створені зміни й видалення скидаються. Постійне зберігання та Pinia не додаються на цьому етапі. Встановлення PWA й офлайн-запуск на фізичному пристрої окремо не перевірялися.')
p('Початкові захищені файли main.js, App.vue, routes.js, AppTabbar.vue, StatusBadge.vue, PriorityBadge.vue залишені без змін. Нова робота розвиває попередню реалізацію; попередній стан доступний у коміті 9e1fb7a репозиторію Cross-platform-development.')
(BASE/'answers.md').write_text('\n\n'.join(f'{i}. **{q}** {a}' for i,(q,a) in enumerate(answers,1)))
def footer(c,doc):
 c.setFont('TNR',9);c.setFillColor(colors.HexColor('#48607b'));c.drawString(56.7,26,'TaskFlow | Практична робота № 5 | 06.11.2026');c.drawRightString(538.6,26,str(doc.page))
OUT.parent.mkdir(parents=True,exist_ok=True)
SimpleDocTemplate(str(OUT),pagesize=(595.28,841.89),leftMargin=56.7,rightMargin=56.7,topMargin=56.7,bottomMargin=56.7,title='TaskFlow: управління списком завдань',author='TaskFlow').build(story,onFirstPage=footer,onLaterPages=footer)
(BASE/'report.md').write_text('\n'.join(md))
print(OUT)
