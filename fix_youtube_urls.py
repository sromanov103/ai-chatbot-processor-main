import os
import json
import re
from pathlib import Path

def extract_video_id(filename):
    # Извлекаем ID видео из имени файла (например, transcript_wLfI_zaFBVY_20250429_192738.txt -> wLfI_zaFBVY_20250429_192738)
    # Удаляем 'transcript_' с начала и '.txt' с конца
    if filename.startswith('transcript_') and filename.endswith('.txt'):
        # Удаляем 'transcript_' (10 символов) и '.txt' (4 символа)
        video_id = filename[10:-4]
        # Удаляем лишний символ подчеркивания в начале, если он есть
        if video_id.startswith('_'):
            video_id = video_id[1:]
        return video_id
    return None

def fix_youtube_url(url, correct_id):
    # Исправляем YouTube URL, заменяя обрезанный ID на правильный
    if not url or not correct_id:
        return url
    
    # Извлекаем временную метку, если она есть
    timestamp = ""
    if "#t=" in url:
        timestamp = url[url.index("#t="):]
    
    # Получаем базовый URL без ID видео
    base_url = "https://www.youtube.com/watch?v="
    
    # Собираем URL с правильным ID и доменом
    return f"{base_url}{correct_id}{timestamp}"

def process_file(file_path):
    try:
        # Открываем лог для отладки
        with open('debug.log', 'a', encoding='utf-8') as debug_log:
            debug_log.write(f"\nОбрабатываем файл: {file_path}\n")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Находим JSON-содержимое между маркерами ```json и ```
            start_marker = '```json'
            end_marker = '```'
            
            if start_marker in content and end_marker in content:
                start_idx = content.find(start_marker) + len(start_marker)
                end_idx = content.find(end_marker, start_idx)
                if end_idx > start_idx:
                    content = content[start_idx:end_idx]
            
            # Удаляем лишние пробелы и переносы строк
            content = content.strip()
            
            # Пытаемся разобрать JSON содержимое
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                # Если разбор JSON не удался, пытаемся исправить типичные проблемы
                content = content.strip()
                if not content.startswith('['):
                    content = '[' + content
                if not content.endswith(']'):
                    content = content + ']'
                data = json.loads(content)
            
            # Получаем правильный ID видео из имени файла
            correct_id = extract_video_id(file_path.name)
            if not correct_id:
                return False, f"Не удалось извлечь ID видео из имени файла: {file_path.name}"
            
            debug_log.write(f"Правильный ID из имени файла: {correct_id}\n")
            
            # Исправляем URL в данных
            for item in data:
                if "fragments" in item:
                    for fragment in item["fragments"]:
                        if "youtube_url" in fragment:
                            debug_log.write(f"Исходный URL: {fragment['youtube_url']}\n")
                            fragment["youtube_url"] = fix_youtube_url(fragment["youtube_url"], correct_id)
                            debug_log.write(f"Исправленный URL: {fragment['youtube_url']}\n")
            
            # Сохраняем исправленный файл
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('```json\n')
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write('\n```')
            
            return True, f"Успешно обработан файл {file_path.name}"
    
    except Exception as e:
        return False, f"Ошибка при обработке файла {file_path.name}: {str(e)}"

def main():
    # Создаем директорию для логов, если её нет
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Инициализируем файлы логов
    success_log = logs_dir / "success.txt"
    failed_log = logs_dir / "failed.txt"
    
    # Очищаем существующие файлы логов
    success_log.write_text("")
    failed_log.write_text("")
    
    # Обрабатываем все txt файлы в директории raw_outputs
    raw_outputs_dir = Path("raw_outputs")
    for file_path in raw_outputs_dir.glob("transcript_*.txt"):
        success, message = process_file(file_path)
        
        # Записываем результат
        if success:
            with open(success_log, 'a', encoding='utf-8') as f:
                f.write(f"{message}\n")
        else:
            with open(failed_log, 'a', encoding='utf-8') as f:
                f.write(f"{message}\n")

if __name__ == "__main__":
    main() 