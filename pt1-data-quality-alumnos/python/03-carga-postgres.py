import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('../data-sets/datos-examen-limpio-python-script.csv')

course_list = pd.unique(df[['favorite_course_1', 'favorite_course_2', 
                                 'favorite_course_3']].values.ravel())
course_list = [course for course in course_list if pd.notna(course) and course != '']
course_list.sort()
course = pd.DataFrame(course_list, columns=['course_name'])
course.rename(columns={'course_name': 'name'}, inplace=True)
course.index += 1
course['id'] = course.index

state_list = pd.unique(pd.concat([df['state'], df['current_state']]).dropna())
state_list = [state for state in state_list if pd.notna(state) and state != '']
state_list.sort()
state = pd.DataFrame(state_list, columns=['state_name'])
state.rename(columns={'state_name': 'name'}, inplace=True)
state.index += 1
state['id'] = state.index

district_list = pd.unique(df['current_district'].dropna())
district_list = [district for district in district_list if pd.notna(district) and district != '']
district_list.sort()
district = pd.DataFrame(district_list, columns=['district_name'])
district = pd.merge(district, df[['current_district', 'current_state']].drop_duplicates(),
                    left_on='district_name', right_on='current_district', how='left')
district = pd.merge(district, state[['id', 'name']], left_on='current_state', right_on='name',
                    how='left')
district.drop(columns=['current_district', 'current_state', 'name'], inplace=True)
district.rename(columns={'district_name': 'name', 'id': 'state_id'}, inplace=True)
district.index += 1
district['id'] = district.index

student = df[['name', 'age', 'grade_average', 'date_of_birth', 'is_working', 
               'workplace', 'semester', 'favorite_artist', 'number_of_residents',
               'state', 'current_district']].copy()
student.rename(columns={'state': 'birth_state'}, inplace=True)
student = pd.merge(student, state[['id', 'name']], left_on='birth_state', right_on='name',
                how='left', suffixes=('', '_birth_state'))
student.drop(columns=['birth_state', 'name_birth_state'], inplace=True)
student.rename(columns={'id': 'birth_state_id'}, inplace=True)

student = pd.merge(student, district[['id', 'name']], left_on='current_district', right_on='name',
                how='left', suffixes=('', '_district'))
student.drop(columns=['current_district', 'name_district'], inplace=True)
student.rename(columns={'id': 'current_district_id'}, inplace=True)
student.index += 1
student['id'] = student.index

answer = df[['name', 'engineering_definition', 'data_definition']]
answer = pd.merge(answer, student[['id', 'name']], on='name', how='inner')
answer.drop(columns=['name'], inplace=True)
answer = answer.rename(columns={'id': 'student_id'})

student_hobbies = df[['name', 'hobby_1', 'hobby_2', 'hobby_3']]
student_hobbies = pd.merge(student_hobbies, student[['id', 'name']], on='name', how='inner')
student_hobbies.drop(columns=['name'], inplace=True)
student_hobbies = student_hobbies.rename(columns={'id': 'student_id'})

student_favorite_courses = df[['name', 'favorite_course_1', 'favorite_course_2', 'favorite_course_3']]
student_favorite_courses = pd.merge(student_favorite_courses, student[['id', 'name']], on='name', how='inner')
student_favorite_courses = student_favorite_courses.rename(columns={'id': 'student_id'})
student_favorite_courses.drop(columns=['name'], inplace=True)
student_favorite_courses = pd.merge(student_favorite_courses, course[['id', 'name']], left_on='favorite_course_1',
                                    right_on='name', how='inner')
student_favorite_courses = student_favorite_courses.rename(columns={'id': 'favorite_course_1_id'})
student_favorite_courses.drop(columns=['favorite_course_1', 'name'], inplace=True)
student_favorite_courses = pd.merge(student_favorite_courses, course[['id', 'name']], left_on='favorite_course_2',
                                    right_on='name', how='inner')
student_favorite_courses = student_favorite_courses.rename(columns={'id': 'favorite_course_2_id'})
student_favorite_courses.drop(columns=['favorite_course_2', 'name'], inplace=True)
student_favorite_courses = pd.merge(student_favorite_courses, course[['id', 'name']], left_on='favorite_course_3',
                                    right_on='name', how='inner')
student_favorite_courses = student_favorite_courses.rename(columns={'id': 'favorite_course_3_id'})
student_favorite_courses.drop(columns=['favorite_course_3', 'name'], inplace=True)

engine = create_engine('postgresql://postgres:usuario@localhost:5432/data_quality')

course.to_sql(
    'course',
    engine,
    if_exists='append',
    index=False
)
state.to_sql(
    'state',
    engine,
    if_exists='append',
    index=False
)
district.to_sql(
    'district',
    engine,
    if_exists='append',
    index=False
)
student.to_sql(
    'student',
    engine,
    if_exists='append',
    index=False
)
answer.to_sql(
    'answer',
    engine,
    if_exists='append',
    index=False
)
student_hobbies.to_sql(
    'student_hobbies',
    engine,
    if_exists='append',
    index=False
)
student_favorite_courses.to_sql(
    'student_favorite_courses',
    engine,
    if_exists='append',
    index=False
)