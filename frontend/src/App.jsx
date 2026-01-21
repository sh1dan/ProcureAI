import { useEffect, useMemo, useState } from 'react';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000/api';
const PRESETS = {
  1: { VALUE_EURO: 50000, CAE_NAME: 'Urząd Miasta Warszawa', NUTS: 'PL911', TYPE_OF_CONTRACT: 'SERVICES' },
  2: { VALUE_EURO: 150000, CAE_NAME: 'Szpital Miejski', NUTS: 'PL911', TYPE_OF_CONTRACT: 'SUPPLIES' },
  3: { VALUE_EURO: 500000, CAE_NAME: 'Urząd Miasta', NUTS: 'PL911', TYPE_OF_CONTRACT: 'WORKS' },
};

const translations = {
  pl: {
    heroEyebrow: 'AI Procurement Copilot',
    heroTitle: 'ProcureAI',
    heroLead:
      'Klasyfikacja zamówień publicznych wspierana AI. Wprowadź podstawowe parametry przetargu, a my zaproponujemy najbardziej prawdopodobne kody CPV wraz z pewnością modelu.',
    modelLabel: 'Model',
    categoriesLabel: 'Kategorie',
    featuresLabel: 'Cechy',
    metaPredictionTime: 'Średni czas predykcji',
    metaUpdate: 'Aktualizacja',
    metaSecurity: 'Bezpieczeństwo',
    badgeVersion: 'Model v1.0',
    formEyebrow: 'Dane wejściowe',
    formTitle: 'Konfiguracja zapytania',
    formSubtitle: 'Dostosuj parametry zapytania, aby uzyskać rekomendowany kod CPV.',
    apiBadge: 'API: /predict',
    valueLabel: 'Wartość kontraktu (EUR)',
    valuePlaceholder: 'np. 250000',
    valueHelper: 'Im wyższa kwota, tym większa szansa na roboty lub duże dostawy.',
    caeLabel: 'Zamawiający (CAE_NAME)',
    nutsLabel: 'Lokalizacja (NUTS)',
    typeLabel: 'Typ kontraktu',
    submitIdle: 'Przewidź kod CPV',
    submitLoading: 'Przewidywanie...',
    presetsTitle: 'Gotowe scenariusze:',
    preset1: 'Usługi · 50k €',
    preset2: 'Dostawy · 150k €',
    preset3: 'Roboty · 500k €',
    footerInfo: 'Model gotowy do użycia. Dane syntetyczne: 15 kategorii CPV, 40 cech, 1000 rekordów.',
    resultEyebrow: 'Wynik predykcji',
    resultTitle: 'Najlepsze dopasowanie CPV',
    resultSubtitle: 'Poniżej znajdziesz ranking pięciu najbardziej prawdopodobnych kodów.',
    realtimeBadge: 'Realtime',
    loadingTitle: 'Analizujemy sygnały...',
    loadingSubtitle: 'Model oblicza rozkład prawdopodobieństw dla kodów CPV.',
    topResult: 'Top wynik',
    confidence: 'Pewność',
    tableTitle: 'Ranking Top 5',
    tableSubtitle: 'Kody uporządkowane wg malejącego prawdopodobieństwa.',
    thIndex: '#',
    thCpv: 'CPV',
    thProb: 'Prawdopodobieństwo',
    detailsSummary: 'Dane wejściowe',
    placeholderTitle: 'Wprowadź dane i kliknij „Przewidź”',
    placeholderSubtitle: 'Zobaczysz tutaj ranking kodów CPV wraz z pewnością modelu.',
    langLabel: 'Język',
  },
  en: {
    heroEyebrow: 'AI Procurement Copilot',
    heroTitle: 'ProcureAI CPV Predictor',
    heroLead:
      'AI-powered public procurement classification. Provide tender parameters and we will suggest the most likely CPV codes with confidence.',
    modelLabel: 'Model',
    categoriesLabel: 'Categories',
    featuresLabel: 'Features',
    metaPredictionTime: 'Avg prediction time',
    metaUpdate: 'Updates',
    metaSecurity: 'Security',
    badgeVersion: 'Model v1.0',
    formEyebrow: 'Input data',
    formTitle: 'Query configuration',
    formSubtitle: 'Tune the parameters to get a recommended CPV code.',
    apiBadge: 'API: /predict',
    valueLabel: 'Contract value (EUR)',
    valuePlaceholder: 'e.g. 250000',
    valueHelper: 'Higher amounts lean towards works or large supplies.',
    caeLabel: 'Contracting authority (CAE_NAME)',
    nutsLabel: 'Location (NUTS)',
    typeLabel: 'Contract type',
    submitIdle: 'Predict CPV code',
    submitLoading: 'Predicting...',
    presetsTitle: 'Ready scenarios:',
    preset1: 'Services · 50k €',
    preset2: 'Supplies · 150k €',
    preset3: 'Works · 500k €',
    footerInfo: 'Model ready. Synthetic data: 15 CPV categories, 40 features, 1000 records.',
    resultEyebrow: 'Prediction result',
    resultTitle: 'Best CPV match',
    resultSubtitle: 'Ranking of the five most probable codes.',
    realtimeBadge: 'Realtime',
    loadingTitle: 'Crunching signals...',
    loadingSubtitle: 'The model computes probability distribution for CPV codes.',
    topResult: 'Top result',
    confidence: 'Confidence',
    tableTitle: 'Top 5 ranking',
    tableSubtitle: 'Codes ordered by descending probability.',
    thIndex: '#',
    thCpv: 'CPV',
    thProb: 'Probability',
    detailsSummary: 'Input data',
    placeholderTitle: 'Enter data and click “Predict”',
    placeholderSubtitle: 'You will see the CPV ranking with model confidence here.',
    langLabel: 'Language',
  },
  ua: {
    heroEyebrow: 'AI Procurement Copilot',
    heroTitle: 'ProcureAI CPV Predictor',
    heroLead:
      'Класифікація державних закупівель за допомогою AI. Вкажіть параметри тендеру, і ми запропонуємо найімовірніші коди CPV разом з упевненістю моделі.',
    modelLabel: 'Модель',
    categoriesLabel: 'Категорії',
    featuresLabel: 'Ознаки',
    metaPredictionTime: 'Середній час передбачення',
    metaUpdate: 'Оновлення',
    metaSecurity: 'Безпека',
    badgeVersion: 'Model v1.0',
    formEyebrow: 'Вхідні дані',
    formTitle: 'Налаштування запиту',
    formSubtitle: 'Відкоригуйте параметри, щоб отримати рекомендований код CPV.',
    apiBadge: 'API: /predict',
    valueLabel: 'Вартість контракту (EUR)',
    valuePlaceholder: 'наприклад 250000',
    valueHelper: 'Вища сума підвищує шанс на роботи чи великі поставки.',
    caeLabel: 'Замовник (CAE_NAME)',
    nutsLabel: 'Локація (NUTS)',
    typeLabel: 'Тип контракту',
    submitIdle: 'Передбачити код CPV',
    submitLoading: 'Обробка...',
    presetsTitle: 'Готові сценарії:',
    preset1: 'Послуги · 50k €',
    preset2: 'Поставки · 150k €',
    preset3: 'Роботи · 500k €',
    footerInfo: 'Модель готова. Синтетичні дані: 15 категорій CPV, 40 ознак, 1000 записів.',
    resultEyebrow: 'Результат передбачення',
    resultTitle: 'Найкраще співпадіння CPV',
    resultSubtitle: 'Топ-5 найімовірніших кодів.',
    realtimeBadge: 'Realtime',
    loadingTitle: 'Аналізуємо сигнали...',
    loadingSubtitle: 'Модель розраховує розподіл ймовірностей для кодів CPV.',
    topResult: 'Топ результат',
    confidence: 'Впевненість',
    tableTitle: 'Рейтинг Top 5',
    tableSubtitle: 'Коди впорядковано за спаданням ймовірності.',
    thIndex: '#',
    thCpv: 'CPV',
    thProb: 'Ймовірність',
    detailsSummary: 'Вхідні дані',
    placeholderTitle: 'Введіть дані та натисніть «Передбачити»',
    placeholderSubtitle: 'Тут з’явиться рейтинг CPV із впевненістю моделі.',
    langLabel: 'Мова',
  },
};

const languageNames = { pl: 'PL', en: 'EN', ua: 'UA' };

/**
 * Root application shell handling model metadata, user inputs and CPV predictions.
 * Provides an end-to-end flow from data entry to displaying ranked CPV results.
 * @returns {JSX.Element} Fully rendered CPV predictor experience.
 */
export default function App() {
  const [lang, setLang] = useState('pl');
  const [view, setView] = useState('predictor'); // 'predictor' | 'docs' | 'status'
  const [modelInfo, setModelInfo] = useState(null);
  const [form, setForm] = useState({
    VALUE_EURO: 50000,
    CAE_NAME: '',
    NUTS: '',
    TYPE_OF_CONTRACT: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);
  const [cpvDict, setCpvDict] = useState({});
  const [apiHealthy, setApiHealthy] = useState(null);

  const t = translations[lang] || translations.pl;

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const path = window.location.pathname;
      if (path === '/docs') setView('docs');
      else if (path === '/status') setView('status');
    }

    const fetchInfo = async () => {
      try {
        setError('');
        const res = await fetch(`${API_BASE}/model-info`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Błąd ładowania model-info');
        setModelInfo(data);
        setForm((prev) => ({
          ...prev,
          CAE_NAME: data.cae_names?.[0] || '',
          NUTS: data.nuts_codes?.[0] || '',
          TYPE_OF_CONTRACT: data.contract_types?.[0] || '',
        }));
      } catch (e) {
        setError(e.message);
      }
    };
    fetchInfo();
  }, []);

  useEffect(() => {
    const fetchCpv = async () => {
      try {
        const res = await fetch('/cpv.json');
        if (!res.ok) throw new Error(`Cannot load CPV dictionary: ${res.status}`);
        const data = await res.json();
        if (data && typeof data === 'object') {
          setCpvDict(data);
          console.log(`CPV dictionary loaded: ${Object.keys(data).length} entries`);
        } else {
          console.warn('CPV dictionary invalid format');
        }
      } catch (err) {
        console.warn('CPV dictionary not loaded:', err);
      }
    };
    fetchCpv();
  }, []);

  useEffect(() => {
    const checkApiHealth = async () => {
      try {
        const res = await fetch(`${API_BASE}/model-info`);
        if (res.ok) {
          const data = await res.json();
          // Проверяем, что модель действительно загружена и данные валидны
          if (data && data.model_name && !data.error) {
            setApiHealthy(true);
          } else {
            setApiHealthy(false);
          }
        } else {
          setApiHealthy(false);
        }
      } catch (err) {
        setApiHealthy(false);
      }
    };
    
    // Проверяем при монтировании и при переходе на страницу статуса
    checkApiHealth();
    const interval = setInterval(checkApiHealth, 5000); // Проверка каждые 5 секунд
    return () => clearInterval(interval);
  }, [view]);

  const handleChange = (field) => (e) => {
    setForm((prev) => ({ ...prev, [field]: field === 'VALUE_EURO' ? Number(e.target.value) : e.target.value }));
  };

  const handlePreset = (preset) => () => {
    const v = PRESETS[preset];
    if (v) setForm(v);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (loading) return;
    try {
      setLoading(true);
      setError('');
      setResult(null);
      const res = await fetch(`${API_BASE}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (!res.ok || !data.success) throw new Error(data.error || 'Błąd predykcji');
      setResult(data.result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const top5 = useMemo(() => result?.top5 || [], [result]);
  const confidencePct = useMemo(() => (result ? (result.confidence * 100).toFixed(2) : null), [result]);
  const confidenceLevel = useMemo(() => {
    if (!result) return null;
    const pct = result.confidence * 100;
    if (pct >= 70) return 'high';
    if (pct >= 40) return 'medium';
    return 'low';
  }, [result]);

  const handleExample = () => handlePreset(1)();
  const switchView = (nextView) => {
    setView(nextView);
    if (typeof window !== 'undefined') {
      const path = nextView === 'predictor' ? '/' : `/${nextView}`;
      window.history.pushState({}, '', path);
    }
  };
  const getCpvDescription = (cpv) => {
    if (cpv == null) return '';
    const code = String(cpv);
    
    // If dictionary is not loaded yet, return placeholder
    if (!cpvDict || Object.keys(cpvDict).length === 0) {
      return lang === 'en'
        ? 'Description coming soon for this CPV.'
        : lang === 'ua'
          ? 'Опис для цього CPV невдовзі.'
          : 'Opis dla tego CPV w przygotowaniu.';
    }

    let entry = cpvDict[code];

    // If model returns CPV without checksum (8 digits), try to match CPV-<check_digit> from dictionary
    if (!entry && !code.includes('-') && code.length === 8) {
      for (let i = 0; i <= 9; i += 1) {
        const codeWithCheck = `${code}-${i}`;
        if (cpvDict[codeWithCheck]) {
          entry = cpvDict[codeWithCheck];
          break;
        }
      }
    }

    if (entry && typeof entry === 'object') {
      const preferred = entry[lang] || entry.en || entry.pl || '';
      // If text contains mojibake artefacts, gracefully fall back to EN version
      if (preferred && /[�Ã]/.test(preferred) && entry.en && preferred !== entry.en) {
        return entry.en;
      }
      return preferred || '';
    }
    return lang === 'en'
      ? 'Description coming soon for this CPV.'
      : lang === 'ua'
        ? 'Опис для цього CPV невдовзі.'
        : 'Opis dla tego CPV w przygotowaniu.';
  };

  return (
    <div className="shell">
      <div className="shell__bg" aria-hidden />
      <div className="lang-dock" aria-label={t.langLabel}>
        <div className="lang-switch">
          {Object.keys(languageNames).map((code) => (
            <button
              key={code}
              type="button"
              className={`lang-switch__btn ${lang === code ? 'is-active' : ''}`}
              onClick={() => setLang(code)}
            >
              {languageNames[code]}
            </button>
          ))}
        </div>
      </div>

      <div className="topbar">
        <div className="topbar__left">
          <button type="button" className="logo" onClick={() => switchView('predictor')}>
            ProcureAI
          </button>
          <nav className="topbar__links">
            <button
              type="button"
              className={`topbar__link ${view === 'docs' ? 'is-active' : ''}`}
              onClick={() => switchView('docs')}
            >
              Docs
            </button>
            <button
              type="button"
              className={`topbar__link ${view === 'status' ? 'is-active' : ''}`}
              onClick={() => switchView('status')}
            >
              API Status
            </button>
          </nav>
        </div>
      </div>

      {view === 'predictor' && (
      <header className="hero">
        <div className="hero__content">
          <h1>{t.heroTitle}</h1>
          <p className="hero__lead">{t.heroLead}</p>
          {modelInfo && (
            <div className="hero__stats" aria-label="Model stats">
              <div className="pill pill--primary">
                {t.modelLabel}: {modelInfo.model_name || 'CPVClassifier'}
              </div>
              <div className="pill">
                {t.categoriesLabel}: {modelInfo.num_categories}
              </div>
              <div className="pill">
                {t.featuresLabel}: {modelInfo.num_features}
              </div>
            </div>
          )}
        </div>
        <div className="hero__badge">{t.badgeVersion}</div>
      </header>
      )}

      {view === 'predictor' && (
      <main className="layout">
        <section className="panel panel--form">
          <div className="panel__header">
            <div>
              <p className="eyebrow">{t.formEyebrow}</p>
              <h2>{t.formTitle}</h2>
              <p className="muted">{t.formSubtitle}</p>
            </div>
            <div className="badge-soft">{t.apiBadge}</div>
          </div>

          <form className="form-grid" onSubmit={handleSubmit}>
            <div className="field">
              <label htmlFor="value">{t.valueLabel}</label>
              <div className="input-wrapper">
                <span className="input-prefix">€</span>
                <input
                  id="value"
                  type="number"
                  min="0"
                  step="1000"
                  value={form.VALUE_EURO}
                  onChange={handleChange('VALUE_EURO')}
                  required
                  placeholder={t.valuePlaceholder}
                />
              </div>
              <p className="helper">{t.valueHelper}</p>
            </div>

            <div className="field">
              <label htmlFor="cae">{t.caeLabel}</label>
              <select id="cae" aria-label={t.caeLabel} value={form.CAE_NAME} onChange={handleChange('CAE_NAME')} required>
                {(modelInfo?.cae_names || []).map((v) => (
                  <option key={v} value={v}>{v}</option>
                ))}
              </select>
            </div>

            <div className="field">
              <label htmlFor="nuts">{t.nutsLabel}</label>
              <select id="nuts" aria-label={t.nutsLabel} value={form.NUTS} onChange={handleChange('NUTS')} required>
                {(modelInfo?.nuts_codes || []).map((v) => (
                  <option key={v} value={v}>{v}</option>
                ))}
              </select>
            </div>

            <div className="field">
              <label htmlFor="type">{t.typeLabel}</label>
              <select id="type" aria-label={t.typeLabel} value={form.TYPE_OF_CONTRACT} onChange={handleChange('TYPE_OF_CONTRACT')} required>
                {(modelInfo?.contract_types || []).map((v) => (
                  <option key={v} value={v}>{v}</option>
                ))}
              </select>
            </div>

            <div className="form-actions">
              <button className="btn primary" type="submit" disabled={loading}>
                {loading ? t.submitLoading : t.submitIdle}
              </button>
            </div>
          </form>

          {modelInfo && (
            <div className="panel__footer">
              {t.footerInfo}
            </div>
          )}
        </section>

        <section className="panel panel--results">
          <div className="panel__header">
            <div>
              <p className="eyebrow">{t.resultEyebrow}</p>
              <h2>{t.resultTitle}</h2>
              <p className="muted">{t.resultSubtitle}</p>
            </div>
          </div>

          {error ? (
            <div className="alert alert--error">❌ {error}</div>
          ) : loading ? (
            <div className="skeleton">
              <div className="skeleton__header">
                <div className="skeleton__pill" />
                <div className="skeleton__pill small" />
              </div>
              <div className="skeleton__bars">
                <div className="bar wide" />
                <div className="bar" />
                <div className="bar" />
              </div>
              <div className="skeleton__table">
                {[1, 2, 3, 4, 5].map((i) => (
                  <div key={i} className="row">
                    <span className="dot" />
                    <div className="bar short" />
                  </div>
                ))}
              </div>
            </div>
          ) : result ? (
            <div className="result">
              <div className="result__headline">
                <div>
                  <p className="eyebrow">{t.topResult}</p>
                  <div className="result__code">
                    <span className="result__badge">Top match</span>
                    CPV {result.cpv}
                  </div>
                  <p className="muted small" title={getCpvDescription(result.cpv)}>
                    {getCpvDescription(result.cpv)}
                  </p>
                </div>
                <div className="confidence">
                  <span className="confidence__label">{t.confidence}</span>
                  <span className="confidence__value">{confidencePct}%</span>
                  <span className={`confidence__level ${confidenceLevel || ''}`}>
                    {confidenceLevel === 'high' && 'High confidence'}
                    {confidenceLevel === 'medium' && 'Medium confidence'}
                    {confidenceLevel === 'low' && 'Lower confidence'}
                  </span>
                  <div className="confidence__bar"><div style={{ width: `${confidencePct}%` }} /></div>
                </div>
              </div>

              <div className="table-card">
                <div className="table-card__header">
                  <h3>{t.tableTitle}</h3>
                  <p className="muted">{t.tableSubtitle}</p>
                </div>
                <table className="table">
                  <thead>
                    <tr>
                      <th>{t.thIndex}</th>
                      <th aria-label="CPV column">{t.thCpv}</th>
                      <th>{t.thProb}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {top5.map((r, i) => (
                      <tr key={r.cpv}>
                        <td>{i + 1}</td>
                        <td title={getCpvDescription(r.cpv)}>
                          <strong>{r.cpv}</strong>
                          <div className="muted tiny">{getCpvDescription(r.cpv)}</div>
                        </td>
                        <td><span className="tag">{(r.probability * 100).toFixed(2)}%</span></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <details className="details">
                <summary>{t.detailsSummary}</summary>
                <pre>{JSON.stringify(form, null, 2)}</pre>
              </details>
            </div>
          ) : (
            <div className="placeholder">
              <div className="placeholder__icon">✨</div>
              <div>
                <strong>{t.placeholderTitle}</strong>
                <p className="muted">{t.placeholderSubtitle}</p>
              </div>
            </div>
          )}
        </section>
      </main>
      )}

      {view === 'docs' && (
        <main className="layout layout--single">
          <section className="panel">
            <div className="panel__header">
              <div>
                <p className="eyebrow">API Documentation</p>
                <h2>Integracja z modelem CPV</h2>
                <p className="muted">Minimalne REST API do wykorzystania modelu klasyfikacji CPV w Twoich systemach.</p>
              </div>
            </div>
            <div className="docs">
              <div className="docs__base">
                <span className="docs__label">Base URL</span>
                <code className="docs__base-url">http://localhost:5000/api</code>
              </div>

              <div className="docs__endpoint">
                <div className="docs__endpoint-header">
                  <span className="docs__method docs__method--get">GET</span>
                  <h3 className="docs__endpoint-path">/model-info</h3>
                </div>
                <p className="docs__description">Zwraca metadane modelu: listę CAE, NUTS, typów kontraktów oraz liczbę cech/kategorii.</p>
                <div className="docs__example">
                  <span className="docs__example-label">Response 200</span>
                  <pre className="docs__code">
{`{
  "model_name": "CPVClassifier",
  "num_categories": 15,
  "num_features": 40,
  "cae_names": [
    "Gmina Białystok",
    "Urząd Miasta Warszawa",
    ...
  ],
  "nuts_codes": [
    "PL113",
    "PL911",
    ...
  ],
  "contract_types": [
    "SERVICES",
    "SUPPLIES",
    "WORKS"
  ]
}`}
                  </pre>
                </div>
              </div>

              <div className="docs__endpoint">
                <div className="docs__endpoint-header">
                  <span className="docs__method docs__method--post">POST</span>
                  <h3 className="docs__endpoint-path">/predict</h3>
                </div>
                <p className="docs__description">Główny endpoint predykcji. Zwraca najlepszy kod CPV oraz ranking Top 5.</p>
                <div className="docs__example">
                  <span className="docs__example-label">Request Body</span>
                  <pre className="docs__code">
{`{
  "VALUE_EURO": 50000,
  "CAE_NAME": "Gmina Białystok",
  "NUTS": "PL113",
  "TYPE_OF_CONTRACT": "SERVICES"
}`}
                  </pre>
                </div>
                <div className="docs__example">
                  <span className="docs__example-label">Response 200</span>
                  <pre className="docs__code">
{`{
  "success": true,
  "result": {
    "cpv": "75000000",
    "confidence": 0.83,
    "top5": [
      {
        "cpv": "75000000",
        "probability": 0.83
      },
      {
        "cpv": "85000000",
        "probability": 0.12
      },
      ...
    ]
  }
}`}
                  </pre>
                </div>
              </div>
            </div>
          </section>
        </main>
      )}

      {view === 'status' && (
        <main className="layout layout--single">
          <section className="panel">
            <div className="panel__header">
              <div>
                <p className="eyebrow">API Status</p>
                <h2>Stan usługi predykcyjnej</h2>
                <p className="muted">Podgląd kondycji backendu, wersji modelu i ostatnich aktualizacji.</p>
              </div>
              <div className={`badge-soft ${apiHealthy === true ? 'badge-soft--ok' : apiHealthy === false ? 'badge-soft--error' : 'badge-soft--neutral'}`}>
                <span className={`dot ${apiHealthy === true ? 'pulse' : ''}`} style={{ background: apiHealthy === true ? '#7cf1d5' : apiHealthy === false ? '#f87171' : '#9ca3af' }} />
                Live status
              </div>
            </div>
            <div className="status-grid">
              <div className="status-card">
                <span className="meta-label">Model</span>
                <div style={{ display: 'flex', alignItems: 'baseline', gap: '10px', flexWrap: 'wrap' }}>
                  <strong>{modelInfo ? `${modelInfo.model_name || 'CPVClassifier'} v${modelInfo.version || '1.0'}` : 'CPVClassifier v1.0'}</strong>
                  <span className={`status-pill ${apiHealthy === true ? 'status-pill--ok' : apiHealthy === false ? 'status-pill--error' : ''}`}>
                    {apiHealthy === true ? 'Healthy' : apiHealthy === false ? 'Unavailable' : 'Checking...'}
                  </span>
                </div>
              </div>
              <div className="status-card">
                <span className="meta-label">Średni czas predykcji</span>
                <strong>~120 ms</strong>
              </div>
              <div className="status-card">
                <span className="meta-label">Kategorie CPV</span>
                <strong>{modelInfo ? modelInfo.num_categories || 15 : 15}</strong>
              </div>
              <div className="status-card">
                <span className="meta-label">Cechy modelu</span>
                <strong>{modelInfo ? modelInfo.num_features || 40 : 40}</strong>
              </div>
            </div>
            <div className="status-footer muted">
              Ta strona ma charakter informacyjny dla demo. W środowisku produkcyjnym
              możesz podpiąć tutaj realne metryki (Prometheus, Grafana, Sentry, itp.).
            </div>
          </section>
        </main>
      )}

    </div>
  );
}

