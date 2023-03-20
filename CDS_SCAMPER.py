import numpy as np
import openpyxl as op
import pandas as pd

def readObjectives():

    objList = df['Key_Objectives'].tolist()

    i=0
    for objs in objList:
        if(str(objs)!='nan'):
            objs = objs.split(',')
            j=0
            for o in objs:
                o = o.strip()
                objs[j] = o
                j +=1
            
        objList[i] = objs
        i+=1

    return objList

def readSecondaryFunctions():

    sfList = df['Secondary_Functions'].tolist()

    i=0
    for sfs in sfList:
        if(str(sfs)!='nan'):
            sfs = sfs.split(',')
            j=0
            for sf in sfs:
                sf = sf.strip()
                sfs[j] = sf
                j +=1
            
        sfList[i] = sfs
        i+=1

    return sfList

def interpretAndCombine():

    objectivesDict = {'HYS' : 7, 'DUR' : 6, 'EZY' : 5, 'CLS' : 4, 'EGN' : 3, 'CEF' : 2, 'POR' : 1}
    
    netfeasibleList = []
    for feas in feasibleList:
        netfeasibleList.append(float(feas))

    completeSFs = ['AMC', 'LTC', 'CVI']
    ideaList = []
    accompanyingObjs = []
    scores = []
    indexesList = []

    # Since there are a total of 83*82*81*80 possible ideas, This quadruple for loop iterates through all of them and
    # retrieves the ones with the highest scores based on an algorithm approved by the rest of the team that factors in
    # included objecitves, their priorities, and the feasibility of the four included idea fragments.

    i=0
    for objs in objectivesList:

        j=0
        for objs2 in objectivesList:

            k=0
            for objs3 in objectivesList:

                m=0
                for objs4 in objectivesList:

                    indexList = [i,j,k,m]
                    indexListUni = []

                    for item in indexList: 
                        if item not in indexListUni: 
                            indexListUni.append(item) 
                    
                    count = 0
                    for idx in indexListUni:
                        count+=1

                    if(count==4):

                        netObjs = (objs+objs2+objs3+objs4)
                        netObjsUni = []

                        for item in netObjs: 
                            if item not in netObjsUni: 
                                netObjsUni.append(item) 

                        netObjs = netObjsUni

                        netSFs = (sfsList[i]+sfsList[j]+sfsList[k]+sfsList[m])
                        
                        netSFsUni = []

                        netFeas = netfeasibleList[i]+netfeasibleList[j]+netfeasibleList[k]+netfeasibleList[m]

                        for item in netSFs: 
                            if item not in netSFsUni: 
                                netSFsUni.append(item) 

                        netSFs = netSFsUni

                        currentScore = 0
                        currentScore += netFeas

                        for x in netObjs:
                            currentScore += objectivesDict[x]
                        
                        ##MAIN PARAM HERE!
                        if (currentScore >= 43 and len(netSFs)>=len(completeSFs)):
                            longList = fragmentList[i]+". "+fragmentList[j]+". "+fragmentList[k]+". "+fragmentList[m]+"."
                            ideaList.append(longList)
                            accompanyingObjs.append(netObjs)
                            scores.append(currentScore)
                            indexesList.append([i,j,k,m])
                            break

                    m+=1
                k+=1
            j+=1
        i+=1

        print(str(i)+"/"+str(len(feasibleList)))

    print("\nFinalizing Idea List...")

    idx1 = 0
    gened = str(len(indexesList))

    # These loops iterate through the high-scoring ideas and eliminates ones that are too similar to eachother.

    for indexes in indexesList:

        set1 = set(indexes)
        idx2 = 0

        for indexes2 in indexesList:
                
            set2 = set(indexes2)
            overlap =  set1.intersection(set2)

            if(len(list(overlap))>1 and (idx1 != idx2)):

                ideaList[idx2] = 'null'
                accompanyingObjs[idx2] = []
                scores[idx2] = 0
                indexesList[idx2] = []

            idx2 += 1
        
        idx1 += 1

        print(str(idx1)+"/"+str(gened))

    ideaList = [x for x in ideaList if x != 'null']

    accompanyingObjs = [sublist for sublist in accompanyingObjs if sublist]
    
    scores = [x for x in scores if x != 0]

    indexesList = [sublist for sublist in indexesList if sublist]

    print('\n'+str(len(ideaList))+" out of "+str(idx1)+" ideas selected...")

    return ideaList, accompanyingObjs, scores

def writeToTxt():
    dst = open(writepath, 'w')

    k=0
    for obj in accompanyingObjs:

        j=0
        for o in obj:

            if(j!=len(accompanyingObjs[k])-1):
                accompanyingObjs[k][j] = accompanyingObjs[k][j]+', '

            j+=1

        k+=1

    i = 0
    for fullIdea in ideaList:

        number = i+1
        dst.write('('+str(number)+')'+'\n'+fullIdea+'\nWith Objectives: '+''.join(accompanyingObjs[i])+'\nScore: '+str(scores[i])+'\n\n')

        i+=1

    dst.close()

    print("\nIdeas have been successfuly generated! Find them in "+writepath+"\n")

modelpath = "./cdsideamodel.xlsx"
writepath = "./idea_list.txt"

print("\nGenerating ideas from "+modelpath+"...\n")
df = pd.read_excel(modelpath, index_col = 'Nos' , sheet_name = 'Main')
fragmentList = df['Idea'].tolist()
feasibleList = df['Feasibility'].tolist()

objectivesList = readObjectives()
sfsList = readSecondaryFunctions()
ideaList, accompanyingObjs, scores = interpretAndCombine()
writeToTxt()
