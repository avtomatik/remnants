
from pandas import DataFrame
from python.strings.src.lib import trim_string

LATIN_SUBSTITUTION = '''a,b,v,g,d,e,zh,z,i,y,k,l,m,n,o,p,r,s,t,u,f,kh,ts,ch,sh,shch,,y,,e,yu,ya,,yo'''
MAP_CYRILLIC_TO_LATIN = {
    chr(_): latin for _, latin in enumerate(LATIN_SUBSTITUTION.split(","), start=1072)
}


def transliterate(word: str, mapping: dict[str] = MAP_CYRILLIC_TO_LATIN) -> str:
    return ''.join(
        mapping[_.lower()] if _.lower() in mapping.keys() else _ for _ in word
    )


def trim_columns(df: DataFrame) -> DataFrame:
    df.columns = map(lambda _: trim_string(_, fill='_').lower(), df.columns)
    return df
