import pandas as pd
from openpyxl.utils import range_boundaries
from main.exceptions import BadRequestException


def parse_excel_range(file_obj, sheet_name, cell_range):
    excel_file = pd.ExcelFile(file_obj)
    df_raw = excel_file.parse(sheet_name, header=None)

    min_col, min_row, max_col, max_row = range_boundaries(cell_range.upper())

    if max_row != min_row:
        raise BadRequestException("Header range must be a single row")

    # Extract column headers from the specified row and columns
    headers = df_raw.iloc[min_row - 1, min_col - 1:max_col].tolist()

    # Extract all rows below the header
    df_data = df_raw.iloc[min_row:, min_col - 1:max_col]

    # Drop completely empty rows
    df_data.dropna(how="all", inplace=True)

    # Assign headers
    df_data.columns = headers

    return df_data.reset_index(drop=True)


def generate_chart_data_with_dataframe(dataframe, x_col, y_cols):
    labels = dataframe[x_col].fillna("Unknown").astype(str).tolist()

    datasets = []
    for i, y in enumerate(y_cols):
        datasets.append({
            'label': y,
            'data': dataframe[y].fillna(0).tolist(),
            'backgroundColor': subtle_colors[i]
        })

    return {
        "labels": labels,
        "datasets": datasets
    }


def generate_chart_data_with_axes(file_obj, sheet_name, x, y):
    dataframe = pd.read_excel(file_obj, sheet_name=sheet_name)

    x_col = x.strip()
    y_cols = [col.strip() for col in y.split(',')]

    if x_col not in dataframe.columns:
        raise BadRequestException(
            message=f"Column '{x_col}' not found in Excel file")
    for y_col in y_cols:
        if y_col not in dataframe.columns:
            raise BadRequestException(
                message=f"Column '{y_col}' not found in Excel file")

    return generate_chart_data_with_dataframe(dataframe, x_col, y_cols)


def generate_chart_data_with_cell_range(file_obj, sheet_name, x, y, cell_range):
    file_obj.seek(0)
    dataframe = parse_excel_range(file_obj, sheet_name, cell_range)

    print("DATAGRAME", dataframe)

    x_col = x.strip()
    y_cols = [col.strip() for col in y.split(',')]

    if x_col not in dataframe.columns:
        raise BadRequestException(
            message=f"Column '{x_col}' not found in Excel file")
    for y_col in y_cols:
        if y_col not in dataframe.columns:
            raise BadRequestException(
                message=f"Column '{y_col}' not found in Excel file")

    return generate_chart_data_with_dataframe(dataframe, x_col, y_cols)


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
    'rgba(244, 143, 177, 0.6)',
    'rgba(129, 212, 250, 0.6)',
    'rgba(255, 213, 79, 0.6)',
    'rgba(77, 182, 172, 0.6)',
    'rgba(179, 157, 219, 0.6)',
    'rgba(255, 202, 40, 0.6)',
    'rgba(144, 202, 249, 0.6)',
    'rgba(255, 171, 145, 0.6)',
    'rgba(174, 234, 0, 0.6)',
    'rgba(255, 112, 67, 0.6)',
    'rgba(149, 117, 205, 0.6)',
    'rgba(77, 208, 225, 0.6)',
    'rgba(0, 188, 212, 0.6)',
    'rgba(255, 204, 128, 0.6)',
    'rgba(158, 158, 158, 0.6)',
    'rgba(139, 195, 74, 0.6)',
    'rgba(255, 235, 59, 0.6)',
    'rgba(66, 165, 245, 0.6)',
    'rgba(255, 87, 34, 0.6)',
    'rgba(124, 179, 66, 0.6)',
    'rgba(240, 98, 146, 0.6)',
    'rgba(0, 150, 136, 0.6)',
    'rgba(255, 193, 7, 0.6)',
    'rgba(205, 220, 57, 0.6)',
    'rgba(63, 81, 181, 0.6)',
    'rgba(38, 166, 154, 0.6)',
    'rgba(255, 152, 0, 0.6)',
    'rgba(186, 104, 200, 0.6)',
    'rgba(33, 150, 243, 0.6)',
    'rgba(255, 87, 34, 0.6)',
    'rgba(76, 175, 80, 0.6)',
    'rgba(103, 58, 183, 0.6)',
    'rgba(255, 193, 7, 0.6)',
    'rgba(244, 67, 54, 0.6)',
    'rgba(0, 188, 212, 0.6)',
    'rgba(205, 220, 57, 0.6)',
    'rgba(0, 150, 136, 0.6)',
    'rgba(156, 39, 176, 0.6)',
    'rgba(3, 169, 244, 0.6)',
    'rgba(233, 30, 99, 0.6)'
]
