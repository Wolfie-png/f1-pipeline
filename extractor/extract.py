import fastf1

def extract_session(year, race, session_type):
    fastf1.Cache.enable_cache('cache')
    session = fastf1.get_session(year, race, session_type)
    session.load()
    return session.laps