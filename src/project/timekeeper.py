
import datetime
ZODIAC=[(120,'Capricorn'),(219,'Aquarius'),(320,'Pisces'),(420,'Aries'),(521,'Taurus'),(621,'Gemini'),(722,'Cancer'),(823,'Leo'),(923,'Virgo'),(1023,'Libra'),(1122,'Scorpio'),(1222,'Sagittarius'),(1231,'Capricorn')]
def western_zodiac(dt: datetime.date)->str:
    md=dt.month*100+dt.day
    for cutoff,name in ZODIAC:
        if md<=cutoff: return name
    return 'Capricorn'
def lunar_phase_fraction(dt: datetime.date)->float:
    ref=datetime.date(2000,1,6)
    days=(dt-ref).days
    synodic=29.53058867
    return (days % synodic)/synodic
def lunar_phase_name(frac: float)->str:
    phases=[(0.02,'New Moon'),(0.24,'Waxing Crescent'),(0.26,'First Quarter'),(0.49,'Waxing Gibbous'),(0.51,'Full Moon'),(0.74,'Waning Gibbous'),(0.76,'Last Quarter'),(0.98,'Waning Crescent'),(1.01,'New Moon')]
    for th,name in phases:
        if frac<=th: return name
    return 'New Moon'
def celestial_time(dt: datetime.datetime|None=None)->dict:
    dt=dt or datetime.datetime.utcnow()
    frac=lunar_phase_fraction(dt.date())
    return {'gregorian':dt.strftime('%Y-%m-%d %H:%M:%S UTC'),'zodiac':western_zodiac(dt.date()),'lunar_phase_fraction':round(frac,4),'lunar_phase':lunar_phase_name(frac),'julian_day_approx':dt.toordinal()+1721424.5+(dt.hour+dt.minute/60+dt.second/3600)/24}
