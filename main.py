import sys
from collections import Counter
from Line import *
import matplotlib.pyplot as plt


"""
OPENING FILES
"""
chatfile = "chat.txt"
try:
    file = open(chatfile, "r", encoding='utf-8')
    lines = file.readlines()
except FileNotFoundError:
    print(chatfile + " not found, can't find the chat.")
    sys.exit()

stopfile = "stopwords.txt"
try:
    stops = open(stopfile, "r", encoding='utf-8')
    stop_words = [x.strip() for x in stops.readlines()]
except FileNotFoundError:
    print(stopfile + " not found")
    stop_words = []


"""
DICT SETUP
"""
chat_counter = {
    'chat_count': 0,
    'deleted_chat_count': 0,
    'event_count': 0,
    'senders': [],
    'timestamps': [],
    'words': [],
    'domains': [],
    'emojis': [],
    'fav_emoji': [],
    'fav_word': []
}

previous_line = None
for line in lines:
    chatline = Line(line=line, previous_line=previous_line)
    previous_line = chatline

    # Counter
    if chatline.line_type == 'Chat':
        chat_counter['chat_count'] += 1

    if chatline.line_type == 'Event':
        chat_counter['event_count'] += 1

    if chatline.is_deleted_chat:
        chat_counter['deleted_chat_count'] += 1

    if chatline.sender is not None:
        chat_counter['senders'].append(chatline.sender)
        for i in chatline.emojis:
            chat_counter['fav_emoji'].append((chatline.sender, i))

        for i in chatline.words:
            chat_counter['fav_word'].append((chatline.sender, i))

    if chatline.timestamp:
        chat_counter['timestamps'].append(chatline.timestamp)

    if len(chatline.words) > 0:
        chat_counter['words'].extend(chatline.words)

    if len(chatline.emojis) > 0:
        chat_counter['emojis'].extend(chatline.emojis)

    if len(chatline.domains) > 0:
        chat_counter['domains'].extend(chatline.domains)



"""
REDUCE AND ORDER DATA
"""
def reduce_and_sort(data):
    return sorted(
        dict(
            zip(
                Counter(data).keys(),
                Counter(data).values()
            )
        ).items(),
        key=lambda x: x[1],
        reverse=True
    )

def reduce_and_filter_words(list_of_words):
    val = [w.lower() for w in list_of_words if
           (len(w) > 1) and (w.isalnum()) and (not w.isnumeric()) and (w.lower() not in stop_words)]
    return val

def filter_single_word(w):
    return (len(w) > 1) and (w.isalnum()) and (not w.isnumeric()) and (w.lower() not in stop_words)

def reduce_fav_item(data):
    exist = []
    arr = []
    for i in data:
        if i[1] > 0 and not i[0][0] in exist:
            exist.append(i[0][0])
            arr.append(i)
    return arr


chat_counter['senders'] = reduce_and_sort(chat_counter['senders'])
chat_counter['words'] = reduce_and_sort(reduce_and_filter_words(chat_counter['words']))
chat_counter['domains'] = reduce_and_sort(chat_counter['domains'])
chat_counter['emojis'] = reduce_and_sort(chat_counter['emojis'])
chat_counter['timestamps'] = reduce_and_sort([(x.strftime('%A'), x.strftime('%H')) for x in chat_counter['timestamps']])
chat_counter['fav_emoji'] = reduce_fav_item(reduce_and_sort(chat_counter['fav_emoji']))
chat_counter['fav_word'] = reduce_fav_item(reduce_and_sort([x for x in chat_counter['fav_word'] if filter_single_word(x[1])]))



"""
VISUALIZE
"""

# Hist "Messages per Day of the week"
messages_per_day_of_the_week = True
if messages_per_day_of_the_week:
    per_day_mess = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0, 'Sunday': 0}
    for day_hour, n in chat_counter['timestamps']:
        giorno, _ = day_hour
        try:
            per_day_mess[giorno] += n
        except KeyError:
            pass

    week_days = list(per_day_mess.keys())
    messages = list(per_day_mess.values())

    plt.bar(week_days, messages, color='skyblue', width=0.6)
    plt.xlabel('Day of the week')
    plt.ylabel('Number of messages')
    plt.title('Messages per Day of the week')
    plt.tight_layout()
    plt.show()



# Hist "Top emojis"
top_emojis = True
show = 5 # show top x emoji
if top_emojis:
    emojis = []
    nums = []
    flag = 0

    for em, count in chat_counter['emojis']:
        emojis.append(em)
        nums.append(count)
        flag += 1
        if flag > show:
            break

    plt.rcParams['font.family'] = ['Segoe UI Emoji']
    plt.bar(emojis, nums, color='skyblue', width=0.6)
    plt.xlabel('Emojis')
    plt.ylabel('Count')
    plt.title('Top emojis')
    plt.tight_layout()
    plt.show()


# Hist top words
top_words = True
show = 5
if top_words:
    words = [chat_counter['words'][k][0] for k in range(show)]
    values = [chat_counter['words'][k][1] for k in range(show)]

    plt.bar(words, values, color='skyblue', width=0.6)
    plt.xlabel('Words')
    plt.ylabel('Repetitions')
    plt.title('Most repeted words')
    plt.tight_layout()
    plt.show()


# Pie Messages
messages_percent = True
if messages_percent:
    names = [x for x,y in chat_counter['senders']]
    messages = [y for x,y in chat_counter['senders']]
    s = sum(messages)
    percentages = [(x/s)*100 for x in messages]

    plt.title('Messages Percentage')
    plt.pie(percentages, labels=names, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()






