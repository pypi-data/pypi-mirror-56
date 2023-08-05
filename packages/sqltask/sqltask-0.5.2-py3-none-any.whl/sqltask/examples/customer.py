from datetime import date, datetime
import os

from sqlalchemy.schema import Column
from sqlalchemy.types import Date, DateTime, Float, String
from sqltask import SqlTask, Source, Priority, Category
from sqltask.classes.exceptions import TooFewRowsException


class CustomerTask(SqlTask):
    def __init__(self, report_date: date):
        super().__init__(report_date=report_date)
        source_url = os.getenv("SQLTASK_SOURCE", "sqlite:///source.db")
        target_url = os.getenv("SQLTASK_SOURCE", "sqlite:///target.db")
        source_engine = self.add_engine("source", source_url)
        target_engine = self.add_engine("target", target_url)

        columns = [
            Column("report_date", String, comment="Built-in row id", primary_key=True),
            Column("etl_timestamp", DateTime, comment="Timestamp when row was created", nullable=False),
            Column("customer_id", String, comment="Unique customer identifier", primary_key=True),
            Column("birthdate", Date, comment="Birthdate of customer if defined and in the past"),
            Column("age", Float, comment="Age of customer in years if birthdate defined"),
            Column("sector_code", String, comment="Sector code of customer"),
        ]
        table = self.add_table("customer",
                               engine_context=target_engine,
                               columns=columns,
                               timestamp_column_name="etl_timestamp",
                               batch_params={"report_date": report_date}
                               )

        self.add_source_query("main", """
            SELECT id,
                   birthday,
                   1 as num
            FROM (SELECT DATE('2019-06-30') AS report_date, '1234567' AS id, '1980-01-01' AS birthday UNION ALL 
                  SELECT DATE('2019-06-30') AS report_date, '2345678' AS id, '2080-01-01' AS birthday UNION ALL 
                  SELECT DATE('2019-06-30') AS report_date, '2245678' AS id, '1980-13-01' AS birthday UNION ALL 
                  SELECT DATE('2019-06-30') AS report_date, '3456789' AS id, NULL AS birthday)
            WHERE report_date = :report_date
            """, {"report_date": report_date}, source_engine)

        self.add_lookup_query("sector_code", """
            SELECT customer_id,
                   sector_code
            FROM (SELECT DATE('2019-06-30') AS execution_date, '1234567' AS customer_id, '111211' AS sector_code UNION ALL 
                  SELECT DATE('2019-06-30') AS execution_date, '2345678' AS customer_id, '143' AS sector_code UNION ALL 
                  SELECT DATE('2019-06-30') AS execution_date, '2345678' AS customer_id, '143' AS sector_code UNION ALL 
                  SELECT DATE('2019-06-30') AS execution_date, '3456789' AS customer_id, NULL AS sector_code 
            )
            WHERE execution_date = :report_date
            """, {"report_date": report_date}, table, source_engine)

    def transform(self) -> None:
        report_date = self.batch_params['report_date']
        for in_row in self.get_source_rows("main"):
            row = self.get_new_row("customer")

            # report_date
            row["report_date"] = report_date

            # customer_id
            customer_id = in_row['id']
            row['customer_id'] = customer_id

            # birthdate
            birthday = in_row['birthday']
            age = None
            try:
                birthdate = datetime.strptime(birthday, "%Y-%m-%d").date() if birthday else None
                age = None
                if birthdate is None:
                    self.log_dq(source=Source.SOURCE,
                                priority=Priority.HIGH,
                                dq_type=Category.MISSING,
                                column_name="birthdate",
                                output_row=row)
                elif birthdate > report_date:
                    self.log_dq(source=Source.SOURCE,
                                priority=Priority.HIGH,
                                dq_type=Category.INCORRECT,
                                column_name="birthdate",
                                output_row=row)
                    birthdate = None
                else:
                    age = (report_date - birthdate).days / 365.25
            except ValueError:
                # parse error
                self.log_dq(source=Source.SOURCE,
                            priority=Priority.HIGH,
                            dq_type=Category.INCORRECT,
                            column_name="birthdate",
                            output_row=row)
                birthdate = None
            row["birthdate"] = birthdate

            # age
            if age is None:
                self.log_dq(source=Source.TRANSFORM,
                            priority=Priority.MEDIUM,
                            dq_type=Category.MISSING,
                            column_name="age",
                            output_row=row)
            row["age"] = age

            # sector_code
            sector_code = self.get_lookup_source("sector_code").get(customer_id)
            if sector_code is None:
                self.log_dq(source=Source.SOURCE,
                            priority=Priority.MEDIUM,
                            dq_type=Category.MISSING,
                            column_name="sector_code",
                            output_row=row)
            row["sector_code"] = sector_code

            self.add_row(row)

        for i in range(0):
            row = self.get_new_row("customer")
            row["customer_id"] = 'abcd'
            row["birthdate"] = None
            row["age"] = None
            row["sector_code"] = None
            self.add_row(row)

    def validate(self):
        if len(self._output_rows['customer']) < 2:
            raise TooFewRowsException("Less than 2 rows")


if __name__ == "__main__":
    task = CustomerTask(report_date=date(2019, 6, 30))
    task.execute()
