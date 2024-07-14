#Carries out the temporal Study 5 years.

from __future__ import division
import re
import json
import pprint
import math
import csv

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


fosid_pid={}
pid_fosid={}
pid_year={}
pid_citations={}
id_fos={}
fosid_period={}

with open('/home/saswata/FYP/Dataset/Fos/id_fos.json') as fp:
    id_fos=json.loads(fp.read(),encoding='utf-8')

id_fos=convert(id_fos)
id_fos={int(k):str(v) for k,v in id_fos.items()}

with open('/home/saswata/FYP/Dataset/Fos/fosid_pid.json') as fp:
    fosid_pid=json.loads(fp.read(),encoding='utf-8')

fosid_pid=convert(fosid_pid)
fosid_pid={int(k):[int(i) for i in v] for k,v in fosid_pid.items()}

with open('/home/saswata/FYP/Dataset/Fos/pid_fosid.json') as fp:
    pid_fosid=json.loads(fp.read(),encoding='utf-8')

pid_fosid=convert(pid_fosid)
pid_fosid={int(k):[int(i) for i in v] for k,v in pid_fosid.items()}

with open('/home/saswata/FYP/Dataset/pid_year.json') as fp:
    pid_year=json.loads(fp.read(),encoding='utf-8')

pid_year=convert(pid_year)
pid_year={int(k):int(v) for k,v in pid_year.items()}

with open('/home/saswata/FYP/Dataset/pid_citations.json') as fp:
	pid_citations=json.loads(fp.read(),encoding='utf-8')
pid_citations=convert(pid_citations)
pid_citations={int(k):[int(i) for i in v] for k,v in pid_citations.items()}

with open('/home/saswata/FYP/Dataset/Fos/fosid_period.json') as fp:
    fosid_period=json.loads(fp.read(),encoding='utf-8')
fosid_period=convert(fosid_period)
fosid_period={int(k):str(v) for k,v in fosid_period.items()}

print('-------------------------------------------------------------------------')


arr=[1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23,24]


for fl in range(len(arr)):

    fos=arr[fl]

    print(fos)

    if fos in fosid_period:
        string=fosid_period[fos]
        years=[int(s) for s in string.split() if s.isdigit()]


    cols=29
    rows=160
    mat=[['NULL' for x in range(cols)] for y in range(rows)]


    mat[0][0]='FOS ID'
    mat[0][1]='FOS NAME'
    mat[0][2]='YEAR'
    mat[0][3]='TOTAL PUBLICATIONS'
    mat[0][4]='TOTAL CITATIONS'
    mat[0][5]='INFIELD CITATIONS'
    mat[0][6]='OUTFIELD CITATIONS'
    mat[0][7]='IMAPACT FACTOR'
    mat[0][8]='REVISED IMPACT FACTOR'
    mat[0][9]='FIRST HIGHEST RECEIVED FROM ID'
    mat[0][10]='FIRST HIGHEST RECEIVED FROM NAME'
    mat[0][11]='IN NUMBER'
    mat[0][12]='1-Revised I.F'
    mat[0][13]='SECOND HIGHEST RECEIVED FROM ID'
    mat[0][14]='SECOND HIGHEST RECEIVED FROM NAME'
    mat[0][15]='IN NUMBER'
    mat[0][16]='2-Revised I.F'
    mat[0][17]='THIRD HIGHEST RECEIVED FROM ID'
    mat[0][18]='THIRD HIGHEST RECEIVED FROM NAME'
    mat[0][19]='IN NUMBER'
    mat[0][20]='3-Revised I.F'
    mat[0][21]='FOURTH HIGHEST RECEIVED FROM ID'
    mat[0][22]='FOURTH HIGHEST RECEIVED FROM NAME'
    mat[0][23]='IN NUMBER'
    mat[0][24]='4-Revised I.F'
    mat[0][25]='FIFTH HIGHEST RECEIVED FROM ID'
    mat[0][26]='FIFTH HIGHEST RECEIVED FROM NAME'
    mat[0][27]='IN NUMBER'
    mat[0][28]='5-Revised I.F'

    year=years[0]+5
    count=1
    while year<=years[1]:
        print(year)
        fos_count={}
        mat[count][0]=fos
        if fos in id_fos:
            mat[count][1]=id_fos[fos]

        mat[count][2]=year

        if fos in fosid_pid:
            papers=fosid_pid[fos]

            inc=0
            ouc=0
            pubs=0
            pubslist=[]

            for p in papers:
                if (p in pid_year and (pid_year[p]==(year-1) or pid_year[p]==(year-2) or pid_year[p]==(year-3) or pid_year[p]==(year-4) or pid_year[p]==(year-5))):
                    pubslist.append(p)

            for p in pubslist:

                flag=False

                if p in pid_citations:
                    citlist=pid_citations[p]
                    for c in citlist:
                        if c in pid_year and pid_year[c]==year:
                            flist=[]
                            if c in pid_fosid:
                                flist=pid_fosid[c]

                            for freq in flist:
                                if freq==fos:
                                    inc=inc+1
                                    flag=True
                                    if freq not in fos_count:
                                        fos_count[freq]=1
                                    else:
                                        fos_count[freq]=fos_count[freq]+1

                                elif freq!=0 and freq!=fos:
                                    ouc=ouc+1
                                    flag=True
                                    if freq not in fos_count:
                                        fos_count[freq]=1
                                    else:
                                        fos_count[freq]=fos_count[freq]+1

                if flag:
                    pubs=pubs+1


            mat[count][3]=pubs
            mat[count][4]=inc+ouc
            mat[count][5]=inc
            mat[count][6]=ouc
            if pubs!=0:
                mat[count][7]=(inc+ouc)/pubs
                mat[count][8]=ouc/pubs
            idlist=[]
            clist=[]
            for f in fos_count:
                idlist.append(f)
                clist.append(fos_count[f])

            combine=sorted(zip(clist,idlist),reverse=True)
            sidlist=[e[1] for e in combine]
            sclist=[e[0] for e in combine]

            if len(clist)>=1:
                if sidlist[0] in id_fos:
                    mat[count][9]=sidlist[0]
                    mat[count][10]=id_fos[sidlist[0]]
                    mat[count][11]=sclist[0]
                    mat[count][12]=(inc+ouc-sclist[0])/pubs

            if len(clist)>=2:
                if sidlist[1] in id_fos:
                    mat[count][13]=sidlist[1]
                    mat[count][14]=id_fos[sidlist[1]]
                    mat[count][15]=sclist[1]
                    mat[count][16]=(inc+ouc-sclist[1])/pubs
            if len(clist)>=3:
                if sidlist[2] in id_fos:
                    mat[count][17]=sidlist[2]
                    mat[count][18]=id_fos[sidlist[2]]
                    mat[count][19]=sclist[2]
                    mat[count][20]=(inc+ouc-sclist[2])/pubs
            if len(clist)>=4:
                if sidlist[3] in id_fos:
                    mat[count][21]=sidlist[3]
                    mat[count][22]=id_fos[sidlist[3]]
                    mat[count][23]=sclist[3]
                    mat[count][24]=(inc+ouc-sclist[3])/pubs
            if len(clist)>=5:
                if sidlist[4] in id_fos:
                    mat[count][25]=sidlist[4]
                    mat[count][26]=id_fos[sidlist[4]]
                    mat[count][27]=sclist[4]
                    mat[count][28]=(inc+ouc-sclist[4])/pubs

        year=year+1
        count=count+1
    idd=str(fos)
    #print(idd)
    with open('/home/saswata/FYP/Dataset/Fos/Temporal(5years)/'+idd+'.csv','wb') as f:
        writer = csv.writer(f)
        writer.writerows(mat)
