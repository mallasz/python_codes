import sys
sys.path += ['../test_config', '../pages', '../test_utils']
from fixtures import *
import util


def test_tc9(driver, login_page, start_page, list_all_students_page, new_student_page, db):
    """
    TC9 test case
    new students' registration from a CSV file
    parameters are fixtures
    """
    # file name of the CSV to upload
    file_name = "personaldata.csv"
    # reset the database to the default state to make sure the new students are not in the database
    db.reset_database()
    # count the students in the original database
    number_of_students_before = db.get_data('SELECT count(*) FROM student')[0][0]
    # load login page
    login_page.go_there()
    # log in as admin
    login_page.login('admin')
    # go to students' page
    start_page.go_to_students()
    # go to new student registration
    list_all_students_page.go_to_new_student()
    # register a lot of new students from a CSV file, store their number
    number_of_new_students = new_student_page.create_students_from_csv(file_name)
    # reconnect to the database, because transactions might hide new students
    db.reconnect()
    # load csv data
    new_student_data = util.get_csv_data(file_name)
    # create a query to get students data from the database in the same format they were in the CSV file
    get_statement = '''
    SELECT t.familyName, t.givenName, t.sex, t.motherMaidenName, t.dateOfBirth, t.birthplaceTown, 
    t.nationality, t.appliedTo, t.programName, t.academicYear FROM
    (SELECT s.familyName, s.givenName, s.sex, s.motherMaidenName, s.dateOfBirth, s.birthplaceTown, 
    c.nationality, sc2.programName AS appliedTo, sc.programName, a.academicYear, s.id AS id
    FROM student s
    INNER JOIN country c on c.id = s.nationality_id
    INNER JOIN application a on a.id = s.application_id
    INNER JOIN school sc on sc.id = s.mainProgramToEnter_id
    INNER JOIN school sc2 on sc2.id = a.appliedToProgram_id
    order by s.id DESC limit %s) t
    ORDER BY t.id
    '''
    # do the query
    new_student_db = db.get_data(get_statement, (len(new_student_data),))

    # compare the result with the original CSV as a reference
    for uploaded_student, db_student in zip(new_student_data, new_student_db):
        # in the CSV Male is Male, Female is Female, in the DB Male is M, Female is F
        uploaded_student['Sex'] = uploaded_student['Sex'][0]
        # compare data from the database with the CSV
        for index, value in enumerate(uploaded_student.values()):
            # DB returns the proper types (e.g. datetime objects), CSV has only strings, so convert for comparison
            assert str(db_student[index]) == value

    # number of students must match in the DB
    number_of_students_after = db.get_data('SELECT count(*) FROM student')[0][0]
    assert number_of_students_before + number_of_new_students == number_of_students_after

    # collect all student data from the web page
    start_page.go_to_students()
    all_students = list_all_students_page.page_through_table()

    # construct a dict for faster and easier lookup
    all_students_as_dict = {d['NAME']: (d['DATE OF BIRTH'], d['NATIONALITY']) for d in all_students}

    for uploaded_student in new_student_data:
        # convert student name into the format on the website (family_name, given_name)
        name = f"{uploaded_student['Family name']}, {uploaded_student['Given name']}"
        # name should be in the dictionary
        assert name in all_students_as_dict
        # compare other student data (date_of_birth, nationality)
        date_of_birth, nationality = all_students_as_dict[name]
        assert date_of_birth == uploaded_student['Date of birth']
        assert nationality == uploaded_student['Nationality']

    # log out and check for success
    start_page.log_out()
    assert login_page.is_loaded_exactly()
