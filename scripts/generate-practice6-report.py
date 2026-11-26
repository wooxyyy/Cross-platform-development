from pathlib import Path
import json
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'reports/practice6'; OUT=ROOT/'output/docx/TaskFlow_Pinia_report.docx'
doc=Document();sec=doc.sections[0]
sec.page_width=Cm(21);sec.page_height=Cm(29.7)
sec.top_margin=sec.bottom_margin=sec.left_margin=sec.right_margin=Cm(2)
for name in ['Normal','Title','Heading 1','Heading 2','Caption']:
 st=doc.styles[name];st.font.name='Times New Roman';st.font.size=Pt(14);st.font.color.rgb=RGBColor(0,0,0)
 st.paragraph_format.line_spacing=1.5;st.paragraph_format.space_after=Pt(6)
 st.element.rPr.rFonts.set(qn('w:eastAsia'),'Times New Roman')
doc.styles['Title'].font.size=Pt(22);doc.styles['Title'].font.bold=True
doc.styles['Heading 1'].font.size=Pt(17);doc.styles['Heading 1'].font.bold=True
doc.styles['Heading 1'].paragraph_format.space_before=Pt(10)
doc.styles['Caption'].font.size=Pt(12)
header=sec.header.paragraphs[0];header.text='TaskFlow | Практична робота № 6 | 26.11.2026'
header.runs[0].font.size=Pt(9)
f=sec.footer.paragraphs[0];f.alignment=WD_ALIGN_PARAGRAPH.RIGHT
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');f._p.append(field)
md=[]
def p(t):doc.add_paragraph(t);md.append(t+'\n')
def h(t):doc.add_heading(t,level=1);md.append('## '+t+'\n')
def page():doc.add_page_break()
def code(t):
 pp=doc.add_paragraph();pp.paragraph_format.line_spacing=1.1
 rr=pp.add_run(t);rr.font.name='Courier New';rr.font.size=Pt(10)
 md.append('```js\n'+t+'\n```\n')
def pic(name,caption,maxh=10):
 path=BASE/'screenshots'/f'{name}.png';im=Image.open(path);w,hh=im.size
 scale=min(17/w,maxh/hh)
 pp=doc.add_paragraph();pp.alignment=WD_ALIGN_PARAGRAPH.CENTER;pp.paragraph_format.line_spacing=1
 pp.paragraph_format.space_after=Pt(4);pp.paragraph_format.keep_with_next=True
 pp.add_run().add_picture(str(path),width=Cm(w*scale),height=Cm(hh*scale))
 cap=doc.add_paragraph(caption,style='Caption');cap.paragraph_format.line_spacing=1.1
 md.append(f'![{caption}](screenshots/{name}.png)\n')
def test_table(rows):
 table=doc.add_table(rows=1,cols=4);table.autofit=False
 widths=[4.1,4.3,5.8,2.8]
 for c,w in zip(table.columns,widths):c.width=Cm(w)
 for c,t in zip(table.rows[0].cells,['Дія','Очікувано','Фактично','Висновок']):c.text=t
 repeat=OxmlElement('w:tblHeader');table.rows[0]._tr.get_or_add_trPr().append(repeat)
 for r in rows:
  cells=table.add_row().cells
  for c,t in zip(cells,[r['id']+'. '+r['action'],r['expected'],r['actual'],'Успішно']):c.text=t
 for ri,row in enumerate(table.rows):
  no=OxmlElement('w:cantSplit');row._tr.get_or_add_trPr().append(no)
  for c,w in zip(row.cells,widths):
   c.width=Cm(w)
   pr=c._tc.get_or_add_tcPr();borders=OxmlElement('w:tcBorders')
   for edge in ['top','left','bottom','right']:
    el=OxmlElement('w:'+edge);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D9D9D9');borders.append(el)
   pr.append(borders)
   if ri==0:
    shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'EAF0F7');pr.append(shade)
   for pp in c.paragraphs:
    pp.paragraph_format.line_spacing=1.5;pp.paragraph_format.space_after=Pt(4)
    for rr in pp.runs:rr.font.size=Pt(14);rr.bold=ri==0
results=json.loads((BASE/'verification.json').read_text())['results']
# Crop only empty lower area in the actual Devtools screenshot.
im=Image.open(BASE/'screenshots/devtools.png');im.crop((0,0,im.width,520)).save(BASE/'screenshots/devtools-fragment.png')
doc.add_paragraph('Звіт з практичної роботи № 6',style='Title')
p('TaskFlow. Централізоване керування станом за допомогою Pinia')
p('Дата виконання: 26.11.2026. Методичні вказівки: 2-9.pdf.')
h('1 Тема та мета')
p('Тема: перенесення завдань, проєктів, фільтрів і статистики до сховищ Pinia. Мета: підключити Pinia до Vue 3, застосувати state, getters, actions та storeToRefs(), організувати взаємодію сховищ і синхронне відображення даних на різних сторінках.')
h('2 Вихідний стан і результат')
p('Після роботи № 5 TaskFlow містив 10 демонстраційних завдань, CRUD, пошук, комбіновані фільтри, сортування, категорії, форму з валідацією та підтверджене видалення. Попередній стан збережений у Git-коміті 96405a4.')
p('Реалізовано основні вимоги та всі шість додаткових завдань. Перевірено 17 основних пунктів методички, додаткові функції й регресію сортування. Збірка та локальна production-перевірка пройшли. Код надіслано до origin/main у коміті 4392d0f.')
p('Технології: Vue 3, Framework7, Pinia 3, Vite, vite-plugin-pwa; для перевірок використано Google Chrome, Playwright і Vue Devtools.')
page();h('3 Структура проєкту після змін')
code('src/\n  main.js                        # підключення Pinia\n  store/tasks.js                 # завдання і фільтри\n  store/projects.js              # каталог і статистика\n  components/TaskForm.vue        # вибір проєкту\n  components/TaskListControls.vue # фільтр проєкту\n  components/TaskCard.vue        # назва проєкту\n  pages/HomePage.vue             # спільна статистика\n  pages/TasksPage.vue            # дії та проєкти\n  css/task-list.css              # адаптивний блок')
p('Це дев’ять файлів із методички. Додатково синхронізовано package.json і package-lock.json, оновлено README, додано сценарій перевірки, матеріали та звіт. App.vue, routes.js, data/tasks.js, базові компоненти й конфігурацію Vite/PWA збережено.')
h('4 Принцип роботи спільного стану')
p('Попередній reactive-модуль містив спільний об’єкт і окремі функції. Pinia структурує той самий реактивний стан у stores, додає життєвий цикл екземпляра, підтримку Devtools і явний розподіл відповідальності.')
p('state зберігає tasks, projects і критерії пошуку. getters повертають totalTasks, visibleTasks і projectStats. actions виконують CRUD, перевірку назв та групову зміну статусу. storeToRefs() зберігає реактивність при деструктуризації state/getters. Дії викликаються як методи store.')
code('const taskStore = useTasksStore()\nconst { tasks, visibleTasks } = storeToRefs(taskStore)\ntaskStore.setTaskStatus({ id: 10, status: "progress" })')
page();h('5 Головна сторінка і статистика')
pic('home','Рис. 1. Статистика, проєкти та актуальні завдання на головній сторінці.',maxh=17)
p('Початкові показники: 10 завдань, 3 у роботі, 3 виконано, 4 заплановано, прогрес 30%. У «Загальних» 7 невиконаних; у порожніх проєктів прогрес дорівнює 0%. Дані не копіюються між сторінками.')
page();h('6 Каталог і прив’язка завдання')
pic('projects','Рис. 2. Створений проєкт «Лабораторні» у каталозі.',maxh=4)
p('Назва проєкту очищується від крайніх пробілів; дозволено 3-40 символів. Повторення без урахування регістру відхиляється.')
pic('form','Рис. 3. Створення завдання з вибраним проєктом «Лабораторні».',maxh=13)
p('Форма надсилає projectId через save. Сховище перевіряє існування проєкту; старі записи автоматично отримують general. Редагування зберігає ID завдання.')
page();h('7 Фільтри та групова дія')
pic('combined','Рис. 4. Проєкт, пошук, статус і пріоритет застосовано одночасно.',maxh=10)
p('visibleTasks перевіряє всі умови через логічне І. Фільтри зберігаються при переходах між сторінками. «Лише без терміну» також входить до state й скидається resetFilters().')
pic('bulk','Рис. 5. Окреме підтвердження переведення всіх завдань проєкту в роботу.',maxh=5)
p('Escape або «Скасувати» не змінюють завдання. Підтвердження викликає startProjectTasks(projectId); статус усіх завдань цього проєкту стає progress, включно з раніше виконаними.')
page();h('8 Додаткові завдання та Vue Devtools')
pic('devtools-fragment','Рис. 6. Vue Devtools: сховища tasks і projects; після action лічильник progressTasks дорівнює 4.',maxh=8)
p('1. projectStats у сховищі проєктів обчислює total, completed, incomplete і percent за один прохід. Перевага: одна формула для різних сторінок. Недолік: сховище проєктів залежить від tasks-store, що потрібно враховувати в тестах.')
p('2. На HomePage додано назви проєктів і кількість невиконаних завдань без дублювання масиву tasks.')
p('3. Відсоток дорівнює round(completed / total × 100); для total = 0 повертається 0%.')
p('4. Груповий action виконується після окремого підтвердження. 5. Фільтр без терміну поєднується з іншими умовами.')
p('6. У Vue Devtools перевірено обидва stores та результат action setTaskStatus: progressTasks змінився з 3 на 4, plannedTasks - з 4 на 3. Для знімка використано тимчасову dev-конфігурацію без зміни production-конфігурації.')
page();h('9 Перевірки завантаження і проєктів')
test_table(results[:4])
page();h('10 Перевірки форми й фільтрації')
test_table(results[4:8])
page();h('11 Решта перевірок і адаптивність')
p('09-10. Редагування переносить запис до іншого проєкту зі збереженням ID. Зміна статусу на головній одразу відображається в списку й статистиці.')
p('11-12. Скасування видалення залишає 11 записів; підтвердження зменшує кількість до 10. Головна статистика також оновлюється.')
p('13-15. Скидання повертає початкові фільтри. Умови зберігаються між сторінками. Повний reload відновлює 10 завдань і три початкові проєкти.')
p('16-17. npm run build завершується успішно. На ширині 390 px форма й фільтри розташовані в один стовпчик; горизонтального переповнення немає.')
pic('mobile','Рис. 7. Керування фільтрами на мобільній ширині 390 px.',maxh=10)
p('Додатково перевірено всі вісім режимів сортування: вибраний режим доходить до Pinia, початковий порядок tasks не змінюється. Виправлено помилкові аргументи emit для update:sort.')
page();h('12 Production збірка та публікація')
pic('build','Рис. 8. Фактичний журнал успішного npm run build після npm ci.',maxh=12)
p('Створено production bundle, manifest і service worker. У Chrome локально перевірено відкриття обох сторінок, реєстрацію service worker та офлайн-перезавантаження. Runtime-помилок не виявлено. Vite попереджає про пакет понад 500 kB; це не блокує збірку.')
p('Код надіслано в main: 4392d0f. Автоматична перевірка Cloudflare «Workers Builds: cross-platform-development» завершилась успішно: completed / success, версія 70a3dfc1-4e67-4e6d-909f-b5e1226d0f4a. Це підтверджує успіх автоматичного процесу Cloudflare. Публічна адреса сайту не надана, тому відкриття віддаленого застосунку в браузері окремо не перевірене.')
p('Репозиторій: https://github.com/wooxyyy/Cross-platform-development')
page();h('13 Висновки та обмеження')
p('TaskFlow переведено на два централізовані Pinia-сховища зі збереженням попередніх можливостей. Додано каталог проєктів, прив’язку, комбіновану фільтрацію, проєктну статистику й підтверджену групову дію. Переходи між сторінками використовують єдиний стан.')
p('Pinia не забезпечує постійного збереження. Після повного перезавантаження завдання, проєкти й фільтри відновлюються з демонстраційних даних, як передбачено роботою № 6. IndexedDB не додано. Встановлення PWA на фізичному пристрої не перевірялось.')
p('npm ci повідомляє про 12 вразливостей у дереві залежностей: 1 низька, 5 помірних, 6 високих. Масове оновлення залежностей із можливими несумісними змінами не входило до цієї перевірки.')
p('Повні результати: reports/practice6/verification.json, production.json, build.txt, devtools.txt. Автоматизовані сценарії: scripts/verify-practice6.mjs. Усі скріншоти збережено в reports/practice6/screenshots/.')
qa=[
('Що називають станом застосунку і навіщо централізувати його керування?','Це поточні дані інтерфейсу. Централізація дає спільне джерело даних і синхронізацію компонентів.'),
('Чим Pinia відрізняється від звичайного reactive-об’єкта?','Pinia структурує стан у сховища зі state, getters, actions, інтеграцією Devtools та екземпляром, прив’язаним до застосунку.'),
('Яка роль createPinia() і де його викликати?','Створює екземпляр менеджера сховищ. У main.js він передається до app.use() перед app.mount().'),
('Чому не можна видаляти registerComponents(app)?','Він реєструє f7-компоненти Framework7. Без реєстрації шаблони не зможуть коректно відобразити ці компоненти.'),
('Яка структура Option Store?','defineStore(id, { state, getters, actions }); state є функцією, яка повертає початкові дані.'),
('Що таке state, getters і actions?','tasks і selectedProject - state; visibleTasks - getter; addTask і deleteTask - actions.'),
('Навіщо storeToRefs()?','Він створює refs для state/getters; звичайна деструктуризація примітивних значень втрачає реактивний зв’язок.'),
('Чим getter відрізняється від action?','Getter обчислює похідні дані без змін вихідного стану. Action виконує операції, змінює стан і може бути асинхронним.'),
('Чому showForm та editingId залишено локальними?','Вони потрібні лише сторінці для керування формою, тому спільне сховище для них зайве.'),
('Як два компоненти користуються одним сховищем?','Обидва викликають useTasksStore() в контексті того самого екземпляра Pinia й отримують спільний store.'),
('Навіщо окреме useProjectsStore()?','Каталог, перевірка назв і статистика проєктів мають окрему відповідальність та можуть повторно використовуватись.'),
('Як перевіряється projectId?','Форма дозволяє вибрати лише наявний проєкт; action додатково перевіряє належність ID до каталогу й застосовує резервний general.'),
('Навіщо старим завданням general?','Це забезпечує зворотну сумісність із демонстраційними записами, які ще не містили projectId.'),
('Чому не сортувати вихідний tasks у getter?','sort() змінює масив на місці. Сортується новий масив після filter(), щоб уникнути побічних змін спільного стану.'),
('Як поєднуються фільтри?','Завдання має задовольняти проєкт, нормалізований текст, статус, пріоритет та обидві швидкі умови одночасно.'),
('Яка схема даних і подій?','Pinia передає дані сторінці, сторінка передає Props у TaskCard; картка генерує Emits, сторінка викликає action сховища.'),
('Чому проєкти зникають після reload?','State зберігається лише в пам’яті. Після нового запуску створюються початкові демонстраційні дані.'),
('Що дасть IndexedDB?','Постійне локальне збереження структурованих завдань і проєктів між сеансами та основу для офлайн-роботи зі змінами.'),
('Що перевіряє npm run build?','Компіляцію Vue, імпорти, production-оптимізацію та PWA-генерацію. Dev-сервер не проходить увесь production-процес.'),
('Як централізований стан допомагає масштабуванню?','Дає спільні правила змін, повторне використання обчислень, керовані залежності й основу для збереження та синхронізації.')]
for start,end in [(0,7),(7,14),(14,20)]:
 page();h(f'14 Контрольні запитання {start+1} до {end}')
 for i in range(start,end):
  q,a=qa[i];pp=doc.add_paragraph();rr=pp.add_run(f'{i+1}. {q} ');rr.bold=True;pp.add_run(a)
# Remove inherited theme fonts and decorative title borders.
for style in doc.styles:
 for borders in list(style.element.iter(qn('w:pBdr'))): borders.getparent().remove(borders)
 for fonts in style.element.iter(qn('w:rFonts')):
  for key in list(fonts.attrib):
   if 'theme' in key.lower(): del fonts.attrib[key]
for borders in list(doc.element.iter(qn('w:pBdr'))): borders.getparent().remove(borders)
OUT.parent.mkdir(parents=True,exist_ok=True);doc.save(OUT)
(BASE/'report.md').write_text('\n'.join(md)+'\n\n'+'\n\n'.join(f'{i+1}. **{q}** {a}' for i,(q,a) in enumerate(qa)))
print(OUT)
