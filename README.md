# OrangePi2026 — LyceumTV 3.7.5 для Orange Pi PC

Інформаційний TV: розклад, оголошення, тривоги, фото, відео та музика. Цільова платформа — **Orange Pi PC / Allwinner H3 / 1 ГБ RAM / armhf**, Armbian з Ubuntu 24.04+ або Debian 13+, Python 3.10+, systemd. Екран: Cage + WebKitGTK 6.0 / GTK4; медіа: GStreamer і PulseAudio.

Окремий проєкт на основі LyceumTV 3.7.5 для Orange Pi PC. Код, CI та джерело офіційних оновлень: [salenko93-hash/OrangePi2026](https://github.com/salenko93-hash/OrangePi2026). Збережено функції TV, адміністрації, медіа, розкладів, резервування та kiosk. Версію коду визначає [server/version.py](server/version.py).

**GitHub Release ще потрібно опублікувати:** для встановлення через Windows потрібні підтверджений тег, ZIP і SHA-256 у цьому репозиторії. Архів «Source code» від GitHub не замінює пакет, створений `tools/build_release.py`. Вихідний код можна перевіряти та збирати локально за інструкцією нижче. Походження й межі перевірки описані в [документі проєкту](docs/ORANGEPI2026.md).

## Встановлення й оновлення з Windows

1. Під’єднайте плату до Ethernet і визначте IPv4 через `ip -br addr`. Orange Pi PC не має вбудованого Wi-Fi. Потрібні SSH/sudo та Інтернет для пакетів ОС.
2. Отримайте й розпакуйте підтверджений офіційний ZIP у нову папку. Перед оновленням створіть backup в адмінпанелі.
3. Відкрийте PowerShell у папці пакета. Потрібні Python 3.10+ та Windows OpenSSH. Введіть фактичні адресу, SSH-користувача й підтверджений тег:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
$boardIP = Read-Host "Orange Pi IPv4"
$boardUser = Read-Host "SSH user"
$releaseTag = Read-Host "Confirmed release tag"
.\INSTALL_RELEASE_ORANGEPI.ps1 -BoardHost $boardIP -BoardUser $boardUser -Tag $releaseTag -CheckOnly
```

Це лише перевірка пакета й плати. Для prerelease додайте явний `-AllowPrerelease`. Якщо реліз або контрольні суми недоступні, зупиніться й уточніть публікацію в супроводжувача.

Лише після успішної перевірки встановіть або оновіть систему з тим самим тегом:

```powershell
$approvedVersion = Read-Host "Exact runtime version reported by check"
.\INSTALL_RELEASE_ORANGEPI.ps1 -BoardHost $boardIP -BoardUser $boardUser -Tag $releaseTag -ApproveVersion $approvedVersion
```

Для prerelease додайте `-AllowPrerelease` до обох команд. Не підставляйте тег або версію навмання. Деталі й відкат: [офіційні оновлення](docs/GITHUB_RELEASE_UPDATES.md).

Інсталятор перевіряє пакет і систему; для наявної інсталяції використовує транзакційне оновлення та backup. Локальні розклади, конфігурація, ключі й медіа зберігаються. Автоматичного перезавантаження немає. `INSTALL_TO_ORANGEPI.ps1` делегує цьому інсталятору й без `-ApproveVersion` також лише перевіряє.

## Керування та обслуговування

Відкрийте `https://IP_ПЛАТИ/` (TV), `/admin` (адміністрація), `/ops` (медіа), `/teacher`, `/mobile/`, `/slideshow-preview` або `/api/health`. Довіряйте лише CA-сертифікату своєї плати; деталі — у [посібнику встановлення](docs/INSTALL_ORANGEPI.md).

Ключі генеруються на платі. Отримайте їх через SSH; перевірки стану запускаються окремо:

```powershell
ssh -t "${boardUser}@${boardIP}" "sudo /usr/local/sbin/lyceumtv-show-keys"
.\CHECK_ORANGEPI.ps1 -BoardHost $boardIP -BoardUser $boardUser
.\CHECK_SECURITY_ORANGEPI.ps1 -BoardHost $boardIP -BoardUser $boardUser
```

Не публікуйте ключі й API-токени. Порожні Manifest URL і Google Apps Script URL означають локальний режим синхронізації. Для тривог потрібен власний токен alerts.in.ua.

[FIX_KIOSK_ORANGEPI.ps1](FIX_KIOSK_ORANGEPI.ps1) та [HIDE_CURSOR_ORANGEPI.ps1](HIDE_CURSOR_ORANGEPI.ps1) змінюють налаштування екрана, але не оновлюють сервер. Передавайте фактичні `-BoardHost` і `-BoardUser`. Деталі ремонту та історичні спостереження HDMI/курсора — у [посібнику](docs/INSTALL_ORANGEPI.md) та [звіті попередньої версії](reports/validation.json).

## Межі підтримки

- Легкий профіль `?lite=1` зменшує ефекти. Звичайний запуск зберігає EDID-preferred режим; `--prefer-720p` вимагає явного вибору.
- Починайте з JPG до 1920×1080 та MP4 H.264/AAC 720p, 25–30 кадрів/с. Перекодування немає; важкі 1080p/4K можуть гальмувати.
- GPU/відеоприскорення не гарантується. Фізичні Orange Pi, HDMI, звук, курсор, холодний запуск і продуктивність цієї версії потребують перевірки. Статус hardware-ready не заявляється.
- ZIP містить код та інсталятор, а не образ SD-картки чи офлайн-пакети ОС.

Довідка: [адміністрація](docs/ADMIN.md), [слайдшоу](docs/AFTER_SCHOOL_SLIDESHOW.md), [безпека](docs/SECURITY.md), [backup/OTA](docs/RELIABILITY.md), [changelog](CHANGELOG.md).

## Перевірки та збирання

```bash
python -m pip install -r requirements.txt
python -B VERIFY_PROJECT.py
python -B tools/build_release.py
```

Використовуйте окреме Python-середовище. Node.js потрібен для JavaScript-перевірок; локальні Python/HTTP-тести не потребують GTK. Додаткові інструменти — у `requirements-dev.txt`. Після зміни kiosk helpers перегенеруйте repair: `python tools/build_kiosk_repair.py`.

CI у `.github/workflows/verify.yml` вихідного checkout налаштовано на `VERIFY_PROJECT.py` у Windows/Ubuntu з Python 3.12 і Node.js 22. Workflow не входить до ZIP, не публікує релізи й не звертається до плати; його наявність не означає успішного запуску. Актуальні локальні результати й неперевірені етапи — у [звіті аудиту](reports/RELEASE_CONSISTENCY.md); старі `reports/validation.json` і `reports/RELEASE_375_VERIFICATION.md` є історичними.
