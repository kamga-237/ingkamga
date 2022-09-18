def myddb(mots):
    mots = mots
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    cles = "fac"
    final = ""
    contenub = ""
    contenum = ""
    ac = ""
    voir = 0
    acc = ""
    voirr = 0
    lc = len(cles)
    lm = len(mots)
    es = ""
    d = ""
    s = ""
    ss = ""
    dd = ""
    i = 0
    j = 0
    popol = 1
    popol2 = ""
    popol3 = ""
    # print(mots)
    cii = 0
    cnc = ""
    lc = len(cles)
    cvoir = 0
    cac = ""
    cpopol = 0
    cpopol2 = ""
    while cii < lc:
        if cles[cii] == 'a':
            cac = '1'
            cvoir = 1
        elif cles[cii] == 'b':
            cac = '2'
            cvoir = 2
        elif cles[cii] == 'c':
            cac = '3'
            cvoir = 3
        elif cles[cii] == 'd':
            cac = '4'
            cvoir = 4
        elif cles[cii] == 'e':
            cac = '5'
            cvoir = 5
        elif cles[cii] == 'f':
            cac = '6'
            cvoir = 6
        elif cles[cii] == 'g':
            cac = '7'
            cvoir = 7
        elif cles[cii] == 'h':
            cac = '8'
            cvoir = 8
        elif cles[cii] == 'i':
            cac = '9'
            cvoir = 9
        elif cles[cii] == 'j':
            cac = '10'
            cvoir = 10
        elif cles[cii] == 'k':
            cac = '11'
            cvoir = 11
        elif cles[cii] == 'l':
            cac = '12'
            cvoir = 12
        elif cles[cii] == 'm':
            cac = '13'
            cvoir = 13
        elif cles[cii] == 'n':
            cac = '14'
            cvoir = 14
        elif cles[cii] == 'o':
            cac = '15'
            cvoir = 15
        elif cles[cii] == 'p':
            cac = '16'
            cvoir = 16
        elif cles[cii] == 'q':
            cac = '17'
            cvoir = 17
        elif cles[cii] == 'r':
            cac = '18'
            cvoir = 18
        elif cles[cii] == 's':
            cac = '19'
            cvoir = 19
        elif cles[cii] == 't':
            cac = '20'
            cvoir = 20
        elif cles[cii] == 'u':
            cac = '21'
            cvoir = 21
        elif cles[cii] == 'v':
            cac = '22'
            cvoir = 22
        elif cles[cii] == 'w':
            cac = '23'
            cvoir = 23
        elif cles[cii] == 'x':
            cac = '24'
            cvoir = 24
        elif cles[cii] == 'y':
            cac = '25'
            cvoir = 25
        elif cles[cii] == 'z':
            cac = '26'
            cvoir = 26
        cpopol = 26 - cvoir
        if cpopol == 1:
            cpopol2 = "a"
        elif cpopol == 2:
            cpopol2 = "b"
        elif cpopol == 3:
            cpopol2 = "c"
        elif cpopol == 4:
            cpopol2 = "d"
        elif cpopol == 5:
            cpopol2 = "e"
        elif cpopol == 6:
            cpopol2 = "f"
        elif cpopol == 7:
            cpopol2 = "g"
        elif cpopol == 8:
            cpopol2 = "h"
        elif cpopol == 9:
            cpopol2 = "i"
        elif cpopol == 10:
            cpopol2 = "j"
        elif cpopol == 11:
            cpopol2 = "k"
        elif cpopol == 12:
            cpopol2 = "l"
        elif cpopol == 13:
            cpopol2 = "m"
        elif cpopol == 14:
            cpopol2 = "n"
        elif cpopol == 15:
            cpopol2 = "o"
        elif cpopol == 16:
            cpopol2 = "p"
        elif cpopol == 17:
            cpopol2 = "q"
        elif cpopol == 18:
            cpopol2 = "r"
        elif cpopol == 19:
            cpopol2 = "s"
        elif cpopol == 20:
            cpopol2 = "t"
        elif cpopol == 21:
            cpopol2 = "u"
        elif cpopol == 22:
            cpopol2 = "v"
        elif cpopol == 23:
            cpopol2 = "w"
        elif cpopol == 24:
            cpopol2 = "x"
        elif cpopol == 25:
            cpopol2 = "y"
        elif cpopol == 26:
            cpopol2 = "z"
        elif cpopol == 0:
            cpopol2 == "z"
        cnc += cpopol2
        cii += 1
    cles = cnc
    for mot in mots:
        if i == lc:
            i = 0
            if mot in alpha:
                mot = cles[i]
            else:
                mot = mot
                i -= 1
        else:
            i = i
            if mot in alpha:
                mot = cles[i]
            else:
                mot = mot
                i -= 1
        final += mot
        i += 1
    print(final)
    while j < lm:
        voir = 0
        voirr = 0
        if mots[j] == 'a':
            ac += '1'
            voir += 1
        elif mots[j] == 'b':
            ac += '2'
            voir += 2
        elif mots[j] == 'c':
            ac += '3'
            voir += 3
        elif mots[j] == 'd':
            ac += '4'
            voir += 4
        elif mots[j] == 'e':
            ac += '5'
            voir += 5
        elif mots[j] == 'f':
            ac += '6'
            voir += 6
        elif mots[j] == 'g':
            ac += '7'
            voir += 7
        elif mots[j] == 'h':
            ac += '8'
            voir += 8
        elif mots[j] == 'i':
            ac += '9'
            voir += 9
        elif mots[j] == 'j':
            ac += '10'
            voir += 10
        elif mots[j] == 'k':
            ac += '11'
            voir += 11
        elif mots[j] == 'l':
            ac += '12'
            voir += 12
        elif mots[j] == 'm':
            ac += '13'
            voir += 13
        elif mots[j] == 'n':
            ac += '14'
            voir += 14
        elif mots[j] == 'o':
            ac += '15'
            voir += 15
        elif mots[j] == 'p':
            ac += '16'
            voir += 16
        elif mots[j] == 'q':
            ac += '17'
            voir += 17
        elif mots[j] == 'r':
            ac += '18'
            voir += 18
        elif mots[j] == 's':
            ac += '19'
            voir += 19
        elif mots[j] == 't':
            ac += '20'
            voir += 20
        elif mots[j] == 'u':
            ac += '21'
            voir += 21
        elif mots[j] == 'v':
            ac += '22'
            voir += 22
        elif mots[j] == 'w':
            ac += '23'
            voir += 23
        elif mots[j] == 'x':
            ac += '24'
            voir += 24
        elif mots[j] == 'y':
            ac += '25'
            voir += 25
        elif mots[j] == 'z':
            ac += '26'
            voir += 26
        else:
            ac += mots[j]
        if final[j] == 'a':
            acc += '1'
            voirr += 1
        elif final[j] == 'b':
            acc += '2'
            voirr += 2
        elif final[j] == 'c':
            acc += '3'
            voirr += 3
        elif final[j] == 'd':
            acc += '4'
            voirr += 4
        elif final[j] == 'e':
            acc += '5'
            voirr += 5
        elif final[j] == 'f':
            acc += '6'
            voirr += 6
        elif final[j] == 'g':
            acc += '7'
            voirr += 7
        elif final[j] == 'h':
            acc += '8'
            voirr += 8
        elif final[j] == 'i':
            acc += '9'
            voirr += 9
        elif final[j] == 'j':
            acc += '10'
            voirr += 10
        elif final[j] == 'k':
            acc += '11'
            voirr += 11
        elif final[j] == 'l':
            acc += '12'
            voirr += 12
        elif final[j] == 'm':
            acc += '13'
            voirr += 13
        elif final[j] == 'n':
            acc += '14'
            voirr += 14
        elif final[j] == 'o':
            acc += '15'
            voirr += 15
        elif final[j] == 'p':
            acc += '16'
            voirr += 16
        elif final[j] == 'q':
            acc += '17'
            voirr += 17
        elif final[j] == 'r':
            acc += '18'
            voirr += 18
        elif final[j] == 's':
            acc += '19'
            voirr += 19
        elif final[j] == 't':
            acc += '20'
            voirr += 20
        elif final[j] == 'u':
            acc += '21'
            voirr += 21
        elif final[j] == 'v':
            acc += '22'
            voirr += 22
        elif final[j] == 'w':
            acc += '23'
            voirr += 23
        elif final[j] == 'x':
            acc += '24'
            voirr += 24
        elif final[j] == 'y':
            acc += '25'
            voirr += 25
        elif final[j] == 'z':
            acc += '26'
            voirr += 26
        else:
            acc += final[j]
        d = mots[j]
        s = s + ac + es
        dd = final[j]
        ss = ss + acc + es
        if mots[j] in alpha:
            popol = voir + voirr
            if popol > 26:
                popol = popol - 26
            else:
                popol = popol + 0
            # print(voirr)
            if popol == 1:
                popol2 = "a"
            elif popol == 2:
                popol2 = "b"
            elif popol == 3:
                popol2 = "c"
            elif popol == 4:
                popol2 = "d"
            elif popol == 5:
                popol2 = "e"
            elif popol == 6:
                popol2 = "f"
            elif popol == 7:
                popol2 = "g"
            elif popol == 8:
                popol2 = "h"
            elif popol == 9:
                popol2 = "i"
            elif popol == 10:
                popol2 = "j"
            elif popol == 11:
                popol2 = "k"
            elif popol == 12:
                popol2 = "l"
            elif popol == 13:
                popol2 = "m"
            elif popol == 14:
                popol2 = "n"
            elif popol == 15:
                popol2 = "o"
            elif popol == 16:
                popol2 = "p"
            elif popol == 17:
                popol2 = "q"
            elif popol == 18:
                popol2 = "r"
            elif popol == 19:
                popol2 = "s"
            elif popol == 20:
                popol2 = "t"
            elif popol == 21:
                popol2 = "u"
            elif popol == 22:
                popol2 = "v"
            elif popol == 23:
                popol2 = "w"
            elif popol == 24:
                popol2 = "x"
            elif popol == 25:
                popol2 = "y"
            elif popol == 26:
                popol2 = "z"
            popol3 += popol2
        else:
            popol3 += mots[j]
        j = j + 1
    return (popol3)
#utilisatin de la fonction
#dd = "hpqppxxurauoknrteh"
#kk = myddb(dd)
#print(kk)