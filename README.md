# Michał Szymański & Julian Pulawski c31

# GradeFlow: Dziennik Nauczyciela

## Wymagania projektowe

- Dodanie/usuwanie/edycja ucznia z imieniem, nazwiskiem i PESELEM  
- Sprawdzanie listy obecności (obecny, nieobecny, usprawiedliwiony, spóźniony)  
- Wystawianie ocen za: pracę domową, kartkówki, sprawdziany  
- Edycja ocen i obecności w danym dniu  
- Podgląd ocen i obecności wybranego ucznia  
- Wystawianie zagrożeń (więcej niż 2 nieobecności, spóźnienia na połowie lekcji, średnia < 3)  
- Metoda obliczająca średnią ucznia  
- Metoda sprawdzająca status ucznia (zagrożony / niezagrożony)  
- Generowanie raportów z ocen i obecności (XLSX)  
- Generowanie statystyk i wykresów 
- Przykładowy dziennik 
- Obsługa wyjątków  
- Prosty interfejs użytkownika  

---

## Rozszerzenia projektu

Aby zwiększyć funkcjonalność projektu i uczynić go bardziej nowoczesnym, projekt zostanie rozbudowany o:

### Webowy interfejs (Flask)
- Formularze do zarządzania uczniami, ocenami, obecnością  
- Strony z przeglądem ocen, obecności i statusów  
- Łatwiejsza obsługa niż interfejs tekstowy

### Baza danych (SQLite)
- Przechowywanie danych uczniów, ocen i obecności  
- Zmiana z przechowywania danych w pamięci na trwałą bazę danych  
- Wygodna integracja z SQLAlchemy (ORM)

### Statystyki i analiza danych
- Średnie ocen uczniów i klasy  
- Liczba nieobecności i spóźnień  
- Generowanie wykresów: słupkowe, kołowe, liniowe 
- Eksport do plików Excel (.xlsx)

### Obsługa wyjątków
- Nieprawidłowy PESEL  
- Duplikaty uczniów  
- Błędy formularzy (brak danych)  
- Błąd połączenia z bazą danych  
- Próby edycji/usunięcia nieistniejącego ucznia lub oceny  
- Próby dodania błędnego typu danych  
- Dzielenie przez 0 (np. brak ocen)  
- Operacje na pustej liście  
- Nieprawidłowy format daty  
- Próba eksportu raportu bez danych

---

## Technologie

- **Python 3.11**
- **Flask** – webowy framework
- **SQLite3 + SQLAlchemy** – baza danych i ORM
- **Jinja2** – szablony HTML
- **WTForms** – formularze
- **Openpyxl** – eksport danych do Excel
- **Bootstrap** – estetyczny interfejs użytkownika

