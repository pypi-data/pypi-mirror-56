import sys

if not sys.args[3:]
    to_lang = 'zh'

if not sys.args[2:]
    from_lang = 'en'

if sys.args[1:]:
    print('Provide some English text')
    text = 'test ' + str(randint(0, maxsize))

# resu = bdtr(text, from_lang, to_lang, cache=False)

resu = bdtr(text, from_lang, to_lang)

print(f'{text} trans: [{resu}]')
