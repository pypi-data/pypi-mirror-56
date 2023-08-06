import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, Text, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError


class SetupDb:
    def __init__(self, db_name,  db_username, db_password, db_hostname, logger):
        table_name = 'ips'
        self.logger = logger
        self.Base = declarative_base()

        self.logger.entry('debug', 'Connecting to database...')
        self.engine = create_engine(f'mysql+mysqldb://{db_username}:{db_password}@{db_hostname}:3306')

        try:
            self.engine.execute(f'DROP DATABASE {db_name}')
            self.logger.entry('debug', f'Dropped old database: {db_name}')

        # silently pass error when DB does not exist
        except OperationalError:
            pass

        self.engine.execute(f'CREATE DATABASE {db_name}')
        self.logger.entry('debug', f'Created database: {db_name}')
        self.engine.execute(f'USE {db_name}')

        self.table = self._initiate_table(table_name)
        self.Base.metadata.create_all(self.engine)
        self.logger.entry('debug', f'Created "{table_name}" table in "{db_name}" database')

    def _initiate_table(self, table_name):
        class Data(self.Base):
            __tablename__ = table_name
            id = Column(Integer, primary_key=True)
            computer_id = Column(Integer)
            hostname = Column(Text)
            display_name = Column(Text)
            host_description = Column(Text)
            platform = Column(Text)
            last_ip_used = Column(Text)
            agent_version = Column(Text)
            policy_id = Column(Integer)
            last_agent_comms = Column(Text)
            ips_agent_state = Column(Text)
            ips_status = Column(Text)
            applied_ips_rules = Column(Integer)
            rule_name = Column(Text)
            rule_id = Column(Integer)
            rule_description = Column(Text)
            app_category = Column(Text)
            app_description = Column(Text)
            app_ports = Column(Text)
            total_ports = Column(Integer)
            direction = Column(Text)
            protocol = Column(Text)
            cves = Column(Text)
            total_cves = Column(Integer)
            cvss_score = Column(Float)
            severity = Column(Text)
            rule_type = Column(Text)

            if os.environ.get('DS_APP_NAMES'):
                app_name = Column(Text)

        return Data

    def get_table(self):
        return self.table

    def get_session(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        return session