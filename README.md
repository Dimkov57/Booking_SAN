🏛️ UniRoom — System Rezerwacji Sal Uniwersyteckich

UniRoom to aplikacja webowa do rezerwacji sal wykładowych i innych pomieszczeń uniwersyteckich. Studenci rejestrują się, wybierają wolny termin w danej sali i potwierdzają rezerwację — bez papierologii i kolejek.

Projekt zbudowany na Python + Streamlit z bazą danych PostgreSQL.

 Funkcjonalności
 Rejestracja i logowanie za pomocą numeru studenckiego, adresu e-mail i wydziału (hasło przechowywane jako hash SHA-256)
 Rezerwacja sali — wybór pomieszczenia, daty (do 30 dni naprzód) oraz wolnego przedziału czasowego
 Moje rezerwacje — przegląd nadchodzących i przeszłych rezerwacji, anulowanie, eksport do CSV
 Profil użytkownika — edycja danych osobowych i zmiana hasła
 Przegląd sal — filtrowanie po typie i pojemności, podgląd zajętości terminów w wybranym dniu
 Katalog 18 sal (aule, laboratoria, sale seminaryjne, pracownie) na 3 piętrach w dwóch budynkach (P, K)
Przedziały czasowe
#	Godziny
1	08:00 – 09:30
2	09:45 – 11:15
3	11:30 – 13:00
4	13:15 – 14:45
5	15:00 – 16:30
6	16:45 – 18:15
7	18:30 – 20:15
🛠️ Technologie
Komponent	Technologia
Frontend / UI	Streamlit
Język	Python
Baza danych	PostgreSQL
Sterownik bazy danych	psycopg2-binary
Przetwarzanie danych	pandas
Konfiguracja	python-dotenv
Konteneryzacja	Docker / Docker Compose
 Struktura projektu
Booking_SAN/
├── API/                    # Moduł API
├── main.py                 # Główna aplikacja Streamlit (UI, strony, logika)
├── db.py                   # Obsługa bazy danych (użytkownicy, rezerwacje)
├── api_client.py           # Klient do komunikacji z API
├── Boo.sql                 # Skrypt SQL inicjalizujący bazę danych
├── Dockerfile              # Obraz aplikacji
├── docker-compose.yml      # Orkiestracja app + PostgreSQL
├── requirements.txt        # Zależności Pythona
└── .env                    # Zmienne środowiskowe (nie commituj prawdziwych wartości!)
 Uruchomienie projektu
Wariant 1: Docker Compose (zalecany)

Najprostszy sposób — uruchomienie aplikacji razem z bazą danych za jednym razem:

bash
git clone https://github.com/Dimkov57/Booking_SAN.git
cd Booking_SAN
docker compose up --build

Po uruchomieniu:

Aplikacja będzie dostępna pod adresem http://localhost:8501
PostgreSQL będzie dostępny na porcie 5432
Baza danych booking_san zostanie automatycznie zainicjalizowana skryptem Boo.sql
Wariant 2: Uruchomienie lokalne (bez Dockera)
Zainstaluj zależności:
bash
   pip install -r requirements.txt
Uruchom lokalny PostgreSQL i wykonaj Boo.sql, aby utworzyć tabele.
Utwórz plik .env w katalogu głównym projektu z parametrami połączenia do bazy danych (patrz sekcja poniżej).
Uruchom aplikację:
bash
   streamlit run main.py
Otwórz w przeglądarce http://localhost:8501
 Zmienne środowiskowe (.env)

Plik .env powinien zawierać parametry połączenia z PostgreSQL, na przykład:

env
DB_HOST=db
DB_PORT=5432
DB_NAME=booking_san
DB_USER=postgres
DB_PASSWORD=your_password_here

 Ważne: nie publikuj prawdziwych haseł i kluczy w repozytorium. Dodaj .env do .gitignore i unikaj zapisanych na sztywno danych dostępowych w docker-compose.yml w środowisku produkcyjnym.

 Baza danych

Schemat bazy danych (tabele użytkowników i rezerwacji) opisany jest w pliku Boo.sql i jest automatycznie stosowany przy pierwszym uruchomieniu kontenera db poprzez docker-entrypoint-initdb.d.

Główne encje:

users — numer studencki, imię, nazwisko, e-mail, wydział, hash hasła, data rejestracji
bookings — ID rezerwacji, sala, data, przedział czasowy, autor, cel/przeznaczenie, czas utworzenia
 Jak korzystać
Zarejestruj się, podając numer studencki, uniwersytecki adres e-mail i wydział.
Zaloguj się na swoje konto.
Przejdź do sekcji „Book a Room”, wybierz salę, datę i wolny termin, następnie potwierdź rezerwację.
Przeglądaj i anuluj rezerwacje w sekcji „My Bookings”.
Aktualizuj dane osobowe lub hasło w sekcji „My Profile”.
Sprawdzaj zajętość wszystkich sal w sekcji „Room Overview”.

Zasady rezerwacji:

Czas trwania jednego terminu to 90 minut
Rezerwować można maksymalnie 30 dni naprzód
Rezerwację można anulować w dowolnym momencie przed rozpoczęciem terminu
 O projekcie

Projekt został opracowany jako praca zaliczeniowa (projekt kursowy/laboratoryjny) w ramach przedmiotu w Społecznej Akademii Nauk (SAN).
