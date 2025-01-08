# Line
line - bypass dpi

![dbca38664cb14af1](https://github.com/user-attachments/assets/04fecf40-67cc-49b4-b15d-1c09b51e3f81)

## Описание

Line — это удобный и простой в использовании инструмент, который поможет вам обойти DPI и улучшить доступ к YouTube. Программа предоставляет графический интерфейс для [zapret](https://github.com/bol-van/zapret), разработанной [bol-van](https://github.com/bol-van), и добавляет новые функции, такие как автозапуск, автообновление и уникальная система конфигов.

![Снимок экрана 2025-01-08 071445](https://github.com/user-attachments/assets/33292e6d-e330-49eb-a404-4c2f3134580b)

## Основные Функции

- **Автозапуск**: Line автоматически запускается вместе с Windows, так что вам не нужно каждый раз запускать программу вручную.
- **Автообновление**: Line сама проверяет обновления и устанавливает их, так что у вас всегда будет последняя версия.
- **Уникальная система конфигов**: Вы можете легко настроить параметры запуска winws.exe, основной части zapret, под свои нужды.
- **Графический интерфейс**: Красивый и интуитивно понятный интерфейс, написанный на PySide6.

## Установка

### Требования
- Python 3.10.6
- Библиотеки: PySide6, elevate, psutil, requests

### Установка из исходников

1. Скачайте исходный код с [GitHub репозитория](#).
2. Установите необходимые библиотеки:
   ```bash
   pip install -r requirements.txt
   ```
3. Запустите программу:
   ```bash
   python main.py
   ```

### Установка exe файла
1. Скачайте exe файл с релизов [GitHub репозитория](https://github.com/Read1dno/Line/releases/tag/v1.0.0).
2. Запустите скачанный exe файл.

## Безопасность
PyInstaller: Антивирусы могут жаловаться на exe файл, так как PyInstaller имеет сигнатуры, которые не нравятся антивирусам.
Виндрайвер: Моя программа загружает виндрайвер, необходимый для работы zapret, который может быть определен как вирус, хотя он безопасен.

## Техническая информация
После запуска программы в системной папке Temp создаться папка zapret в которой сгенерируются шрифты, картинки и конфиг. Вместе с этим с офф репа билда [zapret](https://github.com/bol-van/zapret-win-bundle) выкачется winws.exe и все файлы нужные для его работы.

## Ссылки
Буду рад если зайдете в мои:

[Discord](https://discord.gg/n89PDURbTg)

[Telegram](https://t.me/bloomofficialyt)

## Лицензия
Эта программа распространяется под лицензией MIT. Подробнее смотрите в файле LICENSE.
