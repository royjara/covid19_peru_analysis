# imports
import pandas as pd
import seaborn as sns

sns.set(rc={'figure.figsize':(11, 4)})

def add_20(date):
    try:
        assert(isinstance(date, str))
        if date[-4:] != "2020":
            date = date +"20"
    except AssertionError:
        print('assertionError on ', date)
    return date

def load_data(input_file):
    df = pd.read_csv(input_file,
                           encoding='ISO-8859-1',
                           na_values="nan").drop(columns=['UUID']).dropna(subset=['FECHA_RESULTADO'])
    df['fixed_date'] = df['FECHA_RESULTADO'].apply(func=add_20)
    df['fixed_date'] = pd.to_datetime(df['fixed_date'], format="%d/%m/%Y")
    return df


def get_selection():
    departamento = input("Departamento?\n\t").upper()
    provincia = input("Provincia?\n\t").upper()
    distrito = input("Distrito?\n\t").upper()
    # edad = float(input("Edad?\n\t"))  # make it range
    # metodo = input("Metodo? PR/PCR\n\t").upper()
    # sexo = input("Sexo? Masculino/Femenino\n\t").upper()

    selection = {}
    selection['departamento'] = departamento
    selection['provincia'] = provincia
    selection['distrito'] = distrito
    # selection['edad'] = edad
    # selection['metodo'] = metodo
    # selection['sexo'] = sexo
    return selection


def get_final_df(selection, df):
    df['count'] = 1

    if selection['departamento'] != "":
        df = df[df['DEPARTAMENTO']==selection['departamento']]
    else:
        df = df.groupby(['fixed_date'], as_index=False)['count'].sum()
        df = df.set_index('fixed_date').sort_index()
        df['cum'] = df['count'].cumsum()
        return df

    if selection['provincia'] != "":
        df = df[df['PROVINCIA']==selection['provincia']]
    else:
        df = df.groupby(['DEPARTAMENTO', 'fixed_date'], as_index=False)['count'].sum()
        df = df[df['DEPARTAMENTO']==selection['departamento']].set_index('fixed_date').sort_index()
        df['cum'] = df['count'].cumsum()
        return df

    if selection['distrito'] != "":
        df = df[df['DISTRITO']==selection['distrito']]
        df = df.groupby(['DISTRITO', 'fixed_date'], as_index=False)['count'].sum()
        df = df[df['DISTRITO']==selection['distrito']].set_index('fixed_date').sort_index()
        df['cum'] = df['count'].cumsum()
        return df
    else:
        df = df.groupby(['PROVINCIA', 'fixed_date'], as_index=False)['count'].sum()
        df = df[df['PROVINCIA']==selection['provincia']].set_index('fixed_date').sort_index()
        df['cum'] = df['count'].cumsum()
        return df

def plot(df):
    df['cum'].plot(linewidth=0.8);
