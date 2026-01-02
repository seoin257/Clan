def convert_py_to_c(pycode):
    entirelis = pycode.split('\n')
    N = len(entirelis)

    # <함수 정의>
    #print
    def printf(gap, printipe, printlis):
        A='"'
        B=''
        C=' '*gap*4
        for i in range(len(printipe)):
            if i!=len(printipe)-1:
                if printipe[i]==1:
                    A+='%d '
                else:
                    A+='%s '
            else:
                if printipe[i]==1:
                    A+='%d\\n"'
                else:
                    A+='%s\\n"'
        for i in range(len(printlis)):
            if i<len(printlis)-1:
                if printipe[i]==2:
                    B+=f'"{printlis[i]}", '
                else:
                    B+=f"{printlis[i]}, "
            else:
                if printipe[i]==2:
                    B+=f'"{printlis[i]}"'
                else:
                    B+=f"{printlis[i]}"
        return [C+f"printf({A}, {B});"]

    #for i in range
    def forrange(gap, variable, start, stop, step):
        P=gap*4*' '
        return [f"{P}for (int {variable}={start}; {variable}<{stop}; {variable}+{step})", P+'{']

    #while
    def whilec(gap, A):
        P=gap*4*' '
        return [f"{P}while ({A})", P+"{"]

    #if
    def ifc(gap, A):
        P=gap*4*' '
        return [f"{P}if ({A})", P+"{"]

    #elif
    def elifc(gap, A):
        P=gap*4*' '
        return [f"{P}else if ({A})", P+"{"]

    # <공용 변수 정의>
    fin=[]
    variname=[]
    varitype=[]
    gap=[]
    address=[]


    jusuk=0
    #한줄 마다 판별
    for _ in range(N):
        #각 한줄 을 lis에 저장 
        lis = list(entirelis[_])
        pregap=0

        # <들여쓰기>

        if len(lis)==0:
            fin.append('')
            continue

        while lis[pregap]==' ':
            pregap+=1
        lis=lis[pregap:]
        pregap//=4
        gap.append(pregap)

        # <중괄호 끝 판별>
        if len(address)>gap[_]:
            A=len(address)-gap[_]
            for i in range(A):
                address=address[0:-1]
                fin.append(len(address)*4*' '+'}')

        if jusuk==1 and lis[0]+lis[1]+lis[2]!="'''":
            fin+=[gap[_]*4*' '+''.join(lis)]
            continue
        


        # <출력>

        printipe=[]
        if lis[0]=='p' and lis[1]=='r' and lis[2]=='i' and lis[3]=='n' and lis[4]=='t' and lis[5]=='(' and lis[-1]==')':
            sepend=0
            for i in range(6):
                del lis[0]
            del lis[-1]
            lis=''.join(lis)
            printlis=lis.split(", ")

            
            #출력값 형태 구하기
            number=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            for i in range(len(printlis)):
                A=printlis[i]
                if A[0]=='"' and A[-1]=='"':
                    printipe.append(2)
                    printlis[i]=A[1:-1]
                elif number.count(A[0])>=1:
                    printipe.append(1)
                else:
                    if '[' in A:
                        Aname = A[:A.index('[')]
                    else:
                        Aname = A
                    addr = variname.index(Aname)
                    printipe.append(varitype[addr])

            fin+=printf(gap[_], printipe, printlis)

        #주석
        elif lis[0]=='#':
            fin+=[gap[_]*4*' '+'//'+''.join(lis)]
        elif lis[0]+lis[1]+lis[2]=="'''":
            if jusuk==0:
                fin+=[gap[_]*4*' '+'/*']
                jusuk=1
            else:
                fin+=[gap[_]*4*' '+'*/']
                jusuk=0
            

        #for i in range()
        elif lis[0]=='f' and lis[1]=='o' and lis[2]=='r':
            if lis[9]+lis[10]+lis[11]+lis[12]+lis[13]=='range':
                address.append(_)
                A=''.join(lis[15:-2]).split(', ')
                if len(A)==1:
                    A.insert(0, 0)
                    A.append('+')
                elif len(A)==2:
                    A.append('+')
                else:
                    A[2]='='+str(A[2])
                variname.append(lis[4])
                varitype.append(1)
                fin+=forrange(gap[_], lis[4], A[0], A[1], A[2])

                
        #while
        elif lis[0]=='w' and lis[1]=='h' and lis[2]=='i' and lis[3]=='l' and lis[4]=='e':
            lis=lis[6:-1]
            address.append(_)
            A=''
            for i in range(len(lis)):
                A+=lis[i]
            if A=='True':
                A='1'
            fin+=whilec(gap[_], A)

        #if
        elif lis[0]+lis[1]=='if':
            lis=lis[3:-1]
            address.append(_)
            A=''
            i=0
            while True:
                if i==len(lis):
                    break
                if i+2<len(lis):
                    if lis[i]+lis[i+1]+lis[i+2]=='and':
                        A+='&&'
                        i+=3
                        continue
                    if lis[i]+lis[i+1]=='or':
                        A+='||'
                        i+=2
                        continue
                A+=lis[i]
                i+=1
            fin+=ifc(gap[_], A)

        #elif
        elif lis[0]=='e' and lis[1]=='l' and lis[2]=='i' and lis[3]=='f':
            lis=lis[5:-1]
            address.append(_)
            A=''
            i=0
            while True:
                if i==len(lis):
                    break
                if i+2<len(lis):
                    if lis[i]+lis[i+1]+lis[i+2]=='and':
                        A+='&&'
                        i+=3
                        continue
                    if lis[i]+lis[i+1]=='or':
                        A+='||'
                        i+=2
                        continue
                A+=lis[i]
                i+=1
            fin+=elifc(gap[_], A)

        #else
        elif lis[0]=='e' and lis[1]=='l' and lis[2]=='s' and lis[3]=='e':
            fin+=[gap[_]*4*' '+'else', gap[_]*4*' '+'{']
            address.append(_)

        #변수
        elif lis.count('=')==1 and (lis.count('(')==0 or lis.count('p')==0 or lis.count('u')==0 or lis.count('t')==0 or lis.count('i')==0 or lis.count('n')==0):
            Aname=''
            for i in range(len(lis)):
                if lis[i]=='=':
                    b=i
                    break
                Aname+=lis[i]
            sign=['+', '-', '/', '%', '*']
            sign1=['//', '**']
            if sign.count(Aname[-1])==1:
                check=1
                Aname=Aname[0:-1]
                Alis=''.join(lis)+';'
                fin+=[gap[_]*4*' '+Alis]
            elif sign1.count(Aname[-1:])==1:
                check=1
                Aname=Aname[0:-2]
                Alis=''.join(lis)+';'
                fin+=[gap[_]*4*' '+Alis]
            elif variname.count(Aname)==1:
                check=2
                Alis=''.join(lis)+';'
                fin+=[gap[_]*4*' '+Alis]
                        
            else:
                check=0
                variname.append(Aname)
                #만약 변수가 리스트라면 
                if lis[b+1]=='[':
                    if lis[b+2]==']':
                        fin+=[gap[_]*4*' '+f"int {Aname}[0];"]
                    else:
                        Alis=''.join(lis[b+2:-1])
                        if Alis[0]=="'":
                            Alis=list(Alis)
                            for j in range(Alis.count("'")):
                                Alis.remove("'")
                            Alis=''.join(Alis).split(', ')
                            varitype.append(2)
                            Pa='{'
                            for j in range(len(Alis)):
                                if j==len(Alis)-1:
                                    Pa+='"'+Alis[j]+'"'
                                    break
                                Pa+='"'+Alis[j]+'"'+", "
                            Pa+='}'
                            fin+=[gap[_]*4*' '+f"char {Aname}[{len(Alis)}]={Pa};"]
                        else:
                            Alis=list(map(int, Alis.split(', ')))
                            varitype.append(1)
                            Pa='{'
                            for j in range(len(Alis)):
                                if j==len(Alis)-1:
                                    Pa+=str(Alis[j])
                                    break
                                Pa+=str(Alis[j])+', '
                            Pa+='}'
                            fin+=[gap[_]*4*' '+f"int {Aname}[{len(Alis)}]={Pa};"]
                #아니라면 
                else:
                    num=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                    #정수라면 
                    if num.count(lis[b+1])==1:
                        Alis=''.join(lis)+';'
                        varitype.append(1)
                        fin+=[gap[_]*4*' '+f"int {Alis}"]
                    #문자열이라면 
                    elif lis[b+1]=="'" or lis[b+1]=='"':
                        varitype.append(2)
                        Adetail=''
                        for i in range(b+2, len(lis)-1):
                            Adetail+=lis[i]
                        fin+=[gap[_]*4*' '+f'char {Aname}[]="{Adetail}";']
                    #변수라면
                    else:
                        Adetail=''
                        c=0
                        for i in range(b+1, len(lis)):
                            Adetail+=lis[i]
                            if variname.count(Adetail)==1:
                                varitype.append(varitype[variname.index(Adetail)])
                                if varitype[variname.index(Adetail)]==1:
                                    Alis=''.join(lis)+';'
                                    fin+=[gap[_]*4*' '+f"int {Alis}"]
                                else:
                                    fin+=[gap[_]*4*' '+f'char {Aname}[]="{Adetail}";']
                                c=1
                                break
                        if c==1:
                            continue
                        Alis='//'+''.join(lis)
                        fin+=[gap[_]*4*' '+Alis]
        elif ''.join(lis)=='break' or ''.join(lis)=='continue':
            fin+=[gap[_]*4*' '+''.join(lis)+';']
        else:
            Alis='//'+''.join(lis)
            fin+=[gap[_]*4*' '+Alis]

    for i in range(gap[-1], 0, -1):
        fin.append('    '*(i-1)+'}')
                
    pp=[]
    pp.append("#include <stdio.h>")
    pp.append("#include <string.h>")
    pp.append("")
    pp.append("int main()")
    pp.append('{')
    for i in range(len(fin)):
        pp.append(' '*4+fin[i])
    pp.append('}')
    return pp


import streamlit as st

st.set_page_config(page_title="Python → C 변환기", layout="wide")

st.title("Python → C 언어 변환기")

default_code = '''print("시작")
fin="끝"
a=0
b=5
c=[1, 2, 3]
a+=b
for i in range(2, 10, 2):
    b+=i
for i in range(3):
    print(c[i])
while a<=10:
    a+=1
print("a는", a, "b는", b)
print(fin)'''

pycode = st.text_area(
    "Python 코드 입력",
    height=400,
    value=default_code
)

convert = st.button("변환")


if convert:
    result = "\n".join(convert_py_to_c(pycode))
    st.code(result, language="c")
