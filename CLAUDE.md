# paithon brand

Il README dice cosa sta qui e come si consuma. Le prove:
`python3 -m unittest discover -s prove`.

Il repo è **pubblico**, e sito e libro lo montano come submodule. Qui va solo
quello che i consumatori servono già in pubblico: niente script, documenti o
template del sito privato, niente percorsi di una macchina, niente credenziali.

## Security review

- **A ogni push** `.githooks/pre-push` lancia la skill `security-review-range`
  esattamente su quello che si sta pushando. Blocca su HIGH/MEDIUM con
  confidenza ≥ 8/10, e anche quando la review non riesce a girare. Le aree
  sono in `.githooks/security-review-areas`, i report in
  `.git/security-reviews/`. Una volta per clone:
  `git config core.hooksPath .githooks`. Da una sessione Claude il push va
  lanciato in background, perché la review dura 3–10 minuti. Saltarla solo
  apposta, con l'ok di chi mantiene il repo: `SKIP_SECURITY_REVIEW=1 git push`.
- **Il brand non ha un deploy suo**: arriva ai lettori quando il sito o il
  libro aggiornano il submodule. Prima di quel deploy in produzione si lancia
  `/security-review-range <sha fissato dal consumatore>..<sha nuovo>`, sempre
  con l'intervallo esplicito. Il tag `deploy/prod-AAAA-MM-GG` lo mette il
  repo che va in produzione.
- **Cosa emerge**: un difetto nel nostro codice si corregge qui, con una
  prova in `prove/` che prima fallisce. I font sono di terzi (OFL): un difetto
  lì si segnala a chi li mantiene, mai una patch locale. Un difetto nell'uso
  del brand dentro sito o libro si corregge nel loro repo.
- Il test dell'hook: `bash prove/hook/pre_push_hook_test.sh`.
