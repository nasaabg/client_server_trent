Uwierzytelniania z użyciem zaufanej trzeciej strony  BAUER-BERSON-FEIERTAG (wykład 3, slajd 24)

Aby uruchomić program należy włączyć 3 karty w konsoli.
Nastepnie wpisać polecenie:

1) python trent.py
2) python bob.py
3) python alice.py


Alicja nawiazuje polączenie z Bobem.
Bob wysyła jej swoje ID oraz wygenerowany NONCE
Alicja wysyła do TRENTA swoje ID i swoj NONCE , oraz ID BOBa oraz NONCE boba
Trent generuje KLUCZ SESYJNY Alicji i Boba.
Nastepne wysyły 2 komunikaty do Alicji.
Jeden zaszyfrowany kluczem alicja-trent (session_key, Bob_id, alice_nonce)
Drugi zaszyfrowany kluczem trent-bob (session_key, Alice_id, bob_nonce)
Alicja 1 wiadomość deszyfruje za pomoca klucza alicja-ternt.
2 wiadomosc wysyla do boba.
Bob deszyfruje wiadomość kluczem trent-bob.
Po deszyfracji Bob i Alicja posiadaja KLUCZ SESYJNY
Nastepnie uruchamiany jest proces autentykacji na serwerze Bob'a.
Alicja musi podać nazwe użytkownika i hasło (przykładowe znajdują się w pliku users.txt)
Przeprowadzana jest autentykacja na bazie zadania 1.
Po udanej autentykacji Alicja wysyła do Boba zaszyfrowaną kluczem sesyjnym wiadomość.
Bob po otrzymaniu wiadomosci odsyła odpowiedz zpisana od tylu i zaszyfrowana kluczem sesyjnym.
Alicja sprawdza poprawmosc odpowiedzi i zamyka polaczenie.



 