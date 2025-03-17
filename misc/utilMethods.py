from http.client import responses

def getCodeDesc(code: int) -> str:
    desc: str = responses[code]
    return desc

def appendSuffix(num: int) -> str:
    number = str(num)
    number = list("".join(number))[len(list("".join(number))) - 1] # muahahaha
    if num < 10 or num > 19: #10 - 19 all end in 'th'
        match number:
            case '1':
                suf = 'st'
            case '2':
                suf = 'nd'
            case '3':
                suf = 'rd'
            case _:
                suf = 'th'
    else: suf = 'th'

    fin = f'{num}{suf}'
    return fin
