
symbol_list = [chr(i) for i in range(33, 48)]
symbol_list.extend([chr(i) for i in range(58, 65)])
symbol_list.extend([chr(i) for i in range(91, 97)])
symbol_list.extend([chr(i) for i in range(123, 127)])


def initially_clean(df):
    df.drop('review_id', axis=1, inplace=True)
    df['review'] = df['review'].str.strip().str.lower()


def clean_ascii_symbols(df, col):
    for s in symbol_list:
        df[col] = df[col].str.replace(s, '')


def clean_blank_rows(df, col):
    blank_index_list = df[df[col].str.match(r'^[^\S]*$')].index
    df.drop(blank_index_list, inplace=True)