Questo repository serve per allenarsi e imparare concetti della Data Analysis.

Come prima cosa, scaricare il dataset e gli script. Lanciare lo script clean\_dataset.py per effettuare un cleaning del dataset, ovvero rimuovere duplicati e valori nulli, formattare dei valori di alcune colonne,
eseguire feature engineering per aggiungere colonne con informazioni inizialmente implicite, come il numero di prodotti per ogni transazione, il numero di transazioni uniche per ogni cliente o la somma del fatturato totale per ogni paese.

Dopodiché, lanciare lo script charts\_generator.py per generare dei grafici con insight molto utili, suddivise in grafici temporali (che mostrano l'andamento di fatturato, resi o altro durante i vari mesi) e grafici di entità (che mostrano
specifiche caratteristiche e confronti su prodotti, clienti e paesi).



I grafici temporali si presentano come segue:



average\_monthly\_revenue\_seasonality.jpg mostra un istogramma che riporta il fatturato totale mensile (sum(TotalPrice)) in scala 10^6, e ne si calcola la media (groupby Month). La media è calcolata considerando ogni mese per tutti gli anni (esempio: fatturato gennaio 2010 + fatturato gennaio 2011, diviso 2).

Dal grafico si evince un andamento intermittente da gennaio ad agosto, con un forte incremento nei successivi mesi fino a novembre, in cui si raggiunge il picco, con profitto 1.400.000.



average\_transaction\_value.jpg mostra quanto è stato il fatturato totale (sum(TotalPrice)) per ogni transazione (fratto il numero di Invoice uniche) calcolato in media per ogni mese-anno (groupby YearMonth). La media è calcolata considerando ogni mese-anno per ogni Invoice (esempio: fatturato gennaio 2010 transazione 1 + fatturato gennaio 2010 transazione 2, diviso 2).

Il grafico mostra una notevole diminuzione del fatturato da dicembre 2009 fino a luglio 2010, con un forte incremento successivo fino a dicembre 2010, in cui si tocca il massimo. Segue una forte riduzione fino ad aprile 2011 con successiva ripresa, che arriva a toccare il secondo punto più alto a dicembre 2011.



monthly\_revenue.jpg mostra il fatturato totale mensile (sum(TotalPrice)) in scala 10^6.

Si parte da circa 800.000 nel mese di dicembre 2009, per poi scendere fino a febbraio 2010. Si evincono dei continui incrementi e decrementi a intermittenza fino a luglio 2010, per poi salire moltissimo fino a novembre 2010. Dopo altri andamenti sparpagliati fino ad agosto 2011, vi è un incremento fino al punto massimo di 1.500.000 a novembre 2011, per poi calare nuovamente.



monthly\_transactions.jpg mostra il numero di transazioni (numero totale di Invoice uniche) per tutto il tempo.

Anche in questo caso, si parte da oltre 2000 transazioni iniziali a dicembre 2009, per poi scendere e risalire continuamente fino ad agosto 2010. Il picco si raggiunge a ottobre 2010, con oltre 3000 transazioni. In seguito, decrementa fino a gennaio 2011, per poi continuare a incrementare e decrementare fino ad agosto 2011, dopo cui si raggiungono oltre 3000 transazioni nuovamente a novembre 2011, per poi scendere drasticamente a dicembre.



return\_percentage.jpg mostra la percentuale di resi (numero totale di righe con Price < 0 o Quantity < 0) per ogni mese.

L'andamento è simile a quello dei precedenti grafici, con alti e bassi, e si può notare come nel mese di novembre 2010 vi è stata la percentuale di resi più elevata, toccando quasi il 3%. Il punto minimo invece è toccato a novembre dell'anno successivo, con un valore minore di 1.4%.



Tutti i grafici mostrano dei picchi nei mesi di ottobre-novembre, probabilmente dovuti agli sconti del Black Friday o alla vendita numerosa di prodotti natalizi.





I grafici di entità si presentano come segue:



country\_analysis.jpg mostra la top 10 dei paesi con maggior profitto, maggior numero di transazioni e maggior percentuale di resi.

Come profitto e transazioni, il Regno Unito sta in prima posizione, con ben 17.000.000 di fatturato e oltre 40.000 transazioni, tra l'altro è anche il paese più frequente nel dataset. Per quanto riguarda i resi, gli USA stanno in prima posizione, seguiti da Giappone, Repubblica Ceca, Korea e Arabia Saudita.



customer\_analysis.jpg mostra la top 10 dei clienti che hanno portato profitto, che hanno effettuato più transazioni e quanto in media hanno speso ogni volta che hanno effettuato una transazione.

I clienti validi, per cui l'analisi è stata fatta, sono stati quelli il cui ID era indicato.

18102 è arrivato a portare un profitto di 600.000, 14911 ha eseguito oltre 500 transazioni, e 16446 ha raggiunto un valore medio di oltre 50.000.



product\_analysis.jpg mostra la top 10 dei prodotti che hanno portato maggior profitto totale e quelli maggiormente presenti nelle transazioni; inoltre mostra la top 20 delle percentuali dei prodotti resi.

I prodotti 22423 e M hanno portato quasi a 350.000 di profitto, mentre il prodotto 85123A è stato presente in oltre 5000 transazioni. Molti prodotti, come CRUK, 21254, 21315 ecc. sono sempre stati resi, e prodotti come D, S e AMAZONFEE sono quasi sempre stati resi. Molto probabilmente, questi prodotti erano difettosi e non hanno soddisfatto nessun cliente.



