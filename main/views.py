import logging
import tempfile
import os
from typing import Union, Any
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.http.request import HttpRequest
from .services.file_parser import parse_file
from .services.report_generator import generate_report

logger = logging.getLogger(__name__)


class FileUploadView(View):
    def dispatch(self, *args: Any, **kwargs: Any) -> Any:
        logger.info("Обработка запроса в FileUploadView")
        return super().dispatch(*args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        logger.info("GET запрос на загрузку страницы")
        return render(request, "upload.html")

    def post(self, request: HttpRequest) -> Union[HttpResponse, FileResponse]:
        logger.info("POST запрос для загрузки файла")
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            logger.warning("Файл не был передан в запросе")
            return HttpResponse("Файл не найден", status=400)

        logger.info(f"Получен файл: {uploaded_file.name}")

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            logger.info(f"Файл сохранён во временное хранилище: {temp_file_path}")

            parsed_data = parse_file(temp_file_path)
            logger.info("Файл успешно разобран")

            report_path = generate_report(parsed_data)
            logger.info(f"Отчет успешно создан: {report_path}")

            return FileResponse(
                open(report_path, "rb"), as_attachment=True, filename="report.xlsx"
            )

        except Exception as e:
            logger.error(f"Ошибка обработки файла: {str(e)}", exc_info=True)
            return HttpResponse(f"Ошибка обработки: {str(e)}", status=500)

        finally:
            try:
                if temp_file_path:
                    os.remove(temp_file_path)
                    logger.info(f"Временный файл удалён: {temp_file_path}")
            except Exception as cleanup_error:
                logger.warning(
                    f"Ошибка при удалении временного файла: {str(cleanup_error)}"
                )
