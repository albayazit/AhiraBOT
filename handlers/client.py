from aiogram import Dispatcher, types
from create_bot import dp
from keyboards import client_kb
from parcer import parcer_dagestan, parcer_kazakhstan, parcer_other, parcer_tatarstan, parcer_hadis, parcer_codes, parcer_food
from handlers import other
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import sqlite_bd
from datetime import datetime
from create_bot import scheduler, bot
import asyncio

# FSM
class FSMaddress(StatesGroup):
	address = State()
	school = State()

class FSMtracker(StatesGroup):
	fajr = State()
	zuhr = State()
	asr = State()
	magrib = State()
	isha = State()
	vitr = State()
	first_date = State()
	second_date = State()

class FSMhalal(StatesGroup):
	code = State()

# max message length
MESS_MAX_LENGTH = 4096
# по умолчанию
current_city = 'Казань'
# months
months = {
	'1':'Январь',
	'2':'Февраль',
	'3':'Март',
	'4':'Апрель',
	'5':'Май',
	'6':'Июнь',
	'7':'Июль',
	'8':'Август',
	'9':'Сентябрь',
	'10':'Октябрь',
	'11':'Ноябрь',
	'12':'Декабрь'
}

zikrs = {
	'1':'Салават',
	'2':'Дуа за родителей',
	'3':'Калима Тавхид',
	'4':'Субханаллаһи ва бихамдиһи',
	'5':'Аллаһумма иннака `афуун...',
	'6':'Дуа "Кунут"',
	'7':'Аят "Аль-Курси"',
	'8':'Ля хауля уа ляя куввата илляя билляһ',
	'9':'Хасбуналлаһу ва ни`маль вакиль',
	'10':'Субханаллаһ валь хамдулилляһ',
	'11':'Ля иляха илляллаһу вахдаху ля шарика ляһ',
	'12':'Ля иляһа илля анта субханака',
	'13':'Раббана атина фи-д-дунья',
	'14':'Аллаһумма а`инни `аля зикрика',
	'15':'Таравих тасбих',
	'16':'Без категории',
}

zikr_polzi = {
	'1':'<b>Лишь малая часть из польз салавата:</b>\n\n1. «В Судный день из людей ближе всего будет ко мне тот, кто больше всех произносил мне салаваты и салямы» (Тирмизи, Витр, 21)\n\n2. «Совершайте салаваты и салямы мне. Ведь где бы вы ни были, ваши салаваты и салямы доносятся мне» (Абу Дауд, Манасик, 96-97/2042)\n\n3. «Кто совершит салават и салям мне один раз, тому Всевышний Аллах дарует десять милостей» (Муслим, Салят, 70)\n 4. Посланник Аллаха (мир ему и благословение Аллаха) сказал: «Будет скупым тот человек, кто не отправит мне приветствия, если мое имя упоминается в его присутствии» (Тирмизи)\n\n5. «Да будет отстранен от милости тот, кто не произнес салават и салям, услышав мое имя! Да будет отстранен от милости тот, кто прожил месяц Рамадан и не заслужил прощения! Да будет отстранен от милости тот, кто не заслужил довольства своих пожилых родителей и не удостоился рая!» (Тирмизи, Да’ват, 100/3545)',
	'2':'<b>Польза "Дуа за родителей"</b>:\n\n1. (смысл): «И преклоняй пред ними [твоими родителями] крыло смирения из милосердия [будь смиренным и мягким к ним] и говори: "Господи! Помилуй их, подобно тому, как они растили меня ребёнком"». (сура «Аль-Исра»: 24)\n\n2. Сообщается, что Абу Абдуррахман Абдуллах бин Мас’уд (да будет доволен им Аллах) сказал: «Однажды я спросил Пророка (мир ему и благословение Аллаха): "Какое дело Аллах любит больше всего?" Он сказал: "Совершаемую своевременно молитву". Я спросил: "А после этого?" Он сказал: «Проявление почтительности к родителям». (Бухари, Муслим)\n\n3. Пророк (мир ему и благословение Аллаха) сказал: «Воистину, степень человека будет непрестанно возвышаться в Раю, и он скажет: "Откуда всё это?" Ему ответят: "Это по причине того, что твой сын просил за тебя прощения"». (Ибн-Маджа)\n\n4. Cообщается, что Абу Усайд Малик бин Раби’а ас-Са’иди (да будет доволен им Аллах) сказал: «Однажды, когда мы сидели с Посланником Аллаха (мир ему и благословение Аллаха), к нему пришёл какой-то человек из племени Бану Салама и спросил: "О посланник Аллаха, могу ли я каким-нибудь образом проявлять почтительность по отношению к моим родителям и после их смерти?" Он сказал: "Да, если будешь молиться за них (обращаться к Аллаху с мольбами за родителей), просить у Аллаха прощения для них, выполнять их обещания после их кончины, поддерживать родственные связи с людьми, с которыми ты связан только через (своих родителей), и оказывать уважение их друзьям"». (Абу Дауд)\n\n5. От Абдуллаха бин Амра бин аль-Аса (да будет доволен им Аллах) передаётся, что Пророк (мир ему и благословение Аллаха) сказал: «К числу тяжких грехов относятся многобожие, проявление непочтительности по отношению к родителям, убийство и ложная клятва». (Бухари)',
	'3':'Слова тавхида – самое превосходное поминание Аллаха (зикр), как об этом сказал Пророк (мир ему и благословение). Эти слова – обычай аскетов, опора мюридов, направление идущих к довольству Аллаха, подарок предыдущих, ключ от рая, ключи знаний и познания Создателя.',
	'4':'<b>Польза "Субханаллаһи ва бихамдиһи"</b>:\n\nПророк Мухаммад (мир ему и благословение) в известном хадисе сказал: «Есть два слова, которые любит Милостивый, и они легки для языка, а на Весах они будут тяжелы. (Это слова) “Слава Аллаху и хвала Ему, слава Аллаху Великому! Субхана-Ллахи ва бихамдихи, субханаЛлахиль Азым!”» (Сахих Бухари, Сахих Муслим)',
	'5':'<b>Польза "Аллаһумма иннака `афуун..."</b>:\n\nОднажды Аиша (да будет доволен ею Аллах) спросила Пророка ﷺ: «О Посланник Аллаха, скажи, если я узнаю (о наступлении) ночи предопределения, что мне следует говорить?» Пророк ﷺ ответил: «Говори: "Аллаhумма иннака ‘афуввун каримун туẍиббу-ль-‘афва фа’фу ‘анни"» (Тирмизи)',
	'6':'Согласно ханафитскому мазхабу, дуа «Кунут» читается в намазе витр (совершаемом после намаза иша), в третьем ракаате.',
	'7':'<b>Лишь малая часть из польз аята "Аль-Курси"</b>:\n\n1. «Поистине, у всего есть вершина, и сура Аль-Бакара – вершина Корана, и в этой суре есть аят, который является господином всех аятов Корана – Аятуль-Курси» (Тирмизи, Хаким)\n\n2. «Тот, кто будет произносить этот аят по утрам, для того он станет защитой до самого вечера, а кто прочитает их вечером, то будет защищен до самого утра» (Тирмизи)\n\n3. «Тому, кто читал «Аятуль-Курси» после каждой обязательной молитвы, только смерть препятствует попасть в Рай» (Насаи)',
	'8':'<b>Польза "Ля хауля уа ляя куввата илляя билляһ"</b>:\n\nПередают, что Абу Муса, да будет доволен им Аллах, сказал: «Однажды мы были вместе с Пророком, да благословит его Аллах и приветствует, в одной из поездок, и когда мы поднимались (на возвышенность), то возвеличивали Аллаха, и тогда Пророк, да благословит его Аллах и приветствует, сказал: “О люди! Умерьте свой пыл! Поистине, вы взываете не к глухому и не к отсутствующему, однако, вы взываете к Слышащему, Видящему”. Затем пришёл ‘Али, а я говорил себе: “Нет силы и мощи ни у кого, кроме Аллаха”, и тогда он сказал: “О ‘Абдуллах ибн Кайс, произноси: ‹Нет силы и мощи ни у кого, кроме Аллаха /Ля хауля ва ля куввата илля би-Ллях/›, ибо, поистине, эти слова являются одним из сокровищ Рая!” (Или он сказал: “Не указать ли мне тебе…”)». (Сахих аль-Бухари, №7386)',
	'9':'Именно эта дуа, спасшее Пророка Ибрахима, выразившее его глубокую веру в Аллаха и довольство, читается во время трудностей и испытаний. Эта дуа была ниспослана пророку Мухаммаду (мир ему), когда враги Пророка ополчились против него. И Аллах ниспослал Ему данный аят. «Люди сказали им: «Народ собрался против вас. Побойтесь же их». Однако это лишь приумножило их веру, и они сказали: «Нам достаточно Аллаха, и как прекрасен этот Попечитель и Хранитель!» [3:173]»',
	'10':'<b>Польза "Субханаллаһ валь хамдулилляһ"</b>:\n\n«Четыре вида речи являются наилучшими и тебе не повредит с какой бы ты не начал их чтение: субханаллахи, вальхамдулилляхи, ва ля иляха илля ллаху, валлаху акбар» (имамы Муслим, Ахмад, Ибн Маджах)',
	'11':'<b>Польза "Ля иляха илляллаһу вахдаху ля шарика ляһ"</b>:\n\nТот, кто 100 раз в день скажет: «Ля иляха илля-ллаху вахдаху ля шарика лях, ляху-ль-мульку ва ляху-ль-хамду ва хува аля кули шей’ин кадир» получит такую же награду, какая полагается за освобождение десяти рабов, и запишется ему совершение ста добрых дел, и будут стёрты записи о ста его дурных делах, и послужат они ему защитой от шайтана на этот день до самого вечера, и никто не сможет сделать ничего лучше того, что сделал он, кроме такого человека, который сделает ещё больше".(Бухари, Муслим)',
	'12':'<b>Польза "Ля иляһа илля анта субханака"</b>:\n\n«Мольбой Зу-н-Нуна (Пророка Юнуса), когда он находился в чреве кита, были следующие слова: “Ля иляха илля анта Субханака инни кунту мин аз-залимин”. И поистине, если какой-нибудь мусульманин попросит у Аллаха посредством этой мольбы, Аллах обязательно ответит ему». (Имам Ахмад, Тирмизи, Байхаки)',
	'13':'<b>Польза от "Раббана атина фи-д-дунья"</b>:\n\nКак передается от Анас Ибн Малика (да будет доволен им Аллах!), больше всего пророк (да благословит его Аллах и приветствует!) читал следующее дуа: «Раббана атина фиддунья хасанатан ва филь ахирати хасанатан ва кына газабаннар. О, Аллах, Господь наш, одари нас добром в этом мире и добром в Последней жизни и защити нас от мучений в огне»',
	'14':'<b>Польза от "Аллаһумма а`инни `аля зикрика"</b>:\n\nПередают со слов Му‘аза, да будет доволен им Аллах, что (однажды) Посланник Аллаха, да благословит его Аллах и приветствует, взял его за руку и сказал: «О Му‘аз, клянусь Аллахом, поистине, я люблю тебя и наказываю тебе, о Му‘аз, никогда не забывать говорить после каждой молитвы: «Аллахумма, а‘ин-ни ‘аля зикри-кя, ва шукри-кя ва хусни ‘ибадати-кя» (О Аллах, помоги мне поминать Тебя, благодарить Тебя и должным образом поклоняться Тебе)». (Абу Дауд, ан-Насаи)',
	'15':'Тасбих читается во время таравих-намазов'
}

zikr_id = {
	'1':'AgACAgIAAxkBAAIDfmMW8ZQkcsGiG1X36uh7iFavlWeNAAJswTEbEa65SEUtSzFqeWSkAQADAgADeQADKQQ',
	'2':'AgACAgIAAxkBAAIDgGMW8ZTrXidS7b7QDT4T0tGXklFNAAJtwTEbEa65SJMu-AdRfsRZAQADAgADeQADKQQ',
	'3':'AgACAgIAAxkBAAIDgmMW8ZqITE8GtzrVtPeQYHwEQqO-AAJuwTEbEa65SF4x_3iCwyxkAQADAgADeQADKQQ',
	'4':'AgACAgIAAxkBAAIDhGMW8Z5FYaA9sPGDslcefmy5KNKtAAJvwTEbEa65SAlXWoA_0n3mAQADAgADeQADKQQ',
	'5':'AgACAgIAAxkBAAIDhmMW8aEdzAgiaq1fgDgb41Aq31YUAAJwwTEbEa65SCEWtUI1Mn3qAQADAgADeQADKQQ',
	'6':'AgACAgIAAxkBAAIDiGMW8afBJ1Np-YM7epV_rIs_v_GbAAJxwTEbEa65SJAMkMAILyRSAQADAgADeQADKQQ',
	'7':'AgACAgIAAxkBAAIDimMW8an9fMEBqujJkIwgsjOlYDSZAAJywTEbEa65SDzLgYaOCya6AQADAgADeAADKQQ',
	'8':'AgACAgIAAxkBAAIDjGMW8a1os_bvBdG2Quj6Vp9aVJwjAAJzwTEbEa65SA2zj3wB_eYmAQADAgADeQADKQQ',
	'9':'AgACAgIAAxkBAAIDjmMW8bDEzFZJayDaaYcXvHVFfHXvAAJ0wTEbEa65SPTCaBwmGItsAQADAgADeQADKQQ',
	'10':'AgACAgIAAxkBAAIDkGMW8bUAAZLR4nBFLpgQC102iSE3bgACdcExGxGuuUg3vZWNPGCTzwEAAwIAA3kAAykE',
	'11':'AgACAgIAAxkBAAIDkmMW8bkHyuxI4JfDxVQwEQABYILCSwACdsExGxGuuUgHCRaeWTDyXAEAAwIAA3kAAykE',
	'12':'AgACAgIAAxkBAAIDlGMW8byMlobwy9du4B2Ig7D5e_CPAAJ3wTEbEa65SD0wV0MRL7z6AQADAgADeQADKQQ',
	'13':'AgACAgIAAxkBAAIDlmMW8b_EbV1t2Xn58c80URq_V7DzAAJ4wTEbEa65SHlV1jOCt3rXAQADAgADeQADKQQ',
	'14':'AgACAgIAAxkBAAIDmGMW8cS25ulgUKdzguGisaJdRbTSAAJ5wTEbEa65SAGDYbT3fAerAQADAgADeQADKQQ',
	'15':'AgACAgIAAxkBAAIDmmMW8crxl5vpxMlkyzFirdLOd1rPAAJ6wTEbEa65SGkXm-S4QXt_AQADAgADeQADKQQ',
	'16':'Без категории',
}

dua_id = {
	'1':'AgACAgIAAxkBAAPkYxUP2H3S0BsKOkiAaPl2OiBb820AAtHBMRtuNqhICUHNnAwFPCUBAAMCAAN5AAMpBA',
	'2':'AgACAgIAAxkBAAPmYxUP2YSivGNJWDVh5y_6nwqYZS0AAtLBMRtuNqhIojwYIhhksicBAAMCAAN5AAMpBA',
	'3':'AgACAgIAAxkBAAPnYxUP2SNfP8yY88iyceJFLWrfm-8AAtPBMRtuNqhI9RaN-YXEYZ0BAAMCAAN5AAMpBA',
	'4':'AgACAgIAAxkBAAPpYxUP2SRABSbrhRwGC4Lw_Hb2IFYAAtTBMRtuNqhIwW67DNEWa9kBAAMCAAN5AAMpBA',
	'5':'AgACAgIAAxkBAAPrYxUP2fD7B8SF7GCVWgrIa1gJzSMAAtXBMRtuNqhIYF_fHMIsyrMBAAMCAAN5AAMpBA',
	'6':'AgACAgIAAxkBAAPuYxUP2pCPLRBjwfedOKdt3Xq-hLYAAtbBMRtuNqhIYm_Xw5T66sUBAAMCAAN5AAMpBA',
	'7':'AgACAgIAAxkBAAPwYxUP2jaA8IRTkoQ12s5imifxmCsAAtfBMRtuNqhIKo6tZPC2VfUBAAMCAAN5AAMpBA',
	'8':'AgACAgIAAxkBAAPxYxUP2kgfCcc5TO1Mj7glFTwZCHQAAtjBMRtuNqhI9HNpjsToR90BAAMCAAN5AAMpBA',
	'9':'AgACAgIAAxkBAAP0YxUP2w2glMBZBYjUIRj3DRbM6NgAAtnBMRtuNqhIxlEgQwoIxVgBAAMCAAN5AAMpBA',
	'10':'AgACAgIAAxkBAAP2YxUP28fdn3dFx-Z9Q7A9zn8INakAAtrBMRtuNqhIbUtsRdqsTFwBAAMCAAN5AAMpBA',
	'11':'AgACAgIAAxkBAAP4YxUP22aw_yvqiSTC01LYcV4EqsYAAtvBMRtuNqhI74ZDWGdqm-QBAAMCAAN5AAMpBA',
	'12':'AgACAgIAAxkBAAP6YxUP3JQw1RX7Engwu4fbLu8PLUMAAtzBMRtuNqhIj5xg7YZ03vUBAAMCAAN5AAMpBA',
	'13':'AgACAgIAAxkBAAP8YxUP3JlnL4AWrdzZNSCfHIvAIH4AAt3BMRtuNqhIpMlZs1SxyJABAAMCAAN5AAMpBA'
}

names_id = {
	'1':'AgACAgIAAxkBAAIBkGMW1X868whtqdOF0lJo8ZrokK8gAALbwDEbEa65SKt1Aw_HTz7UAQADAgADeQADKQQ',
	'2':'AgACAgIAAxkBAAIBlGMW11cT4A-9uTDXCOrEvW8CnU4CAALewDEbEa65SIV1Aq6Erjv_AQADAgADeQADKQQ',
	'3':'AgACAgIAAxkBAAIBnGMW13MCigTz7FIBJLztl6fujK0jAALfwDEbEa65SNPSnVhujCTWAQADAgADeQADKQQ',
	'4':'AgACAgIAAxkBAAIBnmMW138k8BfkmsW1vyBeza4UavirAALgwDEbEa65SE4eUkMKVii0AQADAgADeQADKQQ',
	'5':'AgACAgIAAxkBAAIBoGMW15IHGGUHleKcLRzYuyHqpO04AALhwDEbEa65SL-eTNxOlHVaAQADAgADeQADKQQ',
	'6':'AgACAgIAAxkBAAIBomMW18hxA6VGSrMXfshyiyxy43nzAALiwDEbEa65SK7JVk5zdowNAQADAgADeQADKQQ',
	'7':'AgACAgIAAxkBAAIBo2MW18gKyBU7ywcc84niWO2Qgk-LAALjwDEbEa65SHpa_fxTswltAQADAgADeQADKQQ',
	'8':'AgACAgIAAxkBAAIBpWMW18lRAtEr0HgYlxnploAaBttfAALkwDEbEa65SEyllQAB50FEzgEAAwIAA3kAAykE',
	'9':'AgACAgIAAxkBAAIBpmMW18kpPq341kC6TeoDDMuogI2uAALlwDEbEa65SKNYuf_YosMFAQADAgADeQADKQQ',
	'10':'AgACAgIAAxkBAAIBp2MW18mmoA4DC9nDWRWMHXwrEeqlAALmwDEbEa65SB1Mexb62fwKAQADAgADeQADKQQ',
	'11':'AgACAgIAAxkBAAIBrGMW2CqsQgaLI-8uVKv3uKdrbT1NAALowDEbEa65SIo3kK_0vQM6AQADAgADeQADKQQ',
	'12':'AgACAgIAAxkBAAIBrmMW2CpBhjwCUJlMnir4_6YRuDlSAALpwDEbEa65SHFnI6J9AAE5DwEAAwIAA3kAAykE',
	'13':'AgACAgIAAxkBAAIBr2MW2CrsKej8d3mU2vglLwGDf4nvAALqwDEbEa65SLZyuiRPWIOTAQADAgADeQADKQQ',
	'14':'AgACAgIAAxkBAAIBsmMW2Cvw4lsJqHeuDBf1sdPkqYa9AALrwDEbEa65SEU6FgjrgY7qAQADAgADeQADKQQ',
	'15':'AgACAgIAAxkBAAIBs2MW2CuWwlUXunC4v8BeaFKOvDloAALswDEbEa65SBuZcDfWjFVEAQADAgADeQADKQQ',
	'16':'AgACAgIAAxkBAAIBtmMW2HS7x7z4dyItj6rBnJhE-P1-AALtwDEbEa65SP2D0H4kSnC5AQADAgADeQADKQQ',
	'17':'AgACAgIAAxkBAAIBuGMW2HX1Es2jTZpZI6rUM6GBBmKOAALuwDEbEa65SPwd_Yqv4QZoAQADAgADeQADKQQ',
	'18':'AgACAgIAAxkBAAIBuWMW2HVLjHfba5OnWFodZAaGaDliAALvwDEbEa65SLu5V6elE4htAQADAgADeQADKQQ',
	'19':'AgACAgIAAxkBAAIBumMW2HX1NXylZj6JrB5ztJtTN2_3AALwwDEbEa65SNHMReXWYfLBAQADAgADeQADKQQ',
	'20':'AgACAgIAAxkBAAIBu2MW2HVMlyvifCsv8350YFrRqdkmAALxwDEbEa65SLopghfinp2YAQADAgADeQADKQQ',
	'21':'AgACAgIAAxkBAAIBwGMW2O9TS125woSw9PxgZOj43uY1AALywDEbEa65SLJXlQpjAZ3UAQADAgADeQADKQQ',
	'22':'AgACAgIAAxkBAAIBwWMW2O-8wSO9zK1W363AbpHcLK2vAALzwDEbEa65SJwj8MdnujG7AQADAgADeQADKQQ',
	'23':'AgACAgIAAxkBAAIBw2MW2PBtr9fIvc30__QAAUVFxFOnWgAC9cAxGxGuuUiwVEu8nNooUAEAAwIAA3kAAykE',
	'24':'AgACAgIAAxkBAAIBxGMW2PAdW43bLR3OFz6UIH9gWlXNAAL2wDEbEa65SPL5hNwEi2X_AQADAgADeQADKQQ',
	'25':'AgACAgIAAxkBAAIBxWMW2PD7oMBWr1yPLZJkjO8ijc97AAL3wDEbEa65SBHV-YrmUsX8AQADAgADeQADKQQ',
	'26':'AgACAgIAAxkBAAIBymMW2TyVmnYECTvgL1jhrhrIzmqoAAL7wDEbEa65SIGeRvBE8H2OAQADAgADeQADKQQ',
	'27':'AgACAgIAAxkBAAIBzGMW2T0ntp0otLoiNpYb4hzVGGzHAAL8wDEbEa65SANk7RCzOwMpAQADAgADeQADKQQ',
	'28':'AgACAgIAAxkBAAIBzWMW2T2X1cQM1YX0wWWYFlroyyixAAL9wDEbEa65SNTTZZwXGjHwAQADAgADeQADKQQ',
	'29':'AgACAgIAAxkBAAIBz2MW2T0lvO63X7cy7Lkwl5xNnlzbAAL-wDEbEa65SD56P8DA4NauAQADAgADeQADKQQ',
	'30':'AgACAgIAAxkBAAIB0WMW2T3u_9LsCl9nKillLsgXXmcYAAL_wDEbEa65SPdaEDj-0n8FAQADAgADeQADKQQ',
	'31':'AgACAgIAAxkBAAIB1GMW2XTh5GCsxUXf6nd5_T2JmUDDAAPBMRsRrrlIRUqBKXFoaoMBAAMCAAN5AAMpBA',
	'32':'AgACAgIAAxkBAAIB1WMW2XSNrlzcUktIhJEga_glDS4BAAIBwTEbEa65SJ5yDUUljy1KAQADAgADeQADKQQ',
	'33':'AgACAgIAAxkBAAIB12MW2XV4-cKpA1WzexACrOYFqAh7AAICwTEbEa65SC2hTFlqw3lBAQADAgADeQADKQQ',
	'34':'AgACAgIAAxkBAAIB2GMW2XVq0tgkaWUI0_y7TwyLqggIAAIDwTEbEa65SNpQpQ6KCCvvAQADAgADeQADKQQ',
	'35':'AgACAgIAAxkBAAIB2WMW2XUKhrvgwRcD7iy6fwwyNtNeAAIEwTEbEa65SEasSmQz1aSLAQADAgADeQADKQQ',
	'36':'AgACAgIAAxkBAAIB3mMW2auadbYxDDQXDNXs5breng3SAAIFwTEbEa65SNmH2O5fXpdVAQADAgADeQADKQQ',
	'37':'AgACAgIAAxkBAAIB32MW2at2n9lj5JrNAstdQGKDfvLWAAIGwTEbEa65SJaZzLITluI7AQADAgADeQADKQQ',
	'38':'AgACAgIAAxkBAAIB4WMW2avQIY_GXW5Kj5SKsmda009GAAIHwTEbEa65SIsdRat_iVaIAQADAgADeQADKQQ',
	'39':'AgACAgIAAxkBAAIB4mMW2atSe3hVWHSK3QOiAf8w2s7xAAIIwTEbEa65SJ3msGxjOWVHAQADAgADeQADKQQ',
	'40':'AgACAgIAAxkBAAIB42MW2au66pICTrx_vqGpjlzPo7xIAAIJwTEbEa65SF6uRqwqyrevAQADAgADeQADKQQ',
	'41':'AgACAgIAAxkBAAIB6GMW2dnjtBwvx8oFIZcdOhkfmihrAAILwTEbEa65SJ2OAWU7jcngAQADAgADeQADKQQ',
	'42':'AgACAgIAAxkBAAIB6mMW2dmbBKrBAkRkPQVTAlNFQoK9AAIMwTEbEa65SPPSFrbqdPb8AQADAgADeQADKQQ',
	'43':'AgACAgIAAxkBAAIB62MW2dn7omb8cTR0GT_JznXqdZbGAAINwTEbEa65SGeOMtkgczO8AQADAgADeQADKQQ',
	'44':'AgACAgIAAxkBAAIB7GMW2dmDwK7wbXpFxvS5UjCszs2yAAIOwTEbEa65SAit6sPB1DeLAQADAgADeQADKQQ',
	'45':'AgACAgIAAxkBAAIB72MW2dkSXTBsoWdf8KYU76nDlRKvAAIPwTEbEa65SNO1GSdazKv6AQADAgADeQADKQQ',
	'46':'AgACAgIAAxkBAAIB8mMW2hK1RQHEC_HUoSvLFVxkxsNhAAIQwTEbEa65SCLsmotBnGEyAQADAgADeQADKQQ',
	'47':'AgACAgIAAxkBAAIB9GMW2hKOoGM23ZDOwusdvCT4rWbsAAIRwTEbEa65SC7XXdT4kIKTAQADAgADeQADKQQ',
	'48':'AgACAgIAAxkBAAIB9WMW2hL7mW_eZ6PWR_eN5IZYXxehAAISwTEbEa65SPYy2CdJk0r8AQADAgADeQADKQQ',
	'49':'AgACAgIAAxkBAAIB9mMW2hN6bEJWbjzMApDf06G5ER5nAAITwTEbEa65SCGUuyEOlGVuAQADAgADeQADKQQ',
	'50':'AgACAgIAAxkBAAIB-WMW2hPQUiydGSebAfp0IuHK2YJkAAIUwTEbEa65SDf6qea0s89oAQADAgADeQADKQQ',
	'51':'AgACAgIAAxkBAAIB_GMW2lZgtZONZQUAAcnN4V8_wR30cgACFcExGxGuuUixQaVqYJAW0gEAAwIAA3kAAykE',
	'52':'AgACAgIAAxkBAAIB_WMW2lbBeI_SWfCRCaqzznlcWxl6AAIWwTEbEa65SOBs5OpCmwF0AQADAgADeQADKQQ',
	'53':'AgACAgIAAxkBAAIB_2MW2laOb-hHxFwReIC68s6PyI8UAAIXwTEbEa65SFBn_EHTLvxAAQADAgADeQADKQQ',
	'54':'AgACAgIAAxkBAAICAAFjFtpWSoxWCxin-LONXAVV0OTVowACGMExGxGuuUgwyesGnSYPagEAAwIAA3kAAykE',
	'55':'AgACAgIAAxkBAAICAmMW2lbcsFmg_PWAPXInsU5kK6KQAAIZwTEbEa65SG--ayQGIeh6AQADAgADeQADKQQ',
	'56':'AgACAgIAAxkBAAICCmMW2nqVu-0qy2B098HS-79D4iOsAAIawTEbEa65SB51rSBohjdRAQADAgADeQADKQQ',
	'57':'AgACAgIAAxkBAAICC2MW2nrIOI_skZUx9q3HnOwpAAEgyQACG8ExGxGuuUiJvY0SDyy_KgEAAwIAA3kAAykE',
	'58':'AgACAgIAAxkBAAICDWMW2nu-AAE_a1yf01XyztjYV1cAAUsAAhzBMRsRrrlIZz4bxNjuBn0BAAMCAAN5AAMpBA',
	'59':'AgACAgIAAxkBAAICEGMW2ntoQOO0X0_5WMoGmb53CEzoAAIdwTEbEa65SL4sQGTvFBY0AQADAgADeQADKQQ',
	'60':'AgACAgIAAxkBAAICEmMW2ns_2-j2F7dfLkq-9Hcpj5AtAAIewTEbEa65SKizwk8hPFqYAQADAgADeQADKQQ',
	'61':'AgACAgIAAxkBAAICGGMW2wvdZrrGDvIwGFQvBqn0594FAAIgwTEbEa65SH0xh6dYu_8zAQADAgADeQADKQQ',
	'62':'AgACAgIAAxkBAAICGWMW2wvvlNwPOq6SrJ4WVbiXyRNQAAIhwTEbEa65SDt2MqMdTuTAAQADAgADeQADKQQ',
	'63':'AgACAgIAAxkBAAICG2MW2wtjCgp4fZLEemT1hC54ue1vAAIiwTEbEa65SO1k4MR4UlOsAQADAgADeQADKQQ',
	'64':'AgACAgIAAxkBAAICHGMW2wxeKS-GkwOiFbH_BKGwxOx4AAIjwTEbEa65SP2wql0uxj-KAQADAgADeQADKQQ',
	'65':'AgACAgIAAxkBAAICHWMW2wwpEFaIOCLCLZnzbKV2VH_dAAIkwTEbEa65SPPbWMgGzXorAQADAgADeQADKQQ',
	'66':'AgACAgIAAxkBAAICImMW5Bh94H5WdwKG1ZKaFrQJT5AvAAIswTEbEa65SPu7gxaqCHn7AQADAgADeQADKQQ',
	'67':'AgACAgIAAxkBAAICJGMW5Bj1eYxXDFHFNPf02PD40xE9AAItwTEbEa65SAf9gziJHwmqAQADAgADeQADKQQ',
	'68':'AgACAgIAAxkBAAICJWMW5BlTMwABfDJW428LAtNB7xrVAQACLsExGxGuuUip_IzVvPqIpAEAAwIAA3kAAykE',
	'69':'AgACAgIAAxkBAAICKGMW5Bm2AAFPHSpvB_yVYpqrl5aFrQACL8ExGxGuuUipf4WvVD4bAgEAAwIAA3kAAykE',
	'70':'AgACAgIAAxkBAAICKWMW5Bm1sIPZL0RMuE0KqZRmKVjLAAIwwTEbEa65SAd4kmZJO-d3AQADAgADeAADKQQ',
	'71':'AgACAgIAAxkBAAICLGMW5Bnr5A04gpLwbznMlMJvXfYGAAIxwTEbEa65SKYhVWj-SG_TAQADAgADeQADKQQ',
	'72':'AgACAgIAAxkBAAICLmMW5BpXguiMGK5W6dWk6KLyvIBnAAIywTEbEa65SH8mrAABioV-eQEAAwIAA3kAAykE',
	'73':'AgACAgIAAxkBAAICMGMW5Bq7Fjh1tR2INlO9D2eiKIo4AAIzwTEbEa65SCGvttQon-LMAQADAgADeQADKQQ',
	'74':'AgACAgIAAxkBAAICMmMW5BrKoiKAD64XoDOaeqZt7IQuAAI0wTEbEa65SCNj4Pv-e8nAAQADAgADeQADKQQ',
	'75':'AgACAgIAAxkBAAICM2MW5BrRHqKRWexWmgkhJ7JseHJDAAI1wTEbEa65SOvJyBR4D6GzAQADAgADeQADKQQ',
	'76':'AgACAgIAAxkBAAICNWMW5BufJQPBZqtq60YKGVTmRdzZAAI2wTEbEa65SDlaTgABLbAOEAEAAwIAA3kAAykE',
	'77':'AgACAgIAAxkBAAICN2MW5Bt3rDipICagYvCGfeZaIDFdAAI3wTEbEa65SLXZGcU58405AQADAgADeQADKQQ',
	'78':'AgACAgIAAxkBAAICOWMW5Bur0r1uBv5VvmhtwKUT6pm0AAI4wTEbEa65SGOi1M9J9pS5AQADAgADeQADKQQ',
	'79':'AgACAgIAAxkBAAICO2MW5Bv9WVzr3xBzZAdEYo-NdMpQAAI5wTEbEa65SG4wqOFOxPmwAQADAgADeQADKQQ',
	'80':'AgACAgIAAxkBAAICPGMW5BvDyHHtK_wFebCcyWblSWwFAAI6wTEbEa65SKT8U2zbFFKDAQADAgADeQADKQQ',
	'81':'AgACAgIAAxkBAAICZmMW5HqfkSakFdm2Ya2udwz2HGJ5AAI8wTEbEa65SCzGOrRQ7W_IAQADAgADeQADKQQ',
	'82':'AgACAgIAAxkBAAICaGMW5HqJM_wrFaVTQ0gQSwABEsDXtgACPcExGxGuuUiXkoZEzYN4EwEAAwIAA3kAAykE',
	'83':'AgACAgIAAxkBAAICaWMW5Hu6v55wWNQ09_eLVBKeiWPGAAI-wTEbEa65SC-6MklZKJVdAQADAgADeQADKQQ',
	'84':'AgACAgIAAxkBAAICa2MW5HvYMbukmnNQv4N9IR-kscLtAAI_wTEbEa65SAo8QbCFNYVKAQADAgADeQADKQQ',
	'85':'AgACAgIAAxkBAAICbWMW5HsT0LjcK7OVfd84gMpd9LbcAAJAwTEbEa65SFkRjnIbDHL2AQADAgADeQADKQQ',
	'86':'AgACAgIAAxkBAAICb2MW5HsXITW_I415525E3faE9QeWAAJBwTEbEa65SKrcBj2xUx4bAQADAgADeQADKQQ',
	'87':'AgACAgIAAxkBAAICcmMW5HwSUbO-N0J_20nHlRZ1kEo3AAJCwTEbEa65SGrt3NHg6Xi0AQADAgADeQADKQQ',
	'88':'AgACAgIAAxkBAAICc2MW5HxWqZBw7FB7kiOua9TD4lalAAJDwTEbEa65SKJCGnR15F7OAQADAgADeQADKQQ',
	'89':'AgACAgIAAxkBAAICdWMW5HwfkdkP1aJRUsjxVrn21IY_AAJEwTEbEa65SDcZlwABur8_bAEAAwIAA3kAAykE',
	'90':'AgACAgIAAxkBAAICd2MW5HykqTVUqDUU4ksIwfmBcCXuAAJFwTEbEa65SNJJaFyU_0h6AQADAgADeQADKQQ',
	'91':'AgACAgIAAxkBAAICemMW5KikK0d0iJBe_xBf8uZ0trTVAAJGwTEbEa65SPrVnOHYnJczAQADAgADeQADKQQ',
	'92':'AgACAgIAAxkBAAICe2MW5KnUxmcW9Fkv3coZUWvhlKU6AAJHwTEbEa65SIjrrQbJvnOXAQADAgADeQADKQQ',
	'93':'AgACAgIAAxkBAAICfGMW5KlNfqL0DcmhQ4lqk_9Yjq8ZAAJIwTEbEa65SEOZ0PFzqD7-AQADAgADeQADKQQ',
	'94':'AgACAgIAAxkBAAICfmMW5KlrINADmf__0YWQ5IiepofeAAJJwTEbEa65SMrFJlVo1APDAQADAgADeQADKQQ',
	'95':'AgACAgIAAxkBAAICf2MW5Kl2XruKV3eFAAFkYShmQ89GSgACSsExGxGuuUiK9rXkzisLNgEAAwIAA3kAAykE',
	'96':'AgACAgIAAxkBAAICgWMW5KrES9ptZW-EbFcENdi7wKbOAAJLwTEbEa65SH4b4xs7qShGAQADAgADeQADKQQ',
	'97':'AgACAgIAAxkBAAICg2MW5KoKsYBG9OaB-9zFOVA4gw--AAJMwTEbEa65SIWH5wo2kdFtAQADAgADeQADKQQ',
	'98':'AgACAgIAAxkBAAIChWMW5Kp9rTgPOOKZaCIFtF513x0PAAJNwTEbEa65SKD-K_qBcp50AQADAgADeQADKQQ',
	'99':'AgACAgIAAxkBAAIChmMW5Kp4zmpMhudJyKukcXqYt0s3AAJOwTEbEa65SMyRh4MX9vydAQADAgADeQADKQQ',
}

surah_photo = {
	'114':'AgACAgIAAxkBAAMKYxS9QDhte9760Jnh-aySU3IIbxIAAg7BMRtuNqhIViBilQyGPuwBAAMCAAN4AAMpBA',
	'113':'AgACAgIAAxkBAAMMYxS9RKXdOTfMR3rXuztqrpQnGDEAAhPBMRtuNqhIPjOzTDaldlcBAAMCAAN4AAMpBA',
	'112':'AgACAgIAAxkBAAMOYxS9SHkx0s2McTSuT462Umk8l3gAAhXBMRtuNqhI0_83V33j8tsBAAMCAAN4AAMpBA',
	'111':'AgACAgIAAxkBAAMQYxS9S7tMa50ilykTtnDYbrLLvRcAAhbBMRtuNqhI0WXBKLMkyUcBAAMCAAN4AAMpBA',
	'110':'AgACAgIAAxkBAAMSYxS9TmnKSfGgMK8NCWHOtXZDXSAAAhfBMRtuNqhIv1aJ0uYjKhwBAAMCAAN4AAMpBA',
	'109':'AgACAgIAAxkBAAMUYxS9Ukq5D6dBphP1KPcNfCIHY2oAAhnBMRtuNqhIQEws3HADzXUBAAMCAAN4AAMpBA',
	'108':'AgACAgIAAxkBAAMWYxS9Vb7pI1-HA194xmzQ4Lqm6bAAAhrBMRtuNqhIR8_Egh4277QBAAMCAAN4AAMpBA',
	'107':'AgACAgIAAxkBAAMYYxS9WGk_FJbLmMy_GMlszabazqYAAhzBMRtuNqhIQSsKbgxYTLQBAAMCAAN4AAMpBA',
	'106':'AgACAgIAAxkBAAMaYxS9W3Nb6BgWOQF3Rc7qEMGJ49cAAh3BMRtuNqhITPpOW--qe3UBAAMCAAN4AAMpBA',
	'105':'AgACAgIAAxkBAAMcYxS9X7VyAQoFsUsp_cBc4fP6QXQAAh_BMRtuNqhIxEizmvGay84BAAMCAAN4AAMpBA',
	'104':'AgACAgIAAxkBAAINH2Ml43nCmLIdxO2zg--c7VK2OLN3AAINwjEbT7IxSf5F3zT-dnJuAQADAgADeAADKQQ', 
	'103':'AgACAgIAAxkBAAINIWMl435itAsanqXc3gP2y1xCVqd3AALowTEbT7IxSYHp0EJfmRRDAQADAgADeAADKQQ',
	'102':'AgACAgIAAxkBAAINI2Ml44ZAPeCkscCRQ4f-bSC-vqfEAAITwjEbT7IxSZRhCkMWwjkrAQADAgADeAADKQQ',
	'101':'AgACAgIAAxkBAAINJWMl44nYo4W00cup97cYarDTO3cyAAIUwjEbT7IxSTAIvNbVmMnWAQADAgADeAADKQQ',
	'100':'AgACAgIAAxkBAAINJ2Ml46wNO7427SvW73D5dAABdLbWbwACFcIxG0-yMUn7P9zFlzIW7wEAAwIAA3gAAykE',
	'99':'AgACAgIAAxkBAAINKWMl47IzXnZ_E9UHdqW7C0TXZu9CAAIWwjEbT7IxScHOPd3elW0XAQADAgADeAADKQQ',
	'98':'AgACAgIAAxkBAAINK2Ml47d35qCz0Uso-tmkETJ2Eg1_AAIXwjEbT7IxSb5gdBBTZXZoAQADAgADeAADKQQ',
	'97':'AgACAgIAAxkBAAINLWMl47rKhEiDz8MNhbQBOhQpT8WwAAIYwjEbT7IxSROE0oWw_qqRAQADAgADeAADKQQ',
	'96':'AgACAgIAAxkBAAINL2Ml474SQ7wmpPIozLxmGlhePD3qAAIZwjEbT7IxSW74DogWm-r2AQADAgADeAADKQQ',
	'95':'AgACAgIAAxkBAAINMWMl48OD3ubDXNd5ZMbVjXpaxAX0AAIawjEbT7IxSYrzoGapfje9AQADAgADeAADKQQ',
	'94':'AgACAgIAAxkBAAINM2Ml48iN9lh-u7A_OFuhoIni8ktRAAIbwjEbT7IxSccO3014HQlrAQADAgADeAADKQQ',
	'93':'AgACAgIAAxkBAAINNWMl481pyGyYvkoVoZF1sdsjTBoVAAIcwjEbT7IxSfztQ5hE5-_fAQADAgADeAADKQQ',
	'92':'AgACAgIAAxkBAAINN2Ml49FBp7V6GHPeAzl3GGUUQW_AAAIdwjEbT7IxSfy5umnl5G-uAQADAgADeAADKQQ',
	'91':'AgACAgIAAxkBAAINOWMl49aI_fZ9FYMUfomIMEsRi4cRAAIewjEbT7IxSWSkY48X3L7aAQADAgADeAADKQQ',
	'90':'AgACAgIAAxkBAAINO2Ml49puWZxFZH97M-ju1924ByjgAAIfwjEbT7IxSaJoayALF7zzAQADAgADeAADKQQ',
	'89':'AgACAgIAAxkBAAINPWMl495bT_HJAZYTzz4oW55RtZ0EAAIhwjEbT7IxSeWnn5bURe11AQADAgADeAADKQQ',
	'88':'AgACAgIAAxkBAAINP2Ml4-Ip2pLMZcxafnMpgEnV5b6cAAIiwjEbT7IxSSZIWbTRQN5AAQADAgADeAADKQQ',
	'87':'AgACAgIAAxkBAAINQWMl4-eM-rX17S9CBLRia3qoc9IxAAIjwjEbT7IxSfPgW17VZs31AQADAgADeAADKQQ',
	'86':'AgACAgIAAxkBAAINQ2Ml4-zPQ1PxJ0eVBf9wCnEE0oCyAAIkwjEbT7IxSc0vGeeQ2QhHAQADAgADeAADKQQ',
	'85':'AgACAgIAAxkBAAINRWMl4_CVA-u5re7eudKlApnB5vGsAAIlwjEbT7IxSXwf9hku07maAQADAgADeAADKQQ',
	'84':'AgACAgIAAxkBAAINR2Ml4_TOUPMYjqBt3_9DRHo1UwABOwACJ8IxG0-yMUnYvpS3rIx2dAEAAwIAA3gAAykE',
	'83':'AgACAgIAAxkBAAINSWMl4_jZWy4AAQJYwC1ruCHgglZ4YAACKMIxG0-yMUmZBYGEhVL04gEAAwIAA3gAAykE',
	'82':'AgACAgIAAxkBAAINS2Ml4_wEjYl74WyXvWoCgmK5NkZtAAIpwjEbT7IxSZLWCKjWB-VIAQADAgADeAADKQQ',
	'81':'AgACAgIAAxkBAAINTWMl4_-c_AR_EuF7VhBYC1GkmKDPAAIqwjEbT7IxSUX4AmF_bS0tAQADAgADeAADKQQ',
	'80':'AgACAgIAAxkBAAINT2Ml5AOH_2kzDBcwiBCjNUqX0WgOAAIrwjEbT7IxSZ0wTKpo_YHaAQADAgADeAADKQQ',
	'79':'AgACAgIAAxkBAAINUWMl5AjV8hvlgj2YQXJZu2Jsqf_uAAILwjEbT7IxSVOET6bW0jGTAQADAgADeAADKQQ',
	'78':'AgACAgIAAxkBAAINU2Ml5AysBPEZDwmllA2p40RMWHbSAAIswjEbT7IxSdVFGZM3l80TAQADAgADeAADKQQ'
}

surah_translate = {
	'114':'<b>Сура «Ан-Нас»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nСкажи: «Я прибегаю к (защите) Господа людей, Властелина людей, Бога людей, от зла искусителя, отступающего (при упоминании Аллаха), который нашептывает в сердца людей. (Шайтан бывает) из джиннов и людей».',
	'113':'<b>Сура «Аль-Фаляк»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nСкажи: «Прибегаю к (защите) Господа рассвета от зла всех Его творений. От зла ночи, когда она наступает. От зла дующих на узлы. И от зла завистника, когда тот завидует».',
	'112':'<b>Сура «Аль-Ихлас»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nСкажи: «Он — Аллах — Один. Аллах Самодостаточен. Он не родил и не был рожден. И нет никого и ничего подобного Ему».',
	'111':'<b>Сура «Аль-Масад»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nДа отсохнут руки Абу Ляхаба, и сам он уже пропал. Не помогло ему его богатство и то, что приобрел. Он попадет в Ад, полный огня. Жена его — носильщица дров. А на шее у нее будет веревка из пальмовых волокон.',
	'110':'<b>Сура «Ан-Наср»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nКогда придет помощь Аллаха и победа, ты увидишь, как люди обращаются в религию Аллаха толпами. Возвеличивай же хвалой Господа своего и проси у Него прощения. Поистине, Он — Прощающий.',
	'109':'<b>Сура «Аль-Кафирун»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nСкажи: «О неверующие! Я не поклоняюсь тому, чему вы поклоняетесь. Вы не поклоняетесь Тому, Кому поклоняюсь я. Я не буду поклоняться тому, чему поклоняетесь вы. А вы не станете поклоняться Тому, Кому поклоняюсь я. Вам — ваша религия, а мне — моя!»',
	'108':'<b>Сура «Аль-Каусар»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nПоистине, Мы даровали тебе аль-Каусар. Поэтому молись своему Господу и совершай жертвоприношение. Поистине, твой ненавистник сам окажется бездетным.',
	'107':'<b>Сура «Аль-Ма’ун»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nВидел ли ты того, кто не верит в воздаяние? Это — тот, кто гонит сироту и не побуждает накормить бедняка. Горе молящимся, которые небрежны к своим намазам, которые совершают (намаз) напоказ и отказывают даже в малом!',
	'106':'<b>Сура «Аль-Куpaйш»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nИз-за безопасности курайшитов, безопасности их во время зимних и летних поездок, пусть же они поклоняются Господу этого Дома (Каабы), который накормил их после голода и избавил их от страха.',
	'105':'<b>Сура «Аль-Филь»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nРазве ты не видел, как поступил твой Господь с хозяевами слона? Разве Он не разрушил их злые умыслы? Он наслал на них стаи птиц. Они закидали их камнями из обожженной глины. И Аллах превратил их в подобие жеваной травы.',
	'104':'<b>Сура «Аль-Хумаза»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nГоре всякому хулителю и обидчику, который копит богатство и пересчитывает его. Он думает, что богатство даст ему вечную жизнь. Но нет! Он непременно будет ввергнут в аль-Хутома. Откуда ты узнал, что такое аль-Хутома? Это — неугасимый огонь Аллаха, который доходит до сердец. Поистине, он сомкнется над ними, (подпертый) длинными столбами.',
	'103':'<b>Сура «Аль-ʼАср»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nКлянусь временем, поистине, человек — в убытке, кроме тех, которые уверовали, совершали благие поступки, заповедовали друг другу истину и заповедовали друг другу терпение.',
	'102':'<b>Сура «Ат-Такасур»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nОтвлекло вас (от подчинения Аллаху) приумножение (земных благ), (это продолжается до тех пор) пока вы не посетите кладбища (не умрете). Но нет! В будущем вы узнаете! Еще раз нет! В будущем вы узнаете! Нет! Если бы вы знали с убежденностью (вы бы не предпочли земное вечному). Клянусь, вы обязательно увидите Ад. Вы обязательно увидите его собственными глазами! Затем в тот день (в Судный день) вас обязательно спросят о (земных) благах.',
	'101':'<b>Сура «Аль-Кариʼа»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nБедствие (Судный день)! Что такое Бедствие? Откуда ты узнал, что такое Бедствие? В тот день люди будут похожи на разлетевшихся мотыльков. А горы будут как расчесанная шерсть. Тот, чья чаша Весов окажется тяжелой, будет доволен своей жизнью. Тому же, чья чаша Весов окажется легкой, прибежищем станет Хавия. Откуда ты мог знать, что это такое? Это — пылающий (жарко) Огонь!',
	'100':'<b>Сура «Аль-ʼадият»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nКлянусь мчащимися, тяжело дышащими (конями)! Клянусь (конями) высекающими (копытами) искры! Клянусь (конями) нападающими на заре, которые окутывают (врагов густой) пылью, врываясь прямо в центр толпы (врагов). Поистине, человек своему Господу неблагодарен. И, поистине, он сам (человек) этому свидетель. Ведь он страстно любит (земные) блага. Разве он не знает, что, когда воскресят тех, что в могилах, и выявится все (тайное), что (было) в душах (людей), их Господь будет, поистине, знать обо всем (и воздаст им за их убеждения и дела)?!',
	'99':'<b>Сура «Аль-Зальзаля»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nКогда земля задрожит от сотрясений, когда земля выбросит наружу свои тяжести (захороненные ценности и тела умерших), и человек (в испуге) спросит: «Что с ней?» — в тот день она (земля) расскажет свои истории (сообщит о хороших и дурных поступках, которые на ней совершались), (расскажет) потому что твой Господь внушит ей это. В тот день люди придут группами (к месту сбора), чтобы увидеть свои дела (воздаяние за них). Кто совершил добро весом с пылинку (мельчайшую частицу), увидит его (увидит награду за него). И кто совершил зло весом с пылинку, увидит его (увидит воздаяние за него).',
	'98':'<b>Сура «Аль-Байина»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nНеверующие из людей Писания и язычников не освободились (от неверия), пока к ним не пришло ясное доказательство. (Это доказательство —) Посланник от Аллаха, который читает очищенные (от лжи и искажений) страницы. На них (этих страницах) — (содержание) правдивых (священных) Книг. Те, кому была дана Книга, разделились (на группы) лишь после того, как к ним пришло ясное доказательство. Им было приказано лишь поклоняться Аллаху — искренне лишь Ему одному, будучи верующими, а также (полноценно) совершать намаз и выплачивать закят. Это и есть правильная религия. Поистине, неверующие из людей Писания и язычников — в огне Ада. Они пребудут там вечно. Они — худшие из творений. Поистине, верующие, совершавшие праведные поступки — лучшие из творений. Их награда у их Господа — сады Рая, в которых текут реки. Они пребудут там вечно. Аллах доволен ими, и они довольны Аллахом. Это (прекрасная награда) — тем, кто боялся своего Господа (боялся Его наказания, поэтому избегал грехов).',
	'97':'<b>Сура «Аль-Кадр»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nМы, поистине, низвели его (Коран) в ночь Предопределения. Откуда ты мог знать, что такое ночь Предопределения? Ночь Предопределения лучше тысячи месяцев. Ангелы и Дух (Джибриль) спускаются в нее (в эту ночь) с разрешения их Господа (на Землю) со всеми Его повелениями. Она благополучна до наступления рассвета.',
	'96':'<b>Сура «Аль-ʼаляк»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nЧитай с именем твоего Господа, который сотворил (все сущее). Он сотворил человека из сгустка крови. Читай, ведь твой Господь — самый щедрый. Он научил (человека писать) пером. Научил человека тому, чего тот не знал. Но нет! Человек переходит границы (дозволенного), (переходит их) потому что считает, будто не нуждается (в Аллахе). Поистине, к твоему Господу — возвращение. Видел ли ты того, кто запрещает рабу (Аллаха) совершать намаз? Как думаешь, был ли он на верном пути (когда запрещал молиться) или призывал к богобоязненности? Как думаешь, а не отверг ли он (истину) и не отвернулся ли (от нее)? Неужели он не знал, что Аллах видит (его и непременно воздаст ему за его дела)? Но нет! Если он не перестанет (так себя вести), то Мы схватим его за чуб, чуб (обладатель которого) лживый и грешный. Пусть он зовет (на помощь) своих сообщников (родню и единомышленников). Мы же позовем стражей Ада! Нет же! Не подчиняйся ему (Мухаммад), но совершай земные поклоны (усердно продолжай выполнять намазы) и приближайся к Аллаху (через поклонение Ему).',
	'95':'<b>Сура «Ат-Тин»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nКлянусь смоковницей и оливой! Клянусь горой Синай! Клянусь этим безопасным городом (Меккой)! Мы, поистине, создали человека в совершенном виде. А затем Мы опустили его на самый низкий уровень, кроме тех, кто уверовал и совершал благие дела. Им — нескончаемая награда. Что же после этого не дает тебе (человек) поверить в воздаяние?! Разве Аллах не является лучшим Судьей?',
	'94':'<b>Сура «Аш-Шарх»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nРазве Мы не раскрыли твою (Мухаммад) грудь (твое сердце для света пророчества)? (Разве Мы) не сняли с тебя бремя, которое отягощало твою спину? (Разве Мы не) возвысили упоминание тебя? И, поистине, за трудностью — облегчение. Поистине, за трудностью – облегчение. И если освободился (завершил дело), то трудись (возьмись за новое дело). И устремись к Господу своему.',
	'93':'<b>Сура «Ад-Духа»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nКлянусь утром! Клянусь ночью, когда она темнеет! Не покинул тебя (Мухаммад) твой Господь и не возненавидел. Поистине, будущая жизнь лучше для тебя, чем настоящее. Господь твой обязательно воздаст тебе (в будущем благом), так что ты будешь доволен. Разве Он не нашел тебя сиротой и не приютил? И Он нашел тебя не знающим (законы Шариата) и наставил тебя (даровал знание законов Аллаха). Он нашел тебя бедным и обогатил. Поэтому не обижай сироту! Просящего не прогоняй! А о милости твоего Господа — рассказывай!',
	'92':'<b>Сура «Аль-Лейль»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nКлянусь ночью, когда она покрывает (землю тьмой)! Клянусь днем, когда он раскрывает (мир своим светом)! Клянусь Тем, кто сотворил мужчину и женщину! Поистине, ваши стремления различны. Тому, кто раздает (свое имущество на богоугодные дела) и проявляет богобоязненность, кто верит в наилучшее (в положения Ислама), Мы облегчим путь к легкости (к Раю). Тому же, кто был скуп и считал, что не нуждается (в Аллахе), кто не верил в наилучшее, Мы облегчим путь к тяжести (к Аду). Не спасет его богатство, когда он упадет (умрет). Только Мы наставляем (на верный путь). Нам принадлежат вечная жизнь и жизнь земная. Я предостерег вас от пылающего Ада. Войдет в него только самый несчастный, который не поверил (пророку) и отвернулся (от истины). Отдален (избавлен) будет от него (от Ада) самый богобоязненный, который тратит свое имущество (на благое), очищаясь (через это), и любую милость он возмещает сполна, ища (этим) лишь довольства своего Всевышнего Господа. И он будет доволен (наградой от Аллаха).',
	'91':'<b>Сура «Аш-Шамс»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nКлянусь солнцем и его (ярким) светом! Клянусь луной, следующей за ним! Клянусь днем, который выявляет его (солнца) свет! Клянусь ночью, которая скрывает его! Клянусь небом и Тем, кто его соорудил! Клянусь землей и Тем, кто ее расстелил! Клянусь душой (человеком) и Тем, кто придал ей соразмерность и дал ему (человеку) понимание греха и набожности. Поистине, преуспел тот, кто очистил ее (душу), и потерпел убыток тот, кто запятнал ее (грехами). Самудяне не поверили (своему пророку) из-за того, что перешли все границы (в своем неверии и грехах). И самый несчастный из них отправился (убивать верблюдицу). И посланник Аллаха сказал им: «Не троньте верблюдицу и ее питье!» Но они не поверили ему (Салиху) и убили ее. Тогда Господь покарал их за этот грех всех без исключения. И Он не боится последствий этого.',
	'90':'<b>Сура «Аль-Баляд»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nКлянусь этим городом (Меккой)! И ты (Мухаммад) живешь в этом городе. Клянусь родителем и теми, кого он родил! Поистине, Мы создали человека (чтобы он жил) в трудностях (так, что он от рождения и до смерти испытывает и преодолевает различные тяготы). Неужели он (неверующий) считает, что никто не справится с ним? Он говорит: «Я потратил богатство огромное (на борьбу с Исламом)!» Неужели он считает, что его никто не видел?! Разве Мы не наделили его парой глаз, языком и парой губ? Разве Мы не указали ему (верный путь) из двух путей? Он не стал преодолевать трудность (совершая хорошие поступки). Откуда ты мог узнать, что такое «аль-ʼакаба» (трудность, крутой подъем)? Освобождение раба или кормление (бедняка) в трудный (голодный) день, (кормление) сироты из родственников, или попавшего в бедственное положение нищего. Затем (следует) быть из тех, кто уверовал и заповедал другим терпение и заповедал другим милосердие. Таковы люди правой стороны. Те же, кто не поверил в Наши знамения (аяты Корана), они — люди левой стороны. Над ними сомкнется огненный свод.',
	'89':'<b>Сура «Аль-Фаджр»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nКлянусь рассветом! Клянусь десятью ночами! Клянусь четным и нечетным! Клянусь ночью, когда она уходит! Есть ли среди этих (клятв) клятва (достаточная) для обладателя разума? Разве ты не видел, что твой Господь сделал с адитами, (народом) Ирама, у которого были (дома с) колоннами?! Подобных им не было создано на земле! (И разве ты не знаешь, что Аллах сделал) с самудянами, которые пробивали скалы в долине (и строили свои дома)? (И разве ты не знаешь, как Аллах поступил) с Фараоном, обладателем кольев? Они преступали границы (дозволенного) на земле и приумножали на ней вред. И обрушил твой Господь на них бич наказания. Поистине, твой Господь все видит. Когда Господь испытывает человека, проявляя к нему щедрость и наделяя его благами, тот говорит: «Мой Господь оказал мне милость». А когда Он испытывает его, ограничивая его удел, тот говорит: «Мой Господь унизил меня!» Но нет! Вы сами не проявляете щедрость к сиротам. И вы не побуждаете друг друга кормить нищего. И вы проедаете наследство целиком (не разбирая, где ваша доля, а где чужая). И вы любите богатство страстно. Но нет! Когда земля рассыплется на кусочки (и превратится в пыль), и придет (суд или наказание) твоего Господа, и ангелы — рядами, и приведут в тот день Ад, — тогда только (неверующий) человек осознает (истину). Но зачем ему (это) осознание? (Уже будет поздно!) Он (неверующий) скажет (с сожалением): «Если бы я заранее подготовился к своей (вечной) жизни…» В тот день никто не накажет так, как наказывает Он (Аллах), и никто не наложит оковы, какие накладывает Он. (Праведному верующему скажут:) О душа, обретшая покой! Вернись к своему Господу довольной и нашедшей довольство (Аллаха)! Вернись к своему Господу довольной и нашедшей довольство (Аллаха)! Войди в Мой Рай!',
	'88':'<b>Сура «Аль-Гашия»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nДошел ли до тебя рассказ об аль-Гашия? (Некоторые) лица в тот день будут смиренны, измучены трудом, утомлены. Они будут гореть в Огне обжигающем. Их будут поить из источника кипящего. Не будет у них еды, кроме колючек. (Эта еда) не прибавит им веса и не утолит голод. (Другие же) лица в тот день будут радостны. Они будут довольны своими стараниями (в земной жизни). (Они пребудут) в высоком саду (Раю). Они не услышат там пустословия. Там — источник текущий. Там ложа поднятые. И чаши расставлены (вокруг райского источника). (Там —) подушки разложены. И ковры расстелены. Разве они не смотрят на верблюда — (на то) как он создан? На небо — как оно поднято? На горы — как они установлены? На землю — как она расстелена? Наставляй же (Мухаммад), ведь ты — наставляющий (пророк). Ты не властен над ними. А тех, кто отвернется (от истины) и не уверует, Аллах подвергнет великому наказанию. Поистине, к Нам — их возвращение. А затем Мы спросим с них (и воздадим за их поступки).',
	'87':'<b>Сура «Аль-Аʼля»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nВозвеличивай имя Господа твоего Всевышнего, (Он — Тот) кто сотворил (все сущее) и соразмерил, который предопределил и указал путь, который взрастил пастбища. А после Он превратил их в черный сор. Мы дадим тебе прочесть (Коран), и ты не забудешь (ничего из него), кроме того, что пожелает Аллах. Поистине, Он знает явное и сокрытое. Мы облегчим тебе путь к легкому. Наставляй же людей, если напоминание полезно. Воспримет (наставление) тот, кто страшится (Аллаха). И отвернется от него несчастнейший, который войдет в великий огонь. Он не сможет ни умереть там, ни жить. Преуспеет тот, кто очистился, поминал имя своего Господа и совершал намаз. Но вы предпочитаете земную жизнь. А вечная жизнь — лучше и не будет иметь конца. Поистине, об этом (говорится) в первых свитках, свитках Ибрахима и Мусы.',
	'86':'<b>Сура «Ат-Торик»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nКлянусь небом и ат-Торик! Откуда ты мог знать, что такое ат-Торик? Это — звезда, пронзающая (тьму своим светом). Нет души, у которой не было бы хранителя. Пусть человек посмотрит, из чего он сотворен. Он сотворен из излившейся жидкости, которая выходит из позвоночника и грудных костей. Поистине, Он может вернуть его. В тот день будут раскрыты все тайны. И тогда не будет у него (человека) ни силы, ни помощника. Клянусь небом, изливающим дожди! Клянусь землей, которая раскалывается! Это — Слово различающее. Это не шутка. Поистине, они строят козни. И Я воздам им за это. Так дай же неверующим отсрочку! Подожди немного.',
	'85':'<b>Сура «Аль-Бурудж»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nКлянусь небом с созвездиями! Клянусь обещанным днем! Клянусь свидетельствующим и засвидетельствованным! Прокляты хозяева рва, (хозяева) огня пылающего! И они сидели возле него, наблюдая за тем, как поступают с верующими. Они мстили им только за то, что те уверовали в Аллаха Могущественного, Восхваляемого. Ему принадлежит власть над небесами и землей. Аллах — Cвидетель всему! Поистине, кто подвергал мучениям верующих мужчин и женщин и не покаялся, тем — адские муки, муки обжигающего огня. Поистине, кто уверовал и совершал благие поступки, тем — райские сады, в которых текут реки. Это — великое счастье! Поистине, кара твоего Господа страшна! Поистине, Он творит и возвращает. Он — Прощающий, Любящий, владыка Трона, Славный. Он вершит все, что пожелает. Дошел ли до тебя рассказ о войске Фараона и самудянах? Но неверующие считают это ложью. Аллах же (Своим Знанием и Могуществом) охватывает их. Это — величественный Коран в Хранимой скрижали.',
	'84':'<b>Сура «Аль-Иншикак»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nКогда небо расколется, внемля своему Господу, как и должно, когда земля вытянется, извергнет то, что внутри ее, и опустошится, внемля своему Господу, как и положено. О человек! Ты стараешься (и итог твоих стараний) — у твоего Господа. Ты встретишься с Ним. А для того, кому его книга будет вручена в правую руку, отчет будет легким. И он вернется к своей семье радостным. А тот, кому его книга будет подана из-за спины, призовет смерть. Он будет гореть в Аду. В кругу семьи он радовался. Он думал, что не вернется обратно. Но нет! Поистине, его Господь видел его. Клянусь вечерней зарей! Клянусь ночью и тем, что она покрывает! Клянусь полной луною! Вы будете переходить из одного состояния в другое. Что же с ними? Почему же они не верят? Почему не совершают земной поклон, когда им читают Коран? Но неверующие считают это ложью. Аллах лучше знает, что у них внутри. Обрадуй же их болезненным наказанием, (всех людей) кроме тех, кто уверовал и совершал праведные поступки. Им уготована нескончаемая награда.',
	'83':'<b>Сура «Аль-Мутаффифун»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nГоре обвешивающим, тем, кто, (покупая и) взвешивая у других, требует сполна, а когда отмеряют или взвешивают для других, то наносят им убытки. Разве не думают они, что будут воскрешены для Великого дня, дня, когда люди предстанут перед Господом миров?! Нет же! Книга нечестивцев окажется в Сиджине. Откуда ты мог знать, что такое Сиджин? Это — запечатанная книга. Горе в тот день тем, кто не верил в него, кто не верил в День воздаяния! А не верит в него только преступник и грешник. Когда ему читают Наши аяты, он говорит: «Это — сказки древних народов!» Нет же! Окутали их деяния их сердца. Нет же! В тот день они будут отделены от своего Господа завесой. А затем они попадут в Ад. Затем им скажут: «Вот то, во что вы не верили!» Но нет! Книга праведников окажется в Иллийюне. Откуда ты мог знать, что такое Иллийюн? Это — запечатанная книга. ам находятся приближенные (ангелы). Поистине, праведники — в блаженстве. Они будут на ложах созерцать (красоты Рая). Ты увидишь на их лицах блеск блаженства. Их будут поить запечатанным вином. В конце (питья оно пахнет как) миск. Пусть же к этому стремятся стремящиеся! Оно смешано с (напитком) из Таснима, источника, из которого пьют приближенные. Поистине, преступники смеялись над верующими. Когда (верующие) проходили мимо них, они перемигивались. А когда возвращались к своим семьям, веселились. Когда видели их, говорили: «Поистине, вот эти сбились с истинного пути». Но они (неверующие) не были посланы к ним наблюдателями. Но в этот день верующие будут смеяться над неверующими, созерцая на ложах: получают ли неверующие воздаяние за то, как они поступали?',
	'82':'<b>Сура «Аль-Инфитар»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nКогда небо разломится, когда звезды рассыплются, когда моря смешаются, когда могилы перевернутся, каждый человек узнает, что он совершал и что оставил после себя. О человек! Что обмануло тебя относительно твоего Щедрого Господа, (Ведь Аллах – тот) Кто сотворил тебя и придал тебе совершенное и соразмеренное строение? Он придал тебе образ, какой пожелал. Но нет! Вы все равно не верите в воздаяние! Поистине, у вас есть наблюдатели, благородные писари. Они знают обо всем, что вы делаете. Поистине, праведники — в блаженстве. И, поистине, нечестивцы — в Аду. Они войдут туда в День воздаяния. И они не выйдут оттуда. Откуда ты (Мухаммад) мог знать, что такое День воздаяния? Действительно, откуда ты мог знать, что такое День воздаяния? В тот день ни один человек ничем не поможет другому. И вся власть в тот день будет у Аллаха.',
	'81':'<b>Сура «Ат-Таквир»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nКогда солнце будет свернуто, когда звезды упадут, когда горы сдвинутся, когда верблюдицы на десятом месяце беременности пропадут, когда дикие животные будут собраны, когда моря запылают, когда души воссоединятся, когда погребенную заживо спросят, за какой грех ее убили, когда свитки будут развернуты, когда небо будет сдернуто, когда Ад будет разожжен, когда Рай будет приближен, тогда узнает душа, с чем пришла. И клянусь (небесными телами) появляющимися, движущимися и исчезающими! Клянусь ночью наступающей! Клянусь утром светлеющим! (Клянусь в том, что) это — слова благородного посланника, обладателя силы и высокого положения при Властелине Арша. Ему там (на небесах) повинуются и доверяют. (Также клянусь, что) ваш знакомый (Мухаммад) не одержимый. Он видел его (Джибриля) на ясном горизонте. Он не скупится передать скрытое. Это — не речь проклятого шайтана. Куда же вы уходите? Это не что иное, как напоминание для миров. Для тех из вас, кто желает следовать верным путем. Но вы не пожелаете этого, если этого не пожелает Аллах, Господь миров.',
	'80':'<b>Сура «’Абаса»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nОн нахмурился и отвернулся, оттого, что к нему пришел слепой. Откуда ты знаешь? Возможно, он очистится или примет наставление, и оно принесет ему пользу. А тому, кто решил, что он (ни в чем) не нуждается, ты уделяешь внимание. Не будет твоей вины, если он не очистится. А того, кто приходит к тебе, спеша и боясь (Аллаха), ты оставляешь без внимания. Но нет! Это — напоминание. И кто пожелает, вспомнит его. Оно — в почитаемых свитках. (Эти свитки) возвышены и чисты. (Они) в руках посланцев благородных и благочестивых. Да будет проклят человек (неверующий)! Как же он неблагодарен! Из чего Аллах сотворил его? Он сотворил его из капли и предопределил (все события его жизни). Затем (Аллах) облегчил ему путь. Затем умертвил его и поместил в могилу. Затем, когда пожелает, (Аллах) воскресит его. Но нет! (Человек) не выполняет того, что (Аллах) ему повелел. Пусть посмотрит человек на свою еду! Мы проливаем обильные ливни, затем рассекаем землю трещинами. И (Мы) взращиваем в ней семена, виноград и люцерну, оливы и пальмы, густые сады, фрукты и травы (все это) на пользу вам и вашему скоту. Когда же раздастся оглушительный шум, в этот день человек побежит от своего брата, матери и отца, жены и детей. В этот день каждый человек будет заботиться только о себе. В тот день одни лица будут сияющими, смеющимися и радостными. На других же лицах в этот день будет пыль, которая покроет их тьмой. Это будут неверующие грешники.',
	'79':'<b>Сура «Назиʼат»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nКлянусь (ангелами) вырывающими (души неверующих) грубо. (Клянусь ангелами) извлекающими (души верующих) нежно. (Клянусь ангелами) плывущими плавно. (Клянусь ангелами) проносящимися стремительно. (Клянусь ангелами) исполняющими поручения. В тот день сотрясется сотрясающаяся (вселенная). Затем последует следующее сотрясение. Сердца в тот день будут трепетать. Их взгляды станут смиренными. Они говорят: «Неужели мы вернемся в прежнее состояние? Ведь мы будем истлевшими костями!» Они говорят: «Если так, то это будет проигрышное возвращение». Но лишь только раздастся один звук, как все они окажутся на поверхности земли. Дошел ли до тебя рассказ о Мусе? И воззвал его Господь к нему в священной долине Тува: «Иди к Фараону, он преступил все границы. И скажи (ему): «Нет ли у тебя желания (покаяться и) очиститься? Я укажу тебе путь к твоему Господу, и ты станешь благочестивым»». Он показал ему великое знамение. Но (Фараон) не поверил (ему) и проявил непокорность. Затем он отвернулся и устремился (прочь). Он собрал толпу и воззвал. И он сказал: «Я — ваш всевышний господь!» Тогда Аллах подверг его примерному наказанию как в следующей жизни, так и в земной. Поистине, в этом — назидание для богобоязненных. (Кого) труднее создать: вас или небо, которое (Аллах) воздвиг? Он поднял его своды и сделал совершенным. Он затемнил его ночью и вывел день (осветив небо). Землю Он после этого сделал ровной. (Аллах) вывел из нее воду и пастбища. И горы Он укрепил. (Все это Он передал) в пользование вам и вашему скоту. Когда нагрянет Величайшая беда, день, когда человек вспомнит все, ради чего он усердствовал. Ад предстанет перед теми, кто будет видеть. Для того, кто перешел все границы и предпочитал земную жизнь, пристанищем станет Ад. А для того, кто боялся предстать перед своим Господом и удерживал себя от (запретных) желаний, пристанищем станет Рай. У тебя (Мухаммад) спрашивают о Часе: когда он наступит? Откуда ты можешь знать об этом? Знание о Часе — только у твоего Господа. Поистине, ты лишь предупреждаешь тех, кто боится его. И в тот день, когда они увидят его, покажется им, что они провели (в этом мире) лишь вечер или утро.',
	'78':'<b>Сура «Ан-Наба»</b> | <i>Источник: <a href = "https://azan.ru/tafsir">Azan.ru</a></i>\n\nО чем они спрашивают друг друга? О великой вести, относительно которой они расходятся во мнениях. Но нет же, они узнают! Еще раз нет, они узнают! Разве Мы не сделали землю ложем? А горы — кольями? Мы сотворили вас парами. А ваш сон Мы сделали покоем. И сделали ночь одеянием. И Мы сделали день жизнью. И Мы построили над вами семь твердынь. И Мы сотворили пылающий светильник. И Мы низвели из туч обильно льющуюся воду, (низвели) чтобы вывести (из земли) зерна, и растения, и густые сады. Поистине, День разделения уже имеет (назначенный) срок. В этот день затрубят в Рог, и вы придете группами. И небо будет раскрыто и окажется вратами. И горы будут приведены в движение и станут миражом. Поистине, Ад в ожидании. (И это) прибежище для грешников. Они останутся там на века. Они не вкусят там ни прохлады, ни питья, а только кипяток и гной. Это будет (для них) подобающим воздаянием. Поистине, они (при жизни) не готовились к отчету. И они настойчиво отрицали Наши знамения. Мы же все (все действия творений) полностью записали (в Ляух аль-Махфуз). А теперь вкушайте! Мы не прибавим вам ничего, кроме наказания. Поистине, богобоязненным — спасение. Cады и виноградники, и молодые девушки-сверстницы, и полные кубки. Они не услышат там ни пустословия, ни лжи. (Все это) — воздаяние от твоего Господа и достаточный дар (воздаяние и дар от) Господа небес и земли и всего, что между ними, Милостивого, с Которым они не посмеют даже заговорить. В тот день Дух и ангелы встанут рядами. Никто не промолвит ни слова, кроме тех, кому разрешит Милостивый. И говорить они будут правду. Этот день — истина. И всякий, кто пожелает, может вернуться к своему Господу. Поистине, Мы предупредили вас о близком наказании. В тот день человек посмотрит на то, что сделал руками, и неверующий скажет: «О, если бы я стал землей!»'
}

surah_caption = {
	'114':'<b>Сура «Ан-Нас» | 114 | 6 аятов</b>',
	'113':'<b>Сура «Аль-Фаляк» | 113 | 5 аятов</b>',
	'112':'<b>Сура «Аль-Ихлас» | 112 | 4 аятов</b>',
	'111':'<b>Сура «Аль-Масад» | 111 | 5 аятов</b>',
	'110':'<b>Сура «Ан-Наср» | 110 | 3 аятов</b>',
	'109':'<b>Сура «Аль-Кафирун» | 109 | 6 аятов</b>',
	'108':'<b>Сура «Аль-Каусар» | 108 | 3 аятов</b>',
	'107':'<b>Сура «Аль-Ма’ун» | 107 | 7 аятов</b>',
	'106':'<b>Сура «Аль-Куpaйш» | 106 | 4 аятов</b>',
	'105':'<b>Сура «Аль-Филь» | 105 | 5 аятов</b>',
	'104':'<b>Сура «Аль-Хумаза» | 104 | 9 аятов</b>',
	'103':'<b>Сура «Аль-ʼАср» | 103 | 3 аятов</b>',
	'102':'<b>Сура «Ат-Такасур» | 102 | 8 аятов</b>',
	'101':'<b>Сура «Аль-Кариʼа» | 101 | 11 аятов</b>',
	'100':'<b>Сура «Аль-ʼадият» | 100 | 11 аятов</b>',
	'99':'<b>Сура «Аль-Зальзаля» | 99 | 8 аятов</b>',
	'98':'<b>Сура «Аль-Байина» | 98 | 8 аятов</b>',
	'97':'<b>Сура «Аль-Кадр» | 97 | 5 аятов</b>',
	'96':'<b>Сура «Аль-ʼаляк» | 96 | 19 аятов</b>',
	'95':'<b>Сура «Ат-Тин» | 95 | 8 аятов</b>',
	'94':'<b>Сура «Аш-Шарх» | 94 | 8 аятов</b>',
	'93':'<b>Сура «Ад-Духа» | 93 | 11 аятов</b>',
	'92':'<b>Сура «Аль-Лейль» | 92 | 21 аятов</b>',
	'91':'<b>Сура «Аш-Шамс» | 91 | 15 аятов</b>',
	'90':'<b>Сура «Аль-Баляд» | 90 | 20 аятов</b>',
	'89':'<b>Сура «Аль-Фаджр» | 89 | 30 аятов</b>',
	'88':'<b>Сура «Аль-Гашия» | 88 | 26 аятов</b>',
	'87':'<b>Сура «Аль-Аʼля» | 87 | 19 аятов</b>',
	'86':'<b>Сура «Ат-Торик» | 86 | 17 аятов</b>',
	'85':'<b>Сура «Аль-Бурудж» | 85 | 22 аятов</b>',
	'84':'<b>Сура «Аль-Иншикак» | 84 | 25 аятов</b>',
	'83':'<b>Сура «Аль-Мутаффифун» | 83 | 36 аятов</b>',
	'82':'<b>Сура «Аль-Инфитар» | 82 | 19 аятов</b>',
	'81':'<b>Сура «Ат-Таквир» | 81 | 29 аятов</b>',
	'80':'<b>Сура «’Абаса» | 80 | 42 аятов</b>',
	'79':'<b>Сура «Назиʼат» | 79 | 46 аятов</b>',
	'78':'<b>Сура «Ан-Наба» | 78 | 40 аятов</b>'
}

surah_audio = {
	'114':'CQACAgIAAxkBAANyYxT9rW12XinEWF_vpL8xDxNh1WsAAlkiAAJuNqhI23mq9U154BgpBA',
	'113':'CQACAgIAAxkBAAN0YxT9tHq88VglbUy_cUuIM9cCNhQAAloiAAJuNqhIHkt1hyso8WspBA',
	'112':'CQACAgIAAxkBAAN2YxT9vW8cm7c8xaOZceQ0h38dYLoAAlsiAAJuNqhIxenECtgZZ7kpBA',
	'111':'CQACAgIAAxkBAAN4YxT9wufqDLsCn16Xom63zidijqIAAlwiAAJuNqhIglRLAlx39GgpBA',
	'110':'CQACAgIAAxkBAAN6YxT9xoeap7dEdz-URYgSTgmiVGIAAl0iAAJuNqhIfE_GObVMrCEpBA',
	'109':'CQACAgIAAxkBAAN8YxT9zYG_UhUDsyvp4alnRcemEgADXiIAAm42qEgKNdoY4qMVGSkE',
	'108':'CQACAgIAAxkBAAN-YxT90pDCsoZdD1mO3fZ00yQryQIAAmAiAAJuNqhIEwJaikjVlf8pBA',
	'107':'CQACAgIAAxkBAAOAYxT92BxoQWZLMhJ7nVj7d_gwEaQAAmIiAAJuNqhIFmfNhm33JZkpBA',
	'106':'CQACAgIAAxkBAAOCYxT93SCHltcUITz6BrqRwfZP52QAAmMiAAJuNqhIMJB7aDvKVJ4pBA',
	'105':'CQACAgIAAxkBAAOEYxT94kDlGoik9ek2sX1NKwABLkXAAAJkIgACbjaoSMMXY7ywwGfDKQQ',
	'104':'CQACAgIAAxkBAAIMvmMkx0vK4JqgJUuy7tUeLl1bAeNEAAJbIgACOk8pSaTIlYCZPuGhKQQ',
	'103':'CQACAgIAAxkBAAIMvGMkx0MPSZdBoD9SRVkaZn75V6LJAAJaIgACOk8pScLvgUoZFm82KQQ',
	'102':'CQACAgIAAxkBAAIMumMkxz-5xPv6G2XO7_oSV0E9dV8BAAJZIgACOk8pSeb40LAOGJJmKQQ',
	'101':'CQACAgIAAxkBAAIMuGMkxzbY_MKXKCibD44EEnP_OkPPAAJYIgACOk8pSXL-92EdwcwMKQQ',
	'100':'CQACAgIAAxkBAAIMtmMkxy1kiZqp-lasY-U8us76xV6rAAJXIgACOk8pSdbW862k2ojyKQQ',
	'99':'CQACAgIAAxkBAAIMtGMkxyQyfObEuDucK6Vh5-TePyOJAAJWIgACOk8pSe89NUX68rX4KQQ',
	'98':'CQACAgIAAxkBAAIMsmMkxxuSXKX4-IWOlkC_9aWiDJTAAAJUIgACOk8pSXO3kQABArTPIikE',
	'97':'CQACAgIAAxkBAAIMsGMkxwnhyV9wnv80ikO68EiiY4FrAAJRIgACOk8pSRrF7448NcuGKQQ',
	'96':'CQACAgIAAxkBAAIMrmMkxwJIXkPFzVdp_iYCIVcOUJSnAAJQIgACOk8pSYhI-KEYPs8nKQQ',
	'95':'CQACAgIAAxkBAAIMrGMkxvQt6EMCvWSSpnax55HcUe1hAAJOIgACOk8pSRW51XiKWkdSKQQ',
	'94':'CQACAgIAAxkBAAIMqmMkxut1CauTwticBLogcBWkoxbgAAJNIgACOk8pSYsJkoiVLmbuKQQ',
	'93':'CQACAgIAAxkBAAIMqGMkxuSCSLQdvlrXYO9pTOjVJpqEAAJMIgACOk8pSXoIOvNUh2rhKQQ',
	'92':'CQACAgIAAxkBAAIMpmMkxtqqnKGa7lM_7rBXp-wPHq1VAAJLIgACOk8pSZ0ssxKq61jsKQQ',
	'91':'CQACAgIAAxkBAAIMpGMkxsogbUBHF4aFlBAdnBPPvzgVAAJJIgACOk8pSafOT4tnF4L-KQQ',
	'90':'CQACAgIAAxkBAAIMomMkxr13z36p3gI8XLcpQoax0BoMAAJIIgACOk8pSRQGLpFWqstqKQQ',
	'89':'CQACAgIAAxkBAAIMoGMkxqyq4NJ1YceFJrMko1_COVuJAAJHIgACOk8pSasTKQU_hUVeKQQ',
	'88':'CQACAgIAAxkBAAIMnmMkxo6rwcoOlRbdqY2Skbw25KsQAAJFIgACOk8pSYVJYxer0S-4KQQ',
	'87':'CQACAgIAAxkBAAIMnGMkxntNDZqvi5m2gqSujXK7U3e8AAJEIgACOk8pSX0izu0lGqJgKQQ',
	'86':'CQACAgIAAxkBAAIMmmMkxmpi7NLLP9Ip8Oe7DgUmmNTcAAJDIgACOk8pSU5K7C1SWOuBKQQ',
	'85':'CQACAgIAAxkBAAIMlmMkxlx1rUGMeWkWgOYUtH69mF-OAAJBIgACOk8pSQstKvCZ8SAoKQQ',
	'84':'CQACAgIAAxkBAAIMkmMkxkJVd5pv2bgz4WIhc-1Kf9RTAAJAIgACOk8pScztxoakez3jKQQ',
	'83':'CQACAgIAAxkBAAIMkGMkxiwrgA9KIULkCm21VqW5nOdqAAI9IgACOk8pSa0WV3CWLvmLKQQ',
	'82':'CQACAgIAAxkBAAIMjmMkxgIgaun6OktW5o0BX4UMaGJfAAI6IgACOk8pSSzz4tEdVbPdKQQ',
	'81':'CQACAgIAAxkBAAIMimMkxe8DbbDWK8EHq_XpIx046g5kAAI4IgACOk8pSY6TY4TaDBfJKQQ',
	'80':'CQACAgIAAxkBAAIMhGMkxdkbofOwKjPjsKXlnRYd6UfNAAI2IgACOk8pSU6Qc4V3_jHoKQQ',
	'79':'CQACAgIAAxkBAAIMgmMkxbv9zrg5NMY-I4fC9et_DPEgAAIxIgACOk8pSc6LcMNP-vONKQQ',
	'78':'CQACAgIAAxkBAAIMgGMkxY2bc0sNHxLdEuSbufO3zT7lAAItIgACOk8pScYlNw67ukcpKQQ'
}



#--------------------Functions--------------------#

# Main keyboard | /start
async def start_command(message: types.Message):
	user_id = message.from_user.id
	try: 
		sqlite_bd.cur.execute('SELECT user_id FROM users WHERE user_id == ?', (user_id, )).fetchone()[0]
		await message.answer('السلام عليكم ورحمة الله وبركاته', reply_markup=client_kb.markup_main)
	except:
		await message.answer('<b>السلام عليكم ورحمة الله وبركاته</b>\n<b>• Время намаза</b> - время намаза для всех городов мира! Для Татарстана, Дагестана и Казахстана с методом расчета от ДУМ этих регионов.\n<b>• Трекер</b> - восстановление пропущенных намазов!\n<b>• E-добавки</b> - проверка E-добавок на дозволенность!\n<b>• 30-й джуз</b> - все суры 30-го джуза Корана с переводом, тафсиром и аудио!\n<b>• 99 имён</b> - список имён Всевышнего со смысловым переводом!\n<b>• Хадисы</b> - достоверные хадисы из сборников Муслима, Бухари и Тирмизи!\n<b>• Зикр</b> - дуа пророков и 14 важных зикров на каждый день!\n<b>• Обучение</b> - обучение намазу для начинающих на основе ханафитского мазхаба!\n<b>• Календарь</b> - все знаменательные даты по хиджре!\nКоманды:\n/start - Начать\n/cancel - Отменить действие\n/reset - Сбросить трекер\n/help - Весь функционал бота\n\n<b>Выберите раздел:</b>', reply_markup=client_kb.markup_main)
		sqlite_bd.cur.execute('INSERT INTO users VALUES (?, ?, ?)', (user_id, message.from_user.first_name, datetime.today()))
		sqlite_bd.base.commit()

# Favorite cities | 'Время намаза' (reply)
async def favorite_command(message: types.Message):
	global user_id
	user_id = message.from_user.id
	await message.answer('<b>Избранные города:</b>ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ', reply_markup=await client_kb.favorite_cities(user_id))

# Add new city | 'Добавить город' (inline)
async def time_command(callback : types.CallbackQuery):
	await callback.message.edit_text('Метод расчета для Татарстана, Дагестана и Казахстана - ДУМ\'ы этих регионов.\nМетод расчета для "Других регионов" - WML Всемирная Лига мусульман.\n\n<b>Выберите регион:</b> ', reply_markup=client_kb.inline_namaz_time)
	await callback.answer()

# Tatarstan cities | 'Татарстан' (inline)
async def tatarstan_command(callback : types.CallbackQuery):
	tat_page = 1
	await callback.message.edit_text('Выберите Ваш <b>населенный пункт:</b> ', reply_markup=await client_kb.inline_namaz_time_tat(tat_page))
	await callback.answer()

async def tatarstan_next(callback : types.CallbackQuery):
	data = callback.data[9:]
	tat_page = int(data) + 1
	await callback.message.edit_text('Выберите Ваш <b>населенный пункт:</b> ', reply_markup=await client_kb.inline_namaz_time_tat(tat_page))
	await callback.answer()

async def tatarstan_back(callback : types.CallbackQuery):
	data = callback.data[9:]
	tat_page = int(data) - 1
	await callback.message.edit_text('Выберите Ваш <b>населенный пункт:</b> ', reply_markup=await client_kb.inline_namaz_time_tat(tat_page))
	await callback.answer()

# Tracker | 'Трекер'  (Reply)
async def tracker_command(message: types.Message):
	user_id = message.from_user.id
	info = sqlite_bd.cur.execute(f'SELECT EXISTS(SELECT * FROM tracker WHERE user_id == ?)', (user_id, ))
	if info.fetchone()[0] == 0:
		await message.answer('<b>Эта функция предназначена для восстановления пропущенных намазов! Выберите способ расчета:</b>', reply_markup=client_kb.markup_tracker_menu)
	else:
		await message.answer('<b>Восстановление намазов:</b>', reply_markup = await client_kb.markup_tracker(user_id))

async def tracker_myself(callback: types.CallbackQuery):
	await FSMtracker.fajr.set()
	await callback.message.delete()
	await callback.message.answer('Напишите количество <b>фаджр</b> намазов, которые необходимо восстановить:', reply_markup = types.ReplyKeyboardRemove())
	await callback.answer()

async def tracker_fajr_get(message: types.Message, state = FSMContext):
	async with state.proxy() as data:
		try:
			num = int(message.text)
			if num < 1:
				await state.finish()
				return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
			else:
				pass
			data['fajr_need'] = message.text
		except:
			await state.finish()
			return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
	await FSMtracker.zuhr.set()
	await message.answer('Напишите количество <b>зухр</b> намазов, которые необходимо восстановить:')

async def tracker_zuhr_get(message: types.Message, state = FSMContext):
	async with state.proxy() as data:
		try:
			num = int(message.text)
			if num < 1:
				await state.finish()
				return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
			else:
				pass
			data['zuhr_need'] = message.text
		except:
			await state.finish()
			return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
	await FSMtracker.asr.set()
	await message.answer('Напишите количество <b>аср</b> намазов, которые необходимо восстановить:')

async def tracker_asr_get(message: types.Message, state = FSMContext):
	async with state.proxy() as data:
		try:
			num = int(message.text)
			if num < 1:
				await state.finish()
				return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
			else:
				pass
			data['asr_need'] = message.text
		except:
			await state.finish()
			return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
	await FSMtracker.magrib.set()
	await message.answer('Напишите количество <b>магриб</b> намазов, которые необходимо восстановить:')

async def tracker_magrib_get(message: types.Message, state = FSMContext):
	async with state.proxy() as data:
		try:
			num = int(message.text)
			if num < 1:
				await state.finish()
				return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
			else:
				pass
			data['magrib_need'] = message.text
		except:
			await state.finish()
			return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
	await FSMtracker.isha.set()
	await message.answer('Напишите количество <b>иша</b> намазов, которые необходимо восстановить:')

async def tracker_isha_get(message: types.Message, state = FSMContext):
	async with state.proxy() as data:
		try:
			num = int(message.text)
			if num < 1:
				await state.finish()
				return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
			else:
				pass
			data['isha_need'] = message.text
		except:
			await state.finish()
			return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
	await FSMtracker.vitr.set()
	await message.answer('Напишите количество <b>витр</b> намазов, которые необходимо восстановить (можно написать 0): ')

async def tracker_vitr_get_yourself(message: types.Message, state = FSMContext):
	user_id = message.from_user.id
	async with state.proxy() as data:
		try:
			num = int(message.text)
			if num < 0:
				await state.finish()
				return await message.answer('Некорректный формат. Напишите положительное число', reply_markup = client_kb.markup_tracker_menu)
			else:
				pass
			data['vitr_need'] = message.text
		except:
			await state.finish()
			return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
	async with state.proxy() as data:
		sqlite_bd.cur.execute('INSERT INTO tracker VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, 0, data['fajr_need'], 0, data['zuhr_need'], 0, data['asr_need'], 0, data['magrib_need'], 0, data['isha_need'], 0, data['vitr_need'], 0, 0))
		sqlite_bd.base.commit()
	await state.finish()
	await message.answer('Секундочку...', reply_markup = client_kb.markup_main)
	reply = await client_kb.markup_tracker(user_id)
	await asyncio.sleep(1)
	await message.answer('Восстановление намазов:', reply_markup = reply)

async def tracker_calculate(callback: types.CallbackQuery):
	await FSMtracker.first_date.set()
	await callback.message.delete()
	await callback.message.answer('Введите период, в течении которого нужно восстановить намазы.\nПервая дата: (формат: день.месяц.год)', reply_markup=types.ReplyKeyboardRemove())
	await callback.answer()

async def tracker_get_first(message: types.Message, state = FSMContext):
	try:
		async with state.proxy() as data:
			data['first_date'] = datetime.strptime(message.text, "%d.%m.%Y")
	except:
		await state.finish()
		return await message.answer('Неправильный формат!', reply_markup=client_kb.markup_main)
	await FSMtracker.second_date.set()
	await message.answer('Введите вторую дату:') 

async def tracker_get_second(message: types.Message, state = FSMContext):
	user_id = message.from_user.id
	try:
		async with state.proxy() as data:
			data['second_date'] = datetime.strptime(message.text, "%d.%m.%Y")
			first_date = data['first_date']
			second_date = data['second_date']
			result = (first_date - second_date).days
			if result < 0:
				result = result * -1 
			if first_date == second_date:
				await state.finish()
				return await message.answer('Даты не должны совпадать!', reply_markup=client_kb.markup_main)
			sqlite_bd.cur.execute('INSERT INTO tracker VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, 0, result, 0, result, 0, result, 0, result, 0, result, 0, result, second_date, first_date))
			sqlite_bd.base.commit()
	except:
		await state.finish()
		return await message.answer('Неправильный формат!', reply_markup=client_kb.markup_main)
	await state.finish()
	await message.answer('Добавить витр-намаз?', reply_markup=client_kb.markup_tracker_vitr)

async def tracker_vitr_get(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	if callback.data[5:] == 'no':
		sqlite_bd.cur.execute('UPDATE tracker SET vitr_need == ? WHERE user_id == ?', (0, user_id))
		sqlite_bd.base.commit()
	else:
		pass
	await callback.answer()
	await callback.message.delete()
	await callback.message.answer('Рассчитываю...', reply_markup = client_kb.markup_main)
	reply = await client_kb.markup_tracker(user_id)
	await asyncio.sleep(1)
	await callback.message.answer('<b>Восстановление намазов:</b>', reply_markup = reply)
	

async def tracker_reset(message: types.Message):
	await message.answer('Вы уверены, что хотите сбросить значения трекера?', reply_markup=client_kb.markup_tracker_reset)

async def tracker_reset_cancel(callback: types.CallbackQuery):
	await callback.message.edit_text('Операция отменена!')
	await callback.answer()

async def tracker_reset_yes(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	try:
		sqlite_bd.cur.execute(f'DELETE FROM tracker WHERE user_id == {user_id}')
		sqlite_bd.base.commit()
		await callback.message.delete()
		await callback.message.answer('Трекер сброшен успешно!', reply_markup=client_kb.markup_main)
	except:
		await callback.message.delete()
		await callback.message.answer('Трекер уже сброшен!', reply_markup=client_kb.markup_main)
	await callback.answer()

async def tracker_plus(callback: types.CallbackQuery):
	salat = callback.data[5:]
	user_id = callback.from_user.id
	try:
		if salat == 'fajr':
			sqlite_bd.cur.execute('UPDATE tracker SET fajr == (fajr + ?) WHERE user_id == ?', (1, user_id))
			sqlite_bd.base.commit()
		elif salat == 'zuhr':
			sqlite_bd.cur.execute('UPDATE tracker SET zuhr == (zuhr + ?) WHERE user_id == ?', (1, user_id))
			sqlite_bd.base.commit()
		elif salat == 'asr':
			sqlite_bd.cur.execute('UPDATE tracker SET asr == (asr + ?) WHERE user_id == ?', (1, user_id))
			sqlite_bd.base.commit()
		elif salat == 'magrib':
			sqlite_bd.cur.execute('UPDATE tracker SET magrib == (magrib + ?) WHERE user_id == ?', (1, user_id))
			sqlite_bd.base.commit()
		elif salat == 'isha':
			sqlite_bd.cur.execute('UPDATE tracker SET isha == (isha + ?) WHERE user_id == ?', (1, user_id))
			sqlite_bd.base.commit()
		else: 
			sqlite_bd.cur.execute('UPDATE tracker SET vitr == (vitr + ?) WHERE user_id == ?', (1, user_id))
			sqlite_bd.base.commit()
		await callback.message.edit_text('<b>Восстановление намазов:</b>', reply_markup = await client_kb.markup_tracker(user_id))
	except:
		await callback.message.answer('Ой, что-то пошло не так!', reply_markup = client_kb.markup_main)
	await callback.answer()
	
async def tracker_minus(callback: types.CallbackQuery):
	salat = callback.data[6:]
	user_id = callback.from_user.id
	if salat == 'fajr':
		if sqlite_bd.cur.execute('SELECT fajr FROM tracker WHERE user_id == ?', (user_id, )).fetchone()[0] == '0':
			await callback.answer()
			return await callback.message.answer('Значение не может быть ниже 0!')
		sqlite_bd.cur.execute('UPDATE tracker SET fajr == (fajr - ?) WHERE user_id == ?', (1, user_id))
		sqlite_bd.base.commit()
	elif salat == 'zuhr':
		if sqlite_bd.cur.execute('SELECT zuhr FROM tracker WHERE user_id == ?', (user_id, )).fetchone()[0] == '0':
			await callback.answer()
			return await callback.message.answer('Значение не может быть ниже 0!')
		sqlite_bd.cur.execute('UPDATE tracker SET zuhr == (zuhr - ?) WHERE user_id == ?', (1, user_id))
		sqlite_bd.base.commit()
	elif salat == 'asr':
		if sqlite_bd.cur.execute('SELECT asr FROM tracker WHERE user_id == ?', (user_id, )).fetchone()[0] == '0':
			await callback.answer()
			return await callback.message.answer('Значение не может быть ниже 0!')
		sqlite_bd.cur.execute('UPDATE tracker SET asr == (asr - ?) WHERE user_id == ?', (1, user_id))
		sqlite_bd.base.commit()
	elif salat == 'magrib':
		if sqlite_bd.cur.execute('SELECT magrib FROM tracker WHERE user_id == ?', (user_id, )).fetchone()[0] == '0':
			await callback.answer()
			return await callback.message.answer('Значение не может быть ниже 0!')
		sqlite_bd.cur.execute('UPDATE tracker SET magrib == (magrib - ?) WHERE user_id == ?', (1, user_id))
		sqlite_bd.base.commit()
	elif salat == 'isha':
		if sqlite_bd.cur.execute('SELECT isha FROM tracker WHERE user_id == ?', (user_id, )).fetchone()[0] == '0':
			await callback.answer()
			return await callback.message.answer('Значение не может быть ниже 0!')
		sqlite_bd.cur.execute('UPDATE tracker SET isha == (isha - ?) WHERE user_id == ?', (1, user_id))
		sqlite_bd.base.commit()
	else:
		if sqlite_bd.cur.execute('SELECT vitr FROM tracker WHERE user_id == ?', (user_id, )).fetchone()[0] == '0':
			await callback.answer()
			return await callback.message.answer('Значение не может быть ниже 0!')
		sqlite_bd.cur.execute('UPDATE tracker SET vitr == (vitr - ?) WHERE user_id == ?', (1, user_id))
		sqlite_bd.base.commit()
	await callback.message.edit_text('<b>Восстановление намазов:</b>', reply_markup = await client_kb.markup_tracker(user_id))
	await callback.answer()

async def other_btn_tracker(callback: types.CallbackQuery):
	data = callback.data[6:]
	await callback.answer()
	if data == 'salat':
		return await callback.message.answer('Название намаза')
	elif data == 'current':
		return await callback.message.answer('Число восстановленных намазов')
	else:
		return await callback.message.answer('Число необходимых намазов')

# learn | 'Обучение намазу' (Reply)
async def tutor_command(message: types.Message):
  await message.answer('Обучение на основе Ханафитского мазхаба | <i>Источник: <a href = "https://dumrt.ru/ru/help-info/training-prayer/">ДУМ РТ</a></i>\nВыберите раздел: ', reply_markup=client_kb.markup_namaz_tutor)
# buttons in learn | (inline)
async def tutor_namaz_command(message: types.Message):
    await message.answer(other.tut_namaz_message, reply_markup=client_kb.markup_tutor_back)
async def tutor_time_command(message: types.Message):
    await message.answer(other.tut_time_message, reply_markup=client_kb.markup_tutor_back)
async def tutor_cond_command(message: types.Message):
	for x in range(0, len(other.tut_cond_message), MESS_MAX_LENGTH - 1400):
		mess_tut = other.tut_cond_message[x: x + MESS_MAX_LENGTH - 1400] 
		await message.answer(mess_tut, reply_markup=client_kb.markup_tutor_back)
async def tutor_gusl_command(message: types.Message):
    await message.answer(other.tut_gusl_message, reply_markup=client_kb.markup_tutor_back)
async def tutor_taharat_command(message: types.Message):
    await message.answer(other.tut_taharat_message, reply_markup=client_kb.markup_tutor_back)
async def tutor_forma_command(message: types.Message):
	for x in range(0, len(other.tut_forma_message), MESS_MAX_LENGTH - 57):
		mess_form = other.tut_forma_message[x: x + MESS_MAX_LENGTH - 57] 
		await message.answer(mess_form, reply_markup=client_kb.markup_tutor_back)
async def tutor_sura_command(message: types.Message):
    await message.answer(other.tut_sura_message, reply_markup=client_kb.markup_tutor_back)
async def tutor_women_command(message: types.Message):
    await message.answer(other.tut_women_message, reply_markup=client_kb.markup_tutor_back)


# Qoran | 'Коран' (Reply)
async def qoran_command(message: types.Message):
	page = 1
	await message.answer('Выберите суру: ', reply_markup=await client_kb.markup_qoran(page))

async def qoran_next(callback: types.CallbackQuery):
	page = callback.data[11:]
	await callback.message.edit_text('Выберите суру: ', reply_markup=await client_kb.markup_qoran(int(page)+1))
	await callback.answer()

async def qoran_back(callback: types.CallbackQuery):
	page = callback.data[11:]
	await callback.message.edit_text('Выберите суру: ', reply_markup=await client_kb.markup_qoran(int(page)-1))
	await callback.answer()

async def qoran_surah_get(callback: types.CallbackQuery):
	data = callback.data[6:]
	await callback.answer()	
	await callback.message.delete()
	await bot.send_photo(callback.from_user.id, surah_photo[data], caption = surah_caption[data], reply_markup= await client_kb.markup_surah(data))

async def qoran_audio(callback: types.CallbackQuery):
	data = callback.data[12:]
	await bot.send_audio(callback.from_user.id, surah_audio[data])
	await callback.answer()

async def qoran_translate(callback: types.CallbackQuery):
	data = callback.data[16:]
	await callback.message.answer(surah_translate[data], disable_web_page_preview=True)
	await callback.answer()

# Books | 'Книги' (Reply)
async def names_command(message: types.Message):
	page = 1
	await message.answer('Выберите нужное имя:ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ', reply_markup= await client_kb.names_inline(page))

async def names_command_back(callback: types.CallbackQuery):
	data = callback.data[11:]
	page = int(data) - 1
	await callback.message.edit_text('Выберите нужное имя:ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ', reply_markup= await client_kb.names_inline(page))
	await callback.answer()

async def names_command_next(callback: types.CallbackQuery):
	data = callback.data[11:]
	page = int(data) + 1
	await callback.message.edit_text('Выберите нужное имя:ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ', reply_markup= await client_kb.names_inline(page))
	await callback.answer()

async def names_get_photo(callback: types.CallbackQuery):
	data = callback.data[6:]
	await callback.answer()
	await callback.message.delete()
	await bot.send_photo(callback.from_user.id, names_id[data], reply_markup=await client_kb.names_photo_inline(int(data)))

async def names_all(callback: types.CallbackQuery):
	page = 1
	await callback.answer()
	await callback.message.delete()
	await callback.message.answer('Выберите нужное имя:ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ', reply_markup= await client_kb.names_inline(page))

async def names_next(callback: types.CallbackQuery):
	data = callback.data[11:]
	await callback.answer()
	await callback.message.delete()
	await bot.send_photo(callback.from_user.id, names_id[str(int(data) + 1)], reply_markup=await client_kb.names_photo_inline(int(data) + 1))

async def names_back(callback: types.CallbackQuery):
	data = callback.data[11:]
	await callback.answer()
	await callback.message.delete()
	await bot.send_photo(callback.from_user.id, names_id[str(int(data) - 1)], reply_markup=await client_kb.names_photo_inline(int(data) - 1))

# Calendar | 'Календарь' (Reply)
async def calendar_command(message: types.Message):
	await bot.send_photo(message.from_user.id, 'AgACAgIAAxkBAAIeOGPITPVNY_stxlNXL0Ru_klhxh5bAAIixjEbkUBASp21PSjyJuMaAQADAgADeAADLQQ', caption= await other.calendar_message())


# Info | 'Помощь' (Reply)
async def info_command(message: types.Message):
    await message.answer(other.info_message, disable_web_page_preview=True)


# Zikr | 'Зикр' (Reply)
async def zikr_command(message: types.Message):
	await message.answer('Выберите раздел: ', reply_markup = client_kb.inline_zikr)

async def zikr_all_get(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	try: 
		sqlite_bd.cur.execute('SELECT user_id FROM zikr WHERE user_id == ?', (user_id, )).fetchone()[0] == user_id
	except:
		sqlite_bd.cur.execute('INSERT INTO zikr VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
		sqlite_bd.base.commit()
	await callback.message.edit_text('Выберите зикр: ', reply_markup=client_kb.inline_zikr_all)
	await callback.answer()

async def dua_get_all(callback: types.CallbackQuery):
	await callback.message.edit_text('<b>Дуа какого пророка (мир Им) прислать?</b>', reply_markup=client_kb.markup_dua)
	await callback.answer()

async def send_message(dp: Dispatcher):
	sqlite_bd.cur.execute('UPDATE zikr SET zikr_1_today == "0", zikr_2_today == "0", zikr_3_today == "0", zikr_4_today == "0", zikr_5_today == "0", zikr_6_today == "0", zikr_7_today == "0", zikr_8_today == "0", zikr_9_today == "0", zikr_10_today == "0", zikr_11_today == "0", zikr_12_today == "0", zikr_13_today == "0", zikr_14_today == "0", zikr_15_today == "0", zikr_16_today == "0"')
	sqlite_bd.base.commit()

def schedule_jobs():
	scheduler.add_job(send_message, "interval", days=1, args=(dp, ))

async def zikr_get(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	text = callback.data[5:]
	await callback.answer()
	await callback.message.delete()
	if text == '16':
		await callback.message.answer(f'Сегодня: {sqlite_bd.cur.execute("SELECT zikr_16_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute("SELECT zikr_16_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup=await client_kb.markup_zikr_lower(16))
	else:
		await bot.send_photo(callback.from_user.id, zikr_id[text], caption=f'Сегодня: {sqlite_bd.cur.execute(f"SELECT zikr_{text}_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute(f"SELECT zikr_{text}_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup=await client_kb.markup_zikr_lower(text))

async def zikr_plus(callback: types.CallbackQuery):
	data = callback.data[10:]
	user_id = callback.from_user.id
	sqlite_bd.cur.execute(f'UPDATE zikr SET zikr_{data}_today == zikr_{data}_today + 1, zikr_{data}_all == zikr_{data}_all + 1 WHERE user_id == ?', (user_id, ))
	sqlite_bd.base.commit()
	await callback.answer()
	if data == '16':
		await callback.message.edit_text(f'Сегодня: {sqlite_bd.cur.execute(f"SELECT zikr_{data}_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute(f"SELECT zikr_{data}_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup= await client_kb.markup_zikr_lower(16))
	else:
		await callback.message.edit_caption(f'Сегодня: {sqlite_bd.cur.execute(f"SELECT zikr_{data}_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute(f"SELECT zikr_{data}_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup= await client_kb.markup_zikr_lower(data))

async def zikr_reset(callback: types.CallbackQuery):
	data = callback.data[11:]
	await callback.message.answer(f'Вы уверены, что хотите сбросить зикр "{zikrs[data]}"?', reply_markup=await client_kb.markup_zikr_reset(data))
	await callback.answer()

async def zikr_reset_cancel(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	data = callback.data[18:]
	if data == '16':
		await callback.message.answer(f'Сегодня: {sqlite_bd.cur.execute("SELECT zikr_16_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute("SELECT zikr_16_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup= client_kb.markup_zikr_lower(16))
	else:
		await bot.send_photo(callback.from_user.id, zikr_id[data], caption=f'Сегодня: {sqlite_bd.cur.execute(f"SELECT zikr_{data}_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute(f"SELECT zikr_{data}_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup=await client_kb.markup_zikr_lower(data))
	await callback.answer()

async def zikr_reset_yes(callback: types.CallbackQuery):
	data = callback.data[15:]
	user_id = callback.from_user.id
	try:
		sqlite_bd.cur.execute(f'UPDATE zikr SET zikr_{data}_all == "0", zikr_{data}_today == "0" WHERE user_id == ?', (user_id, ))
		sqlite_bd.base.commit()
		await callback.answer()
		await callback.message.delete()
		await callback.message.answer('Зикр успешно сброшен!')
	except:
		await callback.answer()
		await callback.message.delete()
		await callback.message.answer('Произошла ошибка!')

async def zikr_all(callback: types.CallbackQuery):
	await callback.answer()
	await callback.message.delete()
	await callback.message.answer('Выберите зикр: ', reply_markup=client_kb.inline_zikr_all)

async def zikr_polza(callback: types.CallbackQuery):
	data = callback.data[11:]
	if data == '16':
		pass
	else:
		await callback.message.answer(zikr_polzi[data])
	await callback.answer()

# Unknown messages
async def help_command(message: types.Message):
	await message.answer('<b>• Время намаза</b> - время намаза для всех городов мира! Для Татарстана, Дагестана и Казахстана с методом расчета от ДУМ этих регионов.\n<b>• Трекер</b> - восстановление пропущенных намазов!\n<b>• E-добавки</b> - проверка E-добавок на дозволенность!\n<b>• 30-й джуз</b> - все суры 30-го джуза Корана с переводом, тафсиром и аудио!\n<b>• 99 имён</b> - список имён Всевышнего со смысловым переводом!\n<b>• Хадисы</b> - достоверные хадисы из сборников Муслима, Бухари и Тирмизи!\n<b>• Зикр</b> - дуа пророков и 14 важных зикров на каждый день!\n<b>• Обучение</b> - обучение намазу для начинающих на основе ханафитского мазхаба!\n<b>• Календарь</b> - все знаменательные даты по хиджре!\nКоманды:\n/start - Начать\n/cancel - Отменить действие\n/reset - Сбросить трекер\n/help - Весь функционал бота\n\n<b>Выберите раздел:</b>', reply_markup=client_kb.markup_main)


# back button
async def back_command(message: types.Message):
    await message.answer('Выберите раздел: ', reply_markup=client_kb.markup_main)


# today time for tatarstan
async def namaz_day_command(callback : types.CallbackQuery):
	user_id = callback.from_user.id
	global current_city
	current_city = callback.data
	try:
		await callback.message.edit_text(await parcer_tatarstan.get_time(current_city, 'today'), reply_markup = await client_kb.inline_city('today', current_city, user_id))
	except:
		await callback.message.answer('Ой, что-то пошло не так...', reply_markup=client_kb.markup_main)
	await callback.answer()


# tomorrow time for tatarstan
async def next_day_time_command(callback : types.CallbackQuery):
	user_id = callback.from_user.id
	global current_city
	try:
		await callback.message.edit_text(await parcer_tatarstan.get_time(current_city, 'tomorrow'), reply_markup = await client_kb.inline_city('tomorrow', current_city, user_id))
	except:
		await callback.message.answer('Ой, что-то пошло не так...', reply_markup=client_kb.markup_main)
	await callback.answer()

# all days in month for tatarstan
async def month_time_command(callback : types.CallbackQuery):
	try:
		await callback.message.edit_text(f'Город: <b>{current_city}</b>\nМесяц: <b>{months[str(datetime.now().month)]}</b>\n<b>Выберите день:</b>ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ', reply_markup=await client_kb.inline_month())
	except:
		await callback.message.answer('Ой, что-то пошло не так...', reply_markup=client_kb.markup_main)
	await callback.answer()
#--------------------Get new other city--------------------#
# first message
async def address_add(callback: types.CallbackQuery):
	global user_id
	user_id = callback.from_user.id
	await FSMaddress.address.set()
	await callback.message.delete()
	await callback.message.answer('<b>ВНИМАНИЕ!</b> Метод расчета для "Других регионов" - WML Всемирная Лига мусульман. Расчеты могут быть <b>неточными</b>! В первую очередь, ориентируйтесь на расчеты ДУМ\'а Вашего города и на собственные наблюдения!\n\n<b>Напишите название города:</b>', reply_markup=types.ReplyKeyboardRemove())
	await callback.answer()

async def cancel_handler(message: types.Message, state: FSMContext):
	current_state = await state.get_state()
	if current_state is None:
		return
	await state.finish()
	await message.answer('Действие отменено ❌', reply_markup=client_kb.markup_main)

# check address
async def address_get(message: types.message, state=FSMContext):
	for item in sqlite_bd.cur.execute(f'SELECT address FROM favorite_other WHERE user_id == {user_id}').fetchall():
		if item[0].lower() == message.text.lower():
			await state.finish()
			return await message.answer('Город с таким названием уже есть в избранных!', reply_markup = client_kb.markup_main)
	try:
		await parcer_other.city_check(message.text)
		await message.answer('Город найден! ✅', reply_markup=client_kb.markup_main)
	except:
		await state.finish()
		return await message.answer('Такого города не нашлось, проверьте название!', reply_markup = client_kb.markup_main)
	async with state.proxy() as data:
		data['address'] = message.text
	await FSMaddress.school.set()
	await message.answer('<b>Выберите мазхаб:</b>', reply_markup=client_kb.markup_school)
# school
async def school_get(callback: types.CallbackQuery, state=FSMContext):
	global address, school
	user_id = callback.from_user.id
	async with state.proxy() as data:
		data['school'] = callback.data[7]
		address = data['address']
		school = data['school']
	time = await parcer_other.get_day_time(state)
	await callback.answer()
	msg = await callback.message.edit_text('Секундочку...')
	await asyncio.sleep(1)
	try:
		await msg.edit_text(time, reply_markup=await client_kb.other_inline(user_id, address, 'today'))
	except:
		await callback.message.answer('Ой, что-то пошло не так...', reply_markup=client_kb.markup_main)
	await state.finish()
# time from menu for other regions

async def time_other(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global address
	address = str(callback.data[11:])
	try:
		await callback.message.edit_text(await parcer_other.get_day_time_from_menu(user_id, str(callback.data[11:])),reply_markup=await client_kb.other_inline(user_id, str(callback.data[11:]), 'today'))
	except:
		await callback.message.edit_text('Что-то пошло не так, повторите попытку!')
	await callback.answer()

async def favorite_add_other(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	sqlite_bd.cur.execute('INSERT INTO favorite_other VALUES (?, ?, ?)', (user_id, address, school))
	sqlite_bd.base.commit()
	await callback.message.edit_text('Добавлено в избранные ✅', reply_markup = client_kb.markup_favorite)
	await callback.answer()

async def favorite_delete_other(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	sqlite_bd.cur.execute('DELETE FROM favorite_other WHERE user_id == ? AND address == ?', (user_id, address))
	sqlite_bd.base.commit()
	await callback.message.edit_text('Удалено из избранных ✅', reply_markup = client_kb.markup_favorite)
	await callback.answer()

async def month_days_other(callback: types.CallbackQuery):
	await callback.message.edit_text(f'Город: <b>{address}</b>\nМесяц: <b>{months[str(datetime.now().month)]}</b>\n<b>Выберите день:</b> ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ',reply_markup=await client_kb.inline_month_other())
	await callback.answer()

async def tomorrow_time_other(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	try:
		school = sqlite_bd.cur.execute('SELECT school FROM favorite_other WHERE user_id == ? AND address = ?', (user_id, address))
	except:
		pass
	try:
		await callback.message.edit_text(await parcer_other.get_calendar_time(address, datetime.now().day + 1, school), reply_markup=await client_kb.other_inline(user_id, address, 'tomorrow'))
	except:
		await callback.message.answer('Ой, что-то пошло не так...', reply_markup=client_kb.markup_main)
	await callback.answer()

async def today_time_other(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	try:
		school = sqlite_bd.cur.execute('SELECT school FROM favorite_other WHERE user_id == ? AND address = ?', (user_id, address))
	except:
		pass
	try:
		await callback.message.edit_text(await parcer_other.get_calendar_time(address, datetime.now().day, school), reply_markup=await client_kb.other_inline(user_id, address, 'today'))
	except:
		await callback.message.answer('Ой, что-то пошло не так...', reply_markup=client_kb.markup_main)
	await callback.answer()

async def month_time_other(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	try:
		school = sqlite_bd.cur.execute('SELECT school FROM favorite_other WHERE user_id == ? AND address = ?', (user_id, address))
	except:
		pass
	day = callback.data[11:]
	try:
		await callback.message.edit_text(await parcer_other.get_calendar_time(address, day, school), reply_markup=await client_kb.other_inline(user_id, address, 'month'))
	except:
		await callback.message.answer('Ой, что-то пошло не так...', reply_markup=client_kb.markup_main)
	await callback.answer()

async def tatarstan_month(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	try:
		await callback.message.edit_text(await parcer_tatarstan.get_time(current_city,callback.data[15:]), reply_markup=await client_kb.inline_city('tomorrow', current_city, user_id))
	except:
		await callback.message.answer('Ой, что-то пошло не так...', reply_markup=client_kb.markup_main)	
	await callback.answer()
	await callback.answer()

async def tatarstan_favorite_add(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	sqlite_bd.cur.execute(f'INSERT INTO favorite_tatarstan VALUES (?, ?)', (user_id, current_city))
	sqlite_bd.base.commit()
	await callback.message.edit_text('Добавлено в избранные ✅', reply_markup = client_kb.markup_favorite)
	await callback.answer()

async def tatarstan_favorite_delete(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	sqlite_bd.cur.execute('DELETE FROM favorite_tatarstan WHERE user_id == ? AND address == ?', (user_id, current_city))
	sqlite_bd.base.commit()
	await callback.message.edit_text('Удалено из избранных ✅', reply_markup = client_kb.markup_favorite)
	await callback.answer()

async def dagestan_menu(callback: types.CallbackQuery):
	dag_page = 1
	await callback.message.edit_text('<b>Выберите населенный пункт:</b>', reply_markup=await client_kb.dagestan_markup(dag_page))
	await callback.answer()
async def dagestan_menu_next(callback: types.CallbackQuery):
	data = callback.data[9:]
	dag_page = int(data) + 1
	await callback.message.edit_text('<b>Выберите населенный пункт:</b>', reply_markup=await client_kb.dagestan_markup(dag_page))
	await callback.answer()
async def dagestan_menu_back(callback: types.CallbackQuery):
	data = callback.data[9:]
	dag_page = int(data) - 1
	await callback.message.edit_text('<b>Выберите населенный пункт:</b>', reply_markup=await client_kb.dagestan_markup(dag_page))
	await callback.answer()

async def dagestan_today_time(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global dag_city
	dag_city = callback.data[9:]
	try:
		await callback.message.edit_text(await parcer_dagestan.get_day_time(dag_city), reply_markup= await client_kb.dag_city(dag_city, 'today',user_id))
	except:
		await callback.message.answer('Ой, что-то пошло не так...', reply_markup=client_kb.markup_main)
	await callback.answer()

async def dagestan_tomorrow_time(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global dag_city
	try:
		await callback.message.edit_text(await parcer_dagestan.get_tomorrow_time(dag_city), reply_markup= await client_kb.dag_city(dag_city, 'tomorrow',user_id))
	except:
		await callback.message.answer('Ой, что-то пошло не так...', reply_markup=client_kb.markup_main)	
	await callback.answer()

async def dagestan_month(callback: types.CallbackQuery):
	global dag_city
	try:
		await callback.message.edit_text(f'Город: <b>{dag_city}</b>\nМесяц: <b>{months[str(datetime.now().month)]}</b>\n<b>Выберите день:</b>ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ',reply_markup=await client_kb.dagestan_month())
	except:
		await callback.message.answer('Ой, что-то пошло не так...', reply_markup=client_kb.markup_main)	
	await callback.answer()

async def dagestan_month_time(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global dag_city
	try:
		await callback.message.edit_text(await parcer_dagestan.get_month_time(dag_city, callback.data[9:]), reply_markup= await client_kb.dag_city(dag_city, 'month', user_id))
	except:
		await callback.message.answer('Ой, что-то пошло не так...', reply_markup=client_kb.markup_main)
	await callback.answer()

async def dagestan_favorite_add(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global dag_city
	sqlite_bd.cur.execute(f'INSERT INTO favorite_dagestan VALUES (?, ?)', (user_id, dag_city))
	sqlite_bd.base.commit()
	await callback.message.edit_text('Добавлено в избранные ✅', reply_markup = client_kb.markup_favorite)
	await callback.answer()

async def dagestan_favorite_delete(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global dag_city
	sqlite_bd.cur.execute('DELETE FROM favorite_dagestan WHERE user_id == ? AND address == ?', (user_id, dag_city))
	sqlite_bd.base.commit()
	await callback.message.edit_text('Удалено из избранных ✅', reply_markup = client_kb.markup_favorite)
	await callback.answer()

async def kazakhstan_menu(callback: types.CallbackQuery):
	kaz_page = 1
	await callback.message.edit_text('<b>Выберите населенный пункт:</b>', reply_markup=await client_kb.kazakhstan_markup(kaz_page))
	await callback.answer()
async def kazakhstan_menu_next(callback: types.CallbackQuery):
	data = callback.data[9:]
	kaz_page = int(data) + 1
	await callback.message.edit_text('<b>Выберите населенный пункт:</b>', reply_markup=await client_kb.kazakhstan_markup(kaz_page))
	await callback.answer()
async def kazakhstan_menu_back(callback: types.CallbackQuery):
	data = callback.data[9:]
	kaz_page = int(data) - 1
	await callback.message.edit_text('<b>Выберите населенный пункт:</b>', reply_markup=await client_kb.kazakhstan_markup(kaz_page))
	await callback.answer()

async def kazakhstan_today_time(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global kaz_city
	kaz_city = callback.data[9:]
	try:
		await callback.message.edit_text(await parcer_kazakhstan.get_day_time(kaz_city), reply_markup=await client_kb.kaz_city(kaz_city, 'today', user_id))
	except:
		await callback.message.answer('Ой, что-то пошло не так...', reply_markup=client_kb.markup_main)	
	await callback.answer()

async def kazakhstan_tomorrow_time(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global kaz_city
	try:
		await callback.message.edit_text(await parcer_kazakhstan.get_tomorrow_time(kaz_city), reply_markup=await client_kb.kaz_city(kaz_city, 'tomorrow', user_id))
	except:
		await callback.message.answer('Ой, что-то пошло не так...', reply_markup=client_kb.markup_main)	
	await callback.answer()

async def kazakhstan_month(callback: types.CallbackQuery):
	global kaz_city
	try:
		await callback.message.edit_text(f'Город: <b>{kaz_city}</b>\nМесяц: <b>{months[str(datetime.now().month)]}</b>\n<b>Выберите день:</b>ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ',reply_markup=await client_kb.kazakhstan_month())
	except:
		await callback.message.answer('Ой, что-то пошло не так...', reply_markup=client_kb.markup_main)
	await callback.answer()

async def kazakhstan_month_time(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global kaz_city
	try:
		await callback.message.edit_text(await parcer_kazakhstan.get_month_time(kaz_city, callback.data[9:]), reply_markup= await client_kb.kaz_city(kaz_city, 'month', user_id))
	except:
		await callback.message.answer('Ой, что-то пошло не так...', reply_markup=client_kb.markup_main)	
	await callback.answer()

async def kazakhstan_favorite_add(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global kaz_city
	sqlite_bd.cur.execute(f'INSERT INTO favorite_kazakhstan VALUES (?, ?)', (user_id, kaz_city))
	sqlite_bd.base.commit()
	await callback.message.edit_text('Добавлено в избранные ✅', reply_markup = client_kb.markup_favorite)
	await callback.answer()

async def kazakhstan_favorite_delete(callback: types.CallbackQuery):
	global kaz_city
	user_id = callback.from_user.id
	sqlite_bd.cur.execute('DELETE FROM favorite_kazakhstan WHERE user_id == ? AND address == ?', (user_id, kaz_city))
	sqlite_bd.base.commit()
	await callback.message.edit_text('Удалено из избранных ✅', reply_markup = client_kb.markup_favorite)
	await callback.answer()
	
async def favorite_cities(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	await callback.message.edit_text('<b>Избранные города:</b>ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ', reply_markup=await client_kb.favorite_cities(user_id))
	await callback.answer()

async def dua_get(callback: types.CallbackQuery):
	data = callback.data[4:]
	await bot.send_photo(callback.from_user.id, dua_id[data], reply_markup=client_kb.markup_dua_lower)
	await callback.answer()

async def dua_all(callback: types.CallbackQuery):
	await callback.answer()
	await callback.message.delete()
	await callback.message.answer('<b>Дуа какого пророка (мир Им) прислать?</b>', reply_markup=client_kb.markup_dua)

async def hadis_command(message: types.Message):
	await message.answer('Выберите раздел:', reply_markup=client_kb.markup_hadis)

async def hadis_random(callback: types.CallbackQuery):
	count = await parcer_hadis.get_random_count()
	user_id = callback.from_user.id
	try:
		await callback.message.edit_text(await parcer_hadis.get_hadis(count), reply_markup=await client_kb.markup_hadis_random(count, user_id))
	except:
		count += 1
		await callback.message.edit_text(await parcer_hadis.get_hadis(count), reply_markup=await client_kb.markup_hadis_random(count, user_id))	
	await callback.answer()

async def hadis_add(callback: types.CallbackQuery):
	data = callback.data[19:]
	user_id = callback.from_user.id
	saved_id = 1
	try:
		for item in sqlite_bd.cur.execute('SELECT id FROM hadis WHERE user_id == ?', (user_id, )).fetchall():
			saved_id = int(item[0]) + 1
	except:
		pass
	sqlite_bd.cur.execute('INSERT INTO hadis VALUES(?, ?, ?)', (user_id, data, saved_id))
	sqlite_bd.base.commit()
	await callback.message.edit_text(await parcer_hadis.get_hadis(int(data)), reply_markup=await client_kb.markup_hadis_random(int(data), user_id))
	await callback.answer()

async def hadis_delete(callback: types.CallbackQuery):
	data = callback.data[22:]
	user_id = callback.from_user.id
	sqlite_bd.cur.execute('DELETE FROM hadis WHERE user_id == ? AND hadis_id == ?', (user_id, data))
	sqlite_bd.base.commit()
	count = 0
	for i in sqlite_bd.cur.execute('SELECT hadis_id FROM hadis WHERE user_id == ?', (user_id, )).fetchall():
		count += 1
		sqlite_bd.cur.execute('UPDATE hadis SET id == ? WHERE user_id == ? AND hadis_id == ?', (count, user_id, i[0]))
		sqlite_bd.base.commit()
	await callback.message.edit_text(await parcer_hadis.get_hadis(int(data)), reply_markup=await client_kb.markup_hadis_random(int(data), user_id))
	await callback.answer()

async def hadis_saved(callback : types.CallbackQuery):
	page = 1
	user_id = callback.from_user.id
	await callback.message.edit_text('Выберите хадис:', reply_markup= await client_kb.hadis_favorite(user_id, page))
	await callback.answer()

async def hadis_saved_next(callback : types.CallbackQuery):
	data = callback.data[11:]
	page = int(data) + 1
	user_id = callback.from_user.id
	await callback.message.edit_text('Выберите хадис:', reply_markup= await client_kb.hadis_favorite(user_id, page))
	await callback.answer()

async def hadis_saved_back(callback : types.CallbackQuery):
	data = callback.data[11:]
	page = int(data) - 1
	user_id = callback.from_user.id
	await callback.message.edit_text('Выберите хадис:', reply_markup= await client_kb.hadis_favorite(user_id, page))
	await callback.answer()

async def hadis_get_saved(callback: types.CallbackQuery):
	data = callback.data[12:]
	user_id = callback.from_user.id
	await callback.message.edit_text(await parcer_hadis.get_hadis(int(data)), reply_markup=await client_kb.markup_hadis_random(int(data), user_id))
	await callback.answer()

async def codes_command(message: types.Message):
	await FSMhalal.code.set()
	await message.answer('<b>Добавки, которые ВСЕГДА имеют животное происхождение:</b>\n • E 120 Кошениль: красный краситель, получаемый от самок насекомых,\n • E 441 Желатин: добывают из костей и/или шкуры скота и/или свиней,\n • E 542 Фосфат натрия: экстракт из костей животных,\n • E 904 Шеллак: смола, вырабатываемая лаковыми червецами (насекомыми).\n\n<b>Основные добавки, на которые следует обращать внимание:</b>\n •  Глицерин, глицерол (Е422) – харам, если получен из свинины или иного нехаляльного мяса.\n • Эмульгаторы (Е470-483) – харам, если получены из свинины или иного нехаляльного сырья.\n • Фосфат натрия (E542) – харам, если получен из свинины или иного нехаляльного мяса.\n<i>Источник: <a href = "https://azan.ru/upload/%D0%9F%D0%B8%D1%89%D0%B5%D0%B2%D1%8B%D0%B5%20%D0%B4%D0%BE%D0%B1%D0%B0%D0%B2%D0%BA%D0%B8%20%D1%81%20%C2%ABE%C2%BB-%D0%BA%D0%BE%D0%B4%D0%B0%D0%BC%D0%B8.pdf?ysclid=l86bydf9b9502427516">Azan.ru</a></i>\n\n <b>Напишите E-добавку:</b>', reply_markup=types.ReplyKeyboardRemove(), disable_web_page_preview=True)

async def codes_get_code(message: types.Message, state = FSMContext):
	async with state.proxy() as data:
		data['code'] = message.text
		code = data['code']
	try:
		await message.answer(await parcer_codes.get_code(code), reply_markup=client_kb.markup_main)
	except:
		await message.answer('Такого кода не нашлось!', reply_markup=client_kb.markup_main)
	await state.finish()

async def food_command(message: types.Message):
	food_page = 1
	await message.answer(await parcer_food.get_message(food_page), reply_markup=await client_kb.food_markup(food_page))

async def food_next(callback: types.CallbackQuery):
	data = callback.data[10:]
	food_page = int(data) + 1
	await callback.message.edit_text(await parcer_food.get_message(food_page), reply_markup=await client_kb.food_markup(food_page))

async def food_back(callback: types.CallbackQuery):
	data = callback.data[10:]
	food_page = int(data) - 1
	await callback.message.edit_text(await parcer_food.get_message(food_page), reply_markup=await client_kb.food_markup(food_page))

async def tutor_menu(message: types.Message):
	await message.answer('Обучение на основе Ханафитского мазхаба |  | <i>Источник: <a href = "https://dumrt.ru/ru/help-info/training-prayer/">ДУМ РТ</a></i>\nВыберите раздел: ', reply_markup=client_kb.markup_namaz_tutor, disable_web_page_preview=True)

async def calc_get(callback: types.CallbackQuery):
	data = callback.data[5:]
	if data == 'minus':
		await callback.message.answer('Отнять 1 от выполненных намазов')
	else:
		await callback.message.answer('Прибавить 1 к выполненным намазам')
	await callback.answer()

async def qoran_audio_all(callback: types.CallbackQuery):
	for i in surah_audio:
		await bot.send_audio(callback.from_user.id, surah_audio[i])
	await callback.answer()

async def photo_file_id(message: types.Message):
    await message.answer(message.photo[2].file_id)

# async def document_file_id(message: types.Message):
#     await message.answer(message.document.file_id)

# async def audio_file_id(message: types.Message):
#     await message.answer(message.audio.file_id)

# dispatcher
def register_handlers_client(dp : Dispatcher):
	dp.register_message_handler(start_command, commands=['start'])
	dp.register_message_handler(favorite_command, lambda message: message.text == "🕦 Время намаза")
	dp.register_message_handler(tracker_command, lambda message: message.text == "📈 Трекер")
	dp.register_message_handler(tracker_reset, commands=['reset'])
	dp.register_callback_query_handler(tracker_reset_cancel, text = 'tracker_cancel')
	dp.register_callback_query_handler(tracker_reset_yes, text = 'tracker_reset')
	dp.register_message_handler(tutor_command, lambda message: message.text == "🕌 Обучение")
	dp.register_message_handler(hadis_command, lambda message: message.text == "📕 Хадисы")
	dp.register_message_handler(tutor_namaz_command, lambda message: message.text == "❓\n Что такое намаз")
	dp.register_message_handler(tutor_time_command, lambda message: message.text == "🕦\n Время намазов")
	dp.register_message_handler(tutor_cond_command, lambda message: message.text == "❗\n Условия намаза")
	dp.register_message_handler(tutor_gusl_command, lambda message: message.text == "🚿\n Гусль")
	dp.register_message_handler(tutor_taharat_command, lambda message: message.text == "💧\n Тахарат")	
	dp.register_message_handler(tutor_forma_command, lambda message: message.text == "🧎\n Форма совершения намаза")	
	dp.register_message_handler(tutor_sura_command, lambda message: message.text == "📃\n Суры и дуа намаза")
	dp.register_message_handler(tutor_women_command, lambda message: message.text == "🧕\n Женский намаз")					
	dp.register_message_handler(qoran_command, lambda message: message.text == "📖 30-й джуз")
	dp.register_callback_query_handler(qoran_next, text_startswith = 'qoran_next_')
	dp.register_callback_query_handler(qoran_back, text_startswith = 'qoran_back_')
	dp.register_message_handler(names_command, lambda message: message.text == "❾❾ Имён")
	dp.register_message_handler(calendar_command, lambda message: message.text == "📅 Календарь")
	dp.register_message_handler(info_command, lambda message: message.text == "❗ Помощь")
	dp.register_message_handler(zikr_command, lambda message: message.text == "📿 Зикр")
	dp.register_message_handler(tutor_menu, lambda message: message.text == "⏪ Меню")
	dp.register_message_handler(help_command, commands=['help'])
	dp.register_message_handler(back_command, lambda message: message.text == "⏪ Назад")
	dp.register_message_handler(food_command, lambda message: message.text == "🍔 Халяль гид")
	dp.register_callback_query_handler(time_command, text = 'add_city')
	dp.register_callback_query_handler(namaz_day_command, text = parcer_tatarstan.all_cities)
	dp.register_callback_query_handler(next_day_time_command, text = 'tomorrow_time')
	dp.register_callback_query_handler(tatarstan_command, text = 'tatarstan')
	dp.register_callback_query_handler(tatarstan_next, text_startswith = 'next_tat_')
	dp.register_callback_query_handler(tatarstan_back, text_startswith = 'back_tat_')
	dp.register_callback_query_handler(month_time_command, text = 'month_time')
	dp.register_callback_query_handler(address_add, text = 'other_region')
	dp.register_message_handler(cancel_handler, commands='cancel', state='*')
	dp.register_message_handler(address_get, state=FSMaddress.address)
	dp.register_callback_query_handler(school_get, text_startswith='school_',state=FSMaddress.school)
	dp.register_callback_query_handler(favorite_add_other, text='other_add')
	dp.register_callback_query_handler(favorite_delete_other, text='other_delete')
	dp.register_callback_query_handler(time_other, text_startswith='city_other_')
	dp.register_callback_query_handler(month_days_other, text='other_month')
	dp.register_callback_query_handler(tomorrow_time_other, text='other_tomorrow')
	dp.register_callback_query_handler(today_time_other, text='other_today')
	dp.register_callback_query_handler(month_time_other, text_startswith='other_days_')
	dp.register_callback_query_handler(tatarstan_month, text_startswith='tatarstan_days_')
	dp.register_callback_query_handler(tatarstan_favorite_add, text='tatarstan_favorite_add')
	dp.register_callback_query_handler(tatarstan_favorite_delete, text='tatarstan_favorite_delete')
	dp.register_callback_query_handler(dagestan_menu, text = 'dagestan')
	dp.register_callback_query_handler(kazakhstan_menu, text = 'kazakhstan')
	dp.register_callback_query_handler(kazakhstan_menu_next, text_startswith = 'next_kaz_')
	dp.register_callback_query_handler(kazakhstan_menu_back, text_startswith = 'back_kaz_')
	dp.register_callback_query_handler(kazakhstan_today_time, text_startswith = 'kaz_city_')
	dp.register_callback_query_handler(kazakhstan_tomorrow_time, text = 'kaz_tomorrow')
	dp.register_callback_query_handler(kazakhstan_month, text = 'kaz_month')
	dp.register_callback_query_handler(kazakhstan_month_time, text_startswith = 'kaz_days_')
	dp.register_callback_query_handler(kazakhstan_favorite_add, text='kaz_add')
	dp.register_callback_query_handler(kazakhstan_favorite_delete, text='kaz_delete')
	dp.register_callback_query_handler(dagestan_menu_next, text_startswith = 'next_dag_')
	dp.register_callback_query_handler(dagestan_menu_back, text_startswith = 'back_dag_')
	dp.register_callback_query_handler(dagestan_today_time, text_startswith = 'dag_city_')
	dp.register_callback_query_handler(dagestan_tomorrow_time, text = 'dag_tomorrow')
	dp.register_callback_query_handler(dagestan_month, text = 'dag_month')
	dp.register_callback_query_handler(dagestan_month_time, text_startswith='dag_days_')
	dp.register_callback_query_handler(dagestan_favorite_add, text = 'dag_add')
	dp.register_callback_query_handler(dagestan_favorite_delete, text = 'dag_delete')
	dp.register_callback_query_handler(favorite_cities, text = 'favorite_cities')
	dp.register_callback_query_handler(tracker_myself, text = 'tracker_myself')
	dp.register_message_handler(tracker_fajr_get, state = FSMtracker.fajr)
	dp.register_message_handler(tracker_zuhr_get, state = FSMtracker.zuhr)
	dp.register_message_handler(tracker_asr_get, state = FSMtracker.asr)
	dp.register_message_handler(tracker_magrib_get, state = FSMtracker.magrib)
	dp.register_message_handler(tracker_isha_get, state = FSMtracker.isha)
	dp.register_message_handler(tracker_vitr_get_yourself, state = FSMtracker.vitr)
	dp.register_callback_query_handler(tracker_plus, text_startswith = 'plus_')
	dp.register_callback_query_handler(tracker_minus, text_startswith = 'minus_')
	dp.register_callback_query_handler(other_btn_tracker, text_startswith = 'troth_')
	dp.register_callback_query_handler(tracker_calculate, text = 'tracker_calculate')
	dp.register_message_handler(tracker_get_first, state = FSMtracker.first_date)
	dp.register_message_handler(tracker_get_second, state = FSMtracker.second_date)	
	dp.register_callback_query_handler(tracker_vitr_get, text_startswith = 'vitr_')
	dp.register_callback_query_handler(zikr_reset_cancel, text_startswith = 'zikr_reset_cancel_')
	dp.register_callback_query_handler(zikr_reset_yes, text_startswith = 'zikr_reset_yes_')
	dp.register_callback_query_handler(zikr_reset, text_startswith = 'zikr_reset_')
	dp.register_callback_query_handler(zikr_plus, text_startswith = 'zikr_plus_')
	dp.register_callback_query_handler(dua_get_all, text = 'dua_prorokov')
	dp.register_callback_query_handler(zikr_all_get, text = 'zikr_all_get')
	dp.register_callback_query_handler(zikr_all, text = 'zikr_all')
	dp.register_callback_query_handler(zikr_polza, text_startswith = 'zikr_polza_')
	dp.register_callback_query_handler(zikr_get, text_startswith = 'zikr_')
	dp.register_callback_query_handler(dua_all, text = 'dua_all')
	dp.register_callback_query_handler(dua_get, text_startswith = 'dua_')
	dp.register_callback_query_handler(hadis_random, text = 'hadis_random')
	dp.register_callback_query_handler(hadis_add, text_startswith = 'hadis_favorite_add_')
	dp.register_callback_query_handler(hadis_delete, text_startswith = 'hadis_favorite_delete_')
	dp.register_callback_query_handler(hadis_saved, text = 'hadis_favorite')
	dp.register_callback_query_handler(hadis_get_saved, text_startswith = 'hadis_saved_')
	dp.register_callback_query_handler(hadis_saved_back, text_startswith = 'back_hadis_')
	dp.register_callback_query_handler(hadis_saved_next, text_startswith = 'next_hadis_')
	dp.register_callback_query_handler(names_command_back, text_startswith = 'back_names_')
	dp.register_callback_query_handler(names_command_next, text_startswith = 'next_names_')
	dp.register_callback_query_handler(names_get_photo, text_startswith = 'names_')
	dp.register_callback_query_handler(names_all, text = 'all_names')
	dp.register_callback_query_handler(names_next, text_startswith = 'next_photo_')
	dp.register_callback_query_handler(names_back, text_startswith = 'back_photo_')
	dp.register_callback_query_handler(qoran_translate, text_startswith = 'surah_translate_')
	dp.register_callback_query_handler(qoran_surah_get, text_startswith = 'surah_')
	dp.register_callback_query_handler(qoran_audio_all, text = 'qoran_audio_all')
	dp.register_callback_query_handler(qoran_audio, text_startswith = 'qoran_audio_')
	dp.register_message_handler(codes_command, lambda message: message.text == "📄 E-добавки")	
	dp.register_message_handler(codes_get_code, state = FSMhalal.code)

	# dp.register_callback_query_handler(food_next, text_startswith = 'next_food_')
	# dp.register_callback_query_handler(food_back, text_startswith = 'back_food_')
	dp.register_message_handler(photo_file_id, content_types=["photo"])
	# dp.register_message_handler(audio_file_id, content_types=["audio"])
	# dp.register_message_handler(document_file_id, content_types=["document"])