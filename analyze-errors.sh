#!/bin/bash

LOG_FILE="access.log"
REPORT_FILE="error-report.txt"

# Проверяем, существует ли лог-файл
if [ ! -f "$LOG_FILE" ]; then
    echo "❌ Лог-файл $LOG_FILE не найден"
    exit 1
fi

# Считаем общее количество запросов
total=$(wc -l < "$LOG_FILE")

# Считаем 4xx и 5xx ошибки
errors_4xx=$(grep '" [4][0-9][0-9] ' "$LOG_FILE" | wc -l)
errors_5xx=$(grep '" [5][0-9][0-9] ' "$LOG_FILE" | wc -l)
total_errors=$((errors_4xx + errors_5xx))

# Генерируем отчёт
cat > "$REPORT_FILE" << EOF
=== ОТЧЁТ ОБ ОШИБКАХ API ===
Дата анализа: $(date)
Лог-файл: $LOG_FILE

Всего запросов: $total
Ошибки 4xx (клиентские): $errors_4xx
Ошибки 5xx (серверные): $errors_5xx
Всего ошибок: $total_errors

Топ-5 проблемных эндпоинтов:
EOF

# Топ-5 эндпоинтов с ошибками
grep '" [45][0-9][0-9] ' "$LOG_FILE" | \
awk '{print $7}' | \
sort | \
uniq -c | \
sort -nr | \
head -5 >> "$REPORT_FILE"

echo "✅ Отчёт сохранён в $REPORT_FILE"
cat "$REPORT_FILE"
