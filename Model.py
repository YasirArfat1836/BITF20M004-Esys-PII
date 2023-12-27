import pymysql
from flask import request, jsonify


class Model:


    def view_student(self, s_id, mydb=None):
        try:
            if mydb is None or not mydb.open:
                print("Invalid or closed database connection.")
                return None

            with mydb.cursor() as mydbCursor:
                sql = "SELECT * FROM student_interests WHERE id=%s"
                args = (s_id,)
                mydbCursor.execute(sql, args)
                rows = mydbCursor.fetchall()
                if rows:
                    return rows
        except Exception as e:
            print(f"Error: {str(e)}")

    def delete_student(self, s_id, mydb=None):
        try:
            if mydb is None or not mydb.open:
                print("Invalid or closed database connection.")
                return False

            with mydb.cursor() as mydbCursor:
                sql = "DELETE FROM student_interests WHERE id=%s"
                args = (s_id,)
                mydbCursor.execute(sql, args)
                mydb.commit()
                if mydbCursor.rowcount > 0:
                    return True
                else:
                    return False
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

    def AlreadyGivenInterests(self, mydb=None):
        interests = []

        try:
            if mydb is None or not mydb.open:
                print("Invalid or closed database connection.")
                return interests

            with mydb.cursor() as mydbCursor:
                sql = "SELECT distinct interest FROM student_interests"
                mydbCursor.execute(sql)
                rows = mydbCursor.fetchall()

                if rows:
                    interests = [row[0] for row in rows]

        except Exception as e:
            print(f"Error: {str(e)}")

        return interests

    def AddStudents(self, student, mydb=None):
        inserted = False
        try:
            with mydb.cursor() as mydbCursor:
                sql = "INSERT INTO student_interests (full_name, roll_number, email_address, gender, date_of_birth, city, interest, department, degree_title, subject, start_date, end_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                args = (
                    student.full_name,
                    student.roll_number,
                    student.email_address,
                    student.gender,
                    student.date_of_birth,
                    student.city,
                    student.interest,
                    student.department,
                    student.degree_title,
                    student.subject,
                    student.start_date,
                    student.end_date
                )

                mydbCursor.execute(sql, args)
                mydb.commit()
                inserted = True
        except Exception as e:
            print(str(e))

        return inserted

    def edit_student(self, student_id, updated_student, mydb=None):
        updated = False
        try:
            with mydb.cursor() as mydbCursor:
                sql = "UPDATE student_interests SET full_name=%s, roll_number=%s, email_address=%s, gender=%s, date_of_birth=%s, city=%s, interest=%s, department=%s, degree_title=%s, subject=%s, start_date=%s, end_date=%s WHERE id=%s"
                args = (
                    updated_student.full_name,
                    updated_student.roll_number,
                    updated_student.email_address,
                    updated_student.gender,
                    updated_student.date_of_birth,
                    updated_student.city,
                    updated_student.interest,
                    updated_student.department,
                    updated_student.degree_title,
                    updated_student.subject,
                    updated_student.start_date,
                    updated_student.end_date,
                    student_id
                )

                mydbCursor.execute(sql, args)
                mydb.commit()
                updated = True
        except Exception as e:
            print(str(e))

        return updated


    def get_provincial_distribution(self, mydb):
        try:
            with mydb.cursor() as mydbCursor:
                sql = """
                    SELECT city, COUNT(*) as count
                    FROM student_interests
                    GROUP BY city
                """
                mydbCursor.execute(sql)
                rows = mydbCursor.fetchall()
                provincial_distribution = [{"city": row[0], "count": row[1]} for row in rows]
                return provincial_distribution
        except Exception as e:
            print(str(e))


    def get_daily_submission_counts(self, mydb=None):
        try:
            with mydb.cursor() as mydbCursor:
                sql = """
                    SELECT DATE(start_date) as creation_date, COUNT(*) as count
                    FROM student_interests
                    WHERE start_date >= CURDATE() - INTERVAL 30 DAY
                    GROUP BY DATE(start_date)
                    ORDER BY DATE(start_date)
                """
                mydbCursor.execute(sql)
                rows = mydbCursor.fetchall()
                submission_data = [{"date": row[0].strftime('%Y-%m-%d'), "count": row[1]} for row in rows]
                return submission_data
        except Exception as e:
            print(str(e))

    def get_age_distribution(self, mydb=None):
        try:
            with mydb.cursor() as mydbCursor:
                sql = """
                    SELECT FLOOR(DATEDIFF(CURDATE(), date_of_birth) / 365) as age, COUNT(*) as count
                    FROM student_interests
                    GROUP BY age
                """
                mydbCursor.execute(sql)
                rows = mydbCursor.fetchall()
                age_distribution_data = [{"age": row[0], "count": row[1]} for row in rows]
                return age_distribution_data
        except Exception as e:
            print(f"Error in get_age_distribution: {str(e)}")


    def get_department_distribution(self, mydb):
        try:
            with mydb.cursor() as mydbCursor:
                sql = """
                    SELECT department, COUNT(*) as count
                    FROM student_interests
                    GROUP BY department
                """
                mydbCursor.execute(sql)
                rows = mydbCursor.fetchall()
                department_distribution_data = [{"department": row[0], "count": row[1]} for row in rows]
                return department_distribution_data
        except Exception as e:
            print(str(e))

    def get_gender_distribution(self, mydb):
        try:
            with mydb.cursor() as mydbCursor:
                sql = """
                    SELECT gender, COUNT(*) as count
                    FROM student_interests
                    GROUP BY gender
                """
                mydbCursor.execute(sql)
                rows = mydbCursor.fetchall()
                gender_distribution_data = [{"gender": row[0], "count": row[1]} for row in rows]
                return gender_distribution_data
        except Exception as e:
            print(str(e))

    def get_degree_distribution(self, mydb):
        try:
            with mydb.cursor() as mydbCursor:
                sql = """
                    SELECT degree_title, COUNT(*) as count
                    FROM student_interests
                    GROUP BY degree_title
                """
                mydbCursor.execute(sql)
                rows = mydbCursor.fetchall()
                degree_distribution_data = [{"degree_title": row[0], "count": row[1]} for row in rows]
                return degree_distribution_data
        except Exception as e:
            print(str(e))






    def interest_count(self, mydb=None):
        try:
            with mydb.cursor() as mydbCursor:
                sql = "SELECT DISTINCT COUNT(interest) FROM student_interests "
                mydbCursor.execute(sql)
                rows = mydbCursor.fetchall()
                if rows:
                    return rows[0]
        except Exception as e:
            print(str(e))


    def get_last_30_days_activity(self, mydb):
        try:
            with mydb.cursor() as mydbCursor:
                sql = """
                    SELECT DATE(start_date) as activity_date, COUNT(*) as count
                    FROM student_interests
                    WHERE start_date >= CURDATE() - INTERVAL 30 DAY
                    GROUP BY DATE(start_date)
                    ORDER BY DATE(start_date)
                """
                mydbCursor.execute(sql)
                rows = mydbCursor.fetchall()
                activity_data = [{"date": row[0].strftime('%Y-%m-%d'), "count": row[1]} for row in rows]
                return activity_data
        except Exception as e:
            print(str(e))

    def get_last_24_hours_activity(self, mydb):
        try:
            with mydb.cursor() as mydbCursor:
                sql = """
                    SELECT DATE_FORMAT(start_date, '%Y-%m-%d %H:%i:%s') as activity_time, COUNT(*) as count
                    FROM student_interests
                    WHERE start_date >= NOW() - INTERVAL 24 HOUR
                    GROUP BY activity_time
                    ORDER BY activity_time
                """
                mydbCursor.execute(sql)
                rows = mydbCursor.fetchall()
                activity_data = [{"time": row[0], "count": row[1]} for row in rows]
                return activity_data
        except Exception as e:
            print(str(e))
    def get_student_status(self, mydb):
        try:
            with mydb.cursor() as mydbCursor:
                sql = """
                    SELECT
                        COUNT(CASE WHEN end_date IS NULL THEN 1 END) as currently_studying,
                        COUNT(CASE WHEN start_date >= CURDATE() - INTERVAL 30 DAY THEN 1 END) as recently_enrolled,
                        COUNT(CASE WHEN end_date >= CURDATE() AND end_date IS NOT NULL THEN 1 END) as about_to_graduate,
                        COUNT(CASE WHEN end_date < CURDATE() AND end_date IS NOT NULL THEN 1 END) as graduated
                    FROM student_interests
                """
                mydbCursor.execute(sql)
                rows = mydbCursor.fetchone()
                status_data = {
                    'currently_studying': rows[0],
                    'recently_enrolled': rows[1],
                    'about_to_graduate': rows[2],
                    'graduated': rows[3]
                }
                print(status_data)
                return jsonify(status_data)

        except Exception as e:
            print(str(e))

    def top_5(self, mydb=None):
        try:
            with mydb.cursor() as mydbCursor:
                sql = "SELECT interest FROM student_interests ORDER BY interest ASC LIMIT 5"
                mydbCursor.execute(sql)
                rows = mydbCursor.fetchall()
                if rows:
                    return rows
        except Exception as e:
            print(str(e))

    def bottom_5(self, mydb=None):
        try:
            with mydb.cursor() as mydbCursor:
                sql = "SELECT interest FROM student_interests ORDER BY interest DESC LIMIT 5"
                mydbCursor.execute(sql)
                rows = mydbCursor.fetchall()
                if rows:
                    return rows
        except Exception as e:
            print(str(e))

    def AllStudents(self, mydb=None):
        try:
            with mydb.cursor() as mydbCursor:
                sql = "SELECT * FROM student_interests "
                mydbCursor.execute(sql)
                rows = mydbCursor.fetchall()
                if rows:
                    return rows
        except Exception as e:
            print(str(e))

    def get_activity_by_hour(self, mydb):
        try:
            mydbCursor = mydb.cursor()

            sql = """
                SELECT HOUR(timestamp) as activity_hour, COUNT(*) as count
                FROM user_activity_log
                WHERE timestamp >= CURDATE() - INTERVAL 30 DAY
                GROUP BY activity_hour
                ORDER BY count DESC
            """
            mydbCursor.execute(sql)

            rows = mydbCursor.fetchall()

            activity_data = [{"hour": row[0], "count": row[1]} for row in rows]
            return activity_data

        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor is not None:
                mydbCursor.close()

    def log_user_activity(self, user_id, activity_type, mydb):
        try:
            with mydb.cursor() as mydbCursor:
                sql = "INSERT INTO user_activity_log (user_id, activity_type, timestamp) VALUES (%s, %s, NOW())"
                args = (user_id, activity_type)
                mydbCursor.execute(sql, args)
                mydb.commit()
        except Exception as e:
            print(str(e))

