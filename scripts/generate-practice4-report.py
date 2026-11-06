from pathlib import Path
import json
from xml.sax.saxutils import escape
from PIL import Image as PILImage
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Preformatted, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/pdf/TaskFlow_forms_report.pdf'
BASE=ROOT/'reports/practice4'
FONT=Path('/System/Library/Fonts/Supplemental')
pdfmetrics.registerFont(TTFont('Arial',str(FONT/'Arial.ttf')))
pdfmetrics.registerFont(TTFont('ArialBold',str(FONT/'Arial Bold.ttf')))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='ArialBold',italic='Arial',boldItalic='ArialBold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyUA',fontName='Arial',fontSize=10.5,leading=16,spaceAfter=10))
styles.add(ParagraphStyle(name='HeadingUA',fontName='ArialBold',fontSize=17,leading=22,spaceAfter=17))
styles.add(ParagraphStyle(name='TitleUA',fontName='ArialBold',fontSize=23,leading=29,alignment=TA_CENTER,spaceAfter=26))
styles.add(ParagraphStyle(name='CaptionUA',fontName='Arial',fontSize=9,leading=13,textColor=colors.HexColor('#48607b'),spaceAfter=13))
styles.add(ParagraphStyle(name='AnswerUA',fontName='Arial',fontSize=10,leading=14,spaceAfter=8))
styles.add(ParagraphStyle(name='CodeUA',fontName='Arial',fontSize=8.5,leading=12,backColor=colors.HexColor('#f2f5f9'),borderPadding=9,spaceAfter=14))
story=[];md=[]
def p(text):
 story.append(Paragraph(text,styles['BodyUA']));md.append(text+'\n')
def h(text):
 story.append(Paragraph(text,styles['HeadingUA']));md.append('## '+text+'\n')
def page():story.append(PageBreak())
def code(text):
 story.append(Preformatted(text,styles['CodeUA']));md.append('```js\n'+text+'\n```\n')
def pic(name,caption,maxh=475,width=495):
 path=BASE/'screenshots'/f'{name}.png';im=PILImage.open(path);w,hh=im.size
 scale=min(width/w,maxh/hh)
 story.append(Image(str(path),width=w*scale,height=hh*scale,hAlign='CENTER'))
 story.append(Spacer(1,8));story.append(Paragraph(caption,styles['CaptionUA']))
 md.append(f'![{caption}](screenshots/{name}.png)\n')

a='Звіт з практичної роботи № 4'
story.append(Paragraph(a,styles['TitleUA']));md.append('# '+a+'\n')
p('TaskFlow • Реактивні форми, створення та редагування завдань')
p('Дата виконання: 06.11.2026. Основа: методичні вказівки «2-6.pdf».')
h('1. Тема та мета')
p('Тема: форми користувача, v-model, реактивний стан, перевірка введення, створення та редагування завдань у Vue 3. Мета: навчитися працювати з реактивними полями, передавати результати через Props та Emits і оновлювати спільне сховище TaskFlow.')
h('2. Теоретичні відомості')
p('<b>ref()</b> створює реактивне значення; у JavaScript доступ здійснюється через .value. <b>reactive()</b> повертає реактивний об’єкт, зміни полів якого оновлюють інтерфейс. <b>computed()</b> обчислює та кешує похідні значення, зокрема помилки, фільтри та статистику.')
p('<b>v-model</b> пов’язує input, textarea або select із полем стану в обох напрямках. Модифікатор <b>.trim</b> прибирає крайні пробіли. <b>@submit.prevent</b> обробляє надсилання без перезавантаження сторінки, а novalidate дозволяє показувати власні повідомлення українською.')
p('<b>Props</b> передають вихідне завдання до форми. Форма редагує локальну копію та через <b>Emits</b> повідомляє про save або cancel. Валідація перевіряє дані перед збереженням; однакові правила застосовуються у формі та сховищі.')
h('3. Підсумок виконання')
p('Реалізовано всі основні кроки та 7 додаткових завдань. Збережено попередні фільтри, сортування, деталі, картки та статистику. Дані існують у пам’яті поточного сеансу. У цьому проєкті 10 початкових записів, тому T8 відновлює 10, а не 6 із прикладу методички.')
page()
h('4. Структура та призначення коду')
code('src/\n  components/TaskForm.vue       # новий компонент\n  components/TaskCard.vue       # editable, edit, категорія\n  store/tasks.js               # валідація, addTask, updateTask\n  pages/TasksPage.vue           # відкриття форми, saveTask, пошук\n  pages/HelpPage.vue            # оновлена довідка\n  css/task-form.css            # нові стилі\n  data/tasks.js                # 10 початкових записів\nreports/practice4/              # перевірки та скріншоти\noutput/pdf/TaskFlow_forms_report.pdf')
p('<b>TaskForm.vue</b> отримує task або null, створює локальний reactive-об’єкт, показує лічильники символів, помилки та попередній перегляд. Ключ editingId або new створює окремий екземпляр форми при перемиканні записів.')
p('<b>addTask()</b> повторно перевіряє дані, прибирає крайні пробіли, обчислює ID як max поточних ID + 1 і додає запис. <b>updateTask()</b> знаходить запис за ID та застосовує перевірені значення через Object.assign, зберігаючи ID.')
p('<b>submitForm()</b> вмикає помилки, фокусує перше некоректне поле або генерує save. <b>saveTask()</b> обирає addTask чи updateTask, закриває форму після успіху, показує підтвердження та скидає фільтри й пошук.')
h('5. Приклади двостороннього зв’язування')
code('const form = reactive({ ...defaults(), ...props.task })\nconst errors = computed(() => validateTaskData(form, props.task))\n\n<input v-model.trim="form.title" />\n<form novalidate @submit.prevent="submitForm">\n\nif (Object.keys(errors.value).length) return\nemit(\'save\', { title: form.title.trim(), /* інші поля */ })\n\n<TaskForm :key="editingId ?? \'new\'" :task="editingTask"\n  @save="saveTask" @cancel="cancelForm" />')
page()
h('6. Порожня форма та повідомлення про помилки')
p('Після натискання «Створити завдання» без введення даних показано помилки назви й дати. Стандартні статус, пріоритет і категорія вже коректні. Новий запис не додається, фокус переходить до назви.')
pic('empty-errors','Рис. 1. Порожня форма після першої спроби збереження.',maxh=505)
p('Правила: назва 3-80 символів; опис до 300; статус і пріоритет із дозволених списків; коректна календарна дата. Для нових записів додатково перевіряються унікальність назви та дата не в минулому.')
page()
h('7. Заповнена форма та попередній перегляд')
p('Введено назву, опис, статус «У роботі», пріоритет «Високий», категорію «Робота» та майбутню дату. Попередній перегляд і кількість доступних символів змінюються під час введення.')
pic('filled-preview','Рис. 2. Дані майбутнього запису до збереження.',maxh=510)
p('Для відтворюваної перевірки використано 20.11.2099. Інтерфейс приймає також сьогоднішню дату та інші майбутні дати за локальним календарем браузера.')
page()
h('8. Список до та після додавання')
p('Початково список містить 10 записів. Після збереження форми створено завдання з ID 11; кількість збільшилася до 11. Фільтри повернуто до «Усі», щоб новий запис був доступний.')
for name in ['list-before','list-after']:
 im=PILImage.open(BASE/'screenshots'/f'{name}.png')
 im.crop((0,0,im.width,min(450,im.height))).save(BASE/'screenshots'/f'{name}-fragment.png')
pic('list-before-fragment','Рис. 3. Фрагмент списку до створення: 10 завдань.',maxh=175)
pic('list-after-fragment','Рис. 4. Фрагмент списку після створення: 11 завдань.',maxh=175)
pic('created-result','Рис. 5. Нова картка після збереження.',maxh=170)
page()
h('9. Редагування наявного завдання')
p('Через кнопку «Редагувати» відкрито локальну копію запису № 11. Назву змінено на «Форму успішно перевірено», статус - на «Виконано». Після збереження оновлюється той самий запис.')
pic('editing','Рис. 6. Форма редагування перед збереженням змін.',maxh=515)
p('До збереження зміни не потрапляють до картки. Початкова прострочена дата старого запису дозволена, якщо її залишити без змін. Якщо дату замінюють, нова має бути сьогоднішньою або майбутньою.')
page()
h('10. Результат редагування та скасування')
pic('edited-result','Рис. 7. Збережено нову назву й статус «Виконано».',maxh=200)
p('Після повторного відкриття форми введено назву «Цю зміну треба скасувати» та натиснуто «Скасувати». Картка зберегла попередні дані; додатковий запис не створено.')
pic('cancel-result','Рис. 8. Результат скасування: картка залишилася без змін.',maxh=200)
p('Сховище окремо перевірено на збереження ID, відхилення некоректного оновлення без часткових змін та незмінність об’єктів із початкового модуля даних.')
page()
h('11. Результати тестування T1-T8')
results=json.loads((BASE/'verification.json').read_text())['results']
rows=[[Paragraph('<b>Тест</b>',styles['BodyUA']),Paragraph('<b>Фактичне спостереження</b>',styles['BodyUA']),Paragraph('<b>Статус</b>',styles['BodyUA'])]]
for r in results[:8]:
 rows.append([Paragraph(r['id'],styles['BodyUA']),Paragraph(escape(r['observed']),styles['BodyUA']),Paragraph('Успішно',styles['BodyUA'])])
 md.append(f"- {r['id']}: {r['observed']} Результат: успішно.\n")
t=Table(rows,colWidths=[42,387,66],hAlign='LEFT');t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#edf2f8')),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#cbd5e1')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7)]));story.append(t)
story.append(Spacer(1,15))
p('Перевірено у Chrome через Playwright. Runtime-помилок не виявлено. Додаткові сценарії: дубль без урахування регістру, минула дата, незмінена стара дата, очищення, пошук та ширина 390 px без горизонтального переповнення. Результати: reports/practice4/verification.json і store-verification.json.')
p('<b>npm run build</b>: успішно. Сформовано production bundle, manifest і service worker. Є попередження Vite про JS-пакет понад 500 kB; збірка не блокується. Повний лог: reports/practice4/build.log. Встановлення PWA та офлайн-запуск на фізичному пристрої окремо не перевірялися.')
page()
h('12. Додаткові завдання та адаптивність')
p('1. <b>Категорія:</b> навчання, робота, особисте; показано у формі, перегляді та картці. Для початкових записів без цього поля відображається «Навчання».')
p('2. <b>Дата:</b> нове завдання не може мати минулу дату; стару можна залишити незміненою при редагуванні. Перевірка діє й у сховищі.')
p('3. <b>Символи:</b> показано залишок до 80 для назви й до 300 для опису.')
p('4. <b>Очищення:</b> кнопка повертає стандартні значення у режимі створення та прибирає повідомлення про помилки.')
p('5. <b>Доступність:</b> зірочки, required, підписи label, aria-invalid, aria-describedby, фокус першого помилкового поля, видимі фокусні контури та aria-live для перегляду.')
p('6. <b>Пошук:</b> фільтрує назви під час введення, без урахування регістру, разом із попередніми фільтрами й сортуванням.')
p('7. <b>Унікальність:</b> нова назва перевіряється після trim без урахування регістру. При редагуванні перевірка унікальності не застосовується, відповідно до додаткового завдання.')
pic('mobile-form','Рис. 9. Одноколонкова форма на екрані шириною 390 px.',maxh=250)
page()
h('13. Висновок')
p('Розширено TaskFlow універсальною реактивною формою створення й редагування. Закріплено v-model, reactive, ref, computed, Props та Emits. Дані перевіряються до зміни сховища, скасування зберігає вихідний запис, а статистика автоматично реагує на оновлення спільного стану. Виконано T1-T8 та всі сім додаткових завдань.')
h('14. Відповіді на контрольні запитання')
answers=[
('Що означає реактивність у Vue 3?','Автоматичне оновлення залежного інтерфейсу при зміні реактивного стану.'),
('У чому різниця між ref() і reactive()?','ref обгортає значення з доступом через .value; reactive створює proxy об’єкта з реактивними полями.'),
('Для чого застосовується v-model?','Для двостороннього зв’язування поля форми зі станом компонента.'),
('Що робить v-model.trim?','Прибирає пробіли на початку й наприкінці введеного значення.'),
('Яка роль computed() у валідації?','Обчислює актуальний об’єкт помилок при зміні полів або залежних даних.'),
('Навіщо @submit.prevent?','Обробляє надсилання форми без стандартного переходу чи перезавантаження.'),
('Навіщо novalidate?','Вимикає стандартні повідомлення браузера для єдиної власної валідації українською.'),
('Навіщо локальна копія редагованих даних?','Щоб введення не змінювало оригінал до збереження та працювало скасування.'),
('Які події генерує TaskForm?','save передає перевірені дані до saveTask; cancel викликає закриття форми.'),
('Чим відрізняються створення й редагування?','Створення додає запис із новим ID; редагування змінює знайдений запис зі збереженням ID.'),
('Як формується новий ID?','Максимальний поточний ID + 1; для порожнього масиву - 1.'),
('Навіщо перевірка у сховищі?','Щоб некоректні дані не потрапили до стану при виклику функцій поза формою.'),
('Чому змінюється статистика головної?','Обидві сторінки використовують один taskState; computed залежить від його завдань.'),
('Чому скасування не змінює оригінал?','Воно відкидає локальний чернетковий стан і не викликає addTask чи updateTask.'),
('Що станеться після оновлення браузера?','Додані зміни зникнуть; модуль повторно створить 10 початкових записів із src/data/tasks.js.')]
for i,(q,a) in enumerate(answers,1):
 story.append(Paragraph(f'<b>{i}. {q}</b> {a}',styles['AnswerUA']))
 md.append(f'**{i}. {q}** {a}\n')
(BASE/'answers.md').write_text('\n\n'.join(f'{i}. **{q}** {a}' for i,(q,a) in enumerate(answers,1)))
def footer(c,doc):
 c.setFont('Arial',8.5);c.setFillColor(colors.HexColor('#48607b'))
 c.drawString(45,25,'TaskFlow | Практична робота № 4 | 06.11.2026')
 c.drawRightString(550,25,str(doc.page))
SimpleDocTemplate(str(OUT),pagesize=(595.28,841.89),rightMargin=50,leftMargin=50,topMargin=45,bottomMargin=45,title='TaskFlow: Реактивні форми - практична робота № 4',author='TaskFlow').build(story,onFirstPage=footer,onLaterPages=footer)
(BASE/'report.md').write_text('\n'.join(md))
print(OUT)
