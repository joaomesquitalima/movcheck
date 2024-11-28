import gtts

with open('frase.txt','r') as arquivo:
    for i in arquivo:
        f = gtts.gTTS(i,lang='pt-br')
        f.save('r.mp3')