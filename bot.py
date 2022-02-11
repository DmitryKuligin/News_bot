from config import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if check_user(message.from_user.username):
        text = f'Hello, {message.from_user.username}!'
        bot.send_message(message.chat.id, text, reply_markup=menu_markup())
    else:
        text = f'Hello, {message.from_user.username}!\n\nAt first print your age, to filter news.'
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, get_age)


def get_age(message):
    age = message.text
    if age.isdigit():
        sphere = []
        text = "Perfect!\n\nNow let's choose sphere of news you want to know"
        bot.send_message(message.chat.id, text, reply_markup=filter_markup())
        bot.register_next_step_handler(message, creating_profile, age, sphere)
    else:
        bot.send_message(message.chat.id, 'Try to print your age, but not word!')
        bot.register_next_step_handler(message, get_age)


def creating_profile(message, age, sphere):
    if message.text == 'Apple' or message.text == 'Tesla' or message.text == 'Top Business Headlines US' or message.text == 'Top Business Headlines TC' or message.text == 'WallStreet News':
        if message.text in sphere:
            sphere.remove(message.text)
            bot.send_message(message.chat.id, f'Category *{message.text}* was deleted. You can choose more category or click *Create Profile*',
                             reply_markup=filter_markup(), parse_mode="Markdown")
            bot.register_next_step_handler(message, creating_profile, age, sphere)
        else:
            sphere.append(message.text)
            bot.send_message(message.chat.id, f'Category *{message.text}* was added. You can choose more category or click *Create Profile*',
                             reply_markup=filter_markup(), parse_mode="Markdown")
            bot.register_next_step_handler(message, creating_profile, age, sphere)
    elif message.text == 'Create Profile':
        sphere_bit = ''
        for SPHERE in SPHERES:
            if SPHERE in sphere:
                sphere_bit += '1'
            else:
                sphere_bit += '0'
        
        create_user(message.from_user.username, age, sphere_bit)

        text = 'Your Profile has been successfully created!'
        bot.send_message(message.chat.id, text, reply_markup=menu_markup())




@bot.message_handler(content_types=["text"])
def send_text(message):
    if message.text == 'Show Actual News':
        today = datetime.today()

        TeslaRequest = requests.get(f'https://newsapi.org/v2/everything?q=tesla&from={str(today)[:10]}&sortBy=publishedAt&apiKey={API_TOKEN}').json()

        AppleRequest = requests.get(f'https://newsapi.org/v2/everything?q=apple&from={str(today)[:10]}&sortBy=publishedAt&apiKey={API_TOKEN}').json()

        TBHRequestUS = requests.get(f'https://newsapi.org/v2/top-headlines?country=us&category=business&from={str(today)[:10]}&sortBy=publishedAt&apiKey={API_TOKEN}').json()

        TBHRequestTC = requests.get(f'https://newsapi.org/v2/top-headlines?sources=techcrunch&from={str(today)[:10]}&sortBy=publishedAt&apiKey={API_TOKEN}').json()

        WSJRequest = requests.get(f'https://newsapi.org/v2/everything?domains=wsj.com&from={str(today)[:10]}&sortBy=publishedAt&apiKey={API_TOKEN}').json()

        list = []
        num = 0
        sphere = get_sphere(message.from_user.username)
        for i in range(len(sphere)):
            if sphere[i] == '1':
                if i == 0:
                    list.append(AppleRequest['articles'])
                    num += 1
                if i == 1:
                    list.append(TeslaRequest['articles'])
                    num += 1
                if i == 2:
                    list.append(TBHRequestUS['articles'])
                    num += 1
                if i == 3:
                    list.append(TBHRequestTC['articles'])
                    num += 1
                if i == 4:
                    list.append(WSJRequest['articles'])
                    num += 1
        
        number1 = randint(0, num - 1)
        number2 = randint(0, len(list[number1]) - 1)
        item = list[number1][number2]
        text = f'*{item["title"]}*\n\n{str(item["content"])[:len(item["content"])-12]}\n\n[Tap to read more]({item["url"]})'
        bot.send_message(message.chat.id, text, reply_markup=menu_markup(), parse_mode="Markdown")
            
            



@bot.callback_query_handler(func=lambda message: True)
def filter_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Apple')
    btn2 = types.KeyboardButton('Tesla')
    btn3 = types.KeyboardButton('Top Business Headlines US')
    btn4 = types.KeyboardButton('Top Business Headlines TC')
    btn5 = types.KeyboardButton('WallStreet News')
    btn7 = types.KeyboardButton('Create Profile')
    markup.add(btn1, btn2, btn5).add(btn4, btn3).add(btn7)
    return markup

def menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Show Actual News')
    markup.add(btn1)
    return markup


bot.polling(none_stop=True)