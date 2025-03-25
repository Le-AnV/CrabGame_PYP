import psycopg2
import pandas as pd
import configparser

# doc du lieu tu config file
config = configparser.ConfigParser()
config.read("Game\\config.ini")

dbname = config["database"]["dbName"]
hostname = config["database"]["hostName"]
password = config["database"]["password"]
username = config["database"]["userName"]
port = config.getint("database", "port")


def connect_db():
    conn = psycopg2.connect(
        database=dbname,
        user=username,
        host=hostname,
        password=password,
        port=port,
    )
    return conn


# luu du lieu diem nguoi choi ve db
def save_score(name, score):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO top_member(member_name,score) VALUES (%s, %s)", (name, score)
    )
    conn.commit()
    conn.close()


def get_high_scores():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM top_member ORDER BY score DESC LIMIT 5")
    scores = cur.fetchall()
    conn.close()
    return pd.DataFrame(scores, columns=["STT", "Name", "Score"])


# print(get_high_scores())
