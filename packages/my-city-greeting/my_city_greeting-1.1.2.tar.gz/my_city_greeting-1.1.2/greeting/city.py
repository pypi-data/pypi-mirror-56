from greeting.constants import City


def greeting_diff_city(city):
    all_allow_city = City()
    if city.upper() in all_allow_city.ALLOW_CYTI.keys():     
        a = all_allow_city.ALLOW_CYTI[city.upper()]
        return a

def render_greating(city):
    pass
