import random
# dimensiunePopulatie=20 limitaInferioara = -1 limitaSuperioara =2 af=-1 bf=1 cf=2 precizia=6 pc=0.25 pm=0.01 nrEtape=50

#citim datele de intrare necesare
dimensiunePopulatie = int(input("Introduceti dimensiunea populatiei : "))
limitaInferioara = int(input("Introduceti limita inferioara a domeniului de definitie : "))
limitaSuperioara = int(input("Introduceti limita superioara a domeniului de definitie : "))

af = int(input("Introduceti coeficientul lui x^2 pentru functia de maximizat : "))
bf = int(input("Introduceti coeficientul lui x pentru functia de maximizat : "))
cf = int(input("Introduceti coeficientul termenului liber pentru functia de maximizat : "))

precizia = int(input("Introduceti precizia cu care se lucreaza (cu care se discretizeaza intervalul) : "))
pc = float(input("Introduceti probabilitatea de recombinare (crossover) : "))
pm = float(input("Introduceti probabilitatea de mutatie : "))
nrEtape = int(input("Introduceti numarul de etape ale algoritmului : "))

def f(x):
    return x**3 + 3*(x**2) -4*x +7

#aflam lungimea unui cromozom

x = (limitaSuperioara-limitaInferioara)*(10**precizia)
for i in range(100):
    if (x>(2**i) and x<=(2**(i+1))):
        lungime = i+1
        break

#cream lista de cromozomi
cromozomi=[]
for i in range(1,dimensiunePopulatie+1):
    nr = ''
    for j in range(1,lungime+1):
        x = str(random.randint(0,1))
        nr+=x
    cromozomi.append(nr)

#definim o functie pentru calcularea valoarii pe care o codifica cromozomii, cu ajutorul formulei si setam si precizia
def valoareCodificata(x):
    return round(x*(limitaSuperioara-limitaInferioara)/(2**lungime - 1) + limitaInferioara,precizia)

#parcurgem cromozomii si ii transformam in baza 10, urmand sa le aplicam formula
valoriX=[]

for i in range(dimensiunePopulatie):
    sum = 0
    power = 0
    for j in range(lungime-1,0,-1): #tranformam din binar
        sum += int(cromozomi[i][j]) * (2**power)
        power+=1
    valoriX.append(valoareCodificata(sum)) #adaugam in lista valoarea coficata pentru nr obtinut

#calculam valorile functiei de fitness pentru numerele codificate si le adaugam in lista
valoriF = []

for i in range (dimensiunePopulatie):
    valoriF.append(f(valoriX[i]))

#am obtinut populatia initiala si o afisam
print("Populatia initiala este : ")
for i in range(dimensiunePopulatie):
    print((i+1),":  ",cromozomi[i]," x = ",valoriX[i]," f = ",valoriF[i])

#incepem sa cream noua generatie
#alegem cel mai fit individ care va sari peste incrucisare si mutatie
selectati=[]

for i in range(dimensiunePopulatie):
    if(valoriF[i] == max(valoriF)):
        selectati.append(cromozomi[i])
        break

#calculam probabilitatea de selectie cu ajutorul formulei
#calculam performanta totala a populatiei(suma valorilor functiei fitness)

F=0
for i in range(dimensiunePopulatie):
    F+=valoriF[i]

#calculam pi(probabilitatea de selectie) pentru fiecare cromozom cu formula pi=f(Xi)/F

pi=[]
for i in range(dimensiunePopulatie):
    pi.append(valoriF[i]/F)

#afisam probabilitatile de selectie
print('\n')
print("Probabilitati selectie")
for i in range(dimensiunePopulatie):
    print("cromozom  ",i+1," probabilitate ",pi[i])

#Calculam intervalele probabilitatilor de selectie impartindu-l pe 1 la nr de indivizi si generand numere random
#in range-ul i,i+1/dimensiune populatie pt toti indivizii
print('\n')
print("Intervale probabilitati selectie ")

intervalePI=[]
intervalePI.append(0)
i=1/dimensiunePopulatie
for j in range (1,dimensiunePopulatie):
    x = random.uniform(i,i+1/dimensiunePopulatie)
    i+=1/dimensiunePopulatie
    intervalePI.append(x)

intervalePI.append(1)
print(intervalePI)
print('\n')

#generam numerel random pt principiul ruletei si incepem sa facem selectia

#resetez vectorii de valori calculate si functie fitness pt a retine noile valori
valoriF=[]
valoriX=[]
for i in range(dimensiunePopulatie):
    u = random.uniform(0,1)
    for j in range(len(intervalePI)):    #parcurg vectorul de intervale si verific unde se incadreaza nr generat
        if(u>=intervalePI[j] and u<=intervalePI[j+1]):
            pozitie = j                  #ii retin pozitia pentru a-l putea selecta
            break
    selectati.append(cromozomi[j])

    #calculez valoarea pe care o codifica
    sum = 0
    power = 0
    for j in range(lungime - 1, 0, -1):  # tranformam din binar
        sum += int(cromozomi[i][j]) * (2 ** power)
        power += 1
    valoriX.append(valoareCodificata(sum))  # adaugam in lista valoarea coficata pentru nr obtinut

    #adauga si valoarea functiei fitness
    valoriF.append(f(valoriX[len(valoriX)-1]))
    print("u = ",u,"selectam cromozomul ",j+1)

#pentru ca am rulat de numarul indivizilor algoritmul de mai sus, s-a mai adaugat un individ in plus,
#deoarece pastrasem de la inceput individul cel mai fit
selectati.remove(selectati[dimensiunePopulatie])

#afisam cromozomii selectati
print("\n")
print("Dupa selectie :")
for i in range(dimensiunePopulatie):
    print(i+1,": ",selectati[i]," x = ",valoriX[i]," f = ",valoriF[i])

#afisam probabilitatea de incrucisare
print("\n")
print("Probabilitatea de incrucisare este ",pc)

#resetez lista de cromozomi pe care nu o mai folosisem
cromozomi=[]
#parcurg lista de selectati si generez numere random pentru a vedea cine va participa la incrucisare
#cine nu participa va fi adaugat automat la cromozomi
incrucisare = []

for i in range(dimensiunePopulatie):
    u = random.uniform(0,1)
    if(u<pc):  #verific daca se incadreaza pentru incrucisare
        incrucisare.append(selectati[i])
        print(i + 1, ": ", selectati[i], " u = ", u,"<",pc," va participa")
    else:
        cromozomi.append(selectati[i])
        print(i + 1, ": ", selectati[i], " u = ", u)

print("\n")
#daca nu obtin un nr par, renunt la unul
if(len(incrucisare)%2==1):
    cromozomi.append(incrucisare[len(incrucisare)-1])
    incrucisare.remove(incrucisare[len(incrucisare)-1])

for i in range(0,len(incrucisare),2):
    for j in range(dimensiunePopulatie):
        if(incrucisare[i+1]==selectati[j]):
            x=j+1
            break
    for j in range(dimensiunePopulatie):
        if(incrucisare[i]==selectati[j]):
            y=j+1
            break
    print("Recombinare dintre cromozomul",y," cu cromozomul",x)

    #generam random punctul de rupere
    punct = round(random.uniform(0,lungime))
    punct1 = round(random.uniform(0, lungime))
    print(incrucisare[i],incrucisare[i+1]," punct1:  ",punct, " punct2: ",punct1 )



    #creez noii indivizi si ii adaug in vectorul de cromozomi
    if(punct>punct1):
        nouX = incrucisare[i][:punct1]+incrucisare[i+1][punct1:punct] + incrucisare[i][punct:]
        nouY = incrucisare[i+1][:punct1]+incrucisare[i][punct1:punct] + incrucisare[i+1][punct:]
    else:
        nouX = incrucisare[i][:punct] + incrucisare[i + 1][punct:punct1] + incrucisare[i][punct1:]
        nouY = incrucisare[i + 1][:punct] + incrucisare[i][punct:punct1] + incrucisare[i + 1][punct1:]

    print("Rezultat ",nouX,nouY)

    cromozomi.append(nouX)
    cromozomi.append(nouY)

#parcurgem cromozomii si calculam din nou valorile x si f
valoriF=[]
valoriX=[]

#si afisam populatia dupa incrucisare
print("\n")
print("Dupa recombinare : ")
for i in range(dimensiunePopulatie):
    #calculez valoarea pe care o codifica
    sum = 0
    power = 0
    for j in range(lungime - 1, 0, -1):  # tranformam din binar
        sum += int(cromozomi[i][j]) * (2 ** power)
        power += 1
    valoriX.append(valoareCodificata(sum))  # adaugam in lista valoarea coficata pentru nr obtinut

    #adauga si valoarea functiei fitness
    valoriF.append(f(valoriX[len(valoriX)-1]))

    #afisez
    print(i+1,": ",cromozomi[i]," x = ",valoriX[i]," f = ",valoriF[i])

#afisam probabilitatea de mutatie pm
print("\n")
print("Probabilitatea de mutatie pentru fiecare gena este ",pm)

#parcurg genele fiecarui cromozom si pentru fiecare generez un numar si verific daca este mai mic decat pm
modificati =[]

for i in range(dimensiunePopulatie):
    x=''
    ok=1
    for j in range(lungime):
        #generez numarul random
        u = random.uniform(0,1)
        if(u<pm):
            ok=0
            if(cromozomi[i][j]=='0'):
                x = cromozomi[i][:j] + '1' + cromozomi[i][j+1:]
            else:
                x = cromozomi[i][:j] + '0' + cromozomi[i][j + 1:]

    if(ok==0):
        cromozomi[i]=x
        modificati.append(i+1)

#afisez cromozomii modificati
print("Au fost modificati urmatorii cromozomi :")
for i in range(len(modificati)):
        print(modificati[i])

#recalculez si afisez cromozomii dupa mutatie
valoriF=[]
valoriX=[]

print("Dupa mutatie : ")
for i in range(dimensiunePopulatie):
    #calculez valoarea pe care o codifica
    sum = 0
    power = 0
    for j in range(lungime - 1, 0, -1):  # tranformam din binar
        sum += int(cromozomi[i][j]) * (2 ** power)
        power += 1
    valoriX.append(valoareCodificata(sum))  # adaugam in lista valoarea coficata pentru nr obtinut

    #adauga si valoarea functiei fitness
    valoriF.append(f(valoriX[len(valoriX)-1]))

    #afisez
    print(i+1,": ",cromozomi[i]," x = ",valoriX[i]," f = ",valoriF[i])

#afisez maximul din prima repetare a algoritmului

print('\n')
print("Evolutia maximului : ")
print(max(valoriF))

def repetare(cromozomi,valoriF,valoriX):
    #primesc ca parametrii cromozomii, valorile pe care le codifica, si valoarea functiei de fitness in punctul respectiv

    #creez probabilitatile de selectie pi
    pi = []
    for i in range(dimensiunePopulatie):
        pi.append(valoriF[i] / F)

    #folosesc aceleasi intervale ale probabilitatilor de selectie intervalePI

    # resetez vectorii de valori calculate si functie fitness pt a retine noile valori

    # incepem sa cream noua generatie
    # alegem cel mai fit individ care va sari peste incrucisare si mutatie
    selectati = []

    for i in range(dimensiunePopulatie):
        if (valoriF[i] == max(valoriF)):
            selectati.append(cromozomi[i])
            break

    valoriF = []
    valoriX = []

    for i in range(dimensiunePopulatie):
        u = random.uniform(0, 1)
        for j in range(len(intervalePI)):  # parcurg vectorul de intervale si verific unde se incadreaza nr generat
            if (u >= intervalePI[j] and u <= intervalePI[j + 1]):
                pozitie = j  # ii retin pozitia pentru a-l putea selecta
                break
        selectati.append(cromozomi[j])

        # calculez valoarea pe care o codifica
        sum = 0
        power = 0
        for j in range(lungime - 1, 0, -1):  # tranformam din binar
            sum += int(cromozomi[i][j]) * (2 ** power)
            power += 1
        valoriX.append(valoareCodificata(sum))  # adaugam in lista valoarea coficata pentru nr obtinut

        # adauga si valoarea functiei fitness
        valoriF.append(f(valoriX[len(valoriX) - 1]))

    # pentru ca am rulat de numarul indivizilor algoritmul de mai sus, s-a mai adaugat un individ in plus,
    # deoarece pastrasem de la inceput individul cel mai fit
    selectati.remove(selectati[dimensiunePopulatie])

    # resetez lista de cromozomi pe care nu o mai folosisem
    cromozomi = []
    # parcurg lista de selectati si generez numere random pentru a vedea cine va participa la incrucisare
    # cine nu participa va fi adaugat automat la cromozomi
    incrucisare = []

    for i in range(dimensiunePopulatie):
        u = random.uniform(0, 1)
        if (u < pc):  # verific daca se incadreaza pentru incrucisare
            incrucisare.append(selectati[i])
        else:
            cromozomi.append(selectati[i])

    if (len(incrucisare) % 2 == 1):
        cromozomi.append(incrucisare[len(incrucisare) - 1])
        incrucisare.remove(incrucisare[len(incrucisare) - 1])

    for i in range(0, len(incrucisare), 2):
        for j in range(dimensiunePopulatie):
            if (incrucisare[i + 1] == selectati[j]):
                x = j + 1
                break
        for j in range(dimensiunePopulatie):
            if (incrucisare[i] == selectati[j]):
                y = j + 1
                break

        # generam random punctul de rupere
        punct = round(random.uniform(0, lungime))

        # creez noii indivizi si ii adaug in vectorul de cromozomi
        nouX = incrucisare[i][:punct] + incrucisare[i + 1][punct:]
        nouY = incrucisare[i + 1][:punct] + incrucisare[i][punct:]

        cromozomi.append(nouX)
        cromozomi.append(nouY)

    # parcurgem cromozomii si calculam din nou valorile x si f
    valoriF = []
    valoriX = []

    for i in range(dimensiunePopulatie):
        # calculez valoarea pe care o codifica
        sum = 0
        power = 0
        for j in range(lungime - 1, 0, -1):  # tranformam din binar
            sum += int(cromozomi[i][j]) * (2 ** power)
            power += 1
        valoriX.append(valoareCodificata(sum))  # adaugam in lista valoarea coficata pentru nr obtinut

        # adauga si valoarea functiei fitness
        valoriF.append(f(valoriX[len(valoriX) - 1]))

    # parcurg genele fiecarui cromozom si pentru fiecare generez un numar si verific daca este mai mic decat pm
    modificati = []

    for i in range(dimensiunePopulatie):
        x = ''
        ok = 1
        for j in range(lungime):
            # generez numarul random
            u = random.uniform(0, 1)
            if (u < pm):
                ok = 0
                if (cromozomi[i][j] == '0'):
                    x = cromozomi[i][:j] + '1' + cromozomi[i][j + 1:]
                else:
                    x = cromozomi[i][:j] + '0' + cromozomi[i][j + 1:]

        if (ok == 0):
            cromozomi[i] = x
            modificati.append(i + 1)

    # recalculez cromozomii dupa mutatie
    valoriF = []
    valoriX = []

    for i in range(dimensiunePopulatie):
        # calculez valoarea pe care o codifica
        sum = 0
        power = 0
        for j in range(lungime - 1, 0, -1):  # tranformam din binar
            sum += int(cromozomi[i][j]) * (2 ** power)
            power += 1
        valoriX.append(valoareCodificata(sum))  # adaugam in lista valoarea coficata pentru nr obtinut

        # adauga si valoarea functiei fitness
        valoriF.append(f(valoriX[len(valoriX) - 1]))

    print(max(valoriF))
    for i in range(len(valoriX)):
        if(valoriF[i]==max(valoriF)):
            print(valoriX[i])
            break

#repet procesul de numarul de etape primit de la tastatura
for i in range(nrEtape-1):
    repetare(cromozomi,valoriF,valoriX)