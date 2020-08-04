from dotenv import load_dotenv
load_dotenv()

from app import app, db
from app.models.models import (
    User, Calendar, Trip, 
    Amenity, Necessity, Location, Review)

with app.app_context():
    db.drop_all()
    db.create_all()

    # 4 users
    # 2 locations
    # 3 reviews

    user1 = User(
        first_name='Tony',
        last_name='Stark',
        hashed_password='asdfasdf',
        email='theonlyone@stark.com',
        domicile_type='rv',
        phone_number='678-136-7092',
        user_info='I\'m a wealthy American business magnate, playboy, and ingenious scientist. I suffered a severe chest injury during a kidnapping but survived that and kicking @$$ now.',
        createdAt='2021-07-01'
    )

    user2 = User(
        first_name='Bruce',
        last_name='Wayne',
        hashed_password='asdfasdf',
        email='bruce@wayneenterprises.com',
        domicile_type='camper',
        phone_number='221-516-6944',
        user_info='My favorite song goes like: na na na na na na na na na na BATMAN!!!.',
        createdAt='2021-06-21'
    )

    user3 = User(
        first_name='Natasha',
        last_name='Romanoff',
        hashed_password='asdfasdf',
        email='black.widow@avengers.com',
        domicile_type='car',
        phone_number='484-841-6537',
        user_info='I love watching Lost In Translation in the rain.',
        createdAt='2021-05-14'
    )

    user4 = User(
        first_name='Elvis',
        last_name='Presley',
        hashed_password='asdfasdf',
        email='elvis@lives.com',
        domicile_type='car',
        phone_number='373-611-7335',
        user_info='I ain\'t nothin\' but a hound dog.',
        createdAt='2021-02-15'
    )

    location1_amenity = Amenity(
        electric_hookup=True,
        water_hookup=True,
        septic_hookup=False,
        assigned_parking=False,
        tow_vehicle_parking=True,
        trash_removal=False,
        water_front=True,
        pets_allowed=True,
        internet_access=False
    )

    location2_amenity = Amenity(
        electric_hookup=True,
        water_hookup=True,
        septic_hookup=False,
        assigned_parking=False,
        tow_vehicle_parking=False,
        trash_removal=True,
        water_front=False,
        pets_allowed=True,
        internet_access=True
    )

    location1_neces = Necessity(
        rv_compatible=True,
        generators_allowed=True,
        fires_allowed=True,
        max_days=2,
        pad_type='grass'
    )

    location2_neces = Necessity(
        rv_compatible=True,
        generators_allowed=True,
        fires_allowed=True,
        max_days=5,
        pad_type='dirt'
    )
    
    location1 = Location(
        address='10880 Malibu Point',
        city='Malibu',
        state='CA',
        gps_coords='34.000872,-118.806839',
        description='It overlooks the Pacific Ocean with an amazing view. It was once destroyed from a very unfortunate happening, but now rebuilt like it never happened. Might find some interesting things down the basement.',
        host_notes='Have fun and then get out. Also, don\'t touch things without permission.'
    )

    location2 = Location(
        address='25218 Eu St.',
        city='Banjarmasin',
        state='ZE',
        gps_coords='-3.66105, 144.52694',
        description='Has world class museums, and gardens. It has an well developed walkable river front on the edge of downtown where various events are held.',
        host_notes='I\'m sad, so sad'
    )
    
    review1 = Review(
        overall_rating=4,
        noise=5,
        safety=4,
        cleanliness=5,
        access=1,
        site_quality=5,
        comments='Host is very lovely, the location was perfect and the parking easy.'
    )

    review2 = Review(
        overall_rating=3,
        noise=1,
        safety=4,
        cleanliness=3,
        access=4,
        site_quality=5,
        comments='This is a lovely spot, and a kind and generous host. The neighborhood is peaceful and beautiful, as well as easily walkable to shops and restaurants. A really terrific place to stay.'
    )

    review3 = Review(
        overall_rating=3,
        noise=3,
        safety=3,
        cleanliness=3,
        access=3,
        site_quality=3,
        comments='Hosts were welcoming and generous. Their little spot in the heart of this upscale area of Portland gave me and Journey (my dog) a walkable neighborhood to enjoy. I also relished the porch chats with our hosts, which were full of local history and politics, and a long walking tour of the neighborhood.'
    )

    location1.amenity = location1_amenity
    location1.necessities = location1_neces
    location1.user = user1

    location2.amenity = location2_amenity
    location2.necessities = location2_neces
    location2.user = user2

    review1.location = location1
    review1.user = user3
    review2.location = location1
    review2.user = user4
    review3.location = location2
    review3.user = user4

    db.session.add(location1)
    db.session.add(location2)
    db.session.commit()
