import pandas as pd
from main.views import BaseViewSet
from main.utilities import parse_request_body, log_error


subtle_colors = [
    'rgba(75, 192, 192, 0.6)',
    'rgba(153, 102, 255, 0.6)',
    'rgba(255, 159, 64, 0.6)',
    'rgba(54, 162, 235, 0.6)',
    'rgba(201, 203, 207, 0.6)',
    'rgba(255, 205, 86, 0.6)',
    'rgba(100, 181, 246, 0.6)',
    'rgba(174, 213, 129, 0.6)',
    'rgba(255, 138, 128, 0.6)',
    'rgba(121, 134, 203, 0.6)',
]


class ChartDataViewSet(BaseViewSet):
    def create(self, request):
        try:
            data = parse_request_body(request)

            file_obj = data.get('file')
            if not file_obj:
                return self.error_response(message="Excel file not provided", status=self.status.HTTP_400_BAD_REQUEST)

            x = data.get("x")
            y = data.get("y")
            sheet_name = data.get("sheet_name")

            if None in (x, y, sheet_name):
                return self.error_response(message="Required data is missing. Provide 'x', 'y' and 'sheet_name'", status=self.status.HTTP_400_BAD_REQUEST)

            dataframe = pd.read_excel(file_obj, sheet_name=sheet_name)

            x_col = x.strip()
            y_cols = [col.strip() for col in y.split(',')]

            if x_col not in dataframe.columns:
                return self.error_response(message=f"Column '{x_col}' not found in Excel file", status=400)
            for y_col in y_cols:
                if y_col not in dataframe.columns:
                    return self.error_response(message=f"Column '{y_col}' not found in Excel file", status=400)

            labels = dataframe[x_col].fillna("Unknown").astype(str).tolist()

            datasets = []
            for i, y in enumerate(y_cols):
                datasets.append({
                    'label': y,
                    'data': dataframe[y].fillna(0).tolist(),
                    'backgroundColor': subtle_colors[i]
                })

            return self.success_response(data={
                'labels': labels,
                'datasets': datasets
            })
        except Exception as e:
            print("-" * 100)
            print("Exception caught from 'data.views.ChartDataViewSet.create'")
            print(str(e))
            print("-" * 100)

            log_error(e, 'data.views.ChartDataViewSet.create')

            return self.error_response(message="Something went wrong", error=str(e))
