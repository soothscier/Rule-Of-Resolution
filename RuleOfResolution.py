"""
    This program is written in PYTHON to prove if the given premeses lead to conclusion
    according to Law of resolution of PROPOSITIONAL LOGIC

    The notations in this program are:
    1- NEGATIION is denoted by      '~'
    2- CONJUCTION is denoted by     '^'
    3- DISJUNCTION is denoted by    '|'
    4- IMPLIFICATION is denoted by  '->'

    NOTE: All the premeses must be in 'lowercase' letters.
"""



import re
import string

"""FUNTION WHICH RETURNS BOOLEAN VALUE TELLING IF PREMESES LEADS TO CONCLUSION OR NOT"""

def proof(str1):

    clause = clauses(str1)

    negClause = []
    updatedClause = []
    solution = []
    for i in range(len(clause)):
        if len(clause[i]) > 1:
            negClause.append(clause[i][1])

        else:
            updatedClause.append(clause[i])

    if len(updatedClause) < len(negClause):
        for i in range(len(negClause)):
            solution.append(negClause[i])

        for j in range(len(updatedClause)):
            if updatedClause[j] in solution:
                del solution[solution.index(updatedClause[j])]

    elif len(updatedClause) > len(negClause):
        for i in range(len(updatedClause)):
            solution.append(updatedClause[i])

        for j in range(len(negClause)):
            if negClause[j] in solution:
                del solution[solution.index(negClause[j])]

    if len(solution) != 0:
        for i in solution:
            print('It is dependent on ',i )
        return False

    elif len(solution) == 0:
        print('The premeses are proved')
        return True



"""FUNCTION TO COMPUTE CLAUSES FROM PREMICES"""

def clauses(str1):

    #SPLITTING INTO ARRAY
    premises = str1.split(',') #['str','str']
    conclusion = premises[-1]  #gives last index of splitted array

    del premises[-1]           #dlt last index

    clause = []
    tempConclusion = []

    for i in premises:
        if('(' in i):
            aTemp = brackets(i)
            clause = sum([clause, aTemp], [])

        else:

            aTemp = implies(i)
            clause = sum([clause, aTemp], [])

    aTemp = conclusion_clause(conclusion)
    clause = sum([clause, aTemp], [])

    clause = sorted(clause)

#     for i in clause:
#         print(i)

    return clause



"""FUNCTION TO SOLVE BRACKETS IN GIVEN PREMESE"""

def brackets(prem):

    premList = []
    temp = prem
    impIndex = 0

    replacement = string.ascii_uppercase[:prem.count(')')]



    clause = []

    for i in range(prem.count(')')):
        premList.append(re.search(r'\((.*?)\)',prem).group(0)) #gives '(str)'
        b = re.search(r'\((.*?)\)',prem).group(0)
        prem = prem.replace(b,replacement[i])              #'->r'


    for i in prem:
        if i.islower():
            if '->' in prem:
                if prem.index('->') < prem.index(i):
                    clause.append(i)
                else:
                    clause.append('~' + i)

    for i in range(len(premList)):
        if '->' in premList[i]:
            idx = premList[i].index('->')-1
            premList[i] = premList[i][:idx] + '~' + premList[i][idx:]
            premList[i] = premList[i].replace('->', '|')

    count = 0
    if '->' in prem:

        for i in replacement:
            if prem.index(i) < prem.index('->'):
                aTemp = demorgan(premList[count])
                clause = sum([clause, aTemp], [])

            else:
                aTemp = implies(premList[count])
                clause = sum([clause, aTemp], [])
            count += 1
    else:
        for i in range(len(premList)):

            aTemp = implies(premList[count])
            clause = sum([clause, aTemp], [])

    return(clause)

"""DEMORGAN LAW """

def demorgan(prem):
#     if '->' in prem:
    clause = []
    for i in prem:
        if i.islower():
            if '->' in prem:
                if prem.index('->') > prem.index(i):
                    if prem[prem.index(i)-1] == '~':
                        clause.append(i)
                    else:
                        clause.append('~'+i)
                else:
                    clause.append('~' + i)
            else:
                if prem[prem.index(i)-1] == '~':
                    clause.append(i)
                else:
                    clause.append('~'+i)

    return clause


"""SOLVING IMPLIFICATION"""

def implies(prem):
    clause = []

    if not('(' in prem):
        prem = '(' + prem + ')'

    for i in range(len(prem)):
        if '->' in prem:
            if prem[i].islower():
                if prem.index('->') < prem.index(prem[i]):
                    if prem[i-1] == '~':
                        clause.append('~' + prem[i])
                    else:
                        clause.append(prem[i])

                else:
                    if prem[i-1] == '~':
                        clause.append(prem[i])
                    else:
                        clause.append('~' + prem[i])

        else:

            if prem[i].islower():
                if (prem[prem.index(prem[i])-1]) == '~':
                    clause.append('~'+ prem[i])
                else:
                    clause.append(prem[i])

    return clause


"""SOLVING FOR CONCLUSION WITH A NEGATION"""

def conclusion_clause(conclusion):
    tempConclusion = []

    if len(conclusion) > 1:
        if('(' in conclusion):
            aTemp = brackets(conclusion)
            tempConclusion = sum([tempConclusion, aTemp], [])

        else:
            aTemp = implies(conclusion)
            tempConclusion = sum([tempConclusion, aTemp], [])


#         print(tempConclusion)
        for i in range(len(tempConclusion)):
            if len(tempConclusion[i])>1:
                tempConclusion[i] = tempConclusion[i][1]
            else:
                tempConclusion[i] = '~' + tempConclusion[i]

    else:
        if len(conclusion)>1:
                conclusion = conclusion[1]
                tempConclusion.append(conclusion)

        else:
            conclusion = '~' + conclusion
            tempConclusion.append(conclusion)

    return(tempConclusion)


if __name__ == '__main__':
#     print(clauses('~p^q,r->p,~r->s,s->t,t'))
#     print(proof('t->(m|e),s->e,t^s,m'))
#     print(proof('p->q,~p->r,r->s,~q->s'))
    print(proof('l->a,e->~i,a->e,l->~i'))
