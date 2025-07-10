import sqlite3
import subprocess
from pipeline.transform import transform_users, validate_user_visits
from pipeline.database import update_users_table, update_login_table
from pipeline.config_loader import load_json_config
from pipeline.load_data import load_user_data, load_login_data

def main():
    uk_config = load_json_config('mappings_uk.json')
    fr_config = load_json_config('mappings_fr.json')
    usa_config = load_json_config('mappings_usa.json')
    sc_config = load_json_config('mappings_sc.json')

    users_uk = load_user_data('data/UK User Data.csv', encoding='latin1')
    users_uk = transform_users(users_uk, 'UK',
                               column_mapping=uk_config['column_mapping'],
                               education_mapping=uk_config['education_mapping'],
                               currency='GBP')
    logins_uk = load_login_data('data/UK-User-LoginTS.csv', 'Europe/London')
    validate_user_visits(users_uk, logins_uk)

    users_fr = load_user_data('data/FR User Data.csv')
    users_fr = transform_users(users_fr, 'FR',
                               column_mapping=fr_config['column_mapping'],
                               gender_mapping=fr_config['gender_mapping'],
                               education_mapping=fr_config['education_mapping'],
                               payment_period=12,
                               currency='EUR',
                               int_dial_code='+33')
    logins_fr = load_login_data('data/FR-User-LoginTS.csv', 'Europe/Paris')
    validate_user_visits(users_fr, logins_fr)

    users_usa = load_user_data('data/USA User Data.csv')
    users_usa = transform_users(users_usa, 'USA',
                                column_mapping=usa_config['column_mapping'],
                                gender_mapping=usa_config['gender_mapping'],
                                education_mapping=usa_config['education_mapping'],
                                currency='USD',
                                int_dial_code='+1')
    logins_usa = load_login_data('data/USA-User-LoginTS.csv', 'US/Eastern')
    validate_user_visits(users_usa, logins_usa)

    users_sc = load_user_data('data/SC User Data.csv')
    users_sc = transform_users(users_sc, 'SC',
                               column_mapping=sc_config['column_mapping'],
                               gender_mapping=sc_config['gender_mapping'],
                               education_mapping=sc_config['education_mapping'],
                               currency='GBP')
    logins_sc = load_login_data('data/SC-User-LoginTS.csv', 'Europe/London')
    validate_user_visits(users_sc, logins_sc)

    subprocess.run("sqlite3 customers.db < sql/create_database.sql", shell=True, check=True)
    conn = sqlite3.connect("customers.db")

    for df in [users_uk, users_fr, users_usa, users_sc]:
        update_users_table(df, conn)

    for df in [logins_uk, logins_fr, logins_usa, logins_sc]:
        update_login_table(df, conn)

    conn.close()

if __name__ == "__main__":
    main()