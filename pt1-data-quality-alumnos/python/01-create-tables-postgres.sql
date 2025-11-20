\set AUTOCOMMIT on
CREATE DATABASE data_quality WITH OWNER = admin ENCODING 'UTF8' TEMPLATE template1;

-- Cambiar automáticamente a la nueva base
\connect data_quality;

CREATE TABLE course
(
    id                      int     NOT NULL,
    name                    text    NOT NULL,
    CONSTRAINT course_pk PRIMARY KEY (id),
    CONSTRAINT course_name_uk UNIQUE (name)
);

CREATE TABLE state
(
    id                      int     NOT NULL,
    name                    text    NOT NULL,
    CONSTRAINT state_pk PRIMARY KEY (id),
    CONSTRAINT state_name_uk UNIQUE (name)
);

CREATE TABLE district
(
    id                      int     NOT NULL,
    name                    text    NOT NULL,
    state_id                int     NOT NULL,
    CONSTRAINT district_pk PRIMARY KEY (id),
    CONSTRAINT district_state_id_name_uk UNIQUE (state_id, name),
    CONSTRAINT district_state_id_fk FOREIGN KEY (state_id) REFERENCES state (id)
);

CREATE TABLE student
(
    id                      int     NOT NULL,
    name                    text    NOT NULL,
    age                     int     NOT NULL,
    grade_average           numeric NOT NULL,
    date_of_birth           date    NOT NULL,
    is_working              bool    NOT NULL,
    workplace               text    NULL,
    semester                int     NOT NULL,
    favorite_artist         text    NOT NULL,
    number_of_residents     int     NOT NULL,
    birth_state_id          int     NOT NULL,
    current_district_id     int     NOT NULL,
    CONSTRAINT student_pk PRIMARY KEY (id),
    CONSTRAINT student_age_check CHECK (age >= 17 AND age <= 99),
    CONSTRAINT student_grade_average_check CHECK (grade_average >= 5.0 AND grade_average <= 10.0),
    CONSTRAINT student_semester_check CHECK (semester >= 1),
    CONSTRAINT student_number_of_residents_check CHECK (number_of_residents >= 1),
    CONSTRAINT student_birth_state_id_fk FOREIGN KEY (birth_state_id) REFERENCES state (id),
    CONSTRAINT student_current_district_id_fk FOREIGN KEY (current_district_id) REFERENCES district (id)
);

CREATE TABLE answer
(
    student_id              int     NOT NULL,
    engineering_definition  text    NOT NULL,
    data_definition         text    NOT NULL,
    CONSTRAINT answer_pk PRIMARY KEY (student_id),
    CONSTRAINT answer_student_id_fk FOREIGN KEY (student_id) REFERENCES student (id)
);

CREATE TABLE student_hobbies
(
    student_id              int     NOT NULL,
    hobby_1                 text    NOT NULL,
    hobby_2                 text    NOT NULL,
    hobby_3                 text    NOT NULL,
    CONSTRAINT student_hobbies_pk PRIMARY KEY (student_id),
    CONSTRAINT student_hobbies_hobby_uk UNIQUE (hobby_1, hobby_2, hobby_3),
    CONSTRAINT student_hobbies_student_id_fk FOREIGN KEY (student_id) REFERENCES student (id)
);

CREATE TABLE student_favorite_courses
(
    student_id              int     NOT NULL,
    favorite_course_1_id             int     NULL,
    favorite_course_2_id             int     NULL,
    favorite_course_3_id             int     NULL,
    CONSTRAINT student_favorite_courses_pk PRIMARY KEY (student_id),
    CONSTRAINT student_favorite_courses_favorite_course_1_fk FOREIGN KEY (favorite_course_1_id) REFERENCES course (id),
    CONSTRAINT student_favorite_courses_favorite_course_2_fk FOREIGN KEY (favorite_course_2_id) REFERENCES course (id),
    CONSTRAINT student_favorite_courses_favorite_course_3_fk FOREIGN KEY (favorite_course_3_id) REFERENCES course (id),
    CONSTRAINT student_favorite_courses_favorite_course_uk UNIQUE (favorite_course_1_id, favorite_course_2_id, favorite_course_3_id),
    CONSTRAINT student_favorite_courses_student_id_fk FOREIGN KEY (student_id) REFERENCES student (id)
);