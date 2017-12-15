#!/bin/bash

rm -f scholar.bib

for author in "Jean-Paul Laumond" "Philippe Souères" "Florent Lamiraux" "Nicolas Mansard" "Olivier Stasse" "Michel Taïx" "Bertrand Tondu" "Bruno Watier" "Mehdi Benallegue" "Andrea Del Prete" "Paolo Salaris" "Naoko Abe" "Steve Tonneau" "Oscar Ramos" "Andreas Orthey" "Olivier Roussel" "Aiva Simaite" "Joseph Mirabel" "Nirmal Giftsun" "Justin Carpentier" "Maximilien Naveau" "Christian Vassallo" "Ganesh Kumar" "Antonio El Khoury" "Guilhem Saurel" "Mylène Campana" "Alexis Mifsud"
do
    echo $author
    echo "// ------- $author ----------" >> scholar.bib
    ./scholar/scholar.py --author "$author" --citation bt >> scholar.bib
done
