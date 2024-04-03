import pycountry


def format_country(df, countrycol):
    lst = []
    countries = {}
    for country in pycountry.countries:
        countries[country.name.lower()] = country.alpha_2

    countries["usa"] = "US"
    countries["deutschland"] = "DE"
    countries["vietnam"] = "VE"
    countries["south korea"] = "KR"
    countries["england"] = "UK"
    countries["japan"] = 'JP'
    countries["australia "] = "AU"
    countries["aus"] = "AU"

    for c in df[countrycol]:
        if (len(c) == 2) & (c != "UK"):
            lst.append(c)
        if c == "UK":
            lst.append("GB")
        else:

            lst.append(countries.get(c.lower().strip()))
    df["ISO_code"] = lst
    return df


def country_names():
    lst = []
    for country in pycountry.countries:
        lst.append(country.name)
    return lst
