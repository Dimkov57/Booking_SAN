-- ══════════════════════════════════════════════════════════════════════════════
--  BOOKING_SAN  ·  Schemat PostgreSQL
--  W pełni odpowiada strukturze main.py (Dimkov57/Booking_SAN)
-- ══════════════════════════════════════════════════════════════════════════════
--
--  Jak uruchomić:
--    psql -U postgres -c "CREATE DATABASE booking_san;"
--    psql -U postgres -d booking_san -f booking_san.sql
--
--  Lub w pgAdmin: otwórz plik → zaznacz wszystko → F5 (Execute)
-- ══════════════════════════════════════════════════════════════════════════════

-- Rozszerzenie do UUID (używane w tabeli bookings)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";


-- ══════════════════════════════════════════════════════════════════════════════
--  1.  SŁOWNIKI
-- ══════════════════════════════════════════════════════════════════════════════

-- ─── 1.1  Wydziały  ──────────────────────────────────────────────────────────
-- Lista 1:1 z FACULTIES w main.py

CREATE TABLE faculties (
    faculty_id  SMALLSERIAL  PRIMARY KEY,
    name        VARCHAR(120) NOT NULL UNIQUE
);

INSERT INTO faculties (name) VALUES
    ('Computer Science'),
    ('Mathematics'),
    ('Physics'),
    ('Chemistry'),
    ('Biology'),
    ('Economics'),
    ('Law'),
    ('Humanities'),
    ('Engineering'),
    ('Other');


-- ─── 1.2  Typy sal  ──────────────────────────────────────────────────────────
-- Wartości z pola "type" słownika ROOMS w main.py

CREATE TABLE room_types (
    type_id  SMALLSERIAL PRIMARY KEY,
    name     VARCHAR(40) NOT NULL UNIQUE
);

INSERT INTO room_types (name) VALUES
    ('hall'),
    ('lab'),
    ('seminar'),
    ('study');


-- ─── 1.3  Przedziały czasowe  ────────────────────────────────────────────────
-- Lista 1:1 z TIME_SLOTS w main.py

CREATE TABLE time_slots (
    slot_id     SMALLSERIAL  PRIMARY KEY,
    label       VARCHAR(15)  NOT NULL UNIQUE,  -- np. '08:00–09:30'
    start_time  TIME         NOT NULL,
    end_time    TIME         NOT NULL,
    CONSTRAINT chk_slot_order CHECK (end_time > start_time)
);

INSERT INTO time_slots (label, start_time, end_time) VALUES
    ('08:00–09:30', '08:00', '09:30'),
    ('09:45–11:15', '09:45', '11:15'),
    ('11:30–13:00', '11:30', '13:00'),
    ('13:15–14:45', '13:15', '14:45'),
    ('15:00–16:30', '15:00', '16:30'),
    ('16:45–18:15', '16:45', '18:15');


-- ══════════════════════════════════════════════════════════════════════════════
--  2.  SALE
-- ══════════════════════════════════════════════════════════════════════════════

-- ─── 2.1  Tabela sal  ────────────────────────────────────────────────────────
-- Wszystkie 18 sal ze słownika ROOMS w main.py

CREATE TABLE rooms (
    room_id   VARCHAR(10) PRIMARY KEY,                              -- 'P11', 'K22' …
    type_id   SMALLINT    NOT NULL REFERENCES room_types(type_id),
    floor     SMALLINT    NOT NULL CHECK (floor BETWEEN 1 AND 10),
    capacity  SMALLINT    NOT NULL CHECK (capacity > 0),
    is_active BOOLEAN     NOT NULL DEFAULT TRUE                     -- można dezaktywować salę
);

-- Budynek P
INSERT INTO rooms (room_id, type_id, floor, capacity) VALUES
    ('P11', (SELECT type_id FROM room_types WHERE name='hall'),    1, 120),
    ('P12', (SELECT type_id FROM room_types WHERE name='lab'),     1,  30),
    ('P13', (SELECT type_id FROM room_types WHERE name='study'),   1,  30),
    ('P21', (SELECT type_id FROM room_types WHERE name='seminar'), 2,  20),
    ('P22', (SELECT type_id FROM room_types WHERE name='lab'),     2,  30),
    ('P23', (SELECT type_id FROM room_types WHERE name='study'),   2,  30),
    ('P31', (SELECT type_id FROM room_types WHERE name='seminar'), 3,  20),
    ('P32', (SELECT type_id FROM room_types WHERE name='lab'),     3,  30),
    ('P33', (SELECT type_id FROM room_types WHERE name='study'),   3,  30);

-- Budynek K
INSERT INTO rooms (room_id, type_id, floor, capacity) VALUES
    ('K11', (SELECT type_id FROM room_types WHERE name='seminar'), 1,  30),
    ('K12', (SELECT type_id FROM room_types WHERE name='lab'),     1,  30),
    ('K13', (SELECT type_id FROM room_types WHERE name='seminar'), 1,  30),
    ('K21', (SELECT type_id FROM room_types WHERE name='study'),   2,  30),
    ('K22', (SELECT type_id FROM room_types WHERE name='lab'),     2,  30),
    ('K23', (SELECT type_id FROM room_types WHERE name='study'),   2,  30),
    ('K31', (SELECT type_id FROM room_types WHERE name='seminar'), 3,  30),
    ('K32', (SELECT type_id FROM room_types WHERE name='lab'),     3,  30),
    ('K33', (SELECT type_id FROM room_types WHERE name='study'),   3,  30);


-- ─── 2.2  Udogodnienia  ──────────────────────────────────────────────────────
-- Wszystkie wartości z pola "amenities" w ROOMS (main.py)

CREATE TABLE amenities (
    amenity_id  SMALLSERIAL  PRIMARY KEY,
    name        VARCHAR(80)  NOT NULL UNIQUE
);

INSERT INTO amenities (name) VALUES
    ('Projektor'),
    ('Mikrofon'),
    ('Klimatyzacja'),
    ('Tablica'),
    ('Monitor TV'),
    ('40 komputerów'),
    ('WiFi'),
    ('Wideokonferencja'),
    ('Tablety graficzne'),
    ('Duże ekrany'),
    ('Scena'),
    ('Pełne AV'),
    ('Streaming');


-- ─── 2.3  Relacja sala ↔ udogodnienie (many-to-many)  ────────────────────────

CREATE TABLE room_amenities (
    room_id    VARCHAR(10) NOT NULL REFERENCES rooms(room_id)        ON DELETE CASCADE,
    amenity_id SMALLINT    NOT NULL REFERENCES amenities(amenity_id) ON DELETE CASCADE,
    PRIMARY KEY (room_id, amenity_id)
);

-- Dane dokładnie zgodne z ROOMS w main.py
INSERT INTO room_amenities (room_id, amenity_id)
SELECT v.room_id, a.amenity_id
FROM (VALUES
    -- Budynek P
    ('P11','Projektor'),      ('P11','Mikrofon'),          ('P11','Klimatyzacja'),
    ('P12','Tablica'),        ('P12','Monitor TV'),
    ('P13','40 komputerów'),  ('P13','Projektor'),         ('P13','Klimatyzacja'),
    ('P21','Tablica'),        ('P21','WiFi'),
    ('P22','Tablica'),        ('P22','WiFi'),
    ('P23','Wideokonferencja'), ('P23','Projektor'),       ('P23','Klimatyzacja'),
    ('P31','Tablety graficzne'), ('P31','Duże ekrany'),
    ('P32','Scena'),          ('P32','Pełne AV'),          ('P32','Klimatyzacja'), ('P32','Streaming'),
    ('P33','Scena'),          ('P33','Pełne AV'),          ('P33','Klimatyzacja'), ('P33','Streaming'),
    -- Budynek K
    ('K11','Projektor'),      ('K11','Mikrofon'),          ('K11','Klimatyzacja'),
    ('K12','Tablica'),        ('K12','Monitor TV'),
    ('K13','40 komputerów'),  ('K13','Projektor'),         ('K13','Klimatyzacja'),
    ('K21','Tablica'),        ('K21','WiFi'),
    ('K22','Tablica'),        ('K22','WiFi'),
    ('K23','Wideokonferencja'), ('K23','Projektor'),       ('K23','Klimatyzacja'),
    ('K31','Tablety graficzne'), ('K31','Duże ekrany'),
    ('K32','Scena'),          ('K32','Pełne AV'),          ('K32','Klimatyzacja'), ('K32','Streaming'),
    ('K33','Scena'),          ('K33','Pełne AV'),          ('K33','Klimatyzacja'), ('K33','Streaming')
) AS v(room_id, amenity_name)
JOIN amenities a ON a.name = v.amenity_name;


-- ══════════════════════════════════════════════════════════════════════════════
--  3.  UŻYTKOWNICY
--  Odpowiada strukturze users.json i słownikowi users[sid] w main.py:
--    first_name, last_name, name, email, student_id, faculty, password, joined
-- ══════════════════════════════════════════════════════════════════════════════

CREATE TABLE users (
    student_id  VARCHAR(30)  PRIMARY KEY,           -- klucz słownika, np. 's12345'
    first_name  VARCHAR(80)  NOT NULL,
    last_name   VARCHAR(80)  NOT NULL,
    -- Pole 'name' = first_name || ' ' || last_name — generowane automatycznie przez widok
    email       VARCHAR(160) NOT NULL UNIQUE,
    faculty_id  SMALLINT     NOT NULL REFERENCES faculties(faculty_id),
    password    CHAR(64)     NOT NULL,              -- skrót SHA-256 hex (jak w hash_password())
    joined      DATE         NOT NULL DEFAULT CURRENT_DATE,
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Automatyczna aktualizacja updated_at przy każdej zmianie rekordu
CREATE OR REPLACE FUNCTION fn_aktualizuj_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION fn_aktualizuj_updated_at();

-- Widok z pełnym imieniem (odpowiednik u['name'] w Pythonie)
CREATE VIEW users_view AS
    SELECT
        u.student_id,
        u.first_name,
        u.last_name,
        u.first_name || ' ' || u.last_name  AS name,     -- odpowiednik u['name']
        u.email,
        f.name                               AS faculty,  -- string, jak w main.py
        u.password,
        u.joined,
        u.updated_at
    FROM  users u
    JOIN  faculties f ON f.faculty_id = u.faculty_id;


-- ══════════════════════════════════════════════════════════════════════════════
--  4.  REZERWACJE
--  Odpowiada strukturze bookings.json i słownikowi booking w main.py:
--    id, name, student_id, email, faculty, purpose, room, date, slot, booked_at
-- ══════════════════════════════════════════════════════════════════════════════

CREATE TABLE bookings (
    -- 'id' w main.py: '{student_id}-{date_str}-{slot[:5]}'
    booking_id    VARCHAR(60)  PRIMARY KEY,
    student_id    VARCHAR(30)  NOT NULL REFERENCES users(student_id) ON DELETE CASCADE,
    room_id       VARCHAR(10)  NOT NULL REFERENCES rooms(room_id),
    slot_id       SMALLINT     NOT NULL REFERENCES time_slots(slot_id),
    booking_date  DATE         NOT NULL,
    purpose       TEXT         NOT NULL DEFAULT 'Nie podano celu',
    booked_at     TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    -- Miękkie anulowanie (odpowiednik przycisku "Cancel" na stronie My Bookings)
    cancelled_at  TIMESTAMPTZ  DEFAULT NULL,

    -- Jeden slot — jedna aktywna rezerwacja
    -- (odpowiednik funkcji is_slot_taken() w main.py)
    CONSTRAINT uq_sala_data_slot UNIQUE (room_id, booking_date, slot_id)
);

-- Indeksy dla typowych zapytań z main.py
CREATE INDEX idx_rezerwacje_student    ON bookings(student_id);
CREATE INDEX idx_rezerwacje_sala_data  ON bookings(room_id, booking_date);
CREATE INDEX idx_rezerwacje_data       ON bookings(booking_date);

-- ── Wyzwalacz: nie można rezerwować przeszłych dat  ───────────────────────
-- (odpowiednik min_value=date.today() w st.date_input)

CREATE OR REPLACE FUNCTION fn_sprawdz_date_rezerwacji()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.booking_date < CURRENT_DATE THEN
        RAISE EXCEPTION
            'Nie można rezerwować sali na przeszłą datę: %', NEW.booking_date;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_brak_przeszlych_rezerwacji
    BEFORE INSERT ON bookings
    FOR EACH ROW EXECUTE FUNCTION fn_sprawdz_date_rezerwacji();

-- ── Wyzwalacz: nie można rezerwować dezaktywowanej sali  ─────────────────

CREATE OR REPLACE FUNCTION fn_sprawdz_aktywnosc_sali()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NOT (SELECT is_active FROM rooms WHERE room_id = NEW.room_id) THEN
        RAISE EXCEPTION
            'Sala % jest obecnie niedostępna do rezerwacji.', NEW.room_id;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_sala_musi_byc_aktywna
    BEFORE INSERT ON bookings
    FOR EACH ROW EXECUTE FUNCTION fn_sprawdz_aktywnosc_sali();


-- ══════════════════════════════════════════════════════════════════════════════
--  5.  WIDOKI (VIEWS)
-- ══════════════════════════════════════════════════════════════════════════════

-- ─── 5.1  Pełne informacje o rezerwacji  ─────────────────────────────────────
-- Odpowiada polom słownika booking w main.py

CREATE VIEW bookings_full AS
    SELECT
        b.booking_id                                AS id,           -- b['id']
        u.first_name || ' ' || u.last_name         AS name,         -- b['name']
        b.student_id,                                                -- b['student_id']
        u.email,                                                     -- b['email']
        f.name                                     AS faculty,       -- b['faculty']
        b.purpose,                                                   -- b['purpose']
        b.room_id                                  AS room,          -- b['room']
        b.booking_date                             AS date,          -- b['date']
        ts.label                                   AS slot,          -- b['slot']
        TO_CHAR(b.booked_at, 'YYYY-MM-DD HH24:MI') AS booked_at,   -- b['booked_at']
        -- Dodatkowe pola dla wygody
        rt.name                                    AS room_type,
        r.floor,
        r.capacity,
        ts.start_time,
        ts.end_time,
        CASE WHEN b.cancelled_at IS NULL THEN 'aktywna'
             ELSE 'anulowana' END                  AS status,
        b.cancelled_at
    FROM  bookings    b
    JOIN  users       u  ON u.student_id = b.student_id
    JOIN  faculties   f  ON f.faculty_id = u.faculty_id
    JOIN  rooms       r  ON r.room_id    = b.room_id
    JOIN  room_types  rt ON rt.type_id   = r.type_id
    JOIN  time_slots  ts ON ts.slot_id   = b.slot_id;


-- ─── 5.2  Plan dnia (odpowiednik get_room_bookings dla CURRENT_DATE)  ────────

CREATE VIEW plan_dnia AS
    SELECT
        b.room_id                              AS sala,
        ts.label                               AS slot,
        ts.start_time,
        ts.end_time,
        u.first_name || ' ' || u.last_name     AS zarezerwowane_przez,
        b.student_id,
        b.purpose                              AS cel
    FROM  bookings   b
    JOIN  time_slots ts ON ts.slot_id   = b.slot_id
    JOIN  users      u  ON u.student_id = b.student_id
    WHERE b.booking_date = CURRENT_DATE
      AND b.cancelled_at IS NULL
    ORDER BY b.room_id, ts.start_time;


-- ─── 5.3  Statystyki sal (dla strony Room Overview)  ─────────────────────────

CREATE VIEW statystyki_sal AS
    SELECT
        r.room_id                                             AS sala,
        rt.name                                               AS typ,
        r.floor                                               AS pietro,
        r.capacity                                            AS pojemnosc,
        COUNT(b.booking_id)                                   AS wszystkie_rezerwacje,
        COUNT(b.booking_id) FILTER (
            WHERE b.cancelled_at IS NULL
              AND b.booking_date >= CURRENT_DATE)             AS nadchodzace_rezerwacje
    FROM  rooms r
    JOIN  room_types rt ON rt.type_id = r.type_id
    LEFT  JOIN bookings b ON b.room_id = r.room_id
    GROUP BY r.room_id, rt.name, r.floor, r.capacity
    ORDER BY r.room_id;


-- ══════════════════════════════════════════════════════════════════════════════
--  6.  FUNKCJE  (odpowiedniki funkcji pomocniczych z main.py)
-- ══════════════════════════════════════════════════════════════════════════════

-- ─── 6.1  czy_slot_zajety(sala, data, etykieta_slotu)  ───────────────────────
-- Odpowiednik: is_slot_taken(room, booking_date, slot) w main.py

CREATE OR REPLACE FUNCTION czy_slot_zajety(
    p_room_id  VARCHAR,
    p_data     DATE,
    p_slot     VARCHAR   -- etykieta slotu, np. '09:45–11:15'
) RETURNS BOOLEAN LANGUAGE sql STABLE AS $$
    SELECT EXISTS (
        SELECT 1
        FROM  bookings   b
        JOIN  time_slots ts ON ts.slot_id = b.slot_id
        WHERE b.room_id      = p_room_id
          AND b.booking_date = p_data
          AND ts.label       = p_slot
          AND b.cancelled_at IS NULL
    );
$$;


-- ─── 6.2  rezerwacje_sali(sala, data)  ───────────────────────────────────────
-- Odpowiednik: get_room_bookings(room, booking_date) w main.py

CREATE OR REPLACE FUNCTION rezerwacje_sali(
    p_room_id  VARCHAR,
    p_data     DATE
) RETURNS TABLE (
    booking_id  VARCHAR,
    student_id  VARCHAR,
    imie_nazwisko TEXT,
    email       VARCHAR,
    wydzial     VARCHAR,
    cel         TEXT,
    slot        VARCHAR,
    zarezerwowano_o TEXT
) LANGUAGE sql STABLE AS $$
    SELECT
        b.booking_id,
        b.student_id,
        u.first_name || ' ' || u.last_name,
        u.email,
        f.name,
        b.purpose,
        ts.label,
        TO_CHAR(b.booked_at, 'YYYY-MM-DD HH24:MI')
    FROM  bookings   b
    JOIN  time_slots ts ON ts.slot_id   = b.slot_id
    JOIN  users      u  ON u.student_id = b.student_id
    JOIN  faculties  f  ON f.faculty_id = u.faculty_id
    WHERE b.room_id      = p_room_id
      AND b.booking_date = p_data
      AND b.cancelled_at IS NULL
    ORDER BY ts.start_time;
$$;


-- ─── 6.3  wolne_sloty(sala, data)  ───────────────────────────────────────────
-- Odpowiednik: avail_slots = [s for s in TIME_SLOTS if not is_slot_taken(...)]

CREATE OR REPLACE FUNCTION wolne_sloty(
    p_room_id  VARCHAR,
    p_data     DATE
) RETURNS TABLE (
    slot_id     SMALLINT,
    label       VARCHAR,
    start_time  TIME,
    end_time    TIME
) LANGUAGE sql STABLE AS $$
    SELECT ts.slot_id, ts.label, ts.start_time, ts.end_time
    FROM   time_slots ts
    WHERE  NOT EXISTS (
        SELECT 1 FROM bookings b
        WHERE  b.room_id      = p_room_id
          AND  b.booking_date = p_data
          AND  b.slot_id      = ts.slot_id
          AND  b.cancelled_at IS NULL
    )
    ORDER BY ts.start_time;
$$;


-- ─── 6.4  anuluj_rezerwacje(booking_id, student_id)  ─────────────────────────
-- Odpowiednik: przycisk "Cancel" na stronie My Bookings w main.py

CREATE OR REPLACE FUNCTION anuluj_rezerwacje(
    p_booking_id  VARCHAR,
    p_student_id  VARCHAR
) RETURNS TEXT LANGUAGE plpgsql AS $$
DECLARE
    v_data DATE;
BEGIN
    SELECT booking_date INTO v_data
    FROM   bookings
    WHERE  booking_id  = p_booking_id
      AND  student_id  = p_student_id
      AND  cancelled_at IS NULL;

    IF NOT FOUND THEN
        RETURN 'BŁĄD: Rezerwacja nie została znaleziona lub już anulowana.';
    END IF;

    IF v_data < CURRENT_DATE THEN
        RETURN 'BŁĄD: Nie można anulować rezerwacji z przeszłą datą.';
    END IF;

    UPDATE bookings
       SET cancelled_at = NOW()
     WHERE booking_id = p_booking_id;

    RETURN 'OK';
END;
$$;


-- ══════════════════════════════════════════════════════════════════════════════
--  7.  MIGRACJA  JSON → PostgreSQL
--  Uruchom po wgraniu schematu, aby przenieść dane z users.json i bookings.json
-- ══════════════════════════════════════════════════════════════════════════════

-- Skrypt migracji w Pythonie (zapisz jako migrate.py i uruchom):
--
--   import psycopg2, json, hashlib
--
--   conn = psycopg2.connect("dbname=booking_san user=postgres password=...")
--   cur  = conn.cursor()
--
--   # --- Użytkownicy ---
--   users = json.load(open("users.json"))
--   for sid, u in users.items():
--       cur.execute("""
--           INSERT INTO users (student_id, first_name, last_name, email,
--                              faculty_id, password, joined)
--           VALUES (%s, %s, %s, %s,
--                   (SELECT faculty_id FROM faculties WHERE name = %s),
--                   %s, %s)
--           ON CONFLICT DO NOTHING
--       """, (sid, u['first_name'], u['last_name'], u['email'],
--             u.get('faculty', 'Other'), u['password'],
--             u.get('joined', '2025-01-01')))
--
--   # --- Rezerwacje ---
--   bookings = json.load(open("bookings.json"))
--   for b in bookings:
--       cur.execute("""
--           INSERT INTO bookings
--               (booking_id, student_id, room_id, slot_id,
--                booking_date, purpose, booked_at)
--           SELECT %s, %s, %s, slot_id, %s::date, %s, %s::timestamptz
--           FROM   time_slots WHERE label = %s
--           ON CONFLICT DO NOTHING
--       """, (b['id'], b['student_id'], b['room'],
--             b['date'], b.get('purpose', 'Nie podano celu'),
--             b.get('booked_at', '2025-01-01 00:00'),
--             b['slot']))
--
--   conn.commit()
--   cur.close(); conn.close()
--   print("Migracja zakończona!")


-- ══════════════════════════════════════════════════════════════════════════════
--  8.  PRZYKŁADOWE ZAPYTANIA
-- ══════════════════════════════════════════════════════════════════════════════

-- ── Rejestracja nowego studenta (odpowiednik "Create Account" w main.py)
/*
INSERT INTO users (student_id, first_name, last_name, email, faculty_id, password)
VALUES (
    's12345',
    'Jan',
    'Kowalski',
    'jan.kowalski@san.edu.pl',
    (SELECT faculty_id FROM faculties WHERE name = 'Computer Science'),
    encode(digest('moje_haslo', 'sha256'), 'hex')   -- SHA-256, jak w hash_password()
);
*/

-- ── Logowanie (odpowiednik sprawdzenia hasła w show_auth())
/*
SELECT student_id, first_name || ' ' || last_name AS imie_nazwisko, email
FROM   users
WHERE  student_id = 's12345'
  AND  password   = encode(digest('moje_haslo', 'sha256'), 'hex');
*/

-- ── Rezerwacja sali (odpowiednik przycisku "Confirm Booking")
/*
INSERT INTO bookings (booking_id, student_id, room_id, slot_id, booking_date, purpose)
SELECT
    's12345-2026-05-25-0945',
    's12345',
    'P11',
    slot_id,
    '2026-05-25',
    'Wykład z uczenia maszynowego'
FROM time_slots
WHERE label = '09:45–11:15';
*/

-- ── Wolne sloty dla sali P11 na jutro (odpowiednik avail_slots w main.py)
/*
SELECT * FROM wolne_sloty('P11', CURRENT_DATE + 1);
*/

-- ── Czy slot jest zajęty (odpowiednik is_slot_taken())
/*
SELECT czy_slot_zajety('P11', '2026-05-25', '09:45–11:15');
*/

-- ── Wszystkie rezerwacje studenta (strona "My Bookings")
/*
SELECT date, slot, room, room_type, purpose, status, booked_at
FROM   bookings_full
WHERE  student_id = 's12345'
  AND  status     = 'aktywna'
ORDER  BY date, start_time;
*/

-- ── Anulowanie rezerwacji (przycisk "Cancel" w main.py)
/*
SELECT anuluj_rezerwacje('s12345-2026-05-25-0945', 's12345');
*/

-- ── Wszystkie rezerwacje sali na dany dzień (odpowiednik get_room_bookings())
/*
SELECT * FROM rezerwacje_sali('P11', '2026-05-25');
*/

-- ── Plan dnia dla wszystkich sal
/*
SELECT * FROM plan_dnia;
*/

-- ── Sale z projektorem i pojemnością ≥ 30 (dla filtrów na stronie Room Overview)
/*
SELECT r.room_id, rt.name AS typ, r.floor AS pietro, r.capacity AS pojemnosc
FROM   rooms r
JOIN   room_types     rt ON rt.type_id   = r.type_id
JOIN   room_amenities ra ON ra.room_id   = r.room_id
JOIN   amenities      a  ON a.amenity_id = ra.amenity_id
WHERE  a.name = 'Projektor'
  AND  r.capacity >= 30
ORDER  BY r.room_id;
*/

-- ── Aktualizacja profilu użytkownika (odpowiednik "Save Changes" w My Profile)
/*
UPDATE users
SET    first_name = 'Aleksander',
       last_name  = 'Nowak',
       email      = 'a.nowak@san.edu.pl',
       faculty_id = (SELECT faculty_id FROM faculties WHERE name = 'Mathematics')
WHERE  student_id = 's12345';
*/

-- ── Zmiana hasła (odpowiednik "Update Password")
/*
UPDATE users
SET    password = encode(digest('nowe_haslo', 'sha256'), 'hex')
WHERE  student_id = 's12345'
  AND  password   = encode(digest('stare_haslo', 'sha256'), 'hex');
*/

-- ── Statystyki dla My Profile (metryki Total / Upcoming / Unique Rooms)
/*
SELECT
    COUNT(*)                                          AS wszystkie_rezerwacje,
    COUNT(*) FILTER (WHERE booking_date >= CURRENT_DATE
                       AND cancelled_at IS NULL)      AS nadchodzace,
    COUNT(DISTINCT room_id)                           AS unikalne_sale
FROM bookings
WHERE student_id = 's12345';
*/
