import mysql.connector


# mycursor.execute("""CREATE TABLE gwy_wj (seq_id int, pub_url VARCHAR(255), index_id VARCHAR(255),
#                             gov_theme VARCHAR(255), pub_dept VARCHAR(255), orig_date VARCHAR(255),
#                             doc_title VARCHAR(255), pub_id VARCHAR(255), pub_date  VARCHAR(255),
#                             gov_theme_key_word  VARCHAR(255), doc_content LONGBLOB ,
#                             doc_attr_outerHTML LONGBLOB , doc_content_outerHTML LONGBLOB )""")

def save_policy(policy_dict):
    con = mysql.connector.connect(host='localhost',
                                  port=3306,
                                  database='gov_policy',
                                  user='你的用户名',
                                  password='你设置的密码',
                                  connect_timeout=20)

    my_cursor = con.cursor()
    placeholders = ', '.join(['%s'] * len(policy_dict))
    columns = ', '.join(policy_dict.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ('gwy_wj', columns, placeholders)
    my_cursor.execute(sql, list(policy_dict.values()))

    con.commit()
    my_cursor.close()
