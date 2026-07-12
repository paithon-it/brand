# Font

Tutte Google Fonts, free, caricate via CDN (nessun file self-hosted).

| Ruolo | Famiglia | Pesi | Note |
|---|---|---|---|
| Display / headline | **Fraunces** | 400, 600, 800 | Variable, optical sizing (`opsz 9..144`), italic disponibile |
| Body | **Inter** | 400, 500, 600 | |
| Mono / codice | **JetBrains Mono** | 400, 500, 600 | |

Le famiglie sono referenziate nei token come `--pt-font-display`,
`--pt-font-body`, `--pt-font-mono` (vedi `tokens.css`), con fallback di sistema.

## URL Google Fonts (css2, `display=swap`, subset `latin,latin-ext`)

```
https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..800;1,9..144,400..800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap&subset=latin,latin-ext
```
