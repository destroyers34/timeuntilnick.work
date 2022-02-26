import tweepy
import mysql.connector
import sshtunnel
import os


#ENV VARIABLES
DEBUG = bool(int(os.environ['DEBUG']))
TWITTER_API_BEARER = os.environ['TWITTER_API_BEARER']
SSH_HOST = os.environ['SSH_HOST']
SSH_PORT = int(os.environ['SSH_PORT'])
SSH_USER = os.environ['SSH_USER']
SSH_PASSWORD = os.environ['SSH_PASSWORD']
REMOTE_BIND_ADDRESS = os.environ['REMOTE_BIND_ADDRESS']
REMOTE_BIND_PORT = int(os.environ['REMOTE_BIND_PORT'])
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_PORT = int(os.environ['DB_PORT'])
DB_NAME = os.environ['DB_NAME']


def check_tweet():
    client = tweepy.Client(TWITTER_API_BEARER)
    if not DEBUG:
        print("PROD : " + str(DEBUG))
        conn = mysql.connector.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host='localhost',
            port=3306,
            database=DB_NAME,
        )
        conn.autocommit = True
        mycursor = conn.cursor()
        query = "SELECT config_value FROM config WHERE config_name='last_tweet'"
        mycursor.execute(query)

        last_tweet = mycursor.fetchone()
        print(last_tweet)

        # Search Recent Tweets
        # This endpoint/method returns Tweets from the last seven days
        response = client.search_recent_tweets("planethoster", max_results=100, since_id=last_tweet,
                                               tweet_fields=["created_at"])
        # The method returns a Response object, a named tuple with data, includes,
        # errors, and meta fields
        print(response.meta)
        if response.meta["result_count"] > 0:
            q_update_last_tweet = "UPDATE config SET config_value=%s WHERE config_name='last_tweet'"
            mycursor.execute(q_update_last_tweet, (response.meta["newest_id"],))

            # In this case, the data field of the Response returned is a list of Tweet
            # objects
            tweets = response.data
            # Each Tweet object has default id and text fields
            for tweet in tweets:
                # print("-------------------------------------")
                # print(tweet.created_at)
                # print(tweet.text)
                # print("-------------------------------------\n")
                q_save_tweet = "INSERT INTO `tweets`(`date`, `tweet_id`) VALUES (%s,%s);"
                # print(q_save_tweet, ((tweet.created_at).strftime('%Y-%m-%d %H:%M:%S'),tweet.id,))
                mycursor.execute(q_save_tweet, (tweet.created_at, tweet.id,))
        mycursor.close()

    else:
        print("DEBUG : " + str(DEBUG))
        # establishing the connection
        with sshtunnel.SSHTunnelForwarder(
                (SSH_HOST, SSH_PORT),
                ssh_username=SSH_USER,
                ssh_password=SSH_PASSWORD,
                remote_bind_address=(REMOTE_BIND_ADDRESS, REMOTE_BIND_PORT)
        ) as tunnel:
            conn = mysql.connector.connect(
                user=DB_USER,
                password=DB_PASSWORD,
                host='localhost',
                port=tunnel.local_bind_port,
                database=DB_NAME,
            )
            conn.autocommit = True
            mycursor = conn.cursor()
            query = "SELECT config_value FROM config WHERE config_name='last_tweet'"
            mycursor.execute(query)

            last_tweet = mycursor.fetchone()
            print(last_tweet)

            # Search Recent Tweets
            # This endpoint/method returns Tweets from the last seven days
            response = client.search_recent_tweets("planethoster", max_results=100, since_id=last_tweet,
                                                   tweet_fields=["created_at"])
            # The method returns a Response object, a named tuple with data, includes,
            # errors, and meta fields
            print(response.meta)
            if response.meta["result_count"] > 0:
                q_update_last_tweet = "UPDATE config SET config_value=%s WHERE config_name='last_tweet'"
                mycursor.execute(q_update_last_tweet, (response.meta["newest_id"],))

                # In this case, the data field of the Response returned is a list of Tweet
                # objects
                tweets = response.data
                # Each Tweet object has default id and text fields
                for tweet in tweets:
                    # print("-------------------------------------")
                    # print(tweet.created_at)
                    # print(tweet.text)
                    # print("-------------------------------------\n")
                    q_save_tweet = "INSERT INTO `tweets`(`date`, `tweet_id`) VALUES (%s,%s);"
                    # print(q_save_tweet, ((tweet.created_at).strftime('%Y-%m-%d %H:%M:%S'),tweet.id,))
                    mycursor.execute(q_save_tweet, (tweet.created_at, tweet.id,))
            mycursor.close()


if __name__=="__main__":
    check_tweet()