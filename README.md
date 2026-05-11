# OCR Desktop App

Prosta desktopowa aplikacja w Pythonie do odczytu tekstu z obrazów i zapisania wyniku do pliku `.txt`.

## Cel projektu

Aplikacja ma przyspieszyć ręczne przepisywanie danych z dokumentów, np. faktur, skanów lub zdjęć.

## MVP

- Wybór pliku graficznego z dysku.
- Obsługa drag & drop.
- Odczyt tekstu z obrazu przy użyciu OCR.
- Wyświetlenie rozpoznanego tekstu.
- Możliwość edycji tekstu.
- Zapis wyniku do pliku `.txt`.

## Funkcjonalność

- Lokalna analiza obrazu.
- Eksport rozpoznanego tekstu do pliku.
- Walidacja plików i obsługa błędów.
- Brak bazy danych w wersji MVP.

## Technologie

- Python
- PySide6
- Tesseract OCR
- pytesseract

## Wymagania

- Python 3.11
- `uv`
- Zainstalowany silnik Tesseract OCR dostępny w systemie `PATH`

## Instalacja zależności

```bash
uv sync
```

## Uruchomienie

```bash
uv run python main.py
```

## Plan rozwoju

- Lepsza preprocesacja obrazu przed OCR.
- Obsługa PDF.
- Wsparcie wielu języków.
- Historia rozpoznanych plików.