import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_student_ids(inschrijving_file, punten_file):
    try:
        # Load the Excel files
        inschrijving_df = pd.read_excel(inschrijving_file)
        punten_df = pd.read_excel(punten_file)
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return
    except Exception as e:
        logging.error(f"Error reading Excel files: {e}")
        return

    try:
        # Extract the 'ID' columns
        inschrijving_ids = inschrijving_df['ID']
        punten_ids = punten_df['ID']
    except KeyError as e:
        logging.error(f"Missing 'ID' column: {e}")
        return

    # Replace 'AFW' and 'VER' values in the 'Cijfer' column with 0
    punten_df['Cijfer'] = punten_df['Cijfer'].replace(['AFW', 'VER'], 0)

    # Filter punten DataFrame where Cijfer is not 0
    filtered_punten_df = punten_df[punten_df['Cijfer'] != 0]

    # Check which IDs in inschrijving are present in punten
    matching_ids = inschrijving_ids[inschrijving_ids.isin(punten_ids)]

    # Log the number of matching IDs
    logging.info(f"Number of matching IDs: {len(matching_ids)}")

    # Output the results
    logging.info("Matching IDs and their highest Cijfer values:")
    for id in matching_ids:
        cijfer_values = filtered_punten_df.loc[filtered_punten_df['ID'] == id, 'Cijfer']
        if not cijfer_values.empty:
            max_cijfer = cijfer_values.max()
            logging.info(f"ID: {id}, Highest Cijfer: {max_cijfer}")
        else:
            logging.info(f"ID: {id}, Cijfer: Not found")

# Call the function with the file names
check_student_ids('inschrijving.xlsx', 'punten.xlsx')