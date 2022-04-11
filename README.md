Nume: Buzera Tiberiu
Grupă: 333CA

# Tema <NR> Marketplace

Organizare
-

Pentru implementarea temei am creat 2 dictionare, unul pentru retinerea producatorior si unul pentru
retinerea produselor din cart.
Fiecare cart are un id, si o lista asociata, fiecare element din lista este o pereche de id_producator
si produs.
Fiecare producator are un id si o lista cu produsele sale, fiecare element din lista este o pereche de 
produs si o valoare de 1 sau 0, 1 inseamna ca acel produs este pe raft si 0 inseamna ca acel produs este in
cos, acesta valoare are rolul de a nu modifica dimensiunea listei de produse pana nu se apeleaza place_order.

In clasa consumer in metoda run se carcurge lista de comenzi primita in constructor si se apeleaza 
metodele add sau remove din marketplace in functie de caz. In cazul in care produsul nu se gasea pe 
raft se astepta o perioada de timp inainte sa se reincerce metoda de add.

In clasa produser am implementat un while din care nu se iese pentru a se repeta la nesfarsit procesul de
productie. In interiorul while-ului am parcurs lista de produse care aveau un timp de produse fiecare.
Dupa ce se crea produsul se incerca sa se publice, in cazul in care coada din marketplace era plina se
astepta un timp si se incerca publicarea produsului din nou.

Pentru lucrul cu threaduri am implementat 2 lock-uri unul pentru producatori si unul pentru consumatori
si am delimitat in fiecare functie sectiunile critice.

Implementare
-

Intregul enunt al temei a fost implementat.
Am implementat in plus partea de logging prin care se afisaza informatii si erorile intalnite intr-un
fisier numit marketplace.log.
Am intampinat dificultati la implementarea temei in mod paralel, intrucat am avut probleme cu deadlock-urile.
Pe parcursul temei am descoperit metoda de logging ca o buna metoda de debugging.


Resurse utilizate
-

Ca resurse utilizate am folosit laboratoarele 1 (despre liste si dictionare) si laboratorul 2 (despre lock)
petnru implementarea temei, plus link-urile puse la dispozitie in tema pentru implementarea logger-ului.

Git
-
https://github.com/TibiAlex/MarketPlace
