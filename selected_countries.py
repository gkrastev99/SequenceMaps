from sequence import Sequence

# Maps countries to weight
country_to_weight      = {
                          'Russia':        2772010,
                          'Poland':        1409139,
                          'Germany':        997895,
                          'Czech Republic': 433488,
                          'Italy':          170646,
                          'Turkey':         145000,
                          'Spain':          144668,
                          'United Kingdom': 120600,
                          'France':         105000,
                          'Slovakia':        90612,
                          'Moldova':         90525,
                          'Romania':         86178,
                          'Austria':         82446,
                          'Bulgaria':        77114,
                          'Netherlands':     76600,
                          'Switzerland':     64053,
                          'Lithuania':       63279,
                          'Belgium':         56013,
                          'Estonia':         51501,
                          'Portugal':        49718,
                          'Ireland':         46481,
                          'Sweden':          45552,
                          'Latvia':          36912,
                          'Finland':         36652,
                          'Denmark':         35193,
                          'Hungary':         30000,
                          'Georgia':         26376,
                          'Montenegro':      24482,
                          'Norway':          27844,
                          'Croatia':         21877,
                          'Greece':          18745,
                          'Serbia':          18596,
                          'Cyprus':          13852,
                          'Belarus':         12505
                         }

seq_countries = [
    #["Russia"],
    ["Russia",  "Georgia"],
    ["Russia",  "Georgia",        "Turkey"],
    #["Russia",  "Finland"],#
    ["Russia",  "Estonia"],
    #["Russia",  "Latvia"],#
    ["Russia",  "Latvia",         "Lithuania"],
    #["Russia",  "Belarus"],#

    ["Belarus"],
    ["Belarus", "Latvia"],
    #["Belarus", "Latvia",         "Estonia"],
    #["Belarus", "Lithuania"],#
    #["Belarus", "Russia"],#
    #["Belarus", "Russia",         "Estonia"],#
    ["Belarus", "Russia",         "Finland"],
    #["Belarus", "Poland"],#

    ["Poland"],
    #["Poland",  "Lithuania"],#
    ["Poland",  "Germany"],
    ["Poland",  "Germany",        "Belgium"],
    ["Poland",  "Germany",        "Denmark"],
    ["Poland",  "Germany",        "Netherlands"],
    ["Poland",  "Germany",        "Netherlands", "Denmark", "Sweden"],
    ["Poland",  "Germany",        "Netherlands", "Denmark", "Sweden",  "Norway"],
    #["Poland",  "Czech Republic", "Austria",     "Germany", "Belgium"],#
    ["Poland",  "Czech Republic"],
    #["Poland",  "Czech Republic", "Austria"],#
    ["Poland",  "Czech Republic", "Austria",     "Germany", "Belgium", "France"],
    ["Poland",  "Czech Republic", "Austria",     "Germany", "Belgium", "France",         "United Kingdom"],
    ["Poland",  "Czech Republic", "Austria",     "Germany", "Belgium", "United Kingdom", "Ireland"],

    ["Slovakia"],
    #["Slovakia", "Poland"],#
    #["Slovakia", "Czech Republic"],#
    ["Slovakia", "Austria"],
    #["Slovakia", "Hungary"],#

    ["Hungary"],
    #["Hungary", "Slovakia"],#
    ["Hungary", "Slovakia",       "Italy"],
    #["Hungary", "Austria"],#
    ["Hungary", "Austria",        "Switzerland"],
    ["Hungary", "Austria",        "Switzerland", "France",  "Spain"],
    ["Hungary", "Austria",        "Switzerland", "France",  "Spain",   "Portugal"],
    ["Hungary", "Croatia"],
    #["Hungary", "Serbia"],#
    #["Hungary", "Romania"],#

    ["Romania"],
    #["Romania", "Hungary"],#
    #["Romania", "Serbia"],#
    #["Romania", "Bulgaria"],#
    ["Romania", "Serbia",         "Montenegro"],

    ["Moldova"],
    #["Moldova", "Romania"],
    ["Moldova", "Romania",        "Serbia"],
    #["Moldova", "Romania",        "Serbia",      "Hungary"],#
    ["Moldova", "Romania",        "Bulgaria"],
    ["Moldova", "Romania",        "Bulgaria",    "Greece"],
    ["Moldova", "Romania",        "Bulgaria",    "Turkey",  "Cyprus"],
]

class SelCount:
    def SelSequences(country_to_location):
        sequences = []

        for seq in seq_countries:
            locs = [country_to_location["Ukraine"]]

            for country in seq:
                location = country_to_location[country]
                locs.append(location)

            weight = country_to_weight[country]

            sequences.append(Sequence(locs, weight))
 
        return sequences
