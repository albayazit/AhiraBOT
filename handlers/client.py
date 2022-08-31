from asyncio.windows_events import NULL
from multiprocessing.connection import Client
from tkinter import INSERT
from aiogram import Dispatcher, types
from create_bot import dp
from keyboards import client_kb
from parcer import parcer_dagestan, parcer_kazakhstan, parcer_other, parcer_tatarstan, parcer_hadis
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
	'1':'AgACAgIAAxkBAAIj-2MEqww_R8l4yTihKS9V95GzPv0kAAJ4wDEbbjwoSP9h0ZMpyD2bAQADAgADeQADKQQ',
	'2':'AgACAgIAAxkBAAIj_WMEqxP4-QfrbN0aU5znSZFZlHKhAAJ5wDEbbjwoSNLXeYDXqzGXAQADAgADeQADKQQ',
	'3':'AgACAgIAAxkBAAIj_2MEqx1v7YWepWaOdjq8b_x5eKGqAAJ6wDEbbjwoSDeCXPTR4APQAQADAgADeQADKQQ',
	'4':'AgACAgIAAxkBAAIkAWMEqye9RmwmP_x4G5i_XR0hbc3LAAJ7wDEbbjwoSNbM0lZv1qe8AQADAgADeQADKQQ',
	'5':'AgACAgIAAxkBAAIkA2MEqyyFWVYrigrzR9GkjaJNOtIZAAJ8wDEbbjwoSHuWKaAJkTYdAQADAgADeQADKQQ',
	'6':'AgACAgIAAxkBAAIkBWMEqzS2JRpSdiaIO7Yn98RUznbQAAJ9wDEbbjwoSPgwgN7uLjQWAQADAgADeQADKQQ',
	'7':'AgACAgIAAxkBAAIkB2MEqzofTHX2EvshZ2sk8-Ehf1rvAAJ-wDEbbjwoSJDb9PGGvUs3AQADAgADeAADKQQ',
	'8':'AgACAgIAAxkBAAIkCWMEqz_eLurs9GC9Pxszd_BGwxxIAAJ_wDEbbjwoSF1sp6Wn4OMCAQADAgADeQADKQQ',
	'9':'AgACAgIAAxkBAAIkC2MEq0QZMppnDWP48U72P86n-t51AAKAwDEbbjwoSCHikcX1VGvrAQADAgADeQADKQQ',
	'10':'AgACAgIAAxkBAAIkDWMEq0mG7dzy9WkON0gX5nhfZNifAAKBwDEbbjwoSKDKheWQBGIeAQADAgADeQADKQQ',
	'11':'AgACAgIAAxkBAAIkD2MEq03iR7j_TmYbUiM7DraRblRYAAKCwDEbbjwoSArz1Oa4zOW6AQADAgADeQADKQQ',
	'12':'AgACAgIAAxkBAAIkEWMEq1FqrpMYczi_f4a1ClBR4OcsAAKDwDEbbjwoSFNW39f-yMXaAQADAgADeQADKQQ',
	'13':'AgACAgIAAxkBAAIkE2MEq3DkQ1k3gFWEAAG1on9nE78CAgAChMAxG248KEhWOZN02HeNTAEAAwIAA3kAAykE',
	'14':'AgACAgIAAxkBAAIkFWMEq3irb4oF_CH0CgJ98mzaI6ojAAKFwDEbbjwoSCVKzJIjoxsTAQADAgADeQADKQQ',
	'15':'AgACAgIAAxkBAAIkF2MEq4ONMSge7gwMoyTfLj8PBTp5AAKGwDEbbjwoSMACx-2DW3wpAQADAgADeQADKQQ',
	'16':'Без категории',
}

dua_id = {
	'1':'AgACAgIAAxkBAAIlHGMFTClsgFgTDVxSzxU-HJHrFWgfAAIyvTEbbjwwSGfz_S4tznN-AQADAgADeQADKQQ',
	'2':'AgACAgIAAxkBAAIlHmMFTDDaXuS-OXFWDLCEeJ8dUpNqAAIzvTEbbjwwSHc_Uj00YEc6AQADAgADeQADKQQ',
	'3':'AgACAgIAAxkBAAIlIGMFTDSJFphZROk_EdgmFXxDPUPwAAI0vTEbbjwwSIzrQyGDakW8AQADAgADeQADKQQ',
	'4':'AgACAgIAAxkBAAIlImMFTDgBrgwvcbG2Cx__jZuJ0AmUAAI1vTEbbjwwSJwxlYwb4AMLAQADAgADeQADKQQ',
	'5':'AgACAgIAAxkBAAIlJGMFTDyyvbageKijElCpaAABlAJZ_gACNr0xG248MEieTZcBA2SFbwEAAwIAA3kAAykE',
	'6':'AgACAgIAAxkBAAIlJmMFTEFbO0mD3GrIhmF8GcpI7nfzAAI3vTEbbjwwSHIS4BFHZGd8AQADAgADeQADKQQ',
	'7':'AgACAgIAAxkBAAIlKGMFTEXbXZk_VBb6z_5SBfn5xF83AAI4vTEbbjwwSA0mnGYmiDi9AQADAgADeQADKQQ',
	'8':'AgACAgIAAxkBAAIlKmMFTEkX9dwZq2Jj81lFD24wu-LVAAI5vTEbbjwwSAABQ8DammkfgwEAAwIAA3kAAykE',
	'9':'AgACAgIAAxkBAAIlLGMFTE1phlBBNtctKkx6S2Mi6PITAAI6vTEbbjwwSHkuUieLk-MFAQADAgADeQADKQQ',
	'10':'AgACAgIAAxkBAAIlLmMFTFOur1XoL2QEpdKarEUaxfx_AAI7vTEbbjwwSOof4vANzG7KAQADAgADeQADKQQ',
	'11':'AgACAgIAAxkBAAIlMGMFTFtYuorVoO7exS6rt94dITvZAAI8vTEbbjwwSFZBTeD1pR3oAQADAgADeQADKQQ',
	'12':'AgACAgIAAxkBAAIlMmMFTF6z4gPl3Xjfmeuan3WVKWbpAAI9vTEbbjwwSNhRvCxTwEGJAQADAgADeQADKQQ',
	'13':'AgACAgIAAxkBAAIlNGMFTGKlwRsP-n9sxvhHj0_b_YnuAAI-vTEbbjwwSBrfsKObT0qEAQADAgADeQADKQQ'
}

names_id = {
	'1':'AgACAgIAAxkBAAInYGMPIHqaTeT62NyISZgOrG-ThWosAAJ8vDEbQjR4SM6cqwcg_WYiAQADAgADeQADKQQ',
	'2':'AgACAgIAAxkBAAInYWMPIHoOelCxmjizq0NUs5XAz628AAJ9vDEbQjR4SDksPMSMqCN8AQADAgADeQADKQQ',
	'3':'AgACAgIAAxkBAAInY2MPIHv5ewkRqPOgERQDu3dSmFk3AAJ-vDEbQjR4SLK43UtY-6cAAQEAAwIAA3kAAykE',
	'4':'AgACAgIAAxkBAAInZWMPIHuref8J789Vstu7hp7Fsv-UAAJ_vDEbQjR4SAgH_NU6BfHdAQADAgADeQADKQQ',
	'5':'AgACAgIAAxkBAAInZmMPIHvR9y0xctcoqym-6Vka1HoGAAKAvDEbQjR4SE_KfQPSqiVHAQADAgADeQADKQQ',
	'6':'AgACAgIAAxkBAAInaGMPIHtzIMAoZgdqtY8COJFAiJTzAAKCvDEbQjR4SN72jVQKAAEJYwEAAwIAA3kAAykE',
	'7':'AgACAgIAAxkBAAInamMPIHsLeKA98fnXEPMN2ubsshEJAAKDvDEbQjR4SCy96MiwWyydAQADAgADeQADKQQ',
	'8':'AgACAgIAAxkBAAIna2MPIHvrowk2WYfUqaG_Fx3TLRciAAKEvDEbQjR4SFxZ4zf5bk_dAQADAgADeQADKQQ',
	'9':'AgACAgIAAxkBAAInbmMPIHsdmFRGsBx8WUWHiQzAtK80AAKFvDEbQjR4SLa55YLqjPKnAQADAgADeQADKQQ',
	'10':'AgACAgIAAxkBAAIncGMPIHtZC0P0jo0Y_xbjp_G7eca8AAKGvDEbQjR4SMz6Toe_bVk5AQADAgADeQADKQQ',
	'11':'AgACAgIAAxkBAAIncWMPIHtOjTnFDwZRVgftBh077xPpAAKHvDEbQjR4SPAEEFadWW9HAQADAgADeQADKQQ',
	'12':'AgACAgIAAxkBAAIndGMPIHs4bCeMR4bmt_yIIF6x0SRfAAKIvDEbQjR4SLR7wxJR6_8eAQADAgADeQADKQQ',
	'13':'AgACAgIAAxkBAAIneGMPIHwj8aZXfJT0WnOsqXnqLVDvAAKJvDEbQjR4SBXnZHFktjySAQADAgADeQADKQQ',
	'14':'AgACAgIAAxkBAAInemMPIHyLphepXzm3GyDYP5m6SnxxAAKKvDEbQjR4SHh1JpJaZNYvAQADAgADeQADKQQ',
	'15':'AgACAgIAAxkBAAInfGMPIHzY5b-d-2fKza6EZuO09L0cAAKLvDEbQjR4SDSbKc82ty0JAQADAgADeQADKQQ',
	'16':'AgACAgIAAxkBAAInfmMPIHzzRjRkZ5n61khg9yWEvTqAAAKMvDEbQjR4SFb_w4ejp-VoAQADAgADeQADKQQ',
	'17':'AgACAgIAAxkBAAIngGMPIHx0D5j69T028feajGtg1DP2AAKNvDEbQjR4SEa42Llajb7DAQADAgADeQADKQQ',
	'18':'AgACAgIAAxkBAAIngmMPIHyPiB6nz5fA4qdXLYXw5kwjAAKOvDEbQjR4SERKdqQkil87AQADAgADeQADKQQ',
	'19':'AgACAgIAAxkBAAInhWMPIH2xlqwwI53cNmCT_QMdjhF-AAKQvDEbQjR4SEi8mupm0ePVAQADAgADeQADKQQ',
	'20':'AgACAgIAAxkBAAInh2MPIH2LHWXhjwViCta4X4OZ4qYtAAKRvDEbQjR4SEiITvCSo9VGAQADAgADeQADKQQ',
	'21':'AgACAgIAAxkBAAInimMPIH1dERlZktavBzn9LF24fTNoAAKTvDEbQjR4SD6BFbMoczTdAQADAgADeQADKQQ',
	'22':'AgACAgIAAxkBAAInkWMPIH538A3hGPiiYaIhrMkUUiNPAAKWvDEbQjR4SNNe0lR-6kvuAQADAgADeQADKQQ',
	'23':'AgACAgIAAxkBAAInlGMPIH6st5WYK3gvuMYbtCQbiteJAAKYvDEbQjR4SEtAcb1bTKdQAQADAgADeQADKQQ',
	'24':'AgACAgIAAxkBAAInlmMPIH4d0-Y5h6hAg5R18XgiBA1bAAKavDEbQjR4SId36dkemf08AQADAgADeQADKQQ',
	'25':'AgACAgIAAxkBAAInnmMPIH4XLsY4rGLXHpATef_crLZvAAKdvDEbQjR4SIy2FNt1IaQnAQADAgADeQADKQQ',
	'26':'AgACAgIAAxkBAAInhGMPIH1rsnQ8HAZYqgufL32wIhapAAKPvDEbQjR4SKOHrXNKsDftAQADAgADeQADKQQ',
	'27':'AgACAgIAAxkBAAIniGMPIH2q_pjvUKc6wVbtFpMwtw08AAKSvDEbQjR4SAVh-Ubh6KM2AQADAgADeQADKQQ',
	'28':'AgACAgIAAxkBAAIni2MPIH34H6o8qUbJhoUNQAABU-Mk4AAClLwxG0I0eEgPV-gChsKFIgEAAwIAA3kAAykE',
	'29':'AgACAgIAAxkBAAInjmMPIH5KDeRT1xR9IiKVnwNIjYIgAAKVvDEbQjR4SE49tA0BKxrgAQADAgADeQADKQQ',
	'30':'AgACAgIAAxkBAAInkmMPIH4ESmJo_y05MCKMEjo3Q-lyAAKXvDEbQjR4SKahrlvOEzKrAQADAgADeQADKQQ',
	'31':'AgACAgIAAxkBAAInlWMPIH7FdFHaJAlYVpYv0z8sshCIAAKZvDEbQjR4SF53g6eZ6wZ6AQADAgADeQADKQQ',
	'32':'AgACAgIAAxkBAAInmGMPIH4ra2iYuTZAF2w849TH_j3oAAKbvDEbQjR4SJNQmwuDd5UfAQADAgADeQADKQQ',
	'33':'AgACAgIAAxkBAAInm2MPIH5l5t84bDeRYC5qXMYSS_VXAAKcvDEbQjR4SA_PSpbzjMdNAQADAgADeQADKQQ',
	'34':'AgACAgIAAxkBAAInoGMPIH4WohMQpo7HLKHicdLDSV78AAKevDEbQjR4SOv8rieagInsAQADAgADeQADKQQ',
	'35':'AgACAgIAAxkBAAInomMPIH6fUtW3HVxGSJNjiNlwkGKqAAKfvDEbQjR4SIFABfdbsC0aAQADAgADeQADKQQ',
	'36':'AgACAgIAAxkBAAInpmMPIH918BShg8o9A53ViKggXmCeAAKgvDEbQjR4SKSfsomLtjBCAQADAgADeQADKQQ',
	'37':'AgACAgIAAxkBAAInqGMPIH8ZkutuTgbPkWjGbB8pKC7hAAKhvDEbQjR4SPu3Zcd7270qAQADAgADeQADKQQ',
	'38':'AgACAgIAAxkBAAInqmMPIH9_eKywCngkEqwjb75Btix0AAKivDEbQjR4SNKkpRVHJIefAQADAgADeQADKQQ',
	'39':'AgACAgIAAxkBAAInrGMPIH-CRpGB1l9ckQcfqGYHIqupAAKjvDEbQjR4SDJobpNYRz78AQADAgADeQADKQQ',
	'40':'AgACAgIAAxkBAAInrmMPIH-F3-3esjmZaYEWgI9z9oa8AAKkvDEbQjR4SA_LSixjGcj7AQADAgADeQADKQQ',
	'41':'AgACAgIAAxkBAAInsWMPIICQl9b44SASl5yGx9CD2iUQAAKmvDEbQjR4SJBJe2cVqjy9AQADAgADeQADKQQ',
	'42':'AgACAgIAAxkBAAIntWMPIICM2wKqTBKeVh-M_jDFlWOjAAKovDEbQjR4SNY0Ikdmobv3AQADAgADeQADKQQ',
	'43':'AgACAgIAAxkBAAInuGMPIIAyL7uJAju82LrmB3hHcGirAAKqvDEbQjR4SGH7EBB9hBhSAQADAgADeQADKQQ',
	'44':'AgACAgIAAxkBAAInumMPIICfKzPJ_6otbKW4mKSDwIVsAAKsvDEbQjR4SMP6UY39cEYFAQADAgADeQADKQQ',
	'45':'AgACAgIAAxkBAAInsGMPIIB_qL3zi11wGzr9vs7ZK-F_AAKlvDEbQjR4SPmt5A0SWXS8AQADAgADeQADKQQ',
	'46':'AgACAgIAAxkBAAIns2MPIICjMqKlfZLkkZtKCNwTVvSDAAKnvDEbQjR4SC9P7TcnIKVnAQADAgADeQADKQQ',
	'47':'AgACAgIAAxkBAAIntmMPIIDeJ3SC5rbgemzGJFEQL2-MAAKpvDEbQjR4SIobHminBpmAAQADAgADeQADKQQ',
	'48':'AgACAgIAAxkBAAInuWMPIIHeNLBesHj2SkoJBl-GiMOrAAKrvDEbQjR4SLG3WoBCl5gLAQADAgADeQADKQQ',
	'49':'AgACAgIAAxkBAAInv2MPIIF4GELMDQMZTMXhJ6ymfpCBAAKtvDEbQjR4SPpNGlnlp1yXAQADAgADeQADKQQ',
	'50':'AgACAgIAAxkBAAInwWMPIIHg63YKjAuQ68QOvqXsD_aeAAKuvDEbQjR4SMGbBTMYdoONAQADAgADeQADKQQ',
	'51':'AgACAgIAAxkBAAIp0WMPK9Xd0uaBNyY6Kdbl9PF6c0x8AAIwvTEbQjR4SMQlP2TB7OOtAQADAgADeQADKQQ',
	'52':'AgACAgIAAxkBAAInzWMPIIVReZJBlSM7zDUAATDOKs7USAACtLwxG0I0eEgkRD9DX5qrbgEAAwIAA3kAAykE',
	'53':'AgACAgIAAxkBAAInyGMPIIVFQkOuI6-_zhOa5KINIZD4AAKyvDEbQjR4SIQlOFagshJ5AQADAgADeQADKQQ',
	'54':'AgACAgIAAxkBAAIn0GMPIIW_MQre-_a3R7hwYn6bJAAB_gACtrwxG0I0eEh6DDwLIIuCMQEAAwIAA3kAAykE',
	'55':'AgACAgIAAxkBAAIn1GMPIIU3BxAu_-Jrbz81V4xs2v3SAAK3vDEbQjR4SOa8lHSwjS8UAQADAgADeQADKQQ',
	'56':'AgACAgIAAxkBAAIn1WMPIIWPkybkg1DvZVmlRo0IU4-vAAK4vDEbQjR4SAgSqtLCso_1AQADAgADeQADKQQ',
	'57':'AgACAgIAAxkBAAIn2GMPIIajEB_aFspBt0sRafFkeeKMAAK6vDEbQjR4SOTj_xhQiPriAQADAgADeQADKQQ',
	'58':'AgACAgIAAxkBAAIn3WMPIIb0LwRD9uT3ZNDGih-Z9VBfAAK8vDEbQjR4SGXDWUyCxNwKAQADAgADeQADKQQ',
	'59':'AgACAgIAAxkBAAIn4mMPIIYNUr27w4VwewF1Y7KD2z4cAAK_vDEbQjR4SLcHhNOLtQSxAQADAgADeQADKQQ',
	'60':'AgACAgIAAxkBAAIn5mMPIIafSQsqAoBAwMUz2ZncNMk0AALCvDEbQjR4SBLVa6jdU-e6AQADAgADeQADKQQ',
	'61':'AgACAgIAAxkBAAIn7WMPIIdFEQ6BpvfwlcV8dU61N15cAALGvDEbQjR4SNQiTtt7Zwp9AQADAgADeQADKQQ',
	'62':'AgACAgIAAxkBAAIn82MPIIcIjaFdMyWzTdPYzTSDLgXjAALIvDEbQjR4SD2agjtDN2gEAQADAgADeQADKQQ',
	'63':'AgACAgIAAxkBAAIn-GMPIIcbk-Wjhku-8dM0dDP3Be-YAALKvDEbQjR4SJfjXQABCGoKRQEAAwIAA3kAAykE',
	'64':'AgACAgIAAxkBAAIn_GMPIIcBZzhW4VkasFR7blGo5BCwAALLvDEbQjR4SFrZDGaiwKuPAQADAgADeQADKQQ',
	'65':'AgACAgIAAxkBAAIn_2MPIIfO-aAa5I-fXsUDRkiBFPA5AALNvDEbQjR4SCVI810wRCjvAQADAgADeQADKQQ',
	'66':'AgACAgIAAxkBAAInxGMPIIRkHtbpzToQb8jiZEgaw8BNAAKvvDEbQjR4SE30gH-aq8pyAQADAgADeQADKQQ',
	'67':'AgACAgIAAxkBAAInx2MPIIWpW9-oxAFP4y2LotJE1QY2AAKxvDEbQjR4SMx20j_DZeawAQADAgADeQADKQQ',
	'68':'AgACAgIAAxkBAAInyWMPIIVWQntJzQ1B5S_Vjz_rvvP8AAKzvDEbQjR4SAkpuNRqV9o6AQADAgADeQADKQQ',
	'69':'AgACAgIAAxkBAAInzGMPIIXzCP-af5OJoUicDzi23W34AAK1vDEbQjR4SClZkRx2w-SAAQADAgADeQADKQQ',
	'70':'AgACAgIAAxkBAAIn12MPIIV_9d1FhXnglMlCbjV-6y0gAAK5vDEbQjR4SL-QOQwM_c0XAQADAgADeAADKQQ',
	'71':'AgACAgIAAxkBAAIn2WMPIIUbjYuSrfJ6t0WKMrNSuFbqAAK7vDEbQjR4SJ039Fw2cf1HAQADAgADeQADKQQ',
	'72':'AgACAgIAAxkBAAIn32MPIIa71tStxBubqIR1fUwiJmzWAAK9vDEbQjR4SD32Hc_C4kmxAQADAgADeQADKQQ',
	'73':'AgACAgIAAxkBAAIn5GMPIIZrJwIzoaC67hgdOh4yCkHHAALAvDEbQjR4SMdzg4Gv1_UbAQADAgADeQADKQQ',
	'74':'AgACAgIAAxkBAAIn6GMPIIYnPYUiFf3A_UXXWI_MlcEsAALDvDEbQjR4SOVTsoy7s26XAQADAgADeQADKQQ',
	'75':'AgACAgIAAxkBAAIn62MPIIanl1Rswk1HKM1y6nmu_WmKAALFvDEbQjR4SBWhn_Kc8OiuAQADAgADeQADKQQ',
	'76':'AgACAgIAAxkBAAIn4WMPIIb4PkHEeaZNX6rjf2p7xgTBAAK-vDEbQjR4SBFtYIccy0x4AQADAgADeQADKQQ',
	'77':'AgACAgIAAxkBAAIn5WMPIIZPxvMSytsNH1LK1-SPSvhMAALBvDEbQjR4SDIKv10fSxvtAQADAgADeQADKQQ',
	'78':'AgACAgIAAxkBAAIn6mMPIIaJBBjOaFF1jKItumSA95XdAALEvDEbQjR4SFyd7w5YE9ORAQADAgADeQADKQQ',
	'79':'AgACAgIAAxkBAAIn72MPIId9MfGmQRO4B1K6P6eqRxP2AALHvDEbQjR4SMkXac1RRa3iAQADAgADeQADKQQ',
	'80':'AgACAgIAAxkBAAIn9mMPIIeIy1BBazG8nA-3JC8iZySBAALJvDEbQjR4SL93inJltKT-AQADAgADeQADKQQ',
	'81':'AgACAgIAAxkBAAIn_mMPIIebIakevEVNvISNg2zn2hpxAALMvDEbQjR4SKHW3T2bPdG7AQADAgADeQADKQQ',
	'82':'AgACAgIAAxkBAAIoAAFjDyCHezTYbagvTg8W9jlqmelnZQACzrwxG0I0eEhhBjMaJmXWtgEAAwIAA3kAAykE',
	'83':'AgACAgIAAxkBAAIoBGMPIIf4_cCUoCp0Ipl7wpf44HXiAALPvDEbQjR4SB_NAkGhgtjrAQADAgADeQADKQQ',
	'84':'AgACAgIAAxkBAAIoBmMPIIiIaKqn-QEzoSssdOLnTvUDAALQvDEbQjR4SHes1dztFX9qAQADAgADeQADKQQ',
	'85':'AgACAgIAAxkBAAIoCWMPIIiIcTuv_1W5hRkZkAvAZvaUAALSvDEbQjR4SO4jN6nJKUWkAQADAgADeQADKQQ',
	'86':'AgACAgIAAxkBAAIoDGMPIIjY2260PS4o1l91nH8NEumhAALUvDEbQjR4SIOHtYFVGh53AQADAgADeQADKQQ',
	'87':'AgACAgIAAxkBAAIoEGMPIIidAgNKlwNO5amD9HKvGEI3AALWvDEbQjR4SN9t2QfFgi9GAQADAgADeQADKQQ',
	'88':'AgACAgIAAxkBAAIoGWMPIIkKAAF3egHq4sx3T_6SVB3RyAAC2rwxG0I0eEgHrA5IqAi5UAEAAwIAA3kAAykE',
	'89':'AgACAgIAAxkBAAIoG2MPIIm5ZI8UZzv705fGinR-9t27AALbvDEbQjR4SC4JLy2EbEERAQADAgADeQADKQQ',
	'90':'AgACAgIAAxkBAAIoB2MPIIgU5SZFWxZs0PsNZDVFCSruAALRvDEbQjR4SGAm0UA4ln-QAQADAgADeQADKQQ',
	'91':'AgACAgIAAxkBAAIoCmMPIIjGwK4qfvLuVDp9BJSy16bvAALTvDEbQjR4SJ6qZytF7CNUAQADAgADeQADKQQ',
	'92':'AgACAgIAAxkBAAIoD2MPIIiyjWtYxKAJ1duUqjWK1-S5AALVvDEbQjR4SIfYtVYicknTAQADAgADeQADKQQ',
	'93':'AgACAgIAAxkBAAIoEmMPIIgSgTDPTB3Usly8lzeNHUhVAALXvDEbQjR4SP3nBy1QyUztAQADAgADeQADKQQ',
	'94':'AgACAgIAAxkBAAIoE2MPIInXkgm39C3zk7vr4TYzxNMVAALYvDEbQjR4SOn_fjyS42yxAQADAgADeQADKQQ',
	'95':'AgACAgIAAxkBAAIoFmMPIIl-_NGvjMotn8Nq4L_f5z_nAALZvDEbQjR4SAqV_jVn_3EGAQADAgADeQADKQQ',
	'96':'AgACAgIAAxkBAAIoHGMPIIqkV7vGww9El1JRxxMIkyZ5AALcvDEbQjR4SE02M-zAkOFzAQADAgADeQADKQQ',
	'97':'AgACAgIAAxkBAAIoIGMPIIr6yTm8PJLSotNW6EDW8LE0AALdvDEbQjR4SBao5aiUjcntAQADAgADeQADKQQ',
	'98':'AgACAgIAAxkBAAIoImMPIIo9cr90CkCoSe2HwKAT2zJdAALevDEbQjR4SIgUTNRpq8MzAQADAgADeQADKQQ',
	'99':'AgACAgIAAxkBAAIoJGMPIIo377D19feUnUKKiuN9rCQWAALfvDEbQjR4SP7-CZ3e2ufFAQADAgADeQADKQQ',
}

#--------------------Functions--------------------#

# Main keyboard | /start
async def start_command(message: types.Message):
	await message.answer('السلام عليكم ورحمة الله وبركاته', reply_markup=client_kb.markup_main)


# Favorite cities | 'Время намаза' (reply)
async def favorite_command(message: types.Message):
	global user_id
	user_id = message.from_user.id
	await message.answer('<b>Избранные города:</b>ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ', reply_markup=await client_kb.favorite_cities(user_id))

# Add new city | 'Добавить город' (inline)
async def time_command(callback : types.CallbackQuery):
	await callback.message.edit_text('Время намаза для других регионов сделана на основе наиболее предпочтительного метода вычитывания времени для данного города. Такие расчеты не всегда могут быть точными, убедительная просьба самостоятельно проверять наступление намаза по признакам при выборе "Другой регион".\n<b>Выберите регион:</b> ', reply_markup=client_kb.inline_namaz_time)
	await callback.answer()

# Tatarstan cities | 'Татарстан' (inline)
async def tatarstan_command(callback : types.CallbackQuery):
	global tat_page
	tat_page = 1
	await callback.message.edit_text('Выберите Ваш <b>населенный пункт:</b> ', reply_markup=await client_kb.inline_namaz_time_tat(tat_page))
	await callback.answer()

async def tatarstan_next(callback : types.CallbackQuery):
	global tat_page
	tat_page += 1
	await callback.message.edit_text('Выберите Ваш <b>населенный пункт:</b> ', reply_markup=await client_kb.inline_namaz_time_tat(tat_page))
	await callback.answer()

async def tatarstan_back(callback : types.CallbackQuery):
	global tat_page
	tat_page -= 1
	await callback.message.edit_text('Выберите Ваш <b>населенный пункт:</b> ', reply_markup=await client_kb.inline_namaz_time_tat(tat_page))
	await callback.answer()

# Tracker | 'Трекер'  (Reply)
async def tracker_command(message: types.Message):
	user_id = message.from_user.id
	info = sqlite_bd.cur.execute(f'SELECT EXISTS(SELECT * FROM tracker WHERE user_id == ?)', (user_id, ))
	if info.fetchone()[0] == 0:
		await message.answer('<b>Выберите способ:</b>', reply_markup=client_kb.markup_tracker_menu)
	else:
		await message.answer('Восстановление намазов:', reply_markup = await client_kb.markup_tracker(user_id))

async def tracker_myself(callback: types.CallbackQuery):
	await FSMtracker.fajr.set()
	await callback.message.delete()
	await callback.message.answer('Напишите количество <b>фаджр</b> намазов:', reply_markup = types.ReplyKeyboardRemove())
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
	await message.answer('Напишите количество <b>зухр</b> намазов: ')

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
	await message.answer('Напишите количество <b>аср</b> намазов: ')

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
	await message.answer('Напишите количество <b>магриб</b> намазов: ')

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
	await message.answer('Напишите количество <b>иша</b> намазов: ')

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
	await message.answer('Напишите количество <b>витр</b> намазов (при желании, можно написать 0): ')

async def tracker_vitr_get(message: types.Message, state = FSMContext):
	user_id = message.from_user.id
	async with state.proxy() as data:
		try:
			num = int(message.text)
			if num < 1:
				await state.finish()
				return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
			else:
				pass
			data['vitr_need'] = message.text
		except:
			await state.finish()
			return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
	async with state.proxy() as data:
		sqlite_bd.cur.execute('INSERT INTO tracker VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, NULL, data['fajr_need'], NULL, data['zuhr_need'], NULL, data['asr_need'], NULL, data['magrib_need'], NULL, data['isha_need'], NULL,data['vitr_need'], NULL, NULL))
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
			sqlite_bd.cur.execute('INSERT INTO tracker VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, NULL, result, NULL, result, NULL, result, NULL, result, NULL, result, NULL, result, second_date, first_date))
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
	await callback.message.answer('Восстановление намазов:', reply_markup = reply)
	

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
	await callback.message.edit_text('Восстановление намазов:', reply_markup = await client_kb.markup_tracker(user_id))
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
	await callback.message.edit_text('Восстановление намазов:', reply_markup = await client_kb.markup_tracker(user_id))
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
  await message.answer('Обучение на основе Ханафитского мазхаба.\nВыберите раздел: ', reply_markup=client_kb.markup_namaz_tutor)
# buttons in learn | (inline)
async def tutor_namaz_command(message: types.Message):
    await message.answer(other.tut_namaz_message)
async def tutor_time_command(message: types.Message):
    await message.answer(other.tut_time_message)
async def tutor_cond_command(message: types.Message):
	for x in range(0, len(other.tut_cond_message), MESS_MAX_LENGTH - 1400):
		mess_tut = other.tut_cond_message[x: x + MESS_MAX_LENGTH - 1400] 
		await message.answer(mess_tut)
async def tutor_gusl_command(message: types.Message):
    await message.answer(other.tut_gusl_message)
async def tutor_taharat_command(message: types.Message):
    await message.answer(other.tut_taharat_message)
async def tutor_forma_command(message: types.Message):
	for x in range(0, len(other.tut_forma_message), MESS_MAX_LENGTH - 57):
		mess_form = other.tut_forma_message[x: x + MESS_MAX_LENGTH - 57] 
		await message.answer(mess_form)
async def tutor_sura_command(message: types.Message):
    await message.answer(other.tut_sura_message)
async def tutor_women_command(message: types.Message):
    await message.answer(other.tut_women_message)


# Audio | 'Аудио' (Reply)
async def qoran_command(message: types.Message):
    await message.answer('Что Вам прислать? ', reply_markup=client_kb.markup_qoran)



# Books | 'Книги' (Reply)
async def names_command(message: types.Message):
	global page
	page = 1
	await message.answer('Выберите нужное имя:ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ', reply_markup= await client_kb.names_inline(page))

async def names_command_back(callback: types.CallbackQuery):
	global page
	page -= 1
	await callback.message.edit_text('Выберите нужное имя:ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ', reply_markup= await client_kb.names_inline(page))
	await callback.answer()

async def names_command_next(callback: types.CallbackQuery):
	global page
	page += 1
	await callback.message.edit_text('Выберите нужное имя:ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ', reply_markup= await client_kb.names_inline(page))
	await callback.answer()

async def names_get_photo(callback: types.CallbackQuery):
	data = callback.data[6:]
	await callback.answer()
	await callback.message.delete()
	await bot.send_photo(callback.from_user.id, names_id[data], reply_markup=await client_kb.names_photo_inline(int(data)))

async def names_all(callback: types.CallbackQuery):
	global page
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
	user_id = message.from_user.id
	await message.answer(await other.calendar_message(user_id))


# Info | 'Помощь' (Reply)
async def info_command(message: types.Message):
    await message.answer(other.info_message)


# Zikr | 'Зикр' (Reply)
async def zikr_command(message: types.Message):
	user_id = message.from_user.id
	try: 
		sqlite_bd.cur.execute('SELECT user_id FROM zikr WHERE user_id == ?', (user_id, )).fetchone()[0] == user_id
	except:
		sqlite_bd.cur.execute('INSERT INTO zikr VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL))
		sqlite_bd.base.commit()
	await message.answer('Выберите зикр: ', reply_markup=client_kb.inline_zikr_all)

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
		await callback.message.edit_text(f'Сегодня: {sqlite_bd.cur.execute(f"SELECT zikr_{data}_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute(f"SELECT zikr_{data}_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup= await client_kb.markup_zikr_lower(data))
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
	await message.answer('Выберите раздел: ', reply_markup=client_kb.markup_main)


# back button
async def back_command(message: types.Message):
    await message.answer('Выберите раздел: ', reply_markup=client_kb.markup_main)


# today time for tatarstan
async def namaz_day_command(callback : types.CallbackQuery):
	user_id = callback.from_user.id
	global current_city
	current_city = callback.data
	await callback.message.edit_text(await parcer_tatarstan.get_time(current_city, 'today'), reply_markup = await client_kb.inline_city('today', current_city, user_id))
	await callback.answer()


# tomorrow time for tatarstan
async def next_day_time_command(callback : types.CallbackQuery):
	user_id = callback.from_user.id
	global current_city
	await callback.message.edit_text(await parcer_tatarstan.get_time(current_city, 'tomorrow'), reply_markup = await client_kb.inline_city('tomorrow', current_city, user_id))
	await callback.answer()

# all days in month for tatarstan
async def month_time_command(callback : types.CallbackQuery):
	await callback.message.edit_text(f'Город: <b>{current_city}</b>\nМесяц: <b>{months[str(datetime.now().month)]}</b>\n<b>Выберите день:</b>ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ', reply_markup=await client_kb.inline_month())
	await callback.answer()
#--------------------Get new other city--------------------#
# first message
async def address_add(callback: types.CallbackQuery):
	global user_id
	user_id = callback.from_user.id
	await FSMaddress.address.set()
	await callback.message.delete()
	await callback.message.answer('Напишите название города', reply_markup=types.ReplyKeyboardRemove())
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
	await msg.edit_text(time, reply_markup=await client_kb.other_inline(user_id, address, 'today'))
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
		on_db = False
	await callback.message.edit_text(await parcer_other.get_calendar_time(address, datetime.now().day + 1, school), reply_markup=await client_kb.other_inline(user_id, address, 'tomorrow'))
	await callback.answer()

async def today_time_other(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	try:
		school = sqlite_bd.cur.execute('SELECT school FROM favorite_other WHERE user_id == ? AND address = ?', (user_id, address))
	except:
		on_db = False
	await callback.message.edit_text(await parcer_other.get_calendar_time(address, datetime.now().day, school), reply_markup=await client_kb.other_inline(user_id, address, 'today'))
	await callback.answer()

async def month_time_other(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	try:
		school = sqlite_bd.cur.execute('SELECT school FROM favorite_other WHERE user_id == ? AND address = ?', (user_id, address))
	except:
		on_db = False
	day = callback.data[11:]
	await callback.message.edit_text(await parcer_other.get_calendar_time(address, day, school), reply_markup=await client_kb.other_inline(user_id, address, 'month'))
	await callback.answer()

async def tatarstan_month(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	await callback.message.edit_text(await parcer_tatarstan.get_time(current_city,callback.data[15:]), reply_markup=await client_kb.inline_city('tomorrow', current_city, user_id))
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
	global dag_page
	dag_page = 1
	await callback.message.edit_text('<b>Выберите населенный пункт:</b>', reply_markup=await client_kb.dagestan_markup(dag_page))
	await callback.answer()
async def dagestan_menu_next(callback: types.CallbackQuery):
	global dag_page
	dag_page += 1
	await callback.message.edit_text('<b>Выберите населенный пункт:</b>', reply_markup=await client_kb.dagestan_markup(dag_page))
	await callback.answer()
async def dagestan_menu_back(callback: types.CallbackQuery):
	global dag_page
	dag_page -= 1
	await callback.message.edit_text('<b>Выберите населенный пункт:</b>', reply_markup=await client_kb.dagestan_markup(dag_page))
	await callback.answer()

async def dagestan_today_time(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global dag_city
	dag_city = callback.data[9:]
	await callback.message.edit_text(await parcer_dagestan.get_day_time(dag_city), reply_markup= await client_kb.dag_city(dag_city, 'today',user_id))
	await callback.answer()

async def dagestan_tomorrow_time(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global dag_city
	await callback.message.edit_text(await parcer_dagestan.get_tomorrow_time(dag_city), reply_markup= await client_kb.dag_city(dag_city, 'tomorrow',user_id))
	await callback.answer()

async def dagestan_month(callback: types.CallbackQuery):
	global dag_city
	await callback.message.edit_text(f'Город: <b>{dag_city}</b>\nМесяц: <b>{months[str(datetime.now().month)]}</b>\n<b>Выберите день:</b>ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ',reply_markup=await client_kb.dagestan_month())
	await callback.answer()

async def dagestan_month_time(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global dag_city
	await callback.message.edit_text(await parcer_dagestan.get_month_time(dag_city, callback.data[9:]), reply_markup= await client_kb.dag_city(dag_city, 'month', user_id))
	await callback.answer()

async def dagestan_favorite_add(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global daz_city
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
	global kaz_page
	kaz_page = 1
	await callback.message.edit_text('<b>Выберите населенный пункт:</b>', reply_markup=await client_kb.kazakhstan_markup(kaz_page))
	await callback.answer()
async def kazakhstan_menu_next(callback: types.CallbackQuery):
	global kaz_page
	kaz_page += 1
	await callback.message.edit_text('<b>Выберите населенный пункт:</b>', reply_markup=await client_kb.kazakhstan_markup(kaz_page))
	await callback.answer()
async def kazakhstan_menu_back(callback: types.CallbackQuery):
	global kaz_page
	kaz_page -= 1
	await callback.message.edit_text('<b>Выберите населенный пункт:</b>', reply_markup=await client_kb.kazakhstan_markup(kaz_page))
	await callback.answer()

async def kazakhstan_today_time(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global kaz_city
	kaz_city = callback.data[9:]
	await callback.message.edit_text(await parcer_kazakhstan.get_day_time(kaz_city), reply_markup=await client_kb.kaz_city(kaz_city, 'today', user_id))
	await callback.answer()

async def kazakhstan_tomorrow_time(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global kaz_city
	await callback.message.edit_text(await parcer_kazakhstan.get_tomorrow_time(kaz_city), reply_markup=await client_kb.kaz_city(kaz_city, 'tomorrow', user_id))
	await callback.answer()

async def kazakhstan_month(callback: types.CallbackQuery):
	global kaz_city
	await callback.message.edit_text(f'Город: <b>{kaz_city}</b>\nМесяц: <b>{months[str(datetime.now().month)]}</b>\n<b>Выберите день:</b>ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ',reply_markup=await client_kb.kazakhstan_month())
	await callback.answer()

async def kazakhstan_month_time(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global kaz_city
	await callback.message.edit_text(await parcer_kazakhstan.get_month_time(kaz_city, callback.data[9:]), reply_markup= await client_kb.kaz_city(kaz_city, 'month', user_id))
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

async def dua_command(message: types.Message):
	await message.answer('<b>Дуа какого пророка (мир Им) прислать?</b>', reply_markup=client_kb.markup_dua)

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
	global page
	page = 1
	user_id = callback.from_user.id
	await callback.message.edit_text('Выберите хадис:', reply_markup= await client_kb.hadis_favorite(user_id, page))
	await callback.answer()

async def hadis_saved_next(callback : types.CallbackQuery):
	global page
	page += 1
	user_id = callback.from_user.id
	await callback.message.edit_text('Выберите хадис:', reply_markup= await client_kb.hadis_favorite(user_id, page))
	await callback.answer()

async def hadis_saved_back(callback : types.CallbackQuery):
	global page
	page -= 1
	user_id = callback.from_user.id
	await callback.message.edit_text('Выберите хадис:', reply_markup= await client_kb.hadis_favorite(user_id, page))
	await callback.answer()

async def hadis_get_saved(callback: types.CallbackQuery):
	data = callback.data[12:]
	user_id = callback.from_user.id
	await callback.message.edit_text(await parcer_hadis.get_hadis(int(data)), reply_markup=await client_kb.markup_hadis_random(int(data), user_id))
	await callback.answer()





async def photo_file_id(message: types.Message):
    await message.answer(message.photo[2].file_id)

async def document_file_id(message: types.Message):
    await message.answer(message.document.file_id)

async def audio_file_id(message: types.Message):
    await message.answer(message.audio.file_id)

# dispatcher
def register_handlers_client(dp : Dispatcher):
	dp.register_message_handler(start_command, commands=['start'])
	dp.register_message_handler(favorite_command, lambda message: message.text == "🕦 Время намаза")
	dp.register_message_handler(tracker_command, lambda message: message.text == "📈 Трекер")
	dp.register_message_handler(tracker_reset, commands=['reset'])
	dp.register_callback_query_handler(tracker_reset_cancel, text = 'tracker_cancel')
	dp.register_callback_query_handler(tracker_reset_yes, text = 'tracker_reset')
	dp.register_message_handler(tutor_command, lambda message: message.text == "🕌 Обучение")
	dp.register_message_handler(dua_command, lambda message: message.text == "🤲 Дуа")
	dp.register_message_handler(hadis_command, lambda message: message.text == "📕 Хадисы")
	dp.register_message_handler(tutor_namaz_command, lambda message: message.text == "❓\n Что такое намаз")
	dp.register_message_handler(tutor_time_command, lambda message: message.text == "🕦\n Время намазов")
	dp.register_message_handler(tutor_cond_command, lambda message: message.text == "❗\n Условия намаза")
	dp.register_message_handler(tutor_gusl_command, lambda message: message.text == "🚿\n Гусль")
	dp.register_message_handler(tutor_taharat_command, lambda message: message.text == "💧\n Тахарат")	
	dp.register_message_handler(tutor_forma_command, lambda message: message.text == "🧎\n Форма совершения намаза")	
	dp.register_message_handler(tutor_sura_command, lambda message: message.text == "📃\n Суры и дуа намаза")
	dp.register_message_handler(tutor_women_command, lambda message: message.text == "🧕\n Женский намаз")					
	dp.register_message_handler(qoran_command, lambda message: message.text == "📖 Коран")
	dp.register_message_handler(names_command, lambda message: message.text == "❾❾ Имён")
	dp.register_message_handler(calendar_command, lambda message: message.text == "📅 Календарь")
	dp.register_message_handler(info_command, lambda message: message.text == "❗ Помощь")
	dp.register_message_handler(zikr_command, lambda message: message.text == "📿 Зикр")
	dp.register_message_handler(help_command, commands=['help'])
	dp.register_message_handler(back_command, lambda message: message.text == "⏪ Назад")
	dp.register_callback_query_handler(time_command, text = 'add_city')
	dp.register_callback_query_handler(namaz_day_command, text = parcer_tatarstan.all_cities)
	dp.register_callback_query_handler(next_day_time_command, text = 'tomorrow_time')
	dp.register_callback_query_handler(tatarstan_command, text = 'tatarstan')
	dp.register_callback_query_handler(tatarstan_next, text = 'next_tat')
	dp.register_callback_query_handler(tatarstan_back, text = 'back_tat')
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
	dp.register_callback_query_handler(kazakhstan_menu_next, text = 'next_kaz')
	dp.register_callback_query_handler(kazakhstan_menu_back, text = 'back_kaz')
	dp.register_callback_query_handler(kazakhstan_today_time, text_startswith = 'kaz_city_')
	dp.register_callback_query_handler(kazakhstan_tomorrow_time, text = 'kaz_tomorrow')
	dp.register_callback_query_handler(kazakhstan_month, text = 'kaz_month')
	dp.register_callback_query_handler(kazakhstan_month_time, text_startswith = 'kaz_days_')
	dp.register_callback_query_handler(kazakhstan_favorite_add, text='kaz_add')
	dp.register_callback_query_handler(kazakhstan_favorite_delete, text='kaz_delete')
	dp.register_callback_query_handler(dagestan_menu_next, text = 'next_dag')
	dp.register_callback_query_handler(dagestan_menu_back, text = 'back_dag')
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
	dp.register_message_handler(tracker_vitr_get, state = FSMtracker.vitr)
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
	dp.register_callback_query_handler(hadis_saved_back, text = 'back_hadis')
	dp.register_callback_query_handler(hadis_saved_next, text = 'next_hadis')
	dp.register_callback_query_handler(names_command_back, text = 'back_names')
	dp.register_callback_query_handler(names_command_next, text = 'next_names')
	dp.register_callback_query_handler(names_get_photo, text_startswith = 'names_')
	dp.register_callback_query_handler(names_all, text = 'all_names')
	dp.register_callback_query_handler(names_next, text_startswith = 'next_photo_')
	dp.register_callback_query_handler(names_back, text_startswith = 'back_photo_')

	dp.register_message_handler(photo_file_id, content_types=["photo"])
	dp.register_message_handler(audio_file_id, content_types=["audio"])
	dp.register_message_handler(document_file_id, content_types=["document"])