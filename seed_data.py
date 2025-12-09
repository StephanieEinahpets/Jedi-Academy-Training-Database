from flask_bcrypt import generate_password_hash
from datetime import datetime
from db import db
from models.users import Users
from models.temples import Temples
from models.species import Species
from models.masters import Masters
from models.padawans import Padawans
from models.crystals import Crystals
from models.lightsabers import Lightsabers
from models.courses import Courses
from models.padawan_courses import PadawanCourses


def seed_database(app):
  with app.app_context():
    print("Beginning Jedi Academy database seeding...")
    
    db.session.query(PadawanCourses).delete()
    db.session.query(Lightsabers).delete()
    db.session.query(Courses).delete()
    db.session.query(Padawans).delete()
    db.session.query(Masters).delete()
    db.session.query(Crystals).delete()
    db.session.query(Species).delete()
    db.session.query(Users).delete()
    db.session.query(Temples).delete()
    db.session.commit()

    temples = [
      Temples(
        temple_name="Jedi Temple Coruscant",
        planet="Coruscant",
        master_count=50,
        padawan_limit=500
      ),
      Temples(
        temple_name="Jedi Enclave Dantooine",
        planet="Dantooine",
        master_count=20,
        padawan_limit=100
      ),
      Temples(
        temple_name="Hidden Temple Ahch-To",
        planet="Ahch-To",
        master_count=1,
        padawan_limit=10
      )
    ]
    
    for temple in temples:
      db.session.add(temple)
    db.session.commit()
    print(f"Created {len(temples)} temples")

    species_list = [
      Species(species_name="Human", homeworld="Various", force_sensitive=True, avg_lifespan=100),
      Species(species_name="Togruta", homeworld="Shili", force_sensitive=True, avg_lifespan=94),
      Species(species_name="Twi'lek", homeworld="Ryloth", force_sensitive=True, avg_lifespan=75),
      Species(species_name="Rodian", homeworld="Rodia", force_sensitive=True, avg_lifespan=80),
      Species(species_name="Wookiee", homeworld="Kashyyyk", force_sensitive=True, avg_lifespan=400),
      Species(species_name="Yoda's Species", homeworld="Unknown", force_sensitive=True, avg_lifespan=900)
    ]
    
    for species in species_list:
      db.session.add(species)
    db.session.commit()
    print(f"Documented {len(species_list)} species")

    coruscant = db.session.query(Temples).filter(Temples.temple_name == "Jedi Temple Coruscant").first()
    dantooine = db.session.query(Temples).filter(Temples.temple_name == "Jedi Enclave Dantooine").first()
    ahch_to = db.session.query(Temples).filter(Temples.temple_name == "Hidden Temple Ahch-To").first()
    
    human = db.session.query(Species).filter(Species.species_name == "Human").first()
    togruta = db.session.query(Species).filter(Species.species_name == "Togruta").first()
    yoda_species = db.session.query(Species).filter(Species.species_name == "Yoda's Species").first()

    users_data = [
      {
        "username": "yoda",
        "email": "yoda@jediorder.com",
        "password": "ForceMaster900",
        "force_rank": "Grand Master",
        "midi_count": 17700,
        "temple_id": coruscant.temple_id
      },
      # Council Members
      {
        "username": "mace_windu",
        "email": "mace@jediorder.com",
        "password": "PurpleBlade77",
        "force_rank": "Council",
        "midi_count": 12000,
        "temple_id": coruscant.temple_id
      },
      # Masters
      {
        "username": "obi_wan",
        "email": "obi-wan@jediorder.com",
        "password": "HighGround66",
        "force_rank": "Master",
        "midi_count": 13400,
        "temple_id": coruscant.temple_id
      },
      {
        "username": "qui_gon",
        "email": "qui-gon@jediorder.com",
        "password": "LivingForce88",
        "force_rank": "Master",
        "midi_count": 10000,
        "temple_id": dantooine.temple_id
      },
      # Knights
      {
        "username": "anakin",
        "email": "anakin@jediorder.com",
        "password": "ChosenOne99",
        "force_rank": "Knight",
        "midi_count": 20000,
        "temple_id": coruscant.temple_id
      },
      # Padawans
      {
        "username": "ahsoka",
        "email": "ahsoka@jediorder.com",
        "password": "Snips123",
        "force_rank": "Padawan",
        "midi_count": 15000,
        "temple_id": coruscant.temple_id
      },
      {
        "username": "barriss",
        "email": "barriss@jediorder.com",
        "password": "Healer456",
        "force_rank": "Padawan",
        "midi_count": 12500,
        "temple_id": coruscant.temple_id
      },
      # Younglings
      {
        "username": "caleb",
        "email": "caleb@jediorder.com",
        "password": "Youngling789",
        "force_rank": "Youngling",
        "midi_count": 11000,
        "temple_id": dantooine.temple_id
      }
    ]

    created_users = []
    for user_data in users_data:
      new_user = Users(
        temple_id=user_data["temple_id"],
        username=user_data["username"],
        email=user_data["email"],
        password=generate_password_hash(user_data["password"]).decode('utf8'),
        force_rank=user_data["force_rank"],
        midi_count=user_data["midi_count"]
      )
      db.session.add(new_user)
      created_users.append(new_user)
    
    db.session.commit()
    print(f"Created {len(created_users)} Force users")

    yoda = db.session.query(Users).filter(Users.username == "yoda").first()
    obi_wan = db.session.query(Users).filter(Users.username == "obi_wan").first()
    qui_gon = db.session.query(Users).filter(Users.username == "qui_gon").first()
    anakin = db.session.query(Users).filter(Users.username == "anakin").first()
    ahsoka = db.session.query(Users).filter(Users.username == "ahsoka").first()
    barriss = db.session.query(Users).filter(Users.username == "barriss").first()

    masters_data = [
      {
        "user_id": yoda.user_id,
        "master_name": "Yoda",
        "specialization": "Force Mastery",
        "years_training": 800,
        "max_padawans": 5
      },
      {
        "user_id": obi_wan.user_id,
        "master_name": "Obi-Wan Kenobi",
        "specialization": "Soresu Defense",
        "years_training": 25,
        "max_padawans": 3
      },
      {
        "user_id": qui_gon.user_id,
        "master_name": "Qui-Gon Jinn",
        "specialization": "Living Force",
        "years_training": 30,
        "max_padawans": 3
      }
    ]

    created_masters = []
    for master_data in masters_data:
      new_master = Masters(**master_data)
      db.session.add(new_master)
      created_masters.append(new_master)
    
    db.session.commit()
    print(f"Created {len(created_masters)} Jedi Masters")

    master_yoda = db.session.query(Masters).filter(Masters.master_name == "Yoda").first()
    master_obi_wan = db.session.query(Masters).filter(Masters.master_name == "Obi-Wan Kenobi").first()
    master_qui_gon = db.session.query(Masters).filter(Masters.master_name == "Qui-Gon Jinn").first()

    padawans_data = [
      {
        "user_id": anakin.user_id,
        "species_id": human.species_id,
        "padawan_name": "Anakin Skywalker",
        "age": 19,
        "master_id": master_obi_wan.master_id,
        "training_level": 5
      },
      {
        "user_id": ahsoka.user_id,
        "species_id": togruta.species_id,
        "padawan_name": "Ahsoka Tano",
        "age": 14,
        "master_id": master_yoda.master_id,
        "training_level": 3
      },
      {
        "user_id": barriss.user_id,
        "species_id": human.species_id,
        "padawan_name": "Barriss Offee",
        "age": 16,
        "master_id": master_qui_gon.master_id,
        "training_level": 4
      }
    ]

    created_padawans = []
    for padawan_data in padawans_data:
      new_padawan = Padawans(**padawan_data)
      db.session.add(new_padawan)
      created_padawans.append(new_padawan)
    
    db.session.commit()
    print(f"Created {len(created_padawans)} Padawans")

    padawan_ahsoka = db.session.query(Padawans).filter(Padawans.padawan_name == "Ahsoka Tano").first()
    padawan_barriss = db.session.query(Padawans).filter(Padawans.padawan_name == "Barriss Offee").first()

    crystals_data = [
      {
        "crystal_type": "Ilum Crystal - Blue",
        "origin_planet": "Ilum",
        "rarity_level": "Common",
        "force_amplify": 1.2
      },
      {
        "crystal_type": "Ilum Crystal - Green",
        "origin_planet": "Ilum",
        "rarity_level": "Common",
        "force_amplify": 1.2
      },
      {
        "crystal_type": "Adegan Crystal",
        "origin_planet": "Adega",
        "rarity_level": "Uncommon",
        "force_amplify": 1.5
      },
      {
        "crystal_type": "Krayt Dragon Pearl",
        "origin_planet": "Tatooine",
        "rarity_level": "Legendary",
        "force_amplify": 2.0
      },
      {
        "crystal_type": "Synthetic Crystal",
        "origin_planet": "Laboratory",
        "rarity_level": "Rare",
        "force_amplify": 1.8
      }
    ]

    created_crystals = []
    for crystal_data in crystals_data:
      new_crystal = Crystals(**crystal_data)
      db.session.add(new_crystal)
      created_crystals.append(new_crystal)
  
    db.session.commit()
    print(f"Cataloged {len(created_crystals)} crystals")

    blue_crystal = db.session.query(Crystals).filter(Crystals.crystal_type == "Ilum Crystal - Blue").first()
    green_crystal = db.session.query(Crystals).filter(Crystals.crystal_type == "Ilum Crystal - Green").first()
    pearl = db.session.query(Crystals).filter(Crystals.crystal_type == "Krayt Dragon Pearl").first()

    print("Constructing Lightsabers...")
    lightsabers_data = [
      {
        "owner_id": anakin.user_id,
        "crystal_id": blue_crystal.crystal_id,
        "saber_name": "Skywalker's Blade",
        "hilt_material": "Durasteel",
        "blade_color": "Blue",
        "is_completed": True
      },
      {
        "owner_id": ahsoka.user_id,
        "crystal_id": green_crystal.crystal_id,
        "saber_name": "Tano's Shoto",
        "hilt_material": "Cortosis",
        "blade_color": "Green",
        "is_completed": True
      },
      {
        "owner_id": obi_wan.user_id,
        "crystal_id": blue_crystal.crystal_id,
        "saber_name": "Kenobi's Saber",
        "hilt_material": "Alloy Metal",
        "blade_color": "Blue",
        "is_completed": True
      }
    ]

    created_lightsabers = []
    for lightsaber_data in lightsabers_data:
      new_lightsaber = Lightsabers(**lightsaber_data)
      db.session.add(new_lightsaber)
      created_lightsabers.append(new_lightsaber)
    
    db.session.commit()
    print(f"Constructed {len(created_lightsabers)} lightsabers")

    courses_data = [
      {
        "instructor_id": master_yoda.master_id,
        "course_name": "Force Meditation and Control",
        "difficulty": "Advanced",
        "duration_weeks": 16,
        "max_students": 15
      },
      {
        "instructor_id": master_obi_wan.master_id,
        "course_name": "Lightsaber Combat Form III: Soresu",
        "difficulty": "Intermediate",
        "duration_weeks": 12,
        "max_students": 20
      },
      {
        "instructor_id": master_qui_gon.master_id,
        "course_name": "Living Force Philosophy",
        "difficulty": "Beginner",
        "duration_weeks": 8,
        "max_students": 25
      },
      {
        "instructor_id": master_yoda.master_id,
        "course_name": "Lightsaber Combat Form I: Shii-Cho",
        "difficulty": "Beginner",
        "duration_weeks": 10,
        "max_students": 30
      }
    ]

    created_courses = []
    for course_data in courses_data:
      new_course = Courses(**course_data)
      db.session.add(new_course)
      created_courses.append(new_course)
    
    db.session.commit()
    print(f"Created {len(created_courses)} training courses")

    meditation_course = db.session.query(Courses).filter(Courses.course_name == "Force Meditation and Control").first()
    soresu_course = db.session.query(Courses).filter(Courses.course_name == "Lightsaber Combat Form III: Soresu").first()
    shii_cho_course = db.session.query(Courses).filter(Courses.course_name == "Lightsaber Combat Form I: Shii-Cho").first()

    enrollments_data = [
      {
        "padawan_id": padawan_ahsoka.padawan_id,
        "course_id": meditation_course.course_id
      },
      {
        "padawan_id": padawan_ahsoka.padawan_id,
        "course_id": soresu_course.course_id
      },
      {
        "padawan_id": padawan_barriss.padawan_id,
        "course_id": shii_cho_course.course_id
      }
    ]

    created_enrollments = []
    for enrollment_data in enrollments_data:
      new_enrollment = PadawanCourses(**enrollment_data)
      db.session.add(new_enrollment)
      created_enrollments.append(new_enrollment)
    
    db.session.commit()
    print(f"Created {len(created_enrollments)} course enrollments")

    print("TEST CREDENTIALS:")
    print("-" * 60)
    print("Grand Master: yoda@jediorder.com / ForceMaster900")
    print("Council:      mace@jediorder.com / PurpleBlade77")
    print("Master:       obi-wan@jediorder.com / HighGround66")
    print("Knight:       anakin@jediorder.com / ChosenOne99")
    print("Padawan:      ahsoka@jediorder.com / Snips123")
    print("Youngling:    caleb@jediorder.com / Youngling789")
    print("="*60)
    print("May the Force be with you!")
