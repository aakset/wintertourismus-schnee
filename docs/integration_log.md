| schritt                                 |   vorher |   nachher |   differenz | grund                                                                           |
|:----------------------------------------|---------:|----------:|------------:|:--------------------------------------------------------------------------------|
| Hotellerie: Auswahl Wintersportorte     |    29459 |      7080 |      -22379 | 186 auf 45 Gemeinden (Winteranteil >= 1/3)                                      |
| Hotellerie: nur Wintermonate            |     7080 |      2375 |       -4705 | Dezember bis März                                                               |
| Unvollständiger Winter 2012/13 entfernt |     2375 |      2255 |        -120 | Dezember 2012 fehlt in den BFS-Daten                                            |
| + Herkunft (Tabelle 101)                |     2255 |      2255 |           0 | left join auf bfs_nr/jahr/monat; 0 Zeilen ohne Herkunftsdaten (BFS-Datenschutz) |
| + Wetter (Open-Meteo)                   |     2255 |      2255 |           0 | left join auf bfs_nr/jahr/monat; 0 Zeilen ohne Wetterdaten                      |
| + Gemeinde-Stammdaten                   |     2255 |      2255 |           0 | left join auf bfs_nr (m:1); Höhe des Referenzorts                               |
| Fehlende Zielgrösse/Wetter entfernt     |     2255 |      2255 |           0 | vertrauliche Werte ('...') im BFS                                               |