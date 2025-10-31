#!/usr/bin/env python3
"""
Синхронная версия промышленного сборщика новостей
Production Container Technologies News Collector (Sync Version)
"""

import feedparser
import json
import sqlite3
import hashlib
import re
import logging
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from pathlib import Path
import time
from urllib.parse import urlparse

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class NewsItem:
    """Структура новости"""
    title: str
    link: str
    description: str
    pub_date: datetime
    source_name: str
    category: str
    importance: int
    language: str
    security_related: bool
    version_mentioned: str
    keywords: List[str]
    hash_id: str

class ProductionSyncCollector:
    """Синхронная версия промышленного сборщика"""
    
    def __init__(self):
        self.db_path = Path("data/production_container_news.db")
        self.init_database()
        self.sources = self.get_production_sources()
        
        self.stats = {
            'sources_processed': 0,
            'news_collected': 0,
            'errors': 0,
            'duplicates_skipped': 0
        }

    def init_database(self):
        """Инициализация БД"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS production_news (
                    id INTEGER PRIMARY KEY,
                    hash_id TEXT UNIQUE,
                    title TEXT NOT NULL,
                    link TEXT UNIQUE,
                    description TEXT,
                    pub_date TEXT,
                    source_name TEXT,
                    category TEXT,
                    importance INTEGER,
                    language TEXT,
                    security_related BOOLEAN,
                    version_mentioned TEXT,
                    keywords TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def get_production_sources(self) -> List[Dict]:
        """Полный список производственных источников"""
        return [
            # Kubernetes Official
            {'name': 'Kubernetes Blog', 'url': 'https://kubernetes.io/feed.xml', 'category': 'kubernetes', 'importance': 5, 'language': 'en'},
            {'name': 'Kubernetes Releases', 'url': 'https://github.com/kubernetes/kubernetes/releases.atom', 'category': 'kubernetes', 'importance': 5, 'language': 'en'},
            {'name': 'CNCF Blog', 'url': 'https://www.cncf.io/feed/', 'category': 'kubernetes', 'importance': 5, 'language': 'en'},
            
            # Docker
            {'name': 'Docker Blog', 'url': 'https://www.docker.com/blog/feed/', 'category': 'docker', 'importance': 4, 'language': 'en'},
            {'name': 'Docker Releases', 'url': 'https://github.com/moby/moby/releases.atom', 'category': 'docker', 'importance': 4, 'language': 'en'},
            
            # Container Runtimes
            {'name': 'containerd Releases', 'url': 'https://github.com/containerd/containerd/releases.atom', 'category': 'runtime', 'importance': 4, 'language': 'en'},
            {'name': 'Podman Releases', 'url': 'https://github.com/containers/podman/releases.atom', 'category': 'podman', 'importance': 4, 'language': 'en'},
            {'name': 'CRI-O Releases', 'url': 'https://github.com/cri-o/cri-o/releases.atom', 'category': 'runtime', 'importance': 4, 'language': 'en'},
            
            # Monitoring & Observability  
            {'name': 'Prometheus Releases', 'url': 'https://github.com/prometheus/prometheus/releases.atom', 'category': 'monitoring', 'importance': 4, 'language': 'en'},
            {'name': 'Grafana Releases', 'url': 'https://github.com/grafana/grafana/releases.atom', 'category': 'monitoring', 'importance': 4, 'language': 'en'},
            {'name': 'Jaeger Releases', 'url': 'https://github.com/jaegertracing/jaeger/releases.atom', 'category': 'monitoring', 'importance': 3, 'language': 'en'},
            
            # Service Mesh & Networking
            {'name': 'Istio Releases', 'url': 'https://github.com/istio/istio/releases.atom', 'category': 'service-mesh', 'importance': 4, 'language': 'en'},
            {'name': 'Cilium Releases', 'url': 'https://github.com/cilium/cilium/releases.atom', 'category': 'networking', 'importance': 4, 'language': 'en'},
            {'name': 'Linkerd Releases', 'url': 'https://github.com/linkerd/linkerd2/releases.atom', 'category': 'service-mesh', 'importance': 3, 'language': 'en'},
            {'name': 'Envoy Releases', 'url': 'https://github.com/envoyproxy/envoy/releases.atom', 'category': 'networking', 'importance': 3, 'language': 'en'},
            
            # Security
            {'name': 'Falco Releases', 'url': 'https://github.com/falcosecurity/falco/releases.atom', 'category': 'security', 'importance': 4, 'language': 'en'},
            {'name': 'OPA Releases', 'url': 'https://github.com/open-policy-agent/opa/releases.atom', 'category': 'security', 'importance': 3, 'language': 'en'},
            {'name': 'Trivy Releases', 'url': 'https://github.com/aquasecurity/trivy/releases.atom', 'category': 'security', 'importance': 4, 'language': 'en'},
            {'name': 'Cosign Releases', 'url': 'https://github.com/sigstore/cosign/releases.atom', 'category': 'security', 'importance': 3, 'language': 'en'},
            
            # Storage
            {'name': 'Longhorn Releases', 'url': 'https://github.com/longhorn/longhorn/releases.atom', 'category': 'storage', 'importance': 3, 'language': 'en'},
            {'name': 'OpenEBS Releases', 'url': 'https://github.com/openebs/openebs/releases.atom', 'category': 'storage', 'importance': 3, 'language': 'en'},
            
            # CI/CD & GitOps
            {'name': 'ArgoCD Releases', 'url': 'https://github.com/argoproj/argo-cd/releases.atom', 'category': 'cicd', 'importance': 4, 'language': 'en'},
            {'name': 'Flux Releases', 'url': 'https://github.com/fluxcd/flux2/releases.atom', 'category': 'cicd', 'importance': 4, 'language': 'en'},
            {'name': 'Tekton Releases', 'url': 'https://github.com/tektoncd/pipeline/releases.atom', 'category': 'cicd', 'importance': 3, 'language': 'en'},
            
            # WebAssembly
            {'name': 'WasmEdge Releases', 'url': 'https://github.com/WasmEdge/WasmEdge/releases.atom', 'category': 'webassembly', 'importance': 3, 'language': 'en'},
            {'name': 'Wasmtime Releases', 'url': 'https://github.com/bytecodealliance/wasmtime/releases.atom', 'category': 'webassembly', 'importance': 3, 'language': 'en'},
            
            # Edge & IoT
            {'name': 'K3s Releases', 'url': 'https://github.com/k3s-io/k3s/releases.atom', 'category': 'edge', 'importance': 4, 'language': 'en'},
            {'name': 'KubeEdge Releases', 'url': 'https://github.com/kubeedge/kubeedge/releases.atom', 'category': 'edge', 'importance': 3, 'language': 'en'},
            
            # MicroVMs
            {'name': 'Firecracker Releases', 'url': 'https://github.com/firecracker-microvm/firecracker/releases.atom', 'category': 'microvm', 'importance': 3, 'language': 'en'},
            {'name': 'Kata Containers Releases', 'url': 'https://github.com/kata-containers/kata-containers/releases.atom', 'category': 'microvm', 'importance': 3, 'language': 'en'},
            
            # Industry News
            {'name': 'The New Stack K8s', 'url': 'https://thenewstack.io/kubernetes/feed/', 'category': 'kubernetes', 'importance': 3, 'language': 'en'},
            {'name': 'InfoQ Kubernetes', 'url': 'https://www.infoq.com/Kubernetes/rss', 'category': 'kubernetes', 'importance': 3, 'language': 'en'},
            {'name': 'Container Journal', 'url': 'https://containerjournal.com/feed/', 'category': 'general', 'importance': 2, 'language': 'en'},
            
            # Vendor Blogs
            {'name': 'Red Hat Blog', 'url': 'https://www.redhat.com/en/rss/blog', 'category': 'general', 'importance': 3, 'language': 'en'},
            {'name': 'VMware Tanzu', 'url': 'https://blog.vmware.com/cloudnative/feed', 'category': 'kubernetes', 'importance': 3, 'language': 'en'},
            {'name': 'HashiCorp Blog', 'url': 'https://engineering.hashicorp.com/rss.xml', 'category': 'general', 'importance': 3, 'language': 'en'},
            
            # Security Vendors
            {'name': 'Aqua Security', 'url': 'https://blog.aquasec.com/feed', 'category': 'security', 'importance': 4, 'language': 'en'},
            {'name': 'Sysdig Blog', 'url': 'https://sysdig.com/feed/', 'category': 'security', 'importance': 4, 'language': 'en'},
            
            # Russian Sources
            {'name': 'Habr Kubernetes', 'url': 'https://habr.com/ru/rss/search/?q=kubernetes+k8s&target_type=posts', 'category': 'kubernetes', 'importance': 3, 'language': 'ru'},
            {'name': 'Habr Docker', 'url': 'https://habr.com/ru/rss/search/?q=docker+контейнеры&target_type=posts', 'category': 'docker', 'importance': 3, 'language': 'ru'},
            {'name': 'Habr DevOps', 'url': 'https://habr.com/ru/rss/hub/devops/', 'category': 'devops', 'importance': 2, 'language': 'ru'},
            {'name': 'Yandex Cloud', 'url': 'https://cloud.yandex.ru/blog/rss', 'category': 'cloud', 'importance': 3, 'language': 'ru'},
            {'name': 'Selectel Blog', 'url': 'https://blog.selectel.ru/rss/', 'category': 'cloud', 'importance': 3, 'language': 'ru'},
            {'name': 'VK Cloud', 'url': 'https://mcs.mail.ru/blog/feed/', 'category': 'cloud', 'importance': 3, 'language': 'ru'}
        ]

    def collect_news(self, months: int = 3) -> List[NewsItem]:
        """Сбор новостей за указанное количество месяцев"""
        logger.info(f"Начинаем сбор новостей за {months} месяцев из {len(self.sources)} источников")
        
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=months * 30)
        all_news = []
        
        for i, source in enumerate(self.sources):
            try:
                logger.info(f"[{i+1}/{len(self.sources)}] Обрабатываем {source['name']}...")
                news_items = self.process_source(source, cutoff_date)
                all_news.extend(news_items)
                self.stats['sources_processed'] += 1
                
                logger.info(f"  Собрано {len(news_items)} новостей")
                
                # Пауза между запросами
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"  Ошибка при обработке {source['name']}: {e}")
                self.stats['errors'] += 1
        
        # Удаление дубликатов
        unique_news = self.remove_duplicates(all_news)
        self.stats['news_collected'] = len(unique_news)
        self.stats['duplicates_skipped'] = len(all_news) - len(unique_news)
        
        logger.info(f"Всего собрано {len(all_news)} новостей, уникальных: {len(unique_news)}")
        return unique_news

    def process_source(self, source: Dict, cutoff_date: datetime) -> List[NewsItem]:
        """Обработка одного источника"""
        try:
            feed = feedparser.parse(source['url'])
            
            if feed.bozo:
                logger.warning(f"  RSS parsing issues for {source['name']}")
            
            news_items = []
            
            for entry in feed.entries:
                try:
                    # Парсинг даты
                    pub_date = self.parse_date(entry)
                    if pub_date < cutoff_date:
                        continue
                    
                    # Создание новости
                    news_item = self.create_news_item(entry, source, pub_date)
                    if news_item:
                        news_items.append(news_item)
                        
                except Exception as e:
                    logger.debug(f"  Ошибка обработки записи: {e}")
                    continue
            
            return news_items
            
        except Exception as e:
            logger.error(f"  Ошибка получения RSS: {e}")
            return []

    def create_news_item(self, entry, source: Dict, pub_date: datetime) -> Optional[NewsItem]:
        """Создание объекта новости"""
        try:
            title = entry.get('title', '').strip()
            link = entry.get('link', '').strip()
            description = entry.get('summary', '').strip()
            
            if not title or not link or len(description) < 10:
                return None
            
            # Создание хеша
            hash_id = hashlib.md5(f"{title}{link}".encode()).hexdigest()
            
            # Анализ контента
            text = title + ' ' + description
            security_related = self.is_security_related(text)
            version_mentioned = self.extract_version(text)
            keywords = self.extract_keywords(text)
            
            return NewsItem(
                title=title,
                link=link,
                description=description,
                pub_date=pub_date,
                source_name=source['name'],
                category=source['category'],
                importance=source['importance'],
                language=source['language'],
                security_related=security_related,
                version_mentioned=version_mentioned,
                keywords=keywords,
                hash_id=hash_id
            )
            
        except Exception as e:
            logger.debug(f"Ошибка создания новости: {e}")
            return None

    def parse_date(self, entry) -> datetime:
        """Парсинг даты из RSS"""
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            try:
                return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            except:
                pass
        
        if hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            try:
                return datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
            except:
                pass
        
        return datetime.now(timezone.utc)

    def is_security_related(self, text: str) -> bool:
        """Проверка на безопасность"""
        security_keywords = ['security', 'vulnerability', 'cve', 'exploit', 'patch', 'безопасность', 'уязвимость']
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in security_keywords)

    def extract_version(self, text: str) -> str:
        """Извлечение версии"""
        patterns = [r'v?\d+\.\d+\.\d+', r'version\s+\d+\.\d+']
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        return ''

    def extract_keywords(self, text: str) -> List[str]:
        """Извлечение ключевых слов"""
        tech_keywords = [
            'kubernetes', 'docker', 'podman', 'containerd', 'helm', 'kubectl',
            'prometheus', 'grafana', 'istio', 'cilium', 'falco', 'security',
            'monitoring', 'observability', 'cicd', 'gitops', 'webassembly',
            'release', 'update', 'vulnerability', 'performance'
        ]
        
        text_lower = text.lower()
        found = [keyword for keyword in tech_keywords if keyword in text_lower]
        return found[:5]

    def remove_duplicates(self, news_list: List[NewsItem]) -> List[NewsItem]:
        """Удаление дубликатов"""
        seen_hashes = set()
        seen_titles = set()
        unique_news = []
        
        for item in news_list:
            if item.hash_id in seen_hashes:
                continue
            
            title_normalized = re.sub(r'[^\w\s]', '', item.title.lower()).strip()
            if title_normalized in seen_titles:
                continue
            
            seen_hashes.add(item.hash_id)
            seen_titles.add(title_normalized)
            unique_news.append(item)
        
        return unique_news

    def save_to_database(self, news_items: List[NewsItem]) -> int:
        """Сохранение в БД"""
        with sqlite3.connect(self.db_path) as conn:
            saved_count = 0
            
            for item in news_items:
                try:
                    conn.execute('''
                        INSERT OR REPLACE INTO production_news (
                            hash_id, title, link, description, pub_date,
                            source_name, category, importance, language,
                            security_related, version_mentioned, keywords
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        item.hash_id, item.title, item.link, item.description,
                        item.pub_date.isoformat(), item.source_name, item.category,
                        item.importance, item.language, item.security_related,
                        item.version_mentioned, ','.join(item.keywords)
                    ))
                    saved_count += 1
                    
                except Exception as e:
                    logger.error(f"Ошибка сохранения: {e}")
            
            conn.commit()
            return saved_count

    def export_results(self, filepath: str):
        """Экспорт результатов"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM production_news ORDER BY pub_date DESC")
            news_data = [dict(row) for row in cursor.fetchall()]
        
        export_data = {
            'metadata': {
                'exported_at': datetime.now().isoformat(),
                'total_items': len(news_data),
                'collection_stats': self.stats
            },
            'news': news_data
        }
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Результаты экспортированы в {filepath}")

def main():
    """Основная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Production Container News Collector')
    parser.add_argument('--months', type=int, default=3, help='Months to collect')
    parser.add_argument('--export', help='Export file path')
    
    args = parser.parse_args()
    
    collector = ProductionSyncCollector()
    
    logger.info("="*70)
    logger.info("ПРОМЫШЛЕННЫЙ СБОРЩИК НОВОСТЕЙ КОНТЕЙНЕРНЫХ ТЕХНОЛОГИЙ")
    logger.info("="*70)
    
    start_time = time.time()
    
    # Сбор новостей
    news_items = collector.collect_news(args.months)
    
    # Сохранение в БД
    saved_count = collector.save_to_database(news_items)
    
    # Экспорт
    if args.export:
        collector.export_results(args.export)
    else:
        collector.export_results("data/production_news_export.json")
    
    # Финальная статистика
    end_time = time.time()
    duration = end_time - start_time
    
    logger.info("="*70)
    logger.info("СБОР ЗАВЕРШЕН УСПЕШНО!")
    logger.info("="*70)
    logger.info(f"Время выполнения: {duration:.1f} секунд")
    logger.info(f"Источников обработано: {collector.stats['sources_processed']}")
    logger.info(f"Новостей собрано: {collector.stats['news_collected']}")
    logger.info(f"Дубликатов пропущено: {collector.stats['duplicates_skipped']}")
    logger.info(f"Ошибок: {collector.stats['errors']}")
    logger.info(f"Сохранено в БД: {saved_count}")
    logger.info(f"База данных: {collector.db_path}")
    logger.info("="*70)

if __name__ == "__main__":
    main()