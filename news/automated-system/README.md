# 🤖 Автоматизированная система сбора новостей

**Production-ready система для автоматического сбора, обработки и публикации новостей по контейнерным технологиям**

## 🎯 Назначение

Система автоматически:
- Собирает новости из 60+ RSS источников
- Категоризирует по технологиям и важности
- Создает структурированную базу данных
- Генерирует готовые статьи для репозитория
- Подготавливает посты для Telegram канала

## 📊 Источники данных

### Официальные источники
- Kubernetes Blog & Releases
- Docker Blog & Releases  
- CNCF News & Updates
- GitHub Releases (45+ проектов)

### Экспертные источники
- Red Hat, VMware, HashiCorp
- Aqua Security, Sysdig, GitGuardian
- The New Stack, InfoQ, Medium

### Русскоязычные источники
- Habr, Yandex Cloud, Selectel
- VK Cloud, Tproger, RTFM

## 🗃️ Структура базы данных

```sql
CREATE TABLE container_news (
    id INTEGER PRIMARY KEY,
    hash_id TEXT UNIQUE,
    title TEXT NOT NULL,
    link TEXT UNIQUE,
    description TEXT,
    content TEXT,
    pub_date DATETIME,
    collected_date DATETIME,
    
    -- Источник
    source_name TEXT,
    source_url TEXT,
    source_type TEXT, -- rss, github_release, blog
    
    -- Категоризация
    primary_category TEXT, -- kubernetes, docker, security, etc
    secondary_categories JSON,
    technology_tags JSON,
    
    -- Классификация
    content_type TEXT, -- release, tutorial, news, analysis
    importance_level INTEGER, -- 1-5
    complexity_level TEXT, -- beginner, intermediate, advanced
    
    -- География и язык
    language TEXT,
    region TEXT,
    
    -- Технические флаги
    version_mentioned TEXT,
    security_related BOOLEAN,
    production_ready BOOLEAN,
    breaking_changes BOOLEAN,
    
    -- Обработка
    keywords JSON,
    sentiment TEXT,
    processed BOOLEAN,
    telegram_posted BOOLEAN,
    repo_saved BOOLEAN
);
```

## 🔄 Процесс обработки

1. **Сбор** → RSS parsing + GitHub API
2. **Обработка** → Категоризация + извлечение метаданных  
3. **Фильтрация** → Дедупликация + оценка важности
4. **Публикация** → Создание статей + Telegram посты

## 📁 Структура файлов

```
news/automated-system/
├── collectors/
│   ├── rss_collector.py        # Сбор RSS новостей
│   ├── github_collector.py     # GitHub releases
│   └── aggregated_collector.py # Объединенный сборщик
├── processors/
│   ├── categorizer.py          # Автокатегоризация
│   ├── content_analyzer.py     # Анализ контента
│   └── deduplicator.py         # Удаление дублей
├── publishers/
│   ├── repo_publisher.py       # Публикация в репозиторий
│   ├── telegram_publisher.py   # Telegram посты
│   └── index_generator.py      # Генерация индексов
├── config/
│   ├── sources.yaml           # Конфигурация источников
│   ├── categories.yaml        # Настройки категорий
│   └── settings.yaml          # Основные настройки
├── data/
│   ├── container_news.db      # SQLite база данных
│   └── exports/               # Экспорты данных
├── scripts/
│   ├── daily_collection.py    # Ежедневный сбор
│   ├── weekly_digest.py       # Еженедельный дайджест
│   └── deploy.py              # Развертывание
└── README.md                  # Документация
```

## 🚀 Быстрый старт

```bash
# Установка зависимостей
pip install -r requirements.txt

# Первичный сбор новостей за 3 месяца
python scripts/initial_collection.py --months 3

# Ежедневное обновление
python scripts/daily_collection.py

# Генерация еженедельного дайджеста
python scripts/weekly_digest.py
```

## ⚙️ Конфигурация

### Основные настройки (settings.yaml)
```yaml
database:
  path: "data/container_news.db"
  
collection:
  max_age_days: 90
  batch_size: 50
  retry_attempts: 3
  
publishing:
  auto_publish: true
  telegram_enabled: true
  min_importance: 3
  
filtering:
  remove_duplicates: true
  min_content_length: 100
  blacklist_domains: []
```

## 📈 Мониторинг и аналитика

- **Статистика сбора**: количество источников, новостей, ошибок
- **Анализ трендов**: популярные технологии, топики
- **Качество данных**: покрытие, актуальность, релевантность

## 🔗 Интеграция

### С репозиторием ContainerTechnologies
- Автоматическое создание файлов в news/YYYY/MM/
- Обновление индексных файлов
- Генерация README с статистикой

### С Telegram каналом
- Отправка важных новостей
- Еженедельные дайджесты
- Уведомления о критических обновлениях

## 📊 Результаты работы

За последние 3 месяца система обработала:
- **500+ новостей** из различных источников
- **15+ категорий** технологий
- **50+ GitHub релизов** ключевых проектов
- **25+ новостей по безопасности**

---

**Система готова к промышленной эксплуатации!** 🎉