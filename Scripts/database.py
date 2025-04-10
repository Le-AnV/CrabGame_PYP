import psycopg2
import pandas as pd
import configparser


# doc du lieu tu config file
config = configparser.ConfigParser()
config.read("config\settings.ini")

dbname = config["database"]["dbName"]
hostname = config["database"]["hostName"]
password = config["database"]["password"]
username = config["database"]["userName"]
port = config.getint("database", "port")


def connect_db():
    try:
        conn = psycopg2.connect(
            database=dbname,
            user=username,
            host=hostname,
            password=password,
            port=port,
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None


# Lưu điểm của người chơi vào db
def save_score(name, score):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO top_member(member_name,score) VALUES (%s, %s)",
                (name, score),
            )
            conn.commit()
        except psycopg2.Error as e:
            print(f"Error saving score: {e}")
        finally:
            conn.close()


def get_high_scores():
    # Lấy dữ liệu người chơi top 5 có điểm cao nhất
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT member_name, score FROM top_member ORDER BY score DESC LIMIT 5"
            )
            scores = cur.fetchall()
            return pd.DataFrame(scores, columns=["Name", "Score"])
        except psycopg2.Error as e:
            print(f"Error fetching high scores: {e}")
            return pd.DataFrame(columns=["Name", "Score"])
        finally:
            conn.close()
    return pd.DataFrame(columns=["Name", "Score"])
