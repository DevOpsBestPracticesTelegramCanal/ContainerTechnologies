#!/usr/bin/env python3
"""
Production Container Technologies News Collector
Промышленная система сбора новостей по контейнерным технологиям
"""

import feedparser
import requests
import json
import sqlite3
import hashlib
import re
import asyncio
import aiohttp
import logging
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Set
from pathlib import Path
import yaml
import time
from urllib.parse import urlparse

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/production_collector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ProductionNewsItem:
    """Структура новости для промышленной системы"""
    # Основные поля
    title: str
    link: str
    description: str
    content: str
    pub_date: datetime
    collected_date: datetime
    
    # Метаданные источника
    source_name: str
    source_url: str
    source_type: str
    source_importance: int
    
    # Категоризация
    primary_category: str
    secondary_categories: List[str]
    technology_tags: List[str]
    
    # Классификация контента
    content_type: str
    importance_level: int
    complexity_level: str
    
    # Географические и языковые метки
    language: str
    region: str
    
    # Технические метки
    version_mentioned: Optional[str]
    security_related: bool
    production_ready: bool
    breaking_changes: bool
    
    # Системные поля
    hash_id: str
    keywords: List[str]
    sentiment: str
    
    # Статусы обработки
    processed: bool = False
    telegram_ready: bool = False
    repo_ready: bool = False

class ProductionNewsCollector:
    """Промышленная система сбора новостей"""
    
    def __init__(self, config_path: str = "config/production_config.yaml"):
        """Инициализация коллектора"""
        self.config_path = Path(config_path)
        self.config = self.load_config()
        self.db_path = Path(self.config['database']['path'])
        self.init_database()
        
        # Загрузка источников и настроек
        self.sources = self.load_sources()
        self.categories = self.load_categories()
        self.keywords = self.load_keywords()
        
        # Статистика
        self.stats = {
            'sources_processed': 0,
            'news_collected': 0,
            'errors': 0,
            'duplicates_skipped': 0
        }
        
        logger.info("ProductionNewsCollector инициализирован")

    def load_config(self) -> Dict:
        """Загрузка производственной конфигурации"""
        if not self.config_path.exists():
            return self.create_production_config()
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def create_production_config(self) -> Dict:
        """Создание производственной конфигурации"""
        config = {
            'database': {
                'path': 'data/production_container_news.db'
            },
            'collection': {
                'months_history': 3,
                'max_concurrent': 10,
                'timeout_seconds': 30,
                'retry_attempts': 3,
                'delay_between_requests': 1
            },
            'processing': {
                'auto_categorize': True,
                'extract_versions': True,
                'sentiment_analysis': False,
                'keyword_extraction': True,
                'remove_duplicates': True
            },
            'publishing': {
                'auto_publish_repo': True,
                'auto_publish_telegram': False,
                'min_importance_repo': 2,
                'min_importance_telegram': 4
            },
            'filters': {
                'min_content_length': 50,
                'max_content_length': 10000,
                'blacklist_domains': ['spam.example.com'],
                'required_keywords': [],
                'excluded_keywords': ['advertisement', 'sponsored']
            }
        }
        
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        
        return config

    def init_database(self):
        """Инициализация производственной БД"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS production_news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hash_id TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    link TEXT UNIQUE NOT NULL,
                    description TEXT,
                    content TEXT,
                    pub_date TEXT NOT NULL,
                    collected_date TEXT NOT NULL,
                    
                    -- Source metadata
                    source_name TEXT NOT NULL,
                    source_url TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    source_importance INTEGER NOT NULL,
                    
                    -- Categorization
                    primary_category TEXT NOT NULL,
                    secondary_categories TEXT, -- JSON array
                    technology_tags TEXT,      -- JSON array
                    
                    -- Content classification
                    content_type TEXT NOT NULL,
                    importance_level INTEGER NOT NULL,
                    complexity_level TEXT NOT NULL,
                    
                    -- Geographic and language
                    language TEXT NOT NULL,
                    region TEXT NOT NULL,
                    
                    -- Technical flags
                    version_mentioned TEXT,
                    security_related BOOLEAN NOT NULL DEFAULT 0,
                    production_ready BOOLEAN NOT NULL DEFAULT 0,
                    breaking_changes BOOLEAN NOT NULL DEFAULT 0,
                    
                    -- Keywords and sentiment
                    keywords TEXT,             -- JSON array
                    sentiment TEXT NOT NULL DEFAULT 'neutral',
                    
                    -- Processing status
                    processed BOOLEAN NOT NULL DEFAULT 0,
                    telegram_ready BOOLEAN NOT NULL DEFAULT 0,
                    repo_ready BOOLEAN NOT NULL DEFAULT 0,
                    
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Создание индексов для производительности
            indices = [
                'CREATE INDEX IF NOT EXISTS idx_prod_pub_date ON production_news(pub_date)',
                'CREATE INDEX IF NOT EXISTS idx_prod_category ON production_news(primary_category)',
                'CREATE INDEX IF NOT EXISTS idx_prod_importance ON production_news(importance_level)',
                'CREATE INDEX IF NOT EXISTS idx_prod_source ON production_news(source_name)',
                'CREATE INDEX IF NOT EXISTS idx_prod_language ON production_news(language)',
                'CREATE INDEX IF NOT EXISTS idx_prod_security ON production_news(security_related)',
                'CREATE INDEX IF NOT EXISTS idx_prod_processed ON production_news(processed)',
                'CREATE INDEX IF NOT EXISTS idx_prod_hash ON production_news(hash_id)'
            ]
            
            for idx in indices:
                conn.execute(idx)
            
            conn.commit()

    def load_sources(self) -> List[Dict]:
        """Загрузка полного списка источников для промышленной системы"""
        return [
            # Kubernetes Ecosystem - Official
            {
                'name': 'Kubernetes Official Blog',
                'url': 'https://kubernetes.io/feed.xml',
                'type': 'blog',
                'language': 'en',
                'region': 'global',
                'importance': 5,
                'category': 'kubernetes'
            },
            {
                'name': 'Kubernetes Releases',
                'url': 'https://github.com/kubernetes/kubernetes/releases.atom',
                'type': 'github_release',
                'language': 'en',
                'region': 'global',
                'importance': 5,
                'category': 'kubernetes'
            },
            {
                'name': 'CNCF Blog',
                'url': 'https://www.cncf.io/feed/',
                'type': 'blog',
                'language': 'en',
                'region': 'global',
                'importance': 5,
                'category': 'kubernetes'
            },
            
            # Docker Ecosystem
            {
                'name': 'Docker Official Blog',
                'url': 'https://www.docker.com/blog/feed/',
                'type': 'blog',
                'language': 'en',
                'region': 'global',
                'importance': 4,
                'category': 'docker'
            },
            {
                'name': 'Docker CE Releases',
                'url': 'https://github.com/docker/docker-ce/releases.atom',
                'type': 'github_release',
                'language': 'en',
                'region': 'global',
                'importance': 4,
                'category': 'docker'
            },
            
            # Container Runtimes
            {
                'name': 'containerd Releases',
                'url': 'https://github.com/containerd/containerd/releases.atom',
                'type': 'github_release',
                'language': 'en',
                'region': 'global',
                'importance': 4,
                'category': 'runtime'
            },
            {
                'name': 'Podman Releases',
                'url': 'https://github.com/containers/podman/releases.atom',
                'type': 'github_release',
                'language': 'en',
                'region': 'global',
                'importance': 4,
                'category': 'podman'
            },
            
            # Security
            {
                'name': 'Aqua Security Blog',
                'url': 'https://blog.aquasec.com/feed',
                'type': 'blog',
                'language': 'en',
                'region': 'global',
                'importance': 4,
                'category': 'security'
            },
            {
                'name': 'Sysdig Blog',
                'url': 'https://sysdig.com/feed/',
                'type': 'blog',
                'language': 'en',
                'region': 'global',
                'importance': 4,
                'category': 'security'
            },
            
            # Monitoring & Observability
            {
                'name': 'Prometheus Releases',
                'url': 'https://github.com/prometheus/prometheus/releases.atom',
                'type': 'github_release',
                'language': 'en',
                'region': 'global',
                'importance': 4,
                'category': 'monitoring'
            },
            {
                'name': 'Grafana Releases',
                'url': 'https://github.com/grafana/grafana/releases.atom',
                'type': 'github_release',
                'language': 'en',
                'region': 'global',
                'importance': 4,
                'category': 'monitoring'
            },
            
            # Service Mesh
            {
                'name': 'Istio Releases',
                'url': 'https://github.com/istio/istio/releases.atom',
                'type': 'github_release',
                'language': 'en',
                'region': 'global',
                'importance': 4,
                'category': 'service-mesh'
            },
            {
                'name': 'Cilium Releases',
                'url': 'https://github.com/cilium/cilium/releases.atom',
                'type': 'github_release',
                'language': 'en',
                'region': 'global',
                'importance': 4,
                'category': 'networking'
            },
            
            # WebAssembly
            {
                'name': 'WasmEdge Releases',
                'url': 'https://github.com/WasmEdge/WasmEdge/releases.atom',
                'type': 'github_release',
                'language': 'en',
                'region': 'global',
                'importance': 3,
                'category': 'webassembly'
            },
            
            # Industry News
            {
                'name': 'The New Stack Kubernetes',
                'url': 'https://thenewstack.io/kubernetes/feed/',
                'type': 'news',
                'language': 'en',
                'region': 'global',
                'importance': 3,
                'category': 'kubernetes'
            },
            {
                'name': 'InfoQ Kubernetes',
                'url': 'https://www.infoq.com/Kubernetes/rss',
                'type': 'news',
                'language': 'en',
                'region': 'global',
                'importance': 3,
                'category': 'kubernetes'
            },
            
            # Russian Sources
            {
                'name': 'Habr Kubernetes',
                'url': 'https://habr.com/ru/rss/search/?q=kubernetes+k8s&target_type=posts',
                'type': 'blog',
                'language': 'ru',
                'region': 'russia',
                'importance': 3,
                'category': 'kubernetes'
            },
            {
                'name': 'Habr Docker',
                'url': 'https://habr.com/ru/rss/search/?q=docker+контейнеры&target_type=posts',
                'type': 'blog',
                'language': 'ru',
                'region': 'russia',
                'importance': 3,
                'category': 'docker'
            },
            {
                'name': 'Yandex Cloud Blog',
                'url': 'https://cloud.yandex.ru/blog/rss',
                'type': 'blog',
                'language': 'ru',
                'region': 'russia',
                'importance': 3,
                'category': 'cloud'
            }
        ]

    def load_categories(self) -> Dict:
        """Конфигурация категорий для промышленной системы"""
        return {
            'primary_categories': {
                'kubernetes': ['k8s', 'kubernetes', 'kubectl', 'helm', 'kustomize'],
                'docker': ['docker', 'dockerfile', 'docker-compose', 'buildx'],
                'podman': ['podman', 'buildah', 'skopeo', 'containers'],
                'security': ['security', 'vulnerability', 'cve', 'hardening', 'compliance'],
                'monitoring': ['monitoring', 'observability', 'prometheus', 'grafana', 'metrics'],
                'networking': ['networking', 'service-mesh', 'istio', 'linkerd', 'cilium'],
                'runtime': ['containerd', 'cri-o', 'runc', 'runtime'],
                'webassembly': ['wasm', 'webassembly', 'wasmedge', 'wasmtime'],
                'cicd': ['ci/cd', 'gitops', 'argocd', 'flux', 'tekton', 'jenkins'],
                'storage': ['storage', 'persistent-volume', 'csi', 'longhorn'],
                'edge': ['edge', 'k3s', 'kubeedge', 'iot'],
                'cloud': ['cloud', 'aws', 'azure', 'gcp', 'hybrid']
            },
            'content_types': {
                'release': ['release', 'version', 'changelog', 'update'],
                'tutorial': ['tutorial', 'guide', 'how-to', 'getting started', 'walkthrough'],
                'news': ['news', 'announcement', 'update', 'launched'],
                'analysis': ['analysis', 'benchmark', 'comparison', 'review', 'study'],
                'security': ['security', 'vulnerability', 'patch', 'fix', 'advisory']
            },
            'complexity_levels': {
                'beginner': ['getting started', 'introduction', 'basics', 'tutorial', 'beginner'],
                'intermediate': ['configuration', 'setup', 'deployment', 'guide'],
                'advanced': ['advanced', 'optimization', 'troubleshooting', 'deep dive'],
                'expert': ['enterprise', 'production', 'expert', 'architecture', 'internals']
            }
        }

    def load_keywords(self) -> Dict:
        """Ключевые слова для анализа"""
        return {
            'security_keywords': [
                'vulnerability', 'cve', 'security', 'exploit', 'patch', 'fix',
                'hardening', 'authentication', 'authorization', 'rbac',
                'уязвимость', 'безопасность', 'исправление'
            ],
            'production_keywords': [
                'production', 'enterprise', 'scale', 'performance',
                'optimization', 'best practices', 'sla', 'reliability',
                'продакшн', 'производство', 'оптимизация'
            ],
            'breaking_keywords': [
                'breaking change', 'deprecation', 'removal', 'incompatible',
                'migration required', 'breaking', 'deprecated'
            ],
            'version_patterns': [
                r'v?\d+\.\d+\.\d+',
                r'version\s+\d+\.\d+',
                r'release\s+\d+\.\d+',
                r'версия\s+\d+\.\d+'
            ]
        }

    async def collect_production_news(self, months: int = 3) -> List[ProductionNewsItem]:
        """Промышленный сбор новостей"""
        logger.info(f"Начинаем промышленный сбор новостей за {months} месяцев")
        
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=months * 30)
        all_news = []
        
        # Семафор для ограничения одновременных запросов
        semaphore = asyncio.Semaphore(self.config['collection']['max_concurrent'])
        
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.config['collection']['timeout_seconds'])
        ) as session:
            
            tasks = []
            for source in self.sources:
                task = self.process_source_with_semaphore(semaphore, session, source, cutoff_date)
                tasks.append(task)
            
            # Обработка всех источников параллельно
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Ошибка при обработке источника {self.sources[i]['name']}: {result}")
                    self.stats['errors'] += 1
                else:
                    all_news.extend(result)
                    logger.info(f"Источник {self.sources[i]['name']}: собрано {len(result)} новостей")
        
        # Удаление дубликатов
        unique_news = self.remove_duplicates(all_news)
        
        logger.info(f"Собрано {len(all_news)} новостей, уникальных: {len(unique_news)}")
        self.stats['news_collected'] = len(unique_news)
        self.stats['duplicates_skipped'] = len(all_news) - len(unique_news)
        
        return unique_news

    async def process_source_with_semaphore(self, semaphore, session, source, cutoff_date):
        """Обработка источника с семафором"""
        async with semaphore:
            self.stats['sources_processed'] += 1
            try:
                return await self.fetch_source_news_async(session, source, cutoff_date)
            except Exception as e:
                logger.error(f"Ошибка при обработке {source['name']}: {e}")
                return []

    async def fetch_source_news_async(self, session, source: Dict, cutoff_date: datetime) -> List[ProductionNewsItem]:
        """Асинхронное получение новостей из источника"""
        try:
            # Пауза между запросами
            await asyncio.sleep(self.config['collection']['delay_between_requests'])
            
            # Получение RSS feed
            async with session.get(source['url']) as response:
                if response.status != 200:
                    logger.warning(f"HTTP {response.status} для {source['name']}")
                    return []
                
                content = await response.text()
                feed = feedparser.parse(content)
                
                if feed.bozo:
                    logger.warning(f"Проблемы с парсингом RSS: {source['name']}")
                
                news_items = []
                
                for entry in feed.entries:
                    try:
                        # Парсинг даты
                        pub_date = self.parse_entry_date(entry)
                        if pub_date < cutoff_date:
                            continue
                        
                        # Создание объекта новости
                        news_item = self.create_production_news_item(entry, source, pub_date)
                        if news_item and self.is_valid_news_item(news_item):
                            news_items.append(news_item)
                    
                    except Exception as e:
                        logger.debug(f"Ошибка при обработке записи из {source['name']}: {e}")
                        continue
                
                return news_items
                
        except Exception as e:
            logger.error(f"Ошибка при получении новостей из {source['url']}: {e}")
            return []

    def create_production_news_item(self, entry, source: Dict, pub_date: datetime) -> Optional[ProductionNewsItem]:
        """Создание объекта новости для промышленной системы"""
        try:
            # Извлечение базовой информации
            title = entry.get('title', '').strip()
            link = entry.get('link', '').strip()
            description = entry.get('summary', '').strip()
            content = self.extract_content(entry)
            
            if not title or not link:
                return None
            
            # Фильтрация по длине контента
            if len(description) < self.config['filters']['min_content_length']:
                return None
            
            # Создание хеша
            hash_id = hashlib.md5(f"{title}{link}".encode()).hexdigest()
            
            # Автоматическая обработка
            primary_category = self.categorize_content(title + ' ' + description, source.get('category', 'general'))
            secondary_categories = self.extract_secondary_categories(title + ' ' + description)
            technology_tags = self.extract_technology_tags(title + ' ' + description)
            content_type = self.classify_content_type(title + ' ' + description)
            complexity_level = self.determine_complexity(title + ' ' + description)
            importance_level = self.calculate_importance(title + ' ' + description, source)
            
            # Технические характеристики
            version_mentioned = self.extract_version(title + ' ' + description)
            security_related = self.is_security_related(title + ' ' + description)
            production_ready = self.is_production_related(title + ' ' + description)
            breaking_changes = self.has_breaking_changes(title + ' ' + description)
            
            # Ключевые слова
            keywords = self.extract_keywords(title + ' ' + description)
            
            # Создание объекта
            news_item = ProductionNewsItem(
                title=title,
                link=link,
                description=description,
                content=content,
                pub_date=pub_date,
                collected_date=datetime.now(timezone.utc),
                
                source_name=source['name'],
                source_url=source['url'],
                source_type=source['type'],
                source_importance=source['importance'],
                
                primary_category=primary_category,
                secondary_categories=secondary_categories,
                technology_tags=technology_tags,
                
                content_type=content_type,
                importance_level=importance_level,
                complexity_level=complexity_level,
                
                language=source['language'],
                region=source['region'],
                
                version_mentioned=version_mentioned,
                security_related=security_related,
                production_ready=production_ready,
                breaking_changes=breaking_changes,
                
                hash_id=hash_id,
                keywords=keywords,
                sentiment='neutral'
            )
            
            return news_item
            
        except Exception as e:
            logger.error(f"Ошибка при создании объекта новости: {e}")
            return None

    def is_valid_news_item(self, item: ProductionNewsItem) -> bool:
        """Валидация новости"""
        # Проверка черного списка доменов
        domain = urlparse(item.link).netloc
        if domain in self.config['filters']['blacklist_domains']:
            return False
        
        # Проверка исключенных ключевых слов
        text_lower = (item.title + ' ' + item.description).lower()
        if any(keyword in text_lower for keyword in self.config['filters']['excluded_keywords']):
            return False
        
        # Проверка обязательных ключевых слов (если заданы)
        if self.config['filters']['required_keywords']:
            if not any(keyword in text_lower for keyword in self.config['filters']['required_keywords']):
                return False
        
        return True

    def categorize_content(self, text: str, source_category: str = 'general') -> str:
        """Продвинутая категоризация контента"""
        text_lower = text.lower()
        
        # Сначала проверяем категорию источника
        if source_category != 'general':
            return source_category
        
        # Автоматическое определение категории
        for category, keywords in self.categories['primary_categories'].items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        
        return 'general'

    def calculate_importance(self, text: str, source: Dict) -> int:
        """Расчет важности новости"""
        base_importance = source.get('importance', 3)
        
        text_lower = text.lower()
        
        # Повышение важности
        if any(keyword in text_lower for keyword in self.keywords['security_keywords']):
            base_importance = min(5, base_importance + 1)
        
        if any(keyword in text_lower for keyword in ['release', 'update', 'version']):
            base_importance = min(5, base_importance + 1)
        
        if any(keyword in text_lower for keyword in self.keywords['breaking_keywords']):
            base_importance = min(5, base_importance + 1)
        
        return base_importance

    def remove_duplicates(self, news_list: List[ProductionNewsItem]) -> List[ProductionNewsItem]:
        """Удаление дубликатов новостей"""
        seen_hashes = set()
        seen_titles = set()
        unique_news = []
        
        for item in news_list:
            # Проверка по хешу
            if item.hash_id in seen_hashes:
                continue
            
            # Проверка по похожим заголовкам
            title_normalized = re.sub(r'[^\w\s]', '', item.title.lower()).strip()
            if title_normalized in seen_titles:
                continue
            
            seen_hashes.add(item.hash_id)
            seen_titles.add(title_normalized)
            unique_news.append(item)
        
        return unique_news

    def extract_content(self, entry) -> str:
        """Извлечение полного контента"""
        if hasattr(entry, 'content') and entry.content:
            return entry.content[0].get('value', '')
        return entry.get('summary', '')

    def parse_entry_date(self, entry) -> datetime:
        """Улучшенный парсинг даты"""
        date_fields = ['published_parsed', 'updated_parsed']
        
        for field in date_fields:
            if hasattr(entry, field) and getattr(entry, field):
                try:
                    parsed_time = getattr(entry, field)
                    return datetime(*parsed_time[:6], tzinfo=timezone.utc)
                except:
                    continue
        
        return datetime.now(timezone.utc)

    # Методы анализа контента (аналогичны предыдущей версии, но оптимизированы)
    def extract_secondary_categories(self, text: str) -> List[str]:
        """Извлечение дополнительных категорий"""
        text_lower = text.lower()
        categories = []
        
        for category, keywords in self.categories['primary_categories'].items():
            if any(keyword in text_lower for keyword in keywords):
                categories.append(category)
        
        return list(set(categories))[:3]

    def extract_technology_tags(self, text: str) -> List[str]:
        """Извлечение технологических тегов"""
        all_keywords = []
        for keywords in self.categories['primary_categories'].values():
            all_keywords.extend(keywords)
        
        text_lower = text.lower()
        found_tags = [tag for tag in all_keywords if tag in text_lower]
        
        return list(set(found_tags))[:5]

    def classify_content_type(self, text: str) -> str:
        """Классификация типа контента"""
        text_lower = text.lower()
        
        for content_type, keywords in self.categories['content_types'].items():
            if any(keyword in text_lower for keyword in keywords):
                return content_type
        
        return 'news'

    def determine_complexity(self, text: str) -> str:
        """Определение уровня сложности"""
        text_lower = text.lower()
        
        for level, keywords in self.categories['complexity_levels'].items():
            if any(keyword in text_lower for keyword in keywords):
                return level
        
        return 'intermediate'

    def extract_version(self, text: str) -> Optional[str]:
        """Извлечение версии ПО"""
        for pattern in self.keywords['version_patterns']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        return None

    def is_security_related(self, text: str) -> bool:
        """Проверка связи с безопасностью"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.keywords['security_keywords'])

    def is_production_related(self, text: str) -> bool:
        """Проверка связи с продакшеном"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.keywords['production_keywords'])

    def has_breaking_changes(self, text: str) -> bool:
        """Проверка на breaking changes"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.keywords['breaking_keywords'])

    def extract_keywords(self, text: str) -> List[str]:
        """Извлечение ключевых слов"""
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Технологические ключевые слова
        tech_words = []
        for keywords in self.categories['primary_categories'].values():
            tech_words.extend(keywords)
        
        found_keywords = [word for word in words if word in tech_words]
        
        # Дополнительные важные слова
        important_words = ['release', 'security', 'update', 'vulnerability', 'performance']
        found_keywords.extend([word for word in words if word in important_words])
        
        return list(set(found_keywords))[:10]

    def save_to_database(self, news_items: List[ProductionNewsItem]) -> int:
        """Сохранение новостей в производственную БД"""
        with sqlite3.connect(self.db_path) as conn:
            saved_count = 0
            
            for item in news_items:
                try:
                    conn.execute('''
                        INSERT OR REPLACE INTO production_news (
                            hash_id, title, link, description, content, pub_date, collected_date,
                            source_name, source_url, source_type, source_importance,
                            primary_category, secondary_categories, technology_tags,
                            content_type, importance_level, complexity_level,
                            language, region,
                            version_mentioned, security_related, production_ready, breaking_changes,
                            keywords, sentiment
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        item.hash_id, item.title, item.link, item.description, item.content,
                        item.pub_date.isoformat(), item.collected_date.isoformat(),
                        item.source_name, item.source_url, item.source_type, item.source_importance,
                        item.primary_category, json.dumps(item.secondary_categories), json.dumps(item.technology_tags),
                        item.content_type, item.importance_level, item.complexity_level,
                        item.language, item.region,
                        item.version_mentioned, item.security_related, item.production_ready, item.breaking_changes,
                        json.dumps(item.keywords), item.sentiment
                    ))
                    saved_count += 1
                    
                except Exception as e:
                    logger.error(f"Ошибка при сохранении новости {item.title}: {e}")
            
            conn.commit()
            logger.info(f"Сохранено {saved_count} новостей в базу данных")
            return saved_count

    def get_statistics(self) -> Dict:
        """Получение статистики работы коллектора"""
        return {
            **self.stats,
            'config': {
                'sources_count': len(self.sources),
                'months_collected': self.config['collection']['months_history'],
                'concurrent_limit': self.config['collection']['max_concurrent']
            }
        }

async def main():
    """Основная функция для запуска промышленного сборщика"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Production Container News Collector')
    parser.add_argument('--months', type=int, default=3, help='Months of history to collect')
    parser.add_argument('--config', default='config/production_config.yaml', help='Config file path')
    
    args = parser.parse_args()
    
    collector = ProductionNewsCollector(args.config)
    
    logger.info("Запуск промышленного сборщика новостей...")
    start_time = time.time()
    
    # Сбор новостей
    news_items = await collector.collect_production_news(args.months)
    
    # Сохранение в БД
    saved_count = collector.save_to_database(news_items)
    
    # Статистика
    end_time = time.time()
    duration = end_time - start_time
    stats = collector.get_statistics()
    
    logger.info("="*60)
    logger.info("ПРОМЫШЛЕННЫЙ СБОР ЗАВЕРШЕН")
    logger.info("="*60)
    logger.info(f"Время выполнения: {duration:.2f} секунд")
    logger.info(f"Источников обработано: {stats['sources_processed']}")
    logger.info(f"Новостей собрано: {stats['news_collected']}")
    logger.info(f"Дубликатов пропущено: {stats['duplicates_skipped']}")
    logger.info(f"Ошибок: {stats['errors']}")
    logger.info(f"Сохранено в БД: {saved_count}")
    logger.info("="*60)

if __name__ == "__main__":
    asyncio.run(main())