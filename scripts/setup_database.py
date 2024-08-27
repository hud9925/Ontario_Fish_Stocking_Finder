import pandas as pd
import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Retrieve environment variables
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Database connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine and connect to the database
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        logging.info("Connection successful")

    # Define metadata
    metadata = MetaData()

    # Setup tables
    waterbodies = Table('waterbodies', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('name', String(255), nullable=False),
                        Column('latitude', Float),
                        Column('longitude', Float))

    fish_species = Table('fish_species', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String(255), nullable=False))

    stocking_events = Table('stocking_events', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('waterbody_id', Integer, ForeignKey('waterbodies.id')),
                            Column('species_id', Integer, ForeignKey('fish_species.id')),
                            Column('number_of_fish', Integer))

    # Create tables in PostgreSQL
    metadata.create_all(engine)
    logging.info("Tables created successfully")

    script_dir = os.path.dirname(__file__)
    csv_file_path = os.path.join(script_dir, '..', 'data', 'cleaned_data.csv')

    # Load cleaned data
    df = pd.read_csv(csv_file_path)

    # Check for missing names
    missing_names_df = df[df['Official_Waterbody_Name'].isnull() | df['Official_Waterbody_Name'].str.strip() == '']
    if not missing_names_df.empty:
        logging.error("There are rows with missing waterbody names:")
        logging.error(missing_names_df)
        # Optionally, you can remove these rows
        df = df.dropna(subset=['Official_Waterbody_Name'])

    # Rename columns to match the database schema
    waterbodies_df = df[['Official_Waterbody_Name', 'Latitude', 'Longitude']].drop_duplicates()
    waterbodies_df.columns = ['name', 'latitude', 'longitude']
    waterbodies_df.to_sql('waterbodies', con=engine, if_exists='append', index=False)
    logging.info("Waterbodies table populated successfully")

    # Populate Fish Species
    species_df = df[['Species']].drop_duplicates()
    species_df.columns = ['name']
    species_df.to_sql('fish_species', con=engine, if_exists='append', index=False)
    logging.info("Fish species table populated successfully")

    # Prepare data for Stocking Events
    waterbody_map = pd.read_sql("SELECT id, name FROM waterbodies", engine).set_index('name').to_dict()['id']
    species_map = pd.read_sql("SELECT id, name FROM fish_species", engine).set_index('name').to_dict()['id']

    df['waterbody_id'] = df['Official_Waterbody_Name'].map(waterbody_map)
    df['species_id'] = df['Species'].map(species_map)

    events_df = df[['waterbody_id', 'species_id', 'Number_of_Fish_Stocked']]
    events_df.columns = ['waterbody_id', 'species_id', 'number_of_fish']
    events_df.to_sql('stocking_events', con=engine, if_exists='append', index=False)
    logging.info("Stocking events table populated successfully")

except SQLAlchemyError as e:
    logging.error("An error occurred: %s", e)
except Exception as e:
    logging.error("An unexpected error occurred: %s", e)
