### Инструкция по запуску проекта

1. **Скачиваем проект**  
   Клонируйте репозиторий:  
   ```bash
   git clone https://github.com/venn2713/exl_report_processor.git
   ```

2. **Переходим в папку проекта**  
   ```bash
   cd exl_report_processor
   ```

3. **Копируем пример `.env`**  
   ```bash
   cp .env.example .env
   ```

4. **Заполняем `.env`**  
   Откройте файл `.env` и укажите необходимые значения переменных.

5. **Собираем Docker-образ**  
   ```bash
   docker build -t exl_report_processor .
   ```

6. **Запускаем контейнер**  
   ```bash
   docker run --name exl_processor --env-file .env -p 8000:8000 -d exl_report_processor
   ```

Теперь приложение доступно по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).