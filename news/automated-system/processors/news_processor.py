#!/usr/bin/env python3
"""
News Processing Pipeline
Обработка собранных новостей для интеграции с репозиторием
"""

import sqlite3
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsProcessor:
    """Обработчик новостей для репозитория"""
    
    def __init__(self, db_path: str = "data/production_container_news.db"):
        self.db_path = Path(db_path)
        self.repo_root = Path("../../")  # Корень репозитория
        
    def get_news_by_period(self, year: int, month: int) -> List[Dict]:
        """Получение новостей за определенный период"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Формируем период
            start_date = f"{year}-{month:02d}-01"
            if month == 12:
                end_date = f"{year+1}-01-01"
            else:
                end_date = f"{year}-{month+1:02d}-01"
            
            cursor = conn.execute('''
                SELECT * FROM production_news 
                WHERE pub_date >= ? AND pub_date < ?
                ORDER BY pub_date DESC, importance DESC
            ''', (start_date, end_date))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict:
        """Получение общей статистики"""
        with sqlite3.connect(self.db_path) as conn:
            stats = {}
            
            # Общее количество
            stats['total'] = conn.execute("SELECT COUNT(*) FROM production_news").fetchone()[0]
            
            # По категориям
            stats['by_category'] = dict(conn.execute(
                "SELECT category, COUNT(*) FROM production_news GROUP BY category ORDER BY COUNT(*) DESC"
            ).fetchall())
            
            # По важности
            stats['by_importance'] = dict(conn.execute(
                "SELECT importance, COUNT(*) FROM production_news GROUP BY importance ORDER BY importance DESC"
            ).fetchall())
            
            # По языкам
            stats['by_language'] = dict(conn.execute(
                "SELECT language, COUNT(*) FROM production_news GROUP BY language"
            ).fetchall())
            
            # Новости по безопасности
            stats['security_count'] = conn.execute(
                "SELECT COUNT(*) FROM production_news WHERE security_related = 1"
            ).fetchone()[0]
            
            # С указанием версии
            stats['with_version'] = conn.execute(
                "SELECT COUNT(*) FROM production_news WHERE version_mentioned != ''"
            ).fetchone()[0]
            
            # Топ источники
            stats['top_sources'] = dict(conn.execute(
                "SELECT source_name, COUNT(*) FROM production_news GROUP BY source_name ORDER BY COUNT(*) DESC LIMIT 10"
            ).fetchall())
            
            # Период покрытия
            date_range = conn.execute(
                "SELECT MIN(pub_date) as min_date, MAX(pub_date) as max_date FROM production_news"
            ).fetchone()
            stats['period'] = {
                'from': date_range[0],
                'to': date_range[1]
            }
            
        return stats
    
    def create_monthly_article(self, year: int, month: int) -> Tuple[str, str]:
        """Создание статьи для месяца"""
        news_items = self.get_news_by_period(year, month)
        
        if not news_items:
            return "", ""
        
        # Группировка по категориям
        by_category = {}
        by_importance = {5: [], 4: [], 3: [], 2: [], 1: []}
        security_news = []
        releases = []
        
        for item in news_items:
            category = item['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(item)
            
            by_importance[item['importance']].append(item)
            
            if item['security_related']:
                security_news.append(item)
            
            if item['version_mentioned']:
                releases.append(item)
        
        # Генерация заголовка файла
        month_names = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April',
            5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }
        
        filename = f"index.md"
        
        # Генерация содержимого
        content = f"""# 📰 Container Technologies News - {month_names[month]} {year}

**Сводка новостей по контейнерным технологиям за {month_names[month]} {year}**

## 📊 Статистика месяца

- **Всего новостей:** {len(news_items)}
- **Новости по безопасности:** {len(security_news)}
- **Релизы с версиями:** {len(releases)}
- **Основные категории:** {', '.join(sorted(by_category.keys()))}

## 🔥 Важные новости (приоритет 5)

"""
        
        # Критически важные новости
        for item in by_importance[5][:10]:
            content += f"""### {item['title']}
- **Источник:** {item['source_name']}
- **Категория:** {item['category']}
- **Дата:** {item['pub_date'][:10]}
- **Ссылка:** [{item['title'][:50]}...]({item['link']})

{item['description'][:200]}...

---

"""
        
        # Новости по категориям
        content += "## 📋 По категориям\n\n"
        
        for category in sorted(by_category.keys()):
            items = by_category[category][:5]  # Топ 5 по категории
            content += f"### {category.upper()} ({len(by_category[category])} новостей)\n\n"
            
            for item in items:
                content += f"- **[{item['title'][:60]}...]({item['link']})** "
                content += f"*{item['source_name']}* - {item['pub_date'][:10]}\n"
            
            content += "\n"
        
        # Новости по безопасности
        if security_news:
            content += "## 🔒 Безопасность\n\n"
            for item in security_news[:5]:
                content += f"- **[{item['title']}]({item['link']})**\n"
                content += f"  *{item['source_name']}* - {item['pub_date'][:10]}\n"
                content += f"  {item['description'][:150]}...\n\n"
        
        # Релизы
        if releases:
            content += "## 🚀 Релизы\n\n"
            for item in releases[:10]:
                version = item['version_mentioned']
                content += f"- **{item['title']}** - `{version}`\n"
                content += f"  *{item['source_name']}* - [{item['title'][:40]}...]({item['link']})\n\n"
        
        # Источники
        sources = list(set(item['source_name'] for item in news_items))
        content += f"""## 📡 Источники ({len(sources)})

{', '.join(sorted(sources))}

---

*Автоматически сгенерировано системой сбора новостей*  
*Последнее обновление: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
        
        return filename, content
    
    def create_summary_report(self) -> str:
        """Создание сводного отчета"""
        stats = self.get_statistics()
        
        content = f"""# 📊 Container Technologies News - Сводный отчет

**Полный анализ собранных новостей по контейнерным технологиям**

## 🎯 Общая статистика

- **Всего новостей:** {stats['total']}
- **Период:** {stats['period']['from'][:10]} - {stats['period']['to'][:10]}
- **Новости по безопасности:** {stats['security_count']}
- **С указанием версии:** {stats['with_version']}

## 📈 Распределение по категориям

"""
        
        for category, count in stats['by_category'].items():
            percentage = (count / stats['total']) * 100
            content += f"- **{category}:** {count} новостей ({percentage:.1f}%)\n"
        
        content += "\n## ⭐ Распределение по важности\n\n"
        
        for importance, count in stats['by_importance'].items():
            percentage = (count / stats['total']) * 100
            content += f"- **Уровень {importance}:** {count} новостей ({percentage:.1f}%)\n"
        
        content += "\n## 🌐 Распределение по языкам\n\n"
        
        for language, count in stats['by_language'].items():
            percentage = (count / stats['total']) * 100
            content += f"- **{language}:** {count} новостей ({percentage:.1f}%)\n"
        
        content += "\n## 📡 Топ источники\n\n"
        
        for source, count in list(stats['top_sources'].items())[:10]:
            percentage = (count / stats['total']) * 100
            content += f"- **{source}:** {count} новостей ({percentage:.1f}%)\n"
        
        content += f"""

## 🔍 Анализ трендов

### Kubernetes экосистема
Kubernetes остается доминирующей платформой с наибольшим количеством новостей и релизов.

### Безопасность
{stats['security_count']} новостей связаны с безопасностью, что составляет {(stats['security_count']/stats['total']*100):.1f}% от общего количества.

### Релизы ПО
{stats['with_version']} новостей содержат информацию о конкретных версиях продуктов.

---

*Отчет сгенерирован автоматически*  
*Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
        
        return content
    
    def update_main_readme(self):
        """Обновление основного README с актуальной статистикой"""
        stats = self.get_statistics()
        readme_path = self.repo_root / "news" / "README.md"
        
        if not readme_path.exists():
            return
        
        # Читаем текущий README
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Обновляем статистику
        new_stats_section = f"""## 📊 Актуальная статистика

- **Всего новостей:** {stats['total']}
- **Период покрытия:** {stats['period']['from'][:10]} - {stats['period']['to'][:10]}
- **Новости по безопасности:** {stats['security_count']}
- **Основные категории:** {', '.join(list(stats['by_category'].keys())[:5])}
- **Языки:** {', '.join(stats['by_language'].keys())}

*Последнее обновление: {datetime.now().strftime('%Y-%m-%d %H:%M')}*

"""
        
        # Заменяем или добавляем секцию статистики
        if "## 📊 Актуальная статистика" in content:
            # Заменяем существующую секцию
            pattern = r"## 📊 Актуальная статистика.*?(?=\n## |\n# |\Z)"
            content = re.sub(pattern, new_stats_section.strip(), content, flags=re.DOTALL)
        else:
            # Добавляем в конец
            content += "\n" + new_stats_section
        
        # Сохраняем обновленный README
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"README обновлен: {readme_path}")

def main():
    """Основная функция обработки"""
    import argparse
    
    parser = argparse.ArgumentParser(description='News Processor for Repository Integration')
    parser.add_argument('--year', type=int, default=2024, help='Year to process')
    parser.add_argument('--month', type=int, help='Month to process (1-12)')
    parser.add_argument('--summary', action='store_true', help='Generate summary report')
    parser.add_argument('--update-readme', action='store_true', help='Update main README')
    
    args = parser.parse_args()
    
    processor = NewsProcessor()
    
    if args.summary:
        logger.info("Генерация сводного отчета...")
        summary = processor.create_summary_report()
        
        output_path = Path("data/summary_report.md")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        logger.info(f"Сводный отчет сохранен: {output_path}")
    
    if args.month:
        logger.info(f"Обработка новостей за {args.year}-{args.month:02d}...")
        filename, content = processor.create_monthly_article(args.year, args.month)
        
        # Создаем директорию для месяца
        month_dir = Path(f"../../{args.year}/{args.month:02d}")
        month_dir.mkdir(parents=True, exist_ok=True)
        
        # Сохраняем статью
        article_path = month_dir / filename
        with open(article_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Статья создана: {article_path}")
    
    if args.update_readme:
        logger.info("Обновление основного README...")
        processor.update_main_readme()
    
    # Показать статистику
    stats = processor.get_statistics()
    logger.info("="*50)
    logger.info("СТАТИСТИКА ОБРАБОТКИ")
    logger.info("="*50)
    logger.info(f"Всего новостей: {stats['total']}")
    logger.info(f"Период: {stats['period']['from'][:10]} - {stats['period']['to'][:10]}")
    logger.info(f"Категорий: {len(stats['by_category'])}")
    logger.info(f"Источников: {len(stats['top_sources'])}")
    logger.info(f"Безопасность: {stats['security_count']}")
    logger.info("="*50)

if __name__ == "__main__":
    main()