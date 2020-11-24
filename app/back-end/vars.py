from dotenv import load_dotenv
load_dotenv()

app_name = "NewHat_Triage_Program" # TODO: Come up with name?

settings = {
    'app_id': app_name,
    'api_base': 'https://r4.smarthealthit.org'
}
"""Settings for smart client."""

esi_lookup = {
    'LA21567-5': ['1', 'ESI-1', 'Resuscitation'],
    'LA21752-3': ['2', 'ESI-2', 'Emergent'],
    'LA21753-1': ['3', 'ESI-3', 'Urgent'],
    'LA21754-9': ['4', 'ESI-4', 'Less urgent'],
    'LA21755-6': ['5', 'ESI-5', 'Nonurgent'],
}
"""Dictionary of LOINC codes for ESI rating. Values are the ESI rating, code, and display."""
