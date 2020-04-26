import datetime
from app import save_data, load_data

save_data("卵", "2020/04/29", "イオｘｘ",datetime.datetime(2020,03,31, 0))

print(load_data())
