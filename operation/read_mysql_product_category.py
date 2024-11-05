import pandas as pd
from sqlalchemy import create_engine
from openpyxl import load_workbook

def my_sql_engine():
    return create_engine('mysql+pymysql://myuser:mypassword@localhost/diy')

def create_table(table: str) -> pd.DataFrame:
    query = f'''
    SELECT {table}, 
           SUM(sales_qty) as sales_qty, 
           SUM(sales_qty*price) as sales_amount,
           SUM(sales_qty*cost) as sales_cost,
           SUM((sales_qty*price) - (sales_qty*cost)) as profit
    FROM Sales sl 
    INNER JOIN Products p ON sl.product_code = p.product_code
    INNER JOIN Store st ON sl.store_code = st.store_code
    GROUP BY {table};
    '''
    with my_sql_engine().connect() as conn:
        return pd.read_sql_query(query, conn.connection)

def set_column_width(sheet, widths):
    for col, width in widths.items():
        sheet.column_dimensions[col].width = width

def save_to_excel(dataframes, filename, column_widths):
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        for sheet_name, df in dataframes.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            set_column_width(writer.sheets[sheet_name], column_widths)

def main():
    dataframes = {
        'product_category': create_table('product_category')
    }
    column_widths = {'A': 20, 'B': 15, 'C': 15, 'D': 15, 'E': 15}
    save_to_excel(dataframes, 'product_category.xlsx', column_widths)

if __name__ == '__main__':
    main()
