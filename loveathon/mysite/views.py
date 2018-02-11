from django.shortcuts import render
# from django.shortcuts import redirect
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import nltk
import random

from django.http import HttpResponse
# Create your views here.


def send_email(user_email):
    now = datetime.datetime.now()
    month = now.month
    day = now.day

    if (month == 2 and (day <= 14)):
        day_until = str(14 - day)
    else:
        day_until = ("Many")

    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'LoveathonCupid@gmail.com'
    EMAIL_HOST_PASSWORD = 'sfuhacks2018'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("LoveathonCupid@gmail.com", "sfuhacks2018")

    msg = MIMEMultipart()
    from_mail = ("loveathoncupid@gmail.com")

    msg['From'] = from_mail
    msg['To'] = user_email
    msg['Subject'] = (day_until + " Days Until Valentine's!")

    body = (body_sent)
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()

    #response_code, response_string = server.verify(user_email)
    # print(response_code, response_string)
    # if response_code is 200:
    #     return False
    # else:
    #     server.sendmail(from_mail, user_email, text)
    #     return True
    if "@" in user_email:
        server.sendmail(from_mail, user_email, text)
        return True
    else:
        return False

# def index(request):
#     return HttpResponse("<h1>Hello there! Hi</h1>")


def sent_gen():
    def generate(word):
        sentence = []
        sentence.append(word)

        for i in range(random.randint(8,16)):
            #print(word)
            if word in cfd:
                word = random.choice(list(cfd[word].keys()))
                sentence.append(word.strip())
            else:
                break
        return sentence

    def connect(sentence, connectors):

        for i in range(len(sentence)):
            remove = random.random()
            if len(sentence[i]) == (3 or 2) and (remove<0.3):                    #30% chance of replacing with a standard Shakespeare connector
                sentence[i]=random.choice(connectors)

        return sentence

    def format(sentence):

        print(sentence)
        run = True
        i = 1
        if (ord(sentence[0][0]) in list(range(34,65))):
            del sentence[0]
        if sentence[0].islower()==True:                                           #Capitalize the first word
            sentence[0] = sentence[0].capitalize()

        while run:
            try:
                #print(sentence[i][0])
                if (ord(sentence[i][0]) in list(range(34,46))) or\
                    (ord(sentence[i][0]) in list(range(47,65))) or\
                    (ord(sentence[i][0]) in list(range(91,97))):
                    del sentence[i]
                    continue

                if sentence[i-1] == ("." or "?" or "!"):
                    sentence[i] = sentence[i].capitalize()
                else:
                    if len(sentence[i])<5:
                        sentence[i] = sentence[i].lower()                            #If the word length is less than 4(probably not a name), set to lowercase

                if i==len(sentence)-1:
                    run = False
                i+=1
            except:
                break

        if ord(sentence[len(sentence)-1][0]) != (46 or 63):                      #if the last element is not '.' or '!' append '.'
            sentence.append(".")

        return sentence


    #------------------------------------------------------------------------------
    nltk.corpus.gutenberg.fileids()

    text = nltk.corpus.gutenberg.words('shakespeare-hamlet.txt')

    bigrams = nltk.bigrams(text)                                                 #builds a list of consecutive word pairs
    cfd = nltk.ConditionalFreqDist(bigrams)                                      #tabulates/counts each bigram

    word = random.choice(text)
    connectors = ['thou','thee','thou','thine','thy']                            #Hardcoded words/phrases

    love_phrases = ["Thou art more lovely and more temperate.",
                    "There’s beggary in love that can be reckoned.",
                    "Love sought is good","My heart fly to your service.",
                    "One half of me is yours.",
                    "Who ever loved that loved not at first sight?.",
                    "Men’s vows are women’s traitors.",
                    "You have witchcraft in your lips."]

    sentence = generate(word)
    sentence = connect(sentence,connectors)
    sentence = format(sentence)

    sentpt0 = "Here is a random piece of Shakespeare:"
    sentpt1 = ' '.join(sentence)
    sentpt2 = random.choice(love_phrases)
    sentpt3 = "Happy Valentines day."

    return sentpt0 + "\n\n" + sentpt1 + "\n" + sentpt2 + "\n\n" + sentpt3 + "\n"


body_sent = sent_gen()

def index(request):
    return render(request, 'mysite/home.html', {})


def submit(request):
    email = request.POST["email"]

    if send_email(email):
        return render(request, 'mysite/home.html', {})
    else:
        return render(request, 'mysite/errorpage.html', {})

#
# def reset(request):
#     return sent_gen()

