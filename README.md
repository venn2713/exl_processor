### Инструкция по запуску проекта

---

#### Вариант 1: Локальная сборка Docker-образа

1. **Клонируем проект**  
   Скачиваем репозиторий с помощью команды `git`:  
   ```bash
   git clone https://github.com/venn2713/exl_report_processor.git
   ```

2. **Переходим в папку проекта**  
   После успешного клонирования переходим в директорию с проектом:  
   ```bash
   cd exl_report_processor
   ```

3. **Создаем файл `.env`**  
   Копируем пример файла конфигурации:  
   ```bash
   cp .env.example .env
   ```

4. **Редактируем файл `.env`**  
   Откройте файл `.env` в любом текстовом редакторе (например, `nano`):  
   ```bash
   nano .env
   ```
   Укажите необходимые значения переменных (например, `SECRET_KEY`, `ENVIRONMENT`, и другие). После редактирования сохраните файл (`Ctrl+O`, `Enter`, `Ctrl+X`).

5. **Собираем Docker-образ**  
   Создаем локальный Docker-образ:  
   ```bash
   docker build -t exl_report_processor .
   ```

6. **Запускаем контейнер**  
   Запускаем контейнер с подключением `.env`:  
   ```bash
   docker run --name exl_processor --env-file .env -p 8000:8000 -d exl_report_processor
   ```

Теперь приложение доступно по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

#### Вариант 2: Запуск через готовый Docker-образ

1. **Скачиваем пример `.env` с помощью `curl`**  
   Чтобы получить файл конфигурации `.env.example`, используем команду:  
   ```bash
   curl -o .env https://raw.githubusercontent.com/venn2713/exl_report_processor/master/.env.example
   ```

2. **Редактируем файл `.env`**  
   Откройте файл `.env` для редактирования:  
   ```bash
   nano .env
   ```
   Укажите необходимые значения переменных, такие как `SECRET_KEY`, `ENVIRONMENT`, и т.д. Сохраните файл (`Ctrl+O`, `Enter`, `Ctrl+X`).

3. **Скачиваем и запускаем Docker-образ с Docker Hub**  
   Используем готовый образ из Docker Hub:  
   ```bash
   docker run --name exl_processor --env-file .env -p 8000:8000 -d venn2713/exl-processor:latest
   ```

---

#### Полезные команды

- **Остановить контейнер**  
   ```bash
   docker stop exl_processor
   ```

- **Удалить контейнер**  
   ```bash
   docker rm -f exl_processor
   ```

- **Просмотреть запущенные контейнеры**  
   ```bash
   docker ps
   ```

- **Посмотреть логи контейнера**  
   ```bash
   docker logs exl_processor
   ```

---

Теперь приложение доступно по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).