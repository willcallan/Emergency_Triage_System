from dotenv import load_dotenv
load_dotenv()

app_name = "NewHat_Triage_Program" # TODO: Come up with name?

settings = {
    'app_id': app_name,
    'api_base': 'https://r4.smarthealthit.org'
}
"""Settings for smart client."""

# region patient.py

esi_lookup = {      # Values from https://loinc.org/75636-1/
    'LA21567-5': ['1', 'ESI-1', 'Resuscitation'],
    'LA21752-3': ['2', 'ESI-2', 'Emergent'],
    'LA21753-1': ['3', 'ESI-3', 'Urgent'],
    'LA21754-9': ['4', 'ESI-4', 'Less urgent'],
    'LA21755-6': ['5', 'ESI-5', 'Nonurgent'],
}
"""Dictionary of LOINC codes for ESI rating. Values are the ESI rating, code, and display."""

# endregion

# region observation.py

injury_lookup = {   # Values from https://loinc.org/72300-7/
    'abrasion': ['LA7410-9', 'Abrasion'],
    'avulsion': ['LA18220-6', 'Avulsion'],
    'bite': ['LA19023-3', 'Bite'],
    'blister': ['LA19024-1', 'Blister'],
    'burn': ['LA7318-4', 'Burn'],
    'gunshotWound': ['LA17212-4', 'Gunshot wound'],
    'contusion': ['LA7423-2', 'Contusion'],
    'crushInjury': ['LA17229-8', 'Crush Injury'],
    'erythema': ['LA7433-1', 'Erythema'],
    'fissure': ['LA19025-8', 'Fissure'],
    'laceration': ['LA7452-1', 'Laceration'],
    'maceration': ['LA19026-6', 'Maceration'],
    'pressureUlcer': ['LA19028-2', 'Pressure ulcer'],
    'ulcer': ['LA16827-0', 'Ulcer'],
    'puncture': ['LA19027-4', 'Puncture'],
    'rash': ['LA7469-5', 'Rash'],
    'graft': ['LA17811-3', 'Graft'],
    'surgicalIncision': ['LA19029-0', 'Surgical incision'],
    'trauma': ['LA17058-1', 'Trauma'],
}
"""Dictionary of wound types. Values are the LOINC code and display."""

body_site_lookup = {
    'face': ['89545001', 'Face'],
    'scalp': ['41695006', 'Scalp'],
    'frontOfNeck': ['49928004', 'Anterior portion of neck'],
    'backOfNeck': ['304036007', 'Posterior portion of neck'],
    'leftShoulder': ['91775009', 'Left shoulder'],
    'rightShoulder': ['91774008', 'Right shoulder'],
    'leftUpperArm': ['368208006', 'Left upper arm'],
    'rightUpperArm': ['368209003', 'Right upper arm'],
    'leftLowerArm': ['66480008', 'Left forearm'],
    'rightLowerArm': ['64262003', 'Right forearm'],
    'leftHand': ['85151006', 'Left hand'],
    'rightHand': ['78791008', 'Right hand'],
    'chest': ['51185008', 'Chest'],
    'abdomen': ['818983003', 'Abdomen'],
    'back': ['77568009', 'Back'],
    'groin': ['26893007', 'Groin'],
    'buttock': ['46862004', 'Buttock'],
    'leftUpperLeg': ['61396006', 'Left thigh'],
    'rightUpperLeg': ['11207009', 'Right thigh'],
    'leftLowerLeg': ['48979004', 'Left lower leg'],
    'rightLowerLeg': ['32696007', 'Right lower leg'],
    'leftFoot': ['22335008', 'Left foot'],
    'rightFoot': ['7769000', 'Right foot'],
}
"""Dictionary of body parts. Values are the SNOMED code and display."""

# endregion
