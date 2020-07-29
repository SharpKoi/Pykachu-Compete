
symbol_list = [chr(i) for i in range(33, 48)]
symbol_list.extend([chr(i) for i in range(58, 65)])
symbol_list.extend([chr(i) for i in range(91, 97)])
symbol_list.extend([chr(i) for i in range(123, 127)])


def initially_clean(df, col='review'):
    df[col] = df[col].str.strip().str.lower()


# 不知道為什麼沒辦法清除 '.'
def clean_ascii_symbols(df, col):
    for s in symbol_list:
        df[col] = df[col].str.replace(s, '')
    return df


# The strongest method to clean all symbols include unicode
def clean_symbols(df, col):
    df[col] = df[col].str.replace(r'[^\w\s\r\n]', '')


def clean_blank_rows(df, col):
    blank_index_list = df[df[col].str.match(r'^[^\S]*$')].index
    df.drop(blank_index_list, inplace=True)
