# AI Chatbot Knowledge Base Builder

Этот проект предназначен для автоматизированной обработки транскриптов с YouTube-видео и формирования базы знаний в формате, пригодном для RAG или структурированного поиска.

## 🔧 Что делает скрипт

- Загружает `.txt` транскрипты видео с таймкодами
- Прогоняет каждый файл через LLM (DeepSeek Prover v2)
- Формирует для каждого видео:
  - `topic` — заголовок темы
  - `keywords` — ключевые слова
  - `summary` — краткое описание
  - `text` — связный и чистый текст
  - `fragments` — важные моменты с таймкодами и ссылками на YouTube
- Автоматически исправляет и форматирует YouTube URL в соответствии с ID видео

## 🗂 Структура проекта

ai_chatbot_project/
├── process.py # Основной скрипт обработки
├── fix_youtube_urls.py # Скрипт для исправления YouTube URL
├── transcripts/ # Папка с .txt транскриптами
├── raw_outputs/ # Результаты обработки (по 1 файлу на видео)
├── .env # Ключ OpenRouter API
├── requirements.txt # Зависимости
└── README.md # Описание проекта

## 🚀 Как запустить

1. Установи зависимости:
```bash
pip install -r requirements.txt
```

2. Укажи свой API-ключ OpenRouter в .env:
```
OPENROUTER_API_KEY=sk-...
```

3. Помести .txt файлы в папку transcripts/

4. Запусти обработку:
```bash
python process.py
```

5. После обработки, для исправления YouTube URL запусти:
```bash
python fix_youtube_urls.py
```

## 🔄 Дополнительные возможности
- Скрипт `fix_youtube_urls.py` автоматически:
  - Извлекает ID видео из имени файла
  - Исправляет формат URL в файлах результатов
  - Поддерживает различные форматы имен файлов
  - Ведет лог обработки для отладки
  
[Оригинальный репозиторий](https://github.com/AlexandrNizkovskih/ai-chatbot-processor/tree/main)
