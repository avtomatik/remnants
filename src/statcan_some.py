import pandas as pd

matchers = ['stat_can_file_']
file_names = sorted(get_file_names(matchers=matchers))
df = pd.DataFrame()
for file_name in file_names:
    kwargs = {
        'filepath_or_buffer': file_name,
        'sep': '\t'
    }
    df = pd.concat([df, pd.read_csv(**kwargs)])

FILE_NAME = 'stat_can_file.csv'
kwargs = {
    'excel_writer': FILE_NAME,
    'index': False
}
df.to_csv(**kwargs)
