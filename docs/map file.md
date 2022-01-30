# File .map

Jest to plik, ustawienie elementów na mapie.<br />
Wielkość podstawowa mapy to 800x600. I z tej wielkości elementy są przeskalowywane.<br/>
Jest to plik tekstowy o struktukturze pliku json.<br/>
Wszystkie ścieżki zaczynają się od folderu assets.<br/>
Posiada on 4 atrybuty:

1. background
2. assets
3. map
4. player

## background

Ma typ tekstowy (string)
Przyjmuje scieżkę do pliku z obrazkiem lub kolor w formacie ( #000000 )

## assets

Jest to lista elementów które będą używane na mapie

Ma typ listy elementów Każdy z elementów ma atrybuty:

1. name - typ tesktowy (string), nazwa assetu, require
2. src - Typ tekstowy (string), ścieżka do zasobu(od katalogu assets), require

## map

Jest to lista elementów na mapie

Ma typ listy elementów Każdy z elementów ma atrubuty:

1. type - typ tekstowy ( string ), posiada 2 wartości:
    1. sprite - tworzy object typu obrazkowego (wymagane atrybuty asset, position, size)
    2. rect - tworzy object prostokąt ( wymagane atrybuty color, position, size)
    3. ball = tworzy object piłki ( wymagane atrybuty asset, position, radius, start_velocity)
    4. ladder - tworzy drabinkę ( wymagane atrybuty asset, position, size)
2. asset - typ tekstowy ( string ), odnośnik do assetu po nazwie
3. position - pozycja objektu jako 2 elementowa lista z liczbami [x,y] lewego górnego rogu objektu. Punkt (0,0) jest w
   lewym górnym regu ekranu i wzrasta do prawego dolnego rogu
4. size - wielkość objektu jako 2 elementowa lista z liczbami [width, height] w przypadku typu sprite size może
   przyjmować wartośc null dla jednej z wielkości w takim przypadku zostanie ona ustawiona proporcjonalnie do
   zmiejszenia 2 wielkości
5. stretch - typ tekstowy ( string ) - przyjmujący wartości ( "yes", "no" ) odnosi siędo tworzenia wielu objektów obok
   siebie od pozycji początkowej do pozycji końcowej. Odnosi się to do sprawdzenia czy lewy górny róg objektu jest w
   przedziale ( wymaga atrybutów start-position, end-position)
6. start-position - pozycja zaczęcia rozkładania obiektów jako 2 elementowa lista z liczbami [x,y]
7. end-position - pozycja zakończenia rozkładania obiektów jako 2 elementowa lista z liczbami [x,y]
8. radius - promień kuli jako liczba
9. start_velocity - prędkość początkowa jako 2 elementowa liczba [x,y]

## player

Jest to obiekt zawierający dane o graczu.Gracz ma wysokośc 100. Musi posiadać atrybuty start_position i lives

1. start_position - pozycja początkowa gracza 2 elementowa lista z liczbami [x,y]
2. lives - LIczba reprezentująca dostępne życia gracza na danej mapie










