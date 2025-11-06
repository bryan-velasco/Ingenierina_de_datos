import pandas as pd
import numpy as np
import re

df = pd.read_csv('../data-sets/DatosExamen.csv')

df = df.rename(columns={'Nombre': 'name'})

df['Edad'] = df['Edad'].str.replace(r'\D', '', regex=True)
df['Edad'] = pd.to_numeric(df['Edad'])
df = df.rename(columns={'Edad': 'age'})

# Dictionary to normalize state names
state_mapping = {
    'CDMX': 'Ciudad de México',
    'D.F': 'Ciudad de México',
    'Ciudad de México': 'Ciudad de México',
    'Edo. Méx': 'Estado de México',
    'Estado de México': 'Estado de México',
    'Veracruz': 'Veracruz',
    'Oaxaca': 'Oaxaca',
    'Hidalgo': 'Hidalgo',
    # Add more mappings as needed
}

# Function to extract and normalize the state
def extract_and_normalize_state(location):
    if pd.isna(location):
        return np.nan
    location = location.replace('Nací en ', '').replace(', antes D.F', '').replace('México D.F -> ', '').replace(',Veracruz', ', Veracruz')
    parts = location.split(',')
    for part in parts:
        part = part.strip()
        for key, value in state_mapping.items():
            if key in part:
                return value
    return np.nan # Return NaN if no state is found

df['Lugar de Nacimiento'] = df['Lugar de Nacimiento'].apply(extract_and_normalize_state)
df = df.rename(columns={'Lugar de Nacimiento': 'state'})

df['Promedio'] = df['Promedio'].str.replace(',', '.')
df['Promedio'] = df['Promedio'].str.extract(r'(\d+\.?\d*)')
df['Promedio'] = pd.to_numeric(df['Promedio'])
df = df.rename(columns={'Promedio': 'grade_average'})

# Function to parse the specified date formats in Spanish
def parse_spanish_date_fixed(date_str):
    """Parse dates in formats such as: '11/10/2003', '06/nov/2022', '6/Diciembre/2002',
       '8 octubre 2002', '3 de mayo de 1999', etc."""
    if pd.isna(date_str) or str(date_str).strip() == "":
        return pd.NaT

    s = str(date_str).strip()
    # remove isolated 'de/del' for formats such as '3 de mayo de 1999'
    s = re.sub(r'\bde\b', ' ', s, flags=re.IGNORECASE)
    s = re.sub(r'\bdel\b', ' ', s, flags=re.IGNORECASE)
    s = re.sub(r'\s+', ' ', s).strip()

    # month map (esp → ing)
    month_map = {
        'enero': 'January', 'febrero': 'February', 'marzo': 'March', 'abril': 'April',
        'mayo': 'May', 'junio': 'June', 'julio': 'July', 'agosto': 'August',
        'septiembre': 'September', 'octubre': 'October', 'noviembre': 'November', 'diciembre': 'December',
        'ene': 'Jan', 'feb': 'Feb', 'mar': 'Mar', 'abr': 'Apr', 'may': 'May', 'jun': 'Jun',
        'jul': 'Jul', 'ago': 'Aug', 'sep': 'Sep', 'oct': 'Oct', 'nov': 'Nov', 'dic': 'Dec'
    }

    # replace month names/abbreviations (using \b and re.IGNORECASE)
    s_lower = s.lower()
    for es, en in month_map.items():
        s_lower = re.sub(r'\b' + re.escape(es) + r'\b', en, s_lower, flags=re.IGNORECASE)
    s_mapped = s_lower  # now with months in English when applying

    # formats to test (portable; not %#d)
    formats = [
        '%d/%m/%Y',
        '%d/%b/%Y',
        '%d/%B/%Y',
        '%d %B %Y',
        '%d %b %Y',
    ]

    for fmt in formats:
        try:
            parsed = pd.to_datetime(s_mapped, format=fmt)  # throws ValueError if it doesn't match
            # if we get here and parsed is not NaT, we return
            if not pd.isna(parsed):
                return parsed
        except (ValueError, TypeError):
            continue

    # fallback: let pandas attempt to parse freely (dayfirst=True typical in Spanish)
    return pd.to_datetime(s_mapped, dayfirst=True, errors='coerce')


df['Fecha de Nacimiento'] = df['Fecha de Nacimiento'].apply(parse_spanish_date_fixed)
df = df.rename(columns={'Fecha de Nacimiento': 'date_of_birth'})

# Reuse the state mapping dictionary and add more if needed
state_mapping = {
    'CDMX': 'Ciudad de México',
    'D.F': 'Ciudad de México',
    'Ciudad de México': 'Ciudad de México',
    'Edo. Méx': 'Estado de México',
    'Estado de México': 'Estado de México',
    'Veracruz': 'Veracruz',
    'Oaxaca': 'Oaxaca',
    'Hidalgo': 'Hidalgo',
    # Add more mappings as needed for other states
}

# Function to extract district and state based on refined requirements
def extract_district_and_state_refined(location):
    if pd.isna(location):
        return np.nan, np.nan

    # Clean the string and normalize Coyoacan
    location = location.replace('En ', '').replace(', vivo solo', '').replace('Coyoacan', 'Coyoacán').strip()

    district = np.nan
    state = np.nan

    # Specific handling for known district-state pairs without comma (e.g., "Tizayuca Hidalgo")
    known_pairs_without_comma = {
        'Tizayuca Hidalgo': ('Tizayuca', 'Hidalgo'),
        # Add other pairs if necessary
    }

    for pair_str, (dist, st) in known_pairs_without_comma.items():
        if pair_str.lower() in location.lower():
            return dist, st

    # Attempt to split by comma
    parts = [part.strip() for part in location.split(',') if part.strip()]

    # Prioritize finding a state from the mapping
    found_state_index = -1
    for i, part in enumerate(parts):
        for key, value in state_mapping.items():
            # Use regex for word boundaries to avoid partial matches (e.g., "mex" in "Mexico")
            if re.search(r'\b' + re.escape(key) + r'\b', part, re.IGNORECASE):
                state = value
                found_state_index = i
                break
        if state is not np.nan:
            break

    # If a state was found, the district is the part(s) before it
    if state is not np.nan:
        district_parts = parts[:found_state_index]
        if district_parts:
             # Join the district parts, assuming the last part before the state is the most specific (district)
             district = district_parts[-1]
             # Further cleaning to remove neighborhood info from the district part might be needed
             # This is a simplified approach; a more complex regex could target specific patterns for neighborhoods
        else:
             # Handle cases where state is the first part or only part, but a district might be implied
             # This case might need more specific logic based on data patterns
             pass # Keep district as NaN for now if no clear district part is found before the state


    # Specific handling for "Coyoacán" and "Chimalhuacán" regardless of comma separation
    if 'Coyoacán' in location:
        district = 'Coyoacán'
        state = 'Ciudad de México' # Assign CDMX as the state for Coyoacán
    if 'Benito Juárez' in location:
        district = 'Benito Juárez'
        state = 'Ciudad de México' # Assign CDMX as the state for Coyoacán
    elif 'Chimalhuacán' in location:
        # Assuming Chimalhuacán is always a district in Estado de México based on the data
        district = 'Chimalhuacán'
        state = 'Estado de México' # Assign Estado de México for Chimalhuacán


    # If no state was found and there are parts, assume the first part is the district and try to infer state if possible
    if state is np.nan and len(parts) > 0:
        district = parts[0]
        # Add logic here to infer state based on district name if necessary
        # For example, if district is a known municipality of a specific state


    return district, state

# Apply the function to create two new columns
df[['current_district', 'current_state']] = df['Donde Vivo'].apply(lambda x: pd.Series(extract_district_and_state_refined(x)))

# Drop the original column if no longer needed (optional)
df = df.drop(columns=['Donde Vivo'])

trabajo_mapping = {'Si': True, 'No': False, 'No trabajo': False}
df['Trabajo'] = df['Trabajo'].map(trabajo_mapping)
df = df.rename(columns={'Trabajo': 'is_working'})

# Function to clean the workplace string
def clean_workplace(workplace):
    if pd.isna(workplace):
        return np.nan
    # Remove phrases like "Trabajo en...", case-insensitive
    workplace = re.sub(r'Trabajo en\s*', '', workplace, flags=re.IGNORECASE)
    # Remove phrases like "Trabajo en una consultora llamada...", case-insensitive
    workplace = re.sub(r'una consultora llamada\s*', '', workplace, flags=re.IGNORECASE)
    # Remove additional descriptions after a comma, parenthesis, or phrases starting with " en"
    # Corrected regex: use alternation for splitting
    workplace = re.split(r',|\(|\s+en\s+', workplace)[0].strip()
    # Replace empty strings resulting from cleaning with 'Null'
    if not workplace:
        return 'Null'
    return workplace

# Apply the cleaning function and rename the column
df['Dónde Trabajo'] = df['Dónde Trabajo'].apply(clean_workplace)
df = df.rename(columns={'Dónde Trabajo': 'workplace'})

# Extract numerical part from the string, handling cases like '11vo semestre' and 'Noveno semestre'
def extract_semester(semester_str):
    if pd.isna(semester_str):
        return np.nan
    semester_str = semester_str.lower()
    # Handle specific cases first
    if 'ya debería haber terminado' in semester_str:
        return 11 # Assuming this means beyond the standard semesters

    # Extract numbers
    if 'noveno' in semester_str:
         return 9
    elif 'onceavo' in semester_str or '11vo' in semester_str:
         return 11

    numbers = re.findall(r'\d+', semester_str)
    if numbers:
        # Take the first number found as the semester
        semester_val = int(numbers[0])
        # Apply the rule: if > 10, replace with 11
        return 11 if semester_val > 10 else semester_val

    return np.nan # Return NaN if no clear semester is found

df['Semestre'] = df['Semestre'].apply(extract_semester)

# Ensure the column is numeric, coercing errors to NaN
df['Semestre'] = pd.to_numeric(df['Semestre'], errors='coerce')

# Apply the replacement rule again just in case
df['Semestre'] = df['Semestre'].apply(lambda x: 11 if pd.notna(x) and x > 10 else x)


df = df.rename(columns={'Semestre': 'semester'})

df = df.rename(columns={'Ingeniería': 'engineering_definition'})

df = df.rename(columns={'Dato': 'data_definition'})

df = df.rename(columns={'Artista Favorito': 'favorite_artist'})

# Define a dictionary for normalizing hobby phrases
hobby_normalization = {
    'Escuchar musica': 'Escuchar música',
    'Ver peliculas': 'Ver películas',
    # Add more normalizations as needed
}

# Function to normalize hobby phrases in a string
def normalize_hobbies(text):
    if pd.isna(text):
        return np.nan
    normalized_text = text
    for original, normalized in hobby_normalization.items():
        # Use regex to replace the phrase case-insensitively
        normalized_text = re.sub(re.escape(original), normalized, normalized_text, flags=re.IGNORECASE)
    return normalized_text

# Apply normalization before splitting
df['3 hobbies'] = df['3 hobbies'].apply(normalize_hobbies)


# Split the '3 hobbies' column into three new columns
hobbies = df['3 hobbies'].str.split(',| y ', expand=True)

# Rename the new columns
hobbies.columns = ['hobby_1', 'hobby_2', 'hobby_3']

# Function to capitalize the first letter if it's lowercase, preserving existing case
def custom_capitalize(s):
    if isinstance(s, str) and len(s) > 0 and s[0].islower():
        return s[0].upper() + s[1:]
    return s

# Trim whitespace from the new columns and apply the custom capitalization
hobbies = hobbies.apply(lambda x: x.str.strip().apply(custom_capitalize) if x.dtype == "object" else x)


# Concatenate the new columns to the original DataFrame
df = pd.concat([df, hobbies], axis=1)

# Drop the original '3 hobbies' column
df = df.drop(columns=['3 hobbies'])

# Function to extract numerical value, handling specific cases and non-numeric entries
def extract_number_of_residents(resident_str):
    if pd.isna(resident_str):
        return np.nan # Keep NaN initially to handle the explicit replacement later
    resident_str = str(resident_str).lower()

    # Handle specific phrases or patterns
    if 'vivo solo' in resident_str or 'nadie' in resident_str:
        return 1

    # Try to find a number associated with the total, like "X personas contandome" or "somos Y"
    total_match = re.search(r'(\d+)\s*personas contandome|\s*somos\s*(\d+)', resident_str)
    if total_match:
        # Return the matched number
        return int(total_match.group(1) or total_match.group(2))

    # If no specific total number pattern is found, extract any number
    numbers = re.findall(r'\d+', resident_str)
    if numbers:
        num = 1
        num += int(numbers[0])
        # Take the first number found as the number of residents
        return num

    return np.nan # Return NaN if no number or specific case is found

# Apply the extraction function
df['Con cuantos vivo'] = df['Con cuantos vivo'].apply(extract_number_of_residents)

# Convert to numeric first to ensure NaNs are represented as floats before filling
df['Con cuantos vivo'] = pd.to_numeric(df['Con cuantos vivo'], errors='coerce')

# Ensure the minimum value is 1
df['Con cuantos vivo'] = df['Con cuantos vivo'].apply(lambda x: max(x, 1) if pd.notna(x) else x)

# Convert the column to pandas nullable integer type ('Int64') to handle potential NaNs gracefully.
# If we are certain there are no NaNs after filling, we could use 'int64'.
df['Con cuantos vivo'] = df['Con cuantos vivo'].astype('Int64')


# Rename the column
df = df.rename(columns={'Con cuantos vivo': 'number_of_residents'})

# Value obtained through re-interview
df.at[1, 'number_of_residents'] = 3 # People including the student

# Provided list of valid courses
valid_courses = [
    "Bases de Datos Distribuidas",
    "Minería de Datos",
    "Taller Sociohumanístico - Liderazgo",
    "Diseño Digital Moderno",
    "Bases de Datos",
    "Álgebra",
    "Programación Orientada a Objetos (POO)",
    "Cálculo y Geometría Analítica",
    "Administración de Servicios de Internet",
    "Fundamentos de Estadística",
    "Administración de Proyectos de Software",
    "Sistemas Distribuidos",
    "Cálculo Vectorial",
    "Estructura de Datos y Algoritmos I",
    "Estructura de Datos y Algoritmos II",
    "Dispositivos Electrónicos",
    "Sistemas de Comunicaciones",
    "Sistemas Operativos",
    "Redes de Datos Seguras",
    "Lenguajes Formales y Autómatas",
]

# Create a dictionary for normalization, mapping lowercased input to correct valid course name
course_normalization = {course.lower(): course for course in valid_courses}

# Add some common variations or abbreviations to the normalization map if needed
course_normalization.update({
    'bases de datos': 'Bases de Datos',
    'algebra': 'Álgebra',
    'poo': 'Programación Orientada a Objetos',
    'cálculo y geo.': 'Cálculo y Geometría Analítica',
    'admin. de servicios de internet': 'Administración de Servicios de Internet',
    'estadística': 'Fundamentos de Estadística',
    'administración de proyectos': 'Administración de Proyectos de Software',
    'estructura de datos y algoritmos': 'Estructura de Datos y Algoritmos I',
    'dispositivos': 'Dispositivos Electrónicos',
    'cálculo y geometría analítica': 'Cálculo y Geometría Analítica',
    'sistemas de comunicaciones': 'Sistemas de Comunicaciones',
    'sistemas operativos': 'Sistemas Operativos',
    'redes de datos seguras': 'Redes de Datos Seguras',
    'eda2': 'Estructura de Datos y Algoritmos II',
    'bd': 'Bases de Datos',
    'cisco': 'Redes de Datos Seguras', # Assuming 'Cisco' is a valid entry though not in the list
    'cálculo y geometriía analítica': 'Cálculo y Geometría Analítica',
    'diseño digial moderno': 'Diseño Digital Moderno',
    'taller socio-humanístico: liderazgo': 'Taller Sociohumanístico - Liderazgo',
    'bases de datos (todas)': 'Bases de Datos', # Normalize this entry
    'sistemas de comunicaciones. sistemas operativos': 'Sistemas de Comunicaciones', # Assuming first is the primary
    'calculo y geometria analitica': 'Cálculo y Geometría Analítica',
    'calculo y geometría analítica': 'Cálculo y Geometría Analítica',
    # Add more specific mappings as needed based on data inspection
})


# Function to normalize a single course name
def normalize_course(course_str):
    if pd.isna(course_str):
        return np.nan
    course_str = str(course_str).strip().lower()
    # Return the normalized name if found, otherwise NaN
    return course_normalization.get(course_str, np.nan)

# patterns
y_word_re = re.compile(r'\by\b', flags=re.IGNORECASE)
fallback_pattern_with_y = re.compile(r'\s*(?:,|\.|\by\b)\s*', flags=re.IGNORECASE)
punct_split_pattern = re.compile(r'[.,;|/]+')  # punctuation separators

def split_on_last_y(s: str):
    matches = list(y_word_re.finditer(s))
    if not matches:
        return None
    last = matches[-1]
    left = s[:last.start()].strip()
    right = s[last.end():].strip()
    if left == "" or right == "":
        return None
    return left, right

def split_favs_improved(value):
    if pd.isna(value):
        return ["", "", ""]
    s = str(value).strip()
    if s == "":
        return ["", "", ""]

    # Main attempt: split by commas (apply rule 4 -> discard last)
    parts_comma = [p.strip() for p in s.split(",") if p.strip() != ""]
    if len(parts_comma) == 4:
        parts = parts_comma[:3]
    elif len(parts_comma) >= 3:
        parts = parts_comma[:3]
    elif len(parts_comma) == 2:
        # First: if the second part has punctuation separating two items, use it.
        rhs = parts_comma[1]
        rhs_by_punct = [p.strip() for p in punct_split_pattern.split(rhs) if p.strip()]
        if len(rhs_by_punct) >= 2:
            parts = [parts_comma[0]] + rhs_by_punct  #it can give >3, we'll trim it later
        else:
            # Otherwise, try rsplit by the last ' and '
            last_split = split_on_last_y(rhs)
            if last_split:
                parts = [parts_comma[0], last_split[0], last_split[1]]
            else:
                # Fallback: global split by comma/period/'and'
                parts_re = [p.strip() for p in fallback_pattern_with_y.split(s) if p.strip() != ""]
                parts = parts_re[:3] if len(parts_re) >= 3 else parts_re
    else:
        # No commas: try separating by punctuation first (.,;|/)
        parts_punct = [p.strip() for p in punct_split_pattern.split(s) if p.strip()]
        if len(parts_punct) >= 3:
            parts = parts_punct[:3]
        elif len(parts_punct) == 2:
            # if there are 2 left by score, try rsplit by the last ' and ' in the first or second
            # we prefer not to break an "X and Y" that is part of a compound name
            # try rsplit on the first part
            first_try = split_on_last_y(parts_punct[0])
            if first_try:
                parts = [first_try[0], first_try[1], parts_punct[1]]
            else:
                second_try = split_on_last_y(parts_punct[1])
                if second_try:
                    parts = [parts_punct[0], second_try[0], second_try[1]]
                else:
                    parts = parts_punct
        else:
            # last resort: split by comma/period/or ‘and’ globally
            parts_re = [p.strip() for p in fallback_pattern_with_y.split(s) if p.strip() != ""]
            parts = parts_re[:3] if len(parts_re) >= 3 else parts_re

    # Ensure exactly 3 elements (trim if there are too many, pad with "" if there are too few)
    parts = parts[:3] + [""] * (3 - len(parts[:3]))
    return parts

df[['favorite_course_1', 'favorite_course_2', 'favorite_course_3']] = \
    pd.DataFrame(df['3 Materias Favoritas'].apply(split_favs_improved).tolist(), index=df.index)

# Apply normalization to each new course column
for col in ['favorite_course_1', 'favorite_course_2', 'favorite_course_3']:
    df[col] = df[col].apply(normalize_course)

# Drop the original '3 Materias Favoritas' column
df = df.drop(columns=['3 Materias Favoritas'])

df.to_csv('../data-sets/DatosExamen-limpio-python-script.csv', index=False)