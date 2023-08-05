Akrikola
===============

An early version of a light-weight NLP library for Finnish language.

## Use case

In Finnish language the rules for selecting noun cases "in", "from" and "into" for municipality names are complicated. Even Finns have problem selecting the correct case when using a less common municipality name. In Finland there are over 300 municipalities. This library provides correct case endings.

## Use case explained in Finnish / Käyttötarkoitus suomeksi

Suomalaisten kuntien, kaupunkien ja muiden asutusten nimiä taivutetaan siten kuin paikkakunnalla on totuttu taivuttamaan. Tämä kirjasto taivuttaa suomalaisten kuntien nimet sisä- ja ulkopaikallissijoissa sekä partitiivissa ja genetiivissä. Lisäksi kirjastolla voi tunnistaa kuntien nimiä kaikissa mainituissa taivutusmuodoissa.

## Using Akrikola

To conjugate municipalities just import Municipality class and create an instance with the name of the municipality.

```python
from akrikola import Municipality

town = Municipality("Ylivieska")
print(town.departure)
print(town.destination)
print(town.at)
```

Will produce:

```
Ylivieska
Ylivieskaan
Ylivieskassa
```

Also nominative, partitive and genetive forms can be produced:

```python
city = Municipality("Kauniainen")
print(city.name)
print(city.partitive)
print(city.genetive)
print(city.in_swedish)
```

Will produce:

```
Kauniainen
Kauniaista
Kauniaisten
Grankulla
```

Note that the class will throw KeyError at instance creation if the word is not a name of a municipality.

To check if a word is a municipality name in any the six recognized noun cases (plus in swedish):

```python
from akrikola import Municipality

Municipality.exists("Hattula")
# return True
Municipality.exists("Hattula")
# return False
```

# Author

- [tjkemp](https://github.com/tjkemp)

This project is licensed under the terms of the GNU Lesser General Public License v3.0 (GNU LGPLv3). See ``LICENSE.txt`` for more information.
