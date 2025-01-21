import re
import json
from faker import Faker

# Initialize Faker
fake = Faker()

# Map SQL data types to Faker methods
type_mapping = {
    "varchar": lambda: fake.word(),
    "text": lambda: fake.sentence(),
    "int": lambda: fake.random_int(min=0, max=100),
    "bigint": lambda: fake.random_int(min=0, max=10**12),
    "float": lambda: fake.pyfloat(left_digits=5, right_digits=2, positive=True),
    "decimal": lambda: float(fake.pydecimal(left_digits=5, right_digits=2, positive=True)),
    "tinyint": lambda: fake.random_int(min=0, max=1),
    "timestamp": lambda: fake.date_time().isoformat(),
    "date": lambda: fake.date(),
    "enum": lambda values: fake.random_element(values),
}

# Columns and tables to exclude
excluded_columns = {"id","user_id","owner_id","created_at","updated_at","email_validated_at","email_verified_at","remember_token","api_token"}
excluded_tables = {"sessions","personal_access_tokens","jobs","cache","migrations","job_batches","cache_locks","password_reset_tokens"}  # Example of tables to exclude

# Function to parse table structure
def parse_table_structure(sql):
    tables = {}
    table_name = None
    enum_map = {}

    for line in sql.splitlines():
        if line.startswith("CREATE TABLE"):
            match = re.search(r"`(\w+)`", line)
            if match:
                table_name = match.group(1)
                if table_name in excluded_tables:  # Skip the table entirely if excluded
                    table_name = None
                else:
                    tables[table_name] = []
        elif table_name and "`" in line:
            column_match = re.search(r"`(\w+)` (\w+).*?", line)
            if column_match:
                column_name, column_type = column_match.groups()
                if column_name not in excluded_columns:  # Exclude specific columns
                    # Handle enums separately
                    if "enum" in line:
                        enum_values = re.findall(r"'(.*?)'", line)
                        enum_map[column_name] = enum_values
                    tables[table_name].append((column_name, column_type))
        elif line.startswith(");"):
            table_name = None  # Reset table_name when ending a table definition

    return tables, enum_map


# Generate sample data
def generate_sample_data(tables, enum_map):
    sample_data = {}
    for table, columns in tables.items():
        table_data = {}
        for column_name, column_type in columns:
            # Handle enums
            if column_name in enum_map:
                table_data[column_name] = fake.random_element(enum_map[column_name])
            else:
                # Match the column type to a Faker generator
                for sql_type, faker_func in type_mapping.items():
                    if sql_type in column_type:
                        table_data[column_name] = faker_func()
                        break
        sample_data[table] = table_data
    return sample_data

# Read SQL structure from file
file_path = "table-structure.txt"  # Update this path as needed
with open(file_path, "r") as f:
    table_structure = f.read()

# Parse the table structure
parsed_tables, enums = parse_table_structure(table_structure)

# Generate the sample data
sample_data = generate_sample_data(parsed_tables, enums)

# Write output to JSON file
output_file = "primalfits_data.json"
with open(output_file, "w") as f:
    json.dump(sample_data, f, indent=4)

print(f"Sample data has been written to {output_file}")
