import requests

from api import models

from bs4 import BeautifulSoup


def parse_complexes():
    url = 'https://ask-yug.com/api/filter/commercial/'

    r = requests.get(url).json()

    return r


def parse_complex_rooms(id):
    url = f'https://ask-yug.com/api/filter/commercial/get/?objects={id}'

    r = requests.get(url)

    if not r.content:
        return None

    return r.json()


def get_liter_complex_rooms(rooms, liter):
    return list(filter(lambda x: x['liter'] == liter, rooms))


def parse_liters_sections_floors_plans(id):
    url = f'https://ask-yug.com/api/filter/commercial/object/?object_id={id}'

    r = requests.get(url).json()

    return r


def parse_plan(plan: str):
    soup = BeautifulSoup(plan, 'lxml')

    svg = soup.find('svg')
    print(svg)

    attr_name = 'viewBox'
    if not svg.get(attr_name):
        attr_name = 'viewbox'

    *_, width, height = svg.get(attr_name).split()
    width, height = float(width), float(height)

    image = soup.find('image')

    image_url = image.get('xlink:href')

    tags = soup.findAll(attrs={'id': True, 'fill': True})

    paths = []

    for tag in tags:
        if tag.name == 'rect':
            paths.append(
                {"d": f'M{tag.get("x")},{tag.get("y")}h{tag.get("width")}v{tag.get("height")}h-{tag.get("width")}Z',
                 "room_id": int(tag.get("data-id"))})

        elif tag.name == 'path':
            paths.append({"d": tag.get('d'), "room_id": int(tag.get("data-id"))})

    plan_data = {
        "width": width,
        "height": height,
        "image": image_url,
        "paths": paths
    }

    return plan_data


def get_complex_address(name, complex_rooms):
    for room in complex_rooms:
        if room['object']['name'] == name:
            return room['object']['address']


def fill_db():
    data = parse_complexes()

    cities = data['cityList']

    for city in cities:

        city_instance, created = models.City.objects.get_or_create(name=city['name'])

        districts = city['districts']
        for district in districts:
            if district['name'] == "Любой":
                continue

            district_instance, created = models.District.objects.get_or_create(name=district['name'],
                                                                               city=city_instance)

            for complex in district['complexes']:
                complex_rooms = parse_complex_rooms(complex['id'])

                if not complex_rooms:
                    continue

                complex_address = get_complex_address(complex['name'], complex_rooms)

                complex_instance, created = models.Complex.objects.get_or_create(district=district_instance,
                                                                                 address=complex_address,
                                                                                 name=complex['name'])

                liters = parse_liters_sections_floors_plans(complex['id'])

                for liter in liters:
                    liter_instance, created = models.Liter.objects.get_or_create(number=int(liter['number']),
                                                                                 complex=complex_instance)
                    complex_rooms = get_liter_complex_rooms(complex_rooms, f'Литер {liter_instance.number}')
                    sections = liter['sections']
                    for section in sections.values():
                        section_instance, created = models.Section.objects.get_or_create(liter=liter_instance,
                                                                                         number=int(section['number']))
                        floors = section['floors']
                        for floor in floors:
                            # parsed_plan = parse_plan(floor['plan'])
                            parsed_plan = floor['plan']
                            plan_instance, created = models.Plan.objects.get_or_create(html=parsed_plan)

                            floor_instance, created = models.Floor.objects.get_or_create(section=section_instance,
                                                                                         number=int(floor['number']),
                                                                                         plan=plan_instance)

                            # for path in parsed_plan['paths']:
                            # models.Path.objects.get_or_create(plan=plan_instance,
                            #                                   room_id=path['room_id'],
                            #                                   d=path['d'])

                            for room in complex_rooms:
                                if int(room['floor']) == floor_instance.number and room[
                                    'liter'] == f'Литер {liter["number"]}' and room['object'][
                                    'name'] == complex_instance.name:
                                    if models.Room.objects.filter(id=int(room['id'])).count():
                                        continue

                                    print(dict(id=int(room['id']),
                                               floor=floor_instance,
                                               price=int(room['price'].replace(" ", "")),
                                               name=room['name'],
                                               area=float(room['area'])))

                                    room_instance, created = models.Room.objects.get_or_create(id=int(room['id']),
                                                                                               floor=floor_instance,
                                                                                               price=int(room[
                                                                                                   'price'].replace(
                                                                                                   " ", "")),
                                                                                               name=room['name'],
                                                                                               area=float(room['area']),
                                                                                               plan=f"https://ask-yug.com{room['plan']}")


def fill_commerce():
    data = parse_complexes()

    for city in data['cityList']:
        for district in city['districts']:
            if district['name'] == "Любой":
                continue

            for complex in district['complexes']:
                for commercial in complex['types']:
                    room_id = int(commercial['id'])
                    name = commercial['name']

                    commercial_instance, created = models.Commercial.objects.get_or_create(name=name)

                    if not models.Room.objects.filter(id=room_id).count():
                        continue
                    print(commercial_instance)
                    room = models.Room.objects.get(id=room_id)
                    room.commercial = commercial_instance
                    room.save()


def get_starts_count(html):
    soup = BeautifulSoup(html, 'lxml')

    els = soup.findAll('span', class_='fa fa-star cst')

    return len(els)


def parse_point_ratings(lat, long):
    cookies = "_ym_d=1658499011; _ym_uid=16584990111027789945; sw_t=on; sw_p=on; sw_c=on; tmr_lvid=1fe4a3058cf42a952d32ffb91032fe56; tmr_lvidTS=1658499012240; _ga=GA1.2.750144860.1658499012; _gid=GA1.2.549039303.1658499012; rubric=41175; city=16; _ym_isad=1; _ym_visorc=w; _gat_gtag_UA_76109420_7=1; session=XNZILaSbtro6UP5U; tmr_detect=1%7C1658573433110; tmr_reqNum=55"

    cookie_dict = {}
    for cook in cookies.split(';'):
        k, v = cook.split('=')
        cookie_dict[k] = v.rstrip()

    url = "https://mestomer.com/rubrics2.pl"

    r = requests.get(url, cookies=cookie_dict).json()['data']

    res = []

    for rub in r['rubrics']:
        rub_id = rub['id']
        title = rub['title']
        sector = rub['sector']

        url = f"https://mestomer.com/point.pl?rubric={rub_id}&lat={lat}&lon={long}"
        r = requests.get(url, cookies=cookie_dict)

        json = r.json()['data']
        res.append(dict(
            title=title,
            sector=sector,
            welfare_score=get_starts_count(json['welfare_score']),
            traffic_score=get_starts_count(json['traffic_score']),
            competitors_score=get_starts_count(json['competitors_score']),
            population_score=get_starts_count(json['population_score'])
        ))

    return res


def parse_complexes_ratings():
    complexes = {
        "ЖК «Спортивный Парк»": "45.0463758,39.1093058",
        "ЖК «Смородина»": "45.0576479,39.1042724",
        "ЖК Fresh": "44.9914608,39.0693023",
        "ЖК AVrorA": "45.0656666,38.9715475",
        "ЖК URAL": "45.0374855,39.0703733",
        "ЖК Novella": "45.1013298,38.9553605"
    }

    for k, v in complexes.items():
        complex_instance = models.Complex.objects.get(name=k)

        lat, lon = v.split(',')

        ratings_val = parse_point_ratings(lat, lon)

        for el in ratings_val:
            print(complex_instance.name, el['title'], el['sector'])
            models.CommercialRecommendationsRatings.objects.get_or_create(**el, complex=complex_instance)
