from random import choice, randint

word_list = ['fireball', 'lightning', 'invisibility', 'burn', 'skeleton', 'north', 'south', 'east', 'west', '1', '2', '3', '4', '5']

def get_lexicon(word_list=word_list):
    vocals = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    digits = '0123456789'
    p_vocal = randint(4, 9)
    lexicon = {}
    for i in word_list:
        word = get_word(i, vocals, consonants, digits, p_vocal, lexicon)
        lexicon[word] = i 

    return lexicon

def get_word(meaning, vocals, consonants, digits, p_vocal, lexicon):
    if meaning in ['north', 'south', 'east', 'west']:
        length = 1
    elif meaning in digits:
        length = randint(1, 3)
    else:
        length = randint(2, 7)

    word = ''

    for i in range(length):
        if randint(1, 10) < p_vocal:
            word += choice(vocals)
        else:
            word += choice(consonants)

    if word in lexicon:
        word = get_word(meaning, vocals, consonants, digits, p_vocal, lexicon)

    return word

def translate(magic_verse, lexicon):
    return [lexicon[i] if i in lexicon else i for i in magic_verse]
