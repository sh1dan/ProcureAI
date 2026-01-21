# Contributing to ProcureAI

Dziękujemy za zainteresowanie współtworzeniem ProcureAI! 🎉

## 📋 Jak przyczynić się do projektu / How to Contribute

### Zgłaszanie błędów / Reporting Bugs

1. Sprawdź, czy problem nie został już zgłoszony w [Issues](https://github.com/yourusername/ProcureAI/issues)
2. Jeśli nie, utwórz nowe issue z:
   - Opisem problemu
   - Krokami do reprodukcji
   - Oczekiwanym vs rzeczywistym zachowaniem
   - Informacjami o środowisku (OS, Python/Node wersje)

### Proponowanie funkcji / Suggesting Features

1. Sprawdź istniejące [Issues](https://github.com/yourusername/ProcureAI/issues)
2. Utwórz nowe issue z:
   - Opisem funkcji
   - Uzasadnieniem, dlaczego byłaby przydatna
   - Przykładami użycia

### Pull Requests

1. **Fork** repozytorium
2. Utwórz **branch** dla swojej funkcji (`git checkout -b feature/AmazingFeature`)
3. **Commit** zmiany (`git commit -m 'Add some AmazingFeature'`)
4. **Push** do brancha (`git push origin feature/AmazingFeature`)
5. Otwórz **Pull Request**

## 🔧 Rozwój / Development

### Setup środowiska deweloperskiego

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Style kodu / Code Style

**Python:**
- Używaj PEP 8
- Dodawaj docstringi do funkcji i klas
- Maksymalna długość linii: 100 znaków

**JavaScript/React:**
- Używaj ESLint (jeśli skonfigurowany)
- Preferuj funkcjonalne komponenty
- Używaj const/let zamiast var

### Testy / Testing

Przed wysłaniem PR upewnij się, że:
- Kod działa lokalnie
- Nie ma błędów lintowania
- API działa poprawnie
- Frontend renderuje się bez błędów

## 📝 Commit Messages

Używaj opisowych commit messages:

```
feat: Add new prediction endpoint
fix: Fix CORS configuration
docs: Update README with installation steps
refactor: Improve model loading performance
```

## 🎯 Priorytety rozwoju / Development Priorities

1. **Poprawa dokładności modelu** - Trening na rzeczywistych danych
2. **Rozszerzenie API** - Więcej endpointów i funkcji
3. **Optymalizacja** - Lepsza wydajność i skalowalność
4. **Dokumentacja** - Rozszerzenie dokumentacji API
5. **Testy** - Dodanie testów jednostkowych i integracyjnych

## ❓ Pytania / Questions

Jeśli masz pytania, utwórz issue z tagiem `question` lub skontaktuj się z maintainerami.

Dziękujemy za wkład! 🙏

