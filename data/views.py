import pandas as pd
from main.views import BaseViewSet
from main.exceptions import BadRequestException
from main.utilities import parse_request_body, log_error
from .utilities import generate_chart_data_with_axes, generate_chart_data_with_cell_range


class ChartDataViewSet(BaseViewSet):
    def create(self, request):
        try:
            data = parse_request_body(request)

            file_obj = data.get('file')
            if not file_obj:
                raise BadRequestException(message="Excel file not provided")

            x = data.get("x")
            y = data.get("y")
            sheet_name = data.get("sheet_name")

            if None in (x, y, sheet_name):
                raise BadRequestException(
                    message="Required data is missing. Provide 'x', 'y' and 'sheet_name'")

            cell_range = data.get("cell_range")
            if cell_range:
                data = generate_chart_data_with_cell_range(
                    file_obj, sheet_name, x, y, cell_range)
            else:
                data = generate_chart_data_with_axes(
                    file_obj, sheet_name, x, y)

            return self.success_response(data=data)
        except BadRequestException as e:
            return self.error_response(message=e.message, status=self.status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("-" * 100)
            print("Exception caught from 'data.views.ChartDataViewSet.create'")
            print(str(e))
            print("-" * 100)

            log_error(e, 'data.views.ChartDataViewSet.create')

            return self.error_response(message="Something went wrong", error=str(e))
