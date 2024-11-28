<style>

*{
    box-sizing: border-box;
}

*, *::after, *::before,
h1, h2, h3, h4, h5, h6, p {
    font-family: "Roboto Light", sans-serif;
    margin: 0;
    padding: 0;
}

:root{
    --color-blue: #66f;
    --color-red: #f66;
}


.project-title {
    margin-block: 10px;
    text-align: center;
}

.subtitle {
    text-align: center;
    margin-bottom: 4px;
    font-size: 24px;
}

.container {
    display: flex;
    flex-direction: column;
    row-gap: 30px;
}

.technologies-container:not(:last-child){
    margin-bottom: 10px;
}

.technologies-list {
    display: flex;
    justify-content: space-around;
    align-items: center;
    flex-wrap: wrap;
    margin-inline: 0;
    padding-inline: 0;
    list-style-type: none;
    column-gap: 20px;
    row-gap: 20px;
}

.technologies-list__link{
    text-decoration: none;
    font-size: 18px;
    color: azure;
    padding: 6px 12px;
    background-color: var(--color-blue);
    border-radius: 6px;
    cursor: pointer;
    transition-duration: 0.2s;
}

.technologies-list__link:hover{
    background-color: var(--color-red);
    text-decoration: none;
}

.description-block-title{
    font-size: 22px;
    text-decoration: underline var(--color-blue);
    transition-duration: 0.2s;
}

.description-block:hover .description-block-title {
    text-decoration-color: var(--color-red);
}

.description-block:not(:last-child){
    margin-bottom: 15px;
}

.description-block p {
    margin-top: 10px;    
    text-align: justify;
    font-size: 16px;
    line-height: 1.5;
}



</style>

<h1 class="project-title">First backend FastAPI Pet project</h1>
<hr>
<div class="technologies-container container">
    <h2 class="subtitle">Стек технологий</h2>
    <ul class="technologies-list">
        <li class="technologies-list__item">
            <a href="https://fastapi.tiangolo.com/"
            class="technologies-list__link">
                FastAPI
            </a>
        </li>
        <li class="technologies-list__item">
            <a href="https://www.postgresql.org/"
            class="technologies-list__link">
                PostgreSQL
            </a>
        </li>
        <li class="technologies-list__item">
            <a href="https://docs.celeryq.dev/en/stable/"
            class="technologies-list__link">
                Celery
            </a>
        </li>
        <li class="technologies-list__item">
            <a href="https://redis.io/"
            class="technologies-list__link">
                Redis
            </a>
        </li>
        <li class="technologies-list__item">
            <a href="https://www.sqlalchemy.org/"
            class="technologies-list__link">
                SQLAlchemy
            </a>
        </li>
        <li class="technologies-list__item">
            <a href="https://flower.readthedocs.io/en/latest/"
            class="technologies-list__link">Flower</a>
        </li>
        <li class="technologies-list__item">
            <a href="https://prometheus.io/"
            class="technologies-list__link">
                Prometheus
            </a>
        </li>
        <li class="technologies-list__item">
            <a href="https://www.docker.com/"
            class="technologies-list__link">Docker</a>
        </li>
        <li class="technologies-list__item">
            <a href="https://docs.pytest.org/en/stable/"
            class="technologies-list__link">PyTest</a>
        </li>
        <li class="technologies-list__item">
            <a href="https://gunicorn.org/"
            class="technologies-list__link">Gunicorn</a>
        </li>
        <li class="technologies-list__item">
            <a href="https://www.uvicorn.org/" 
            class="technologies-list__link">
                Uvicorn
            </a>
        </li>
        <li class="technologies-list__item">
            <a href="https://aminalaee.dev/sqladmin/"
            class="technologies-list__link">
                SQLAdmin
            </a>
        </li>
        <li class="technologies-list__item">
            <a href="https://grafana.com/"
            class="technologies-list__link">
                Grafana
            </a>
        </li>
    </ul>
</div>
<hr>
<div class="description-container container">
    <h2 class="subtitle">Описание проекта</h2>
    <div class="description-body">
        <details class="description-block">
            <summary class="description-block-title">Что это за проект?</summary>
            <p>
                Данный проект реализует RESTful API для бронирования отелей,
                разумеется оно достаточно простенькое, да и написан только backend,
                но возможно в будущем я ещё буду развивать этот проект, а если нет,
                значит напишу новый, во много раз превосходящий этот.
            </p>
        </details>
        <details class="description-block">
            <summary class="description-block-title">Зачем каждая из технологий?</summary>
            <p>FastAPI - асинхронное API (интерфейс) приложения.</p>
            <p>
                PostgreSQL - реалиционная база данных, для хранения информации об отелях,
                заказах, комнатах и пользователях.
            </p>
            <p>
                Redis - кэширование ответов сервера, брокеh сообщений для Celery
                (также есть возможность кэшировать результаты работы Celery).
            </p>
            <p>
                SQLAlchemy - ORM для безопасной работы (в том смысле, что есть защита от SQL-инъекций)
                с реалиционными базами данных привычным "питоновским" языком.
            </p>
            <p>Flower - мониторинг за Celery.</p>
            <p>
                Prometheus - записывает различные показатели работы сервера
                в базу данных временных рядов
            </p>
            <p>Grafana - визуализация метрик, записанных Prometheus (дашборды).</p>
            <p>PyTest - тестирование работы API</p>
            <p>SQLAdmin - админка для удобной работы с базами данных, совместимая с SQLAlchemy и FastAPI</p>
            <p>Docker - контейнеризация всех частей приложения (в отдельные контейнеры) для дальнейшего развертывания </p>
            <p>Uvicorn/Gunicorn - ASGI/WSGI HTTP сервера для разработки/деплоя</p>
        </details>
        <details class="description-block">
            <summary class="description-block-title">Какие протоколы связи используются?</summary>
            <p>HTTP(основная часть приложения), SMTP(отправка подтверждения бронирования по email)</p>
        </details>
    </div>
</div>
