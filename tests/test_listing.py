from get_listing import get_listing

#12964428
#22475432
#16331385
#16038702
#427077
#9472023

def test_listing():
    assert type(get_listing(12964428)) == dict

def test_language_multilingual():
    assert '中文' in get_listing(22475432)["host_languages"]
    assert len(get_listing(22475432)["host_languages"]) ==4

def test_language_single():
    assert get_listing(12964428)["host_languages"][0] == "Polish"