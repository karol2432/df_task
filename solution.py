import pandas as pd

def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    #new column label consists only of letters and underscores
    for char in new_column:
        if not (char.isalpha() or char == "_"):
            return pd.DataFrame([])

    #existing column labels in df are also valid
    for col in df.columns:
        if not all(c.isalpha() or c == "_" for c in str(col)):
            return pd.DataFrame([])

    #replace operators with spaces to easily split the names
    clean_role = role.replace("+", " ").replace("-", " ").replace("*", " ")
    role_elements = clean_role.split()

    #all columns used in the role actually exist in df
    for name in role_elements:
        if name not in df.columns:
            return pd.DataFrame([])

    #check if the role contains only allowed characters
    #letters, numbers, underscores, basic operators, and spaces
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789+-* "
    for char in role:
        if char not in allowed_chars:
            return pd.DataFrame([])

    try:
        result_df = df.copy()
        
        if "+" in role:
            parts = role.split("+")
            result_df[new_column] = df[parts[0].strip()] + df[parts[1].strip()]
        elif "-" in role:
            parts = role.split("-")
            result_df[new_column] = df[parts[0].strip()] - df[parts[1].strip()]
        elif "*" in role:
            parts = role.split("*")
            result_df[new_column] = df[parts[0].strip()] * df[parts[1].strip()]
        else:
            return pd.DataFrame([])
            
        return result_df
    except:
        return pd.DataFrame([])
    

#--------------------

data = {
    'name': ['banana', 'apple'],
    'quantity': [10, 3],
    'price': [10, 1]
}
fruits_sales = pd.DataFrame(data)
print(fruits_sales)

sales_total = add_virtual_column(fruits_sales, "quantity * price", "total")

if not sales_total.empty:
    print(sales_total)
else:
    print("Error")