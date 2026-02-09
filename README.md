**Obiettivo del repository**

Questo repository è pensato come ambiente di apprendimento pratico della Data Analysis, coprendo l’intero flusso di lavoro: dalla preparazione del dato grezzo fino all’estrazione di insight utili a supportare decisioni di business.

Il progetto utilizza un dataset transazionale e si concentra su:

•	data cleaning e normalizzazione,

•	feature engineering,

•	analisi esplorativa,

•	visualizzazione dei principali trend temporali e delle entità chiave (clienti, prodotti, paesi).

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Struttura del flusso di lavoro**

1\.	Download del dataset e degli script

2\.	Pulizia e arricchimento dei dati

Eseguendo lo script *clean\_dataset.py* viene effettuata una fase di preprocessing che include:

o	rimozione di duplicati e valori nulli,

o	normalizzazione e formattazione di colonne chiave,

o	feature engineering per rendere esplicite informazioni inizialmente implicite nel dato.

In particolare, vengono introdotte metriche derivate come:

o	numero di prodotti per transazione,

o	numero di transazioni uniche per cliente,

o	fatturato totale aggregato per paese.

Questa fase consente di ottenere un dataset coerente, analizzabile e pronto per l’esplorazione.

3\.	Generazione degli insight visuali

Lo script *charts\_generator.py* produce una serie di grafici suddivisi in:

o	analisi temporali, focalizzate sull’evoluzione delle metriche nel tempo;

o	analisi per entità, che mettono a confronto performance e comportamenti di paesi, clienti e prodotti.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

###### **Analisi temporale**

**Andamento stagionale del fatturato**

**average\_monthly\_revenue\_seasonality.jpg**

Il grafico mostra il fatturato medio mensile (∑ TotalPrice, scala 10⁶), calcolato aggregando ogni mese su tutti gli anni disponibili.

L’analisi evidenzia:

•	un andamento irregolare da gennaio ad agosto,

•	una crescita marcata nel periodo autunnale,

•	un picco significativo a novembre, con un fatturato medio di circa 1,4 milioni.

Questo pattern suggerisce una forte stagionalità, con concentrazione delle vendite negli ultimi mesi dell’anno.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Valore medio delle transazioni**

**average\_transaction\_value.jpg**

Il grafico rappresenta il fatturato medio per transazione, calcolato per ogni coppia mese-anno (YearMonth) e normalizzato sul numero di invoice uniche.

Si osserva:

•	una progressiva riduzione da dicembre 2009 a luglio 2010,

•	una crescita costante fino a dicembre 2010 (massimo storico),

•	una fase di contrazione fino ad aprile 2011,

•	una nuova ripresa fino a settembre 2011, per poi stabilizzarsi.

Questo andamento suggerisce variazioni significative nel valore medio del carrello, potenzialmente legate a politiche promozionali o cambiamenti nel mix di prodotti.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Fatturato mensile totale**

**monthly\_revenue.jpg**

Il fatturato mensile totale (∑ TotalPrice, scala 10⁶) mostra:

•	un avvio a circa 800.000 nel dicembre 2009,

•	fluttuazioni marcate fino a metà 2010,

•	una crescita molto forte fino a novembre 2010,

•	una seconda fase di volatilità,

•	il massimo assoluto a novembre 2011 (≈1,5 milioni), seguito da un brusco calo a dicembre.

Il grafico conferma la presenza di picchi ricorrenti negli stessi periodi dell’anno.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Numero di transazioni**

**monthly\_transactions.jpg**

Il numero di invoice uniche evidenzia:

•	una dinamica simile al fatturato,

•	un primo picco a ottobre 2010 (>3000 transazioni),

•	una fase di contrazione all’inizio del 2011,

•	un nuovo massimo a novembre 2011,

•	una forte riduzione nel mese successivo.

Questo suggerisce che i picchi di fatturato sono sostenuti anche da un aumento del volume delle transazioni, non solo dal valore medio.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Percentuale di resi**

**return\_percentage.jpg**

Il grafico mostra la percentuale di resi mensili (righe con Price < 0 o Quantity < 0).

Gli insight principali:

•	forte variabilità nel tempo,

•	massimo a novembre 2010, con valori prossimi al 3%,

•	minimo a novembre 2011, sotto l’1,4%.

Il confronto con i grafici di fatturato suggerisce che i periodi di vendite elevate possono essere accompagnati da un aumento dei resi, ma non in modo sistematico.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Considerazioni generali sulla stagionalità**

Tutti i grafici temporali mostrano picchi ricorrenti nei mesi di ottobre e novembre, probabilmente legati a:

•	campagne promozionali (es. Black Friday),

•	aumento della domanda per prodotti natalizi.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

###### **Analisi per entità**

**Analisi per paese**

**country\_analysis.jpg**

Il grafico confronta i top 10 paesi per:

•	fatturato totale,

•	numero di transazioni,

•	percentuale di resi.

Risultati principali:

•	il Regno Unito domina per fatturato (~17 milioni) e volume (>40.000 transazioni), coerentemente con la sua elevata frequenza nel dataset;

•	gli USA mostrano la percentuale di resi più alta, seguiti da Giappone, Repubblica Ceca, Corea e Arabia Saudita.

Questo evidenzia come mercati ad alto volume non coincidano necessariamente con quelli a maggiore stabilità operativa.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Analisi clienti**

**customer\_analysis.jpg**

L’analisi è limitata ai clienti con ID valido e mostra:

•	top 10 per fatturato generato,

•	top 10 per numero di transazioni,

•	spesa media per transazione.

Alcuni casi rilevanti:

•	il cliente 18102 ha generato circa 600.000 di fatturato,

•	14911 è il cliente più frequente, con oltre 500 transazioni,

•	16446 presenta una spesa media per transazione superiore a 50.000.

Questi profili evidenziano differenti tipologie di clienti: ad alto valore, ad alta frequenza e ad alto ticket medio.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Analisi prodotti**

**product\_analysis.jpg**

Il grafico mostra:

•	top 10 prodotti per fatturato totale,

•	top 10 prodotti per presenza nelle transazioni,

•	top 20 prodotti con percentuale di resi più elevata.

Insight chiave:

•	i prodotti 22423 e M generano quasi 350.000 di fatturato,

•	il prodotto 85123A è presente in oltre 5000 transazioni,

•	diversi prodotti (es. CRUK, 21254, 21315) risultano sempre restituiti,

•	altri (D, S, AMAZONFEE) mostrano percentuali di reso estremamente elevate.

Questi pattern suggeriscono criticità di qualità o di aspettative del cliente, rendendo tali prodotti candidati ideali per analisi di root cause o rimozione dal catalogo.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

###### **Decisioni finali**



**Stagionalità:**

* Rafforzare campagne promozionali e scorte in ottobre-novembre.
* Monitorare i resi nei periodi di picco.



**Clienti:**



Fidelizzare clienti top spender e ad alta frequenza con offerte personalizzate.

* Prodotti:
* Indagare cause dei resi elevati; valutare rimozione o sostituzione di prodotti critici.
* Promuovere prodotti top per fatturato e frequenza.



**Paesi/mercati:**



* Concentrarsi sui mercati più redditizi (es. UK).
* Analizzare e ridurre i resi nei mercati problematici (es. USA).



**Operatività:**



* Pianificare logistica e personale in base ai picchi di vendite.
* Usare metriche chiave per decisioni rapide e data-driven.



**Monitoraggio continuo:**



* Aggiornare dashboard e dataset per seguire trend e adattarsi ai cambiamenti
