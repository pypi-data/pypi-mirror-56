from datetime import date, timedelta

koreanHolidays = [
  {"dt": date(2019, 1, 1), "name" : "새해"},
  {"dt": date(2019, 2, 4), "name" : "설날"},
  {"dt": date(2019, 2, 5), "name" : "설날"},
  {"dt": date(2019, 2, 6), "name" : "설날"},
  {"dt": date(2019, 3, 1), "name" : "삼일절"},
  {"dt": date(2019, 5, 1), "name" : "근로자의날"},
  {"dt": date(2019, 5, 5), "name" : "어린이날"},
  {"dt": date(2019, 5, 12), "name" : "부처님오신날"},
  {"dt": date(2019, 6, 6), "name" : "현충일"},
  {"dt": date(2019, 8, 15), "name" : "광복절"},
  {"dt": date(2019, 9, 12), "name" : "추석"},
  {"dt": date(2019, 9, 13), "name" : "추석"},
  {"dt": date(2019, 9, 14), "name" : "추석"},
  {"dt": date(2019, 10, 3), "name" : "개천절"},
  {"dt": date(2019, 10, 9), "name" : "한글날"},
  {"dt": date(2019, 12, 25), "name" : "크리스마스"},
  {"dt": date(2020, 1, 1), "name" : "새해"},
  {"dt": date(2020, 1, 24), "name" : "설날"},
  {"dt": date(2020, 1, 25), "name" : "설날"},
  {"dt": date(2020, 1, 26), "name" : "설날"},
  {"dt": date(2020, 3, 1), "name" : "삼일절"},
  {"dt": date(2020, 4, 15), "name" : "21대 국회의원선거"},
  {"dt": date(2020, 4, 30), "name" : "부처님오신날"},
  {"dt": date(2020, 5, 1), "name" : "근로자의날"},
  {"dt": date(2020, 5, 5), "name" : "어린이날"},
  {"dt": date(2020, 6, 6), "name" : "현충일"},
  {"dt": date(2020, 8, 15), "name" : "광복절"},
  {"dt": date(2020, 9, 30), "name" : "추석"},
  {"dt": date(2020, 10, 1), "name" : "추석"},
  {"dt": date(2020, 10, 2), "name" : "추석"},
  {"dt": date(2020, 10, 3), "name" : "개천절"},
  {"dt" : date(2020, 10, 9), "name" : "한글날"},
  {"dt" : date(2020, 12, 25), "name" : "크리스마스"},
  {"dt" : date(2021, 1, 1), "name" : "새해"},
  {"dt" : date(2021, 2, 12), "name" : "설날"},
  {"dt" : date(2021, 2, 13), "name" : "설날"},
  {"dt" : date(2021, 2, 14), "name" : "설날"},
  {"dt" : date(2021, 3, 1), "name" : "삼일절"},
  {"dt" : date(2021, 5, 1), "name" : "근로자의날" },
  {"dt": date(2021, 5, 5), "name" : "어린이날" },
  {"dt": date(2021, 5, 19), "name" : "부처님오신날" },
  {"dt": date(2021, 6, 6), "name" : "현충일" },
  {"dt": date(2021, 8, 15), "name" : "광복절" },
  {"dt": date(2021, 9, 20), "name" : "추석" },
  {"dt": date(2021, 9, 21), "name" : "추석" },
  {"dt": date(2021, 9, 22), "name" : "추석" },
  {"dt": date(2021, 10, 3), "name" : "개천절" },
  {"dt": date(2021, 10, 9), "name" : "한글날" },
  {"dt": date(2021, 12, 25), "name" : "크리스마스" },
  {"dt": date(2022, 1, 1), "name" : "새해" },
  {"dt": date(2022, 1, 31), "name" : "설날" },
  {"dt": date(2022, 2, 1), "name" : "설날" },
  {"dt": date(2022, 2, 2), "name" : "설날" },
  {"dt": date(2022, 3, 1), "name" : "삼일절" },
  {"dt": date(2022, 5, 1), "name" : "근로자의날" },
  {"dt": date(2022, 5, 5), "name" : "어린이날" },
  {"dt": date(2022, 5, 8), "name" : "부처님오신날" },
  {"dt": date(2022, 6, 1), "name" : "2020지방선거" },
  {"dt": date(2022, 6, 6), "name" : "현충일" },
  {"dt": date(2022, 8, 15), "name" : "광복절" },
  {"dt": date(2022, 9, 9), "name" : "추석" },
  {"dt": date(2022, 9, 10), "name" : "추석" },
  {"dt": date(2022, 9, 11), "name" : "추석" },
  {"dt": date(2022, 10, 3), "name" : "개천절" },
  {"dt": date(2022, 10, 9), "name" : "한글날" },
  {"dt": date(2022, 12, 21), "name" : "20대 대통령선거" },
  {"dt": date(2022, 12, 25), "name" : "크리스마스" },
  {"dt": date(2023, 1, 1), "name" : "새해" },
  {"dt": date(2023, 1, 22), "name" : "설날" },
  {"dt": date(2023, 3, 1), "name" : "삼일절" },
  {"dt": date(2023, 5, 1), "name" : "근로자의날" },
  {"dt": date(2023, 5, 5), "name" : "어린이날" },
  {"dt": date(2023, 5, 27), "name" : "부처님오신날" },
  {"dt": date(2023, 6, 6), "name" : "현충일" },
  {"dt": date(2023, 8, 15), "name" : "광복절" },
  {"dt": date(2023, 9, 29), "name" : "추석" },
  {"dt": date(2023, 10, 3), "name" : "개천절" },
  {"dt": date(2023, 10, 9), "name" : "한글날" },
  {"dt": date(2023, 12, 25), "name" : "크리스마스" }
]


def first_business_day(day):
    """
    date 를 포함해서 date이후 첫 영업일 리턴
    date 가 휴일일 경우 date 이후 첫 영업일
    date 가 휴일이 아닐 경우 date 리턴
    :param day: 기준일
    :return:  date 를 포함해서 date 이후 첫 영업일
    """
    candidates = [day + timedelta(days=x) for x in range(0, 50)]
    return list(filter(is_businessday, candidates))[0]


def is_businessday(day):
    return not is_holiday(day)


def is_holiday(day):
    holidays = list(map(lambda d: d.get("dt"), koreanHolidays))
    weekday = day.isoweekday()
    if weekday == 6 or weekday == 7 or day in holidays:
        return True
    else:
        return False


if __name__ == "__main__":
    assert date(2019, 11, 22) == first_business_day(date(2019, 11, 22))
    assert date(2019, 11, 25) == first_business_day(date(2019, 11, 23))
    assert date(2019, 11, 25) == first_business_day(date(2019, 11, 24))
    assert date(2019, 11, 25) == first_business_day(date(2019, 11, 25))
    assert date(2019, 11, 26) == first_business_day(date(2019, 11, 26))
    assert date(2019, 9, 11) == first_business_day(date(2019, 9, 11))
    assert date(2019, 9, 16) == first_business_day(date(2019, 9, 12))
    assert date(2019, 9, 16) == first_business_day(date(2019, 9, 13))



