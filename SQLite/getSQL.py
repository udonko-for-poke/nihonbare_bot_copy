import sqlite3
import os

def makestate(list_, lv):
    if (list_ == None or len(list_) != 6):
        return ''
    txt = ''
    if (lv >= 0):
        if (lv == 0):
            lv = 50
        import math
        rank = [[31,252,1.1],[31,252,1.0],[31,0,1.0],[0,0,0.9]]
        for j in range(4):
            flg = 0
            for i in list_:
                if (flg == 0):
                    st = math.floor((i*2+rank[j][0]+rank[j][1]/4)*lv/100)+lv+10
                    flg = 1
                else:
                    st = math.floor((math.floor((i*2+rank[j][0]+rank[j][1]/4)*lv/100)+5)*rank[j][2])
                txt += str(st).rjust(3)+'-'
            txt = txt[:-1]
            txt += '\n'
    else:
        for i in list_:
            txt += str(i)+'-'
    return txt[:-1]

async def getstatus(type_, arg, isreal):
    fpath = os.path.dirname(__file__)+'/sqldata/pokemon.sqlite3'
    poke_content = sqlite3.connect(fpath)
    c = poke_content.cursor()
    flg = 0
    txt = ''
    if (type_ == 'name'):
        txt = 'SELECT H,A,B,C,D,S FROM pokemon WHERE name = ? '
        flg = 1
    if (flg):
        data = (arg,)
        c.execute(txt, data)
        print(txt)
        print(data)
        list1 = c.fetchone()
        poke_content.commit()
        poke_content.close()
        print(list1)
        return (list1==None or len(list1)!=6), makestate(list1, isreal)
    poke_content.commit()
    poke_content.close()
    return (-1), ''
    
async def sqlrequest(txt, tpl):
    fpath = os.path.dirname(__file__)+'/sqldata/pokemon.sqlite3'
    poke_content = sqlite3.connect(fpath)
    c = poke_content.cursor()
    c.execute(txt, tpl)
    list1 = c.fetchone()
    if (list1 == None):
        return '', -1
    cnt = 0
    txt_2 = ''
    for element in list1:
        txt_2 += str(element) + ','
    cnt += len(txt_2[:-1])
    for hit in c.fetchall():
        txt_2 += '\n'
        for element in hit:
            txt_2 += str(element) + ','
            cnt += len(str(element))
        txt_2 = txt_2[:-1]
    poke_content.commit()
    poke_content.close()
    return txt_2, cnt
