from aiogram import Dispatcher, types
from create_bot import dp

async def unknown_command(message: types.Message):
    await message.answer('Я тебя не понимаю :( Напиши /help')

def register_handlers_other(dp : Dispatcher):
	dp.register_message_handler(unknown_command)


#---текстовые сообщения---#
info_message = (
    'Это бот-помощник для мусульман. Узнавайте время намаза, слушайте Коран, читайте книги и еще множество функции доступных для пользователей.\n\n'
    'Для поддержания работоспособности бота необходимо арендовать сервера. Помощь:\n'
    '<code>2202 2018 6984 5160</code>  (Сбер)\n\n'
    '<i>«Указавшему на благое (полагается) такая же награда, как и совершившему его». (Муслим)</i>'
)

calendar_message = (
	'Календарь на <b>1443-1444</b> год по Хиджре\n\n'
	'4 января --- 1 джумада аль-ахира\n'
	'2 февраля --- 1 раджаб\n'
	'3 февраля --- 2 раджаб	- <i>Ночь Рагаиб</i>\n'
	'27 февраля ---	26 Раджаб	- <i>Ми\'радж</i>\n'
	'4 марта --- 1 ша\'бан\n'
	'17 марта	--- 14 ша\'бан - <i>Ночь Бараат</i>\n'
	'2 апреля	--- 1 Рамадан -	<i>Начало месяца Рамадан</i>\n'
	'27 апреля --- 26 Рамадан -	<i>Ночь Кадр</i>\n'
	'2 мая --- 1 шавваль - <i>Ураза-байрам</i>\n'
	'31 мая	--- 1 Зуль-ка\'да\n'
	'30 июня --- 1 Зуль-хиджа\n'
	'8 июля	--- 9 Зуль-хиджа - <i>День \'Арафа</i>\n'
	'9 июля --- 10 Зуль-хиджа -	<i>Курбан-байрам</i>\n'
	'8 - 12 июля --- 9 - 13 Зуль-хиджа - <i>Дни такбира ат-Ташрик</i>\n'
	'30 июля --- 1 Мухаррам - <i>Начало 1444 года по Хиджре</i>\n'
	'8 августа --- 10 Мухаррам - <i>День Ашура</i>\n'
	'28 августа --- 1 сафар\n'
	'27 сентября --- 1 раби аль-авваль\n'
	'7 октября --- 11 раби аль-авваль - <i>Мавлид Ан-Наби</i>\n'
	'27 октября --- 1 раби аль-ахир\n'
	'25 ноября --- 1 джумада аль-уля\n'
	'24 декабря --- 1 джумада аль-ахир'
)

tut_namaz_message = (
	'<code><b>Что такое намаз?</b></code>\n\n'
	'<b>Намаз</b> – это персидское слово обозначает один из самых важных видов поклонения Всевышнему Аллаху: определенные слова и движения, которые вместе составляют исламский молитвенный обряд.\n'
 	'Каждый совершеннолетний (по Шариату) и находящийся в здравом уме мусульманин <b>обязан</b> сначала обучиться способу совершения намаза, а затем ежедневно – в определенные промежутки времени – выполнять его.\n'
 	'В арабском языке намаз обозначается словом «солят», что изначально означает «дуа» («мольба» – то есть обращение к Аллаху с просьбой о благе для себя или других людей). Весь комплекс слов и движений стал обозначаться этим словом, поскольку дуа – это важнейшая часть нашего намаза.\n'
 	'Намаз – это прежде всего наша связь с Аллахом, а также выражение благодарности Ему за все бесчисленные блага, которыми Он нас одарил.\n'
	'Намаз, являющийся в Исламе вторым по значимости фардом после веры, был вменен в обязанность до хиджры, в Мекке в ночь Ми‘радж.\n\n'
	'<b><u>Намаз обязателен для каждого человека, в котором объединились три условия:</u></b>\n\n'
 	'1. <b>Ислам.</b> Немусульмане не обязаны совершать намаз\n\n'
 	'2. <b>Совершеннолетие по Шариату.</b> До этого ребенок не обязан совершать намаз.\n\n'
 	'3. <b>Рассудок.</b> Для сумасшедшего совершение намаза не обязательно.\n\n'
 	'Родителям следует приучать детей к совершению намаза с семилетнего возраста. По достижении ими десяти лет их необходимо заставлять совершать намаз, а за несовершение – наказывать.\n\n'
	'<i>«Поистине, намаз является обязанностью для верующих в определенные промежутки времени» (сура «Ан-Ниса», аят 103)</i>'
)

tut_time_message = (
	'<code><b>Время намазов</b></code>\n\n'
	'<b>1) Утренний намаз.</b> Время утреннего намаза наступает с появлением рассвета, то есть светлой полосы на горизонте (в расписании намазов это время обозначается словом имсак/завершение сухура). Завершается же время утреннего намаза с восходом солнца.\n'

	'<i>Во всех других намазах, за исключением утреннего намаза, человек считается успевшим на намаз, если он успел произнести такбир до того, как время намаза выйдет. Однако при совершении утреннего намаза, его необходимо завершить, то есть совершить салям до того как взойдет солнце.</i>\n\n'

	'<b>2) Полуденный намаз.</b> Время полуденного намаза наступает, когда солнце достигает зенита и когда тень предметов становится минимальной. А завершается время полуденного намаза, когда тень предмета становится в два раза больше его длинны (плюс минимальная полуденная тень).\n\n'

	'<b>3) Послеполуденный намаз.</b> Время этого намаза наступает в момент завершения времени полуденного намаза и продолжается до захода солнца.\n\n'

	'<b>4) Вечерний намаз.</b> Время вечернего намаза наступает с заходом солнца и заканчивается с исчезновением зарева захода, то есть с наступлением полной темноты.\n\n'

	'<b>5) Ночной намаз.</b> Время ночного намаза наступает после завершения времени вечернего намаза и продолжается до наступления рассвета.\n'

	'<i>Однако, откладывать совершение ночного намаза на вторую половину ночи считается макрухом.</i>'
)

tut_cond_message =(
'<code><b>Условия намаза</b></code>\n\n'

'<b><u>Существует 6 условий (внешних фардов) намаза:</u></b>\n\n'

'1) <b>Очищение от хадаса</b> − устранение ритуальной нечистоты путем совершения малого или большого омовения, а также таяммума.\n\n'

'2) <b>Очищение от наджас</b> − очищение от различных нечистот тела, одежды и места моления.\n'

'<i>Наджаса бывает двух видов:</i>\n'

'<i>а) Наджасату-гализа (тяжелая наджаса). Это нечистоты, выделяемые из переднего или заднего проходов, кровь, алкоголь и свинина. Максимально допустимым размером жидкой наджасы является размер внутренней части ладони, а максимально допустимый размер твердой наджасы равен одному дирхему (приблизительно 3 грамма).</i>\n'

'<i>б) Наджасату-хафифа (легкая наджаса). Это нечистоты животных, мясо которых употребляется в пищу, а также нечистоты хищных птиц. Максимально допустимый размер такой наджасы составляет ¼ часть тела или одежды.</i>\n\n'

'3) <b>Сатру ‘аурат</b> − укрывание тех частей тела, которые считаются ‘ауратом.\n'

'<i>У мужчин ‘ауратом является часть тела от пупка до колен (включая и сами колени). У женщин же ‘ауратом является все тело за исключением лица, кистей рук и ступней.</i>\n'

'<i>‘Аурат мужчины, после достижения им совершеннолетия, не может видеть никто посторонний (в том числе его родители), за исключением его жены.</i>\n'

'<i>Места ‘аурата женщины не может видеть ни один посторонний мужчина, за исключением мужа. Однако мужчины, за которых женщина не может выйти замуж (отец, дед, брат, племянник, дядя), а так же другие женщины могут видеть части ее тела от колен и ниже, и от груди и выше.</i>\n\n'

'4) <b>Истикбалю-Кыбла</b> − совершение намаза, направившись в сторону кыблы (Ка‘абы).\n'

'<i>Строение, которое покрыто черным покрывалом и к которому мы обращаемся во время намаза, называется Ка‘абой, а так же Байтуллах. Название этой мечети – Масджидуль-Харам. Город, в котором она находится, называется Меккой. В этом городе родился посланник Аллаха s, а похоронен он в городе Медине. Точно над Ка‘абой, на небесах находится место, которое называется Байтуль-Ма‘мур, вокруг которого ежедневно семьдесят тысяч ангелов совершают обход.</i>\n'
'<i>При движении в автобусе, самолете или верхом на животном, нафль намазы (а так же фард намазы в случае крайней необходимости) могут совершаться по направлению движения.</i>\n\n'

'5) <b>Время</b> − время совершаемого намаза должно наступить.\n'

'<i>Ни один из пяти обязательных намазов не может совершаться до наступления его времени. Если же фард-намаз или ваджиб-намаз не был совершен вовремя, то он должен быть возмещен в качестве долга.</i>\n\n'

'6) <b>Намерение</b> − иметь намерение на совершение этого намаза.\n'

'<i>Знание сердцем того, какой намаз мы совершаем, является достаточным в качестве намерения.</i>\n\n'

'<b><u>Существует 6 рукнов (внутренних фардов) намаза:</u></b>\n\n'

'1) <b>Вступительный такбир</b> − приступать к совершению намаза со слов Аллаху Акбар.\n\n'

'2) <b>Кыям</b> − стояние на ногах во время намаза.\n'

'<i>Кыям является рукном при совершении фард-намазов и ваджиб-намазов (то есть сунна-намазы и нафль-намазы могут совершаться сидя даже без уважительной причины).</i>\n'

'<i>Тот, у кого нет сил стоять, может совершать намаз, прислонившись к чему-то или держась за что-то.</i>\n'

'<i>Тот, кто может некоторое время стоять на ногах, начинает намаз стоя, насколько позволяют ему силы, а затем садится и продолжает совершение намаза сидя.</i>\n'

'<i>Тот, кто не может совершать намаз стоя или не может совершить в намазе саджда, совершает намаз, сидя на полу. В случае необходимости этот человек может вытянуть ноги в сторону кыблы. Тот, кто не может сделать и этого, совершает намаз исходя из своих сил (движениями головы, сидя или лежа).</i>\n'

'<i>Тот, кто не способен двигать даже головой, оставляет совершение намаза на потом.</i>\n\n'

'3) <b>Кыра‘ат</b> − чтение во время намаза как минимум трех коротких аятов или одного длинного аята (так, чтобы человек слышал сам себя).\n\n'

'4) <b>Руку‘</b> − совершение поясного поклона в намазе.\n'
'<i>Сгибание туловища на 45 градусов или ниже (так, чтобы руки доставали до колен) является фардом. Сгибание туловища на 90 градусов (спина параллельна полу) является сунной.</i>\n\n'

'5) <b>Суджуд</b> − совершение в каждом рака‘ате намаза двух земных поклонов.\n'

'<i>Фардом является касаться земли лбом (и носом) и как минимум пальцами одной ноги.</i>\n\n'

'6) <b>Ка‘дауль-Ахира</b> − последнее сидение в конце намаза на протяжении времени, необходимого для чтения ат-тахията.\n\n'

'<b><u>Намаз и количество рака‘атов</u></b>\n\n'

'<b>В течение дня мы обязаны совершать пять намазов:</b>\n\n'

'1) <b>Утренний намаз</b> состоит из 4 рака‘атов. Два рака‘ата сунна-намаза и два рака‘ата фард-намаза.\n\n'
'2) <b>Полуденный намаз</b> состоит из 10 рака‘атов. Четырех рака‘атов первой сунны, четырех рака‘атов фард-намаза и двух рака‘атов последней сунны.\n\n'
'3) <b>Послеполуденный намаз</b> состоит из 8 рака‘атов. Четырех рака‘атов сунна-намаза и четырех рака‘атов фард-намаза.\n\n'
'4) <b>Вечерний намаз</b> состоит из 5 рака‘атов. Трех рака‘атов фард-намаза и двух рака‘атов сунна-намаза.\n\n'
'5) <b>Ночной намаз</b> состоит из 10 рака‘атов. Четырех рака‘атов первой сунны, четырех рака‘атов фард-намаза и двух рака‘атов последней сунны.\n\n'
'<b>Витр-намаз</b> состоит из 3 рака‘атов.\n\n'

'<i>Значит, в течение одного дня мы совершаем 40 рака‘атов намаза. «20 рака‘атов сунны, 17 рака‘атов фарда, и 3 рака‘ата ваджиба.</i>\n\n'

'<i>Первые сунны послеполуденного и ночного намазов являются суннами гайри муаккада.</i>'
)
tut_gusl_message = (
	'<code><b>Гусль (полное омовение)</b></code>\n\n'
	'<b><u>Фарды полного омовения:</u></b>\n'
	'1) Мадмада − полоскание рта.\n'
	'2) Истиншак − полоскание носа.\n'
	'3) Мытье всего тела с головы до ног.\n\n'

	'<b><u>Виды жидкостей, выделяемых из полового органа мужчины:</u></b>\n'
	'− моча\n'
	'− мази (предэякулят, вязкая бесцветная жидкость, выделяется в виде нескольких капель)\n'
	'− сперма (вязкая и густая бело-желтая жидкость, выделяемая в момент сексуального удовлетворения)\n'
	'− вади (жидкость, похожая на сперму, но выделяемая после мочеиспускания или после поднятия тяжестей).\n'
	'<i>Выделение спермы нарушает гусль (полное омовение), тогда как выделение других жидкостей нарушает лишь малое омовение.</i>\n\n'

	'<b><u>Особые состояния, присущие женщинам:</u></b>\n'
	'- Менструация. Минимальный срок менструации составляет три дня (72 часа), а максимальный срок составляет десять дней (240 часов). В это время женщина не совершает намаз, не соблюдает пост, не читает Куръан и не прикасается к нему, не совершает обход Ка‘абы, не посещает мечеть и не вступает в интимную близость.\n'
	'- Послеродовое кровотечение: Возникает у женщин после родов. Минимальный срок может составлять несколько мгновений, а максимальный срок составляет сорок дней. В это время женщине нельзя то же самое, что и во время менструации.\n'
	'- Кровотечение, продолжавшееся менее трех дней или более десяти дней при месячных, а также более сорока дней при послеродовом кровотечении, является истихадой (кровотечением, которое вызвано каким-либо недугом). Женщина в таком состоянии подобна ма‘зуру, у которого, к примеру, из носа постоянно течет кровь. То есть при наступлении каждого времени намаза, она должна делать малое омовение и совершать поклонение.\n'
	'- После завершения менструации или послеродового кровотечения, или при истечении их максимального срока, женщина должна совершить полное омовение и приступить к совершению своих поклонений (намазы, пропущенные в период месячных, не возмещаются, тогда как пропущенные дни поста необходимо будет возместить).\n\n'

	'<b><u>Обстоятельства, нарушающие гусль, и требующие его выполнения:</u></b>\n'
	'1) семяизвержение;\n'
	'2) половой акт (даже если не было семяизвержения);\n'
	'3) поллюция (семяизвержение во сне);\n'
	'4) завершение месячных и послеродового кровотечения у женщин.\n\n'

	'<b><u>Что нельзя делать в состоянии джанаба (полового осквернения)?</u></b>\n'
	'1) Входить в мечеть;\n'
	'2) совершать намаз;\n'
	'3) читать Куръан и прикасаться к нему;\n'
	'4) совершать саджда-тилява;\n'
	'5) совершать обход Ка‘абы;\n'
	'6) есть и пить, не прополоскав рта и носа (это считается макрухом).\n\n'

	'<b><u>Сунны гусля:</u></b>\n'
	'1) Совершение намерения.\n'
	'2) Приступать к совершению полного омовения с произнесением Бисмиллях.\n'
	'3) Сначала помыть места ‘аурата.\n'
	'4) После этого, перед гуслем сделать малое омовение.\n'
	'5) Сначала помыть голову, правое и левое плечо по три раза, а затем обмыть оставшиеся части тела.\n\n'

	'<b><u>Совершение полного омовения является сунной в следующих случаях:</u></b>\n'
	'1) Перед джурм‘а-намазом.\n'
	'2) Перед праздничными намазами.\n'
	'3) Во время хаджа, перед одеванием ихрама.\n'
	'4) Перед стоянием в долине ‘Арафат.'
)

tut_taharat_message = (
'<code><b>Тахарат (малое омовение)</b></code>\n\n'

'<b><u>Фарды малого омовения</u>:</b>\n'
'1) мыть лицо от корней волос на лбу до подбородка, и от мочки одного уха до мочки другого;\n'
'2) мыть руки, включая локти;\n'
'3) протереть ¼ часть головы;\n'
'4) мыть ноги, включая щиколотки.\n\n'

'<b><u>Сунны малого омовения:</u></b>\n'
'1) сделать намерение;\n'
'2) произнести Бисмиллях;\n'
'3) помыть руки до запястья;\n'
'4) трижды прополоскать рот;\n'
'5) трижды прополоскать нос;\n'
'6) использовать мисвак при совершении малого омовения;\n'
'7) обмывать каждую часть тела, не делая пауз;\n'
'8) мыть каждую часть тела по три раза;\n'
'9) начинать обмывать парные органы с правой стороны;\n'
'10) мыть между пальцами рук и ног;\n'
'11) протирать уши;\n'
'12) протирать шею;\n'
'13) протирать голову полностью.\n\n'

'<b><u>Малое омовение нарушают следующие обстоятельства:</u></b>\n'
'1) выделение нечистот из переднего или заднего проходов;\n'
'2) выпускание газов;\n'
'3) выделение крови или гноя из какой-либо части тела;\n'
'4) кровотечение из десен, если кровь составляет больше половины слюны;\n'
'5) рвота полным ртом;\n'
'6) громкий смех во время намаза;\n'
'7) сон в положении лежа или прислонившись к чему-либо;\n'
'8) потеря сознания, разума или состояние опьянения.\n\n'

'<b><u>Что нельзя делать без малого омовения?</u></b>\n'
'1) Совершать любые виды намазов.\n'
'2) Притрагиваться к Куръану (можно брать Куръан через ткань).\n'
'3) Совершать саджда-тилява.\n'
'4) Совершать таваф (обход Ка‘абы).\n\n'

'<b><u>‘Узр (Оправдание)</u></b>\n'
'Если кровотечение или выделение иной жидкости можно остановить при помощи повязки, то омовение совершается поверх этой повязки (если же вода может причинить вред, то в этом случае повязка протирается влажной рукой).\n'
'Если же кровотечение или выделение иной жидкости не прекращается, то в этом случае человек считается ма‘зуром (человеком, имеющим оправдание). При первом возникновении этого недуга следует подождать, пока до завершения времени намаза не останется приблизительно 10 минут, сделать малое омовение и совершить намаз, даже если кровотечение будет продолжаться. При совершении последующих намазов уже не нужно ждать времени, близкого к завершению. Однако ма‘зур должен совершать омовение с наступлением времени каждого намаза, после чего в течение всего этого времени он может совершать сколько угодно намазов.\n\n'

'<b><u>Истибра</u></b>\n'
'Ожидание мужчинами в течение некоторого времени окончания выделения мочи после мочеиспускания, после чего совершается малое омовение (для того, чтобы в это время нижнее белье не испачкалось нечистотами, можно использовать вату, салфетку или кусок ткани).\n\n'

'<b><u>Протирание хуффов</u></b>\n'
'Хуффы (кожанные носки) одеваются после совершения малого омовения. После нарушения малого омовения начинается срок действия хуффов, который составляет 24 часа для того, кто постоянно проживает в данной местности. После этого при совершении малого омовения ноги не моются, а хуффы протираются влажными руками.\n'
'Для путников, которые отправились в путь протяженностью более 100 километров, срок действия хуффов составляет 72 часа.\n'
'<i>Использование: Протирание хуффов осуществляется как минимум тремя влажными пальцами руки, которыми протирается верхняя часть хуффов (правая нога протирается правой рукой, а левая нога протирается левой рукой).</i>'
)
tut_forma_message = (
'<code><b>Форма совершения намаза</b></code>\n\n'
'<b><u>Совершение намаза 2 ракаата</u></b>\n\n'
'<b>1. Намерение.</b> Встаньте на место намаза (намазлык) в направлении Каабы. Опустите руки вдоль туловища. Взгляд обратите на место саджда (место, которого касаются головой при земном поклоне). Расстояние между ступнями четыре пальца руки. Пусть в вашем сердце появится намерение совершить намаз, обратитесь к Аллаху: <i>"О Аллах я намереваюсь совершить 2 ракаата сунны утреннего намаза, ради Твоего довольства мной"</i>.\n\n'
'<b>2. Такбир.</b> Далее произнесите такбир. То есть со словами «Аллаху акбар», что переводится как «Аллах велик!» поднимите руки:\n'
'- Мужчины до уровня ушей открытыми ладонями в сторону Каабы.\n'
'- Женщины произносят такбир, поднимая руки до уровня груди.\n\n'
'<b>3. Кыям.</b> Затем мужчины складывают руки на животе ниже пупка. Женщины складывают руки на груди. Ладонь правой руки ложится на левую руку. Когда вы сложили руки, вы находитесь в состоянии кыяма – стояния в намазе. В это время читаются дуа и суры из Корана:\n'
'- Дуа «Субханака» читается первой, она переводится как дуа восхваления. У него есть еще одно название «сэнэ»:\n'
'<i>Сүбхәәнәкәл-лааһүммә үә бихәмдикә үә тәбәәракәс-мүкә үә тәгәәләә җәддүкә үә ләәә иләәһә гайрукә.</i>\n'
'<b>Перевод: «Аллах - превыше всего. Мой Аллах, обращаюсь к Тебе, прося прощения и восхваляя Тебя. Имя Твое благословенно. Твое величие безмерно (Твоя слава безгранична) и нет никакого божества, кроме Тебя».</b>\n'
'- Затем произносим агузу и бисмилля:\n' 
'<i>Әгүүзү билләәһи минәш-шәйтаанир-раҗиим. Бисмилләәһир-рахмәәнир-рахиим.</i>\n'
'Перевод: «Прибегаю к Аллаху за помощью против Шайтана, побиваемого камнями. Во имя Аллаха Милостивого, Милующего».\n'
'- Далее читаем суру Корана «Фатиха» переводится как открывающая. У нас ее чаще называют «Элхэм».\n'
'<i>Әлхәмдү лилләәһи раббил-гәәләмиин. Әр-рахмәәнир-рахиим. Мәәлики-йәүмид-диин. Иййәәкә нәгьбүдү үә иййәәкә нәстәгиин. Иһдинәс-сыйрааталь-мүстәкыйм. Сыйрааталь-ләзиинә әнгәмтә гәләйһим. Гайриль-мәгъдууби гәләйһим үәләд-дааааааллиин. Әәмиин.</i>\n'
'Перевод: «Во имя Аллаха, Милостивого, Милующего! Хвала Аллаху, Господу миров, Милостивому, Милующему, Властелину Дня воздаяния! Тебе одному мы поклоняемся и Тебя одного молим о помощи. Веди нас прямым путем, путем тех, кого Ты облагодетельствовал, не тех, на кого пал гнев, и не заблудших». Амин. (Прими мою молитву.)\n'
'- Затем читается еще одна дополнительная сура из Корана:\n'
'<i>Бисмилләәһир-рахмәәнир-рахиим. Куль һүүәллааһу әхәд. Аллааһус-самәд. Ләм йәлид үә ләм йүүләд. Үә ләм йәкүлләһүү күфүүән әхәд.</i>\n'
'Перевод: «Скажи: «Он - Аллах - Един, Аллах - Вечен. Не родил и не был рожден, и никто не может равняться с Ним».\n\n'
'<b>4. Рукуг.</b> Затем со словами "Аллаху акбар" совершается рукуг -поясной поклон. В этом состоянии нужно трижды произнести: <i>Сүбхәәнә раббийәл-гәзыйм</i>.\n'
'Перевод: «Хвала моему Великому Господу!»\n\n'
'<b>5. После рукуг выпрямите тело до вертикального положения.</b> Выпрямляясь произнесите: <i>Сәмигәл-лааһу лимән хәмидәһ.</i>\n'
'Перевод: Да услышит Аллах восхваляющего Его.\n\n'
'<b>6. Выпрямившись полностью</b> произнесите: <i>Раббәнәә ләкәл-хәмд.</i>\n'
'Перевод: Господь наш хвала тебе.\n\n'
'<b>7. Саджда.</b> После этого со словами <i>«Аллаху акбар»</i> совершите саджда - земной поклон. Сначала на пол опускаются колени, затем ладони, а после этого человек касается пола лбом и носом. В этом состоянии следует трижды произнести: <i>Сүбхәәнә раббийәл-әгьләә.</i>\n'
'Перевод: Хвала моему Господу Всевышнему!\n\n'
'<b>8. Второе саджда.</b> Затем со словами <i>«Аллаху акбар»</i> выпрямитесь и сядьте на ноги. Посидите несколько секунд и со словами <i>«Аллаху акбар»</i> совершите второй саджда, когда коснетесь лбом и носом пола снова трижды произнесите: <i>Сүбхәәнә раббийәл-әгьләә.</i>\n'
'Перевод: Хвала моему Господу Всевышнему!\n\n'
'<b>9. Второй ракаат.</b> Затем, со словами <i>«Аллаху акбар»</i>, встаньте для исполнения второго ракаата. Руки смыкаются на прежнем месте. На этом первый ракаат заканчивается. Второй ракаат совершается также как первый кроме:\n'
'- Не читается дуа «субханака».\n'
'- Не произносится агузу.\n\n'
'<b>10. Сидение.</b> Дальше до 2 сажда читаем как первый ракаат, а после 2 саджда человек садится. Взгляд обращен на колени. Руки лежат на коленях, пальцы - в свободном положении. В этом состоянии читаем 3 дуа:\n'
'<b>- Ташаххуд:</b> <i>Әт-тәхиййәәтү лилләәһи үәс-саләүәәтү үәт-таййибәәт. Әс-сәләәмү гәләйкә әййүһән-нәбиййү үә рахмәтул-лааһи үә бәракәәтүһ. Әс-сәләәмү гәләйнәә үә гәләә гибәәдил-ләәһиссаалихиин. Әшһәдү әл-ләәә иләәһә илләл-лааһу үә әшһәдү әннә Мүхәммәдән гәбдүһүү үә расүүлүһ.</i>\n'
'Перевод: «Почести Аллаху и молитвы и добрые слова. Мир и здравие тебе, о Пророк! И милость Аллаха и Его благодать. Мир и здравие нам и добрым рабам Аллаха. Я свидетельствую, что нет божества, кроме Аллаха, еще свидетельствую, что Мухаммад Его раб и Посланник».\n'
'<b>- Салават:</b> <i>Әаллааһүммә салли гәләә Мүхәммәдин үә гәләә әәли Мүхәммәд. Кәмәә салләйтә гәләә Ибрааһиимә үә гәләә әәли Ибрааһиимә иннәкә хәмиидүм-мәҗиид. Әллааһүммә бәәрик гәләә Мүхәммәдин үә гәләә әәли Мүхәммәд. Кәмәә бәәрактә гәләә Ибраһиимә үә гәләә әәли Ибраһиимә иннәкә хәмиидүм-мәҗиид.</i>\n'
'Перевод: «О, Аллах! Благослови Мухаммада и семью Мухаммада, так же, как благословил Ты Ибрахима и семью Ибрахима. О, Аллах! Ниспошли благодать на Мухаммада и семью Мухаммада, так же как ниспослал на Ибрахима и на семью Ибрахима во всех мирах! Истинно, Ты достоин похвалы и славы».\n'
'<b>- Раббана:</b> <i>Раббәнәә әәтинә фид-дүньйәә хәсәнәтән үә фил-әхыарати хәсәнәтән үә кыйнәә гәзәәбән-нәәр.</i>\n'
'Перевод: «Господь наш, даруй нам добро в ближайшей и в загробной жизни и защити нас от наказания геенны огненной».\n\n'
'<b>11. Салям.</b> После этого совершается салям, при этом голова поворачивается сначала вправо, а затем влево, во время саляма взгляд направлен на плечи. При каждом повороте головы произносим: <i>Әс-сәләәмү галәйкүм үә рахмәтуллаһ.</i>\n'
'Перевод: «Да будет над вами мир, милость и благодать Аллаха».\n\n'
'<b>12. Дуа.</b>  Затем подняв руки читаем дуа: <i>Әллааһүммә әңтәс-сәләәмү үә миңкәс-сәләәмү тәбәәрактә йәә зәл-җәләәли үәл-икраам.</i>\n'
'Перевод: «Аллах, Ты – мир и от Тебя – мир. Ты – Благословенный и Возвышенный, Обладающий величием и почетом. Аллах, неустанно я поминаю Тебя».\n'
'Таким образом, намаз считается завершенным.\n\n'

'<b><u>Намазы, состоящие из 4 рака‘атов:</u></b>\n\n'
'а) 4-х рака‘атные фард-намазы читаются следующим образом:\n'
'1-й рака‘ат: Субханакя, А‘узу, Бисмиллях, Фатиха, дополнительная сура.\n'
'2-й рака‘ат: Бисмиллях, Фатиха, дополнительная сура.\n'
'Первое сидение: Ат-тахият.\n'
'3-й рака‘ат: Бисмиллях, Фатиха.\n'
'4-й рака‘ат: Бисмиллях, Фатиха.\n'
'Последнее сидение: Ат-тахият, Салли-Барик, Раббана атина.\n\n'
'б) 4-х рака‘атные намазы, являющиеся сунной-муаккада (например, первая сунна полуденного намаза, а так же первая и последняя сунна джум‘а-намаза):\n'
'1-й рака‘ат: Субханакя, А‘узу, Бисмиллях, Фатиха, дополнительная сура.\n'
'2-й рака‘ат: Бисмиллях, Фатиха, дополнительная сура.\n'
'Первое сидение: Ат-тахият.\n'
'3-й рака‘ат: Бисмиллях, Фатиха, дополнительная сура.\n'
'4-й рака‘ат: Бисмиллях, Фатиха, дополнительная сура.\n'
'Последнее сидение: Ат-тахият, Салли-Барик, Раббана атина.\n'
'<i>Единственным отличием от фард-намаза является то, что в данном случае в 3-м и 4-м рака‘атах после суры аль-Фатиха читаются дополнительные суры.</i>'
)

tut_sura_message = (
'<code><b>Суры и дуа намаза</b></code>\n\n'
'<b><u>Первый ракаат:</u></b>\n'
'<b>1. Намерение</b>\n'
'<b>2. Такбир</b>\n'
'<b>3. Дуа сана</b>\n'
'<b>4. Истиаза и басмала</b>\n'
'<b>5. Фатиха</b>\n'
'<b>6. Вторая сура</b>\n'
'<b>7. Руку\' – поясной поклон.</b>\n' 
'<b>8. Выпрямление с руку\'а</b>\n' 
'<b>9. Суджуд</b>\n'
'<b>10. Ку\'уд</b>\n'
'<b>11. Выход из суджуда</b>\n\n'

'<b>1. Намерение:</b> <i>«Я намерился выполнить два ракаата  (фарз или сунна) сегодняшнего (какого намаза?) намаза ради Аллаха».</i>\n\n'
'<b>2. Такбир:</b> <i>«Аллаху Акбар» ( Аллах — велик!)</i>.\n\n'
'<b>3. Дуа сана:</b> <i>Сөбъхәәнәкәл-лааһүммә үә бихәмдикә үә тәбәәракәс-мүкә үә тәгәәләә җәддүкә үә ләәә иләәһә гайрүк.</i>\n\n'
'<b>4. Истиаза и бисмала:</b> <i>Әгүүз̣ү билләәһи минәш-шәйтаанир-раҗиим. Бисмилләәһир-рахмәәнир-рахиим.</i>\n\n'
'<b>5. Сура "Фатиха":</b> <i>Бисмилләәһир-рахмәәнир-рахиим. Әл-хәмдү лилләәһи раббил-гәәләмиин. Әр-рахмәәнир-рахиим. Мәәлики-йәүмид-диин. Иййәәкә нәгбүдү үә иййәәкә нәстәгиин. Иһдинәс-сырааталь-мүстәкыйм.  Сырааталь-ләз̣иинә әнгәмтә гәләйһим. Гайриль-мәгдууби гәләйһим үәләд-дааааааллиин. Әмин.</i>\n\n'
'<b>6. Вторая сура. "Ихлас":</b>  <i>Бисмиллээһир-рахмээнир-рахиим. Куль һувэллааһу ахэд. Аллааһус-самэд. Лэм йэлид вэ лэм йулэд. Вэ лэм йэкуллуһу куфувэн эхэд.</i>\n\n'
'<b>7. Руку\' – поясной поклон:</b> со словами <i>«Аллаху Акбар»</i> совершить поясной поклон и в этом положении читать <i>Субхана рабби аль \'Азым 3 раза.</i>\n\n'
'<b>8. Выпрямление с руку\'а:</b> <i>Сами\'Аллаху лиман хамидах.</i> Полностью выпрямившись, произносится: <i>Раббана лякяль хамд</i>\n\n'
'<b>9. Суджуд – земной поклон:</b> сказав <i>«Аллаху Акбар»</i>, коснуться пола сначала коленями, потом руками, потом лбом и носом; при этом голова находится между кистями рук, ноги не отрываются от земли, глаза смотрят на кончик носа. В этом положении повторить 3 раза: <i>Субхана Рабби альА\'ля</i>\n\n'
'<b>10.Ку\'уд:</b> сидение между двумя суджудами: со словами <i>«Аллаху Акбар»</i> оторвать лоб от земли и сесть на колени. Руки положить на колени, взгляд направлен на бедра. Со словами <i>«Аллаху Акбар»</i> совершается второй суджуд и в этом положении читается <i>«Субхана Рабби аль А\'ля» 3 раза.</i>\n\n'
'<b>11. Выход из суджуда:</b> Встать со словами <i>«Аллаху Акбар»</i> (для чтения второго рака\'ата) и в положении кыяма (стоя) сомкнуть руки на животе (мужчины) или на груди (женщины).'
)

tut_women_message = (
	'<code><b>Женский намаз</b></code>\n\n'
	'<a href="https://www.youtube.com/watch?v=97gt9Wtwlq4">Видео на татарском языке</a>\n\n'
	'<a href="https://www.youtube.com/watch?v=oKJt6pS-ICU">Видео на русском языке</a>\n\n'
)