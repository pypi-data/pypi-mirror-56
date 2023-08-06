import unittest
import logging
from qbz95.ml2.utils import *



# logger.setLevel(level=logging.DEBUG)


class TestPandasHelper(unittest.TestCase):
    def test_read_mysql(self):
        sql_message = """select customer_id, session_id, create_time as session_time, dest_type, msg_summary as message from customer_service_prod.up_messages 
        order by customer_id, session_id, create_time limit 20;
        """
        conn = MySqlHelper.get_connection()
        df_message = PandasHelper.read_sql(sql_message, conn, data_set_name='message')
        conn.close()
        # logging.info(len(df_message))

    def test_read_redshift(self):
        sql_message = """select session_id, create_time as session_time, dest_type, msg_summary as message from customer_service_prod.messages_history 
        order by session_id, create_time limit 20;
        """
        conn = RedshiftHelper.get_connection(user='tpch', password='Zeus000!', port=15439)
        df_message = PandasHelper.read_sql(sql_message, conn, data_set_name='message')
        conn.close()
        logging.info(len(df_message))
