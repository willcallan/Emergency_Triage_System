from fhirclient import client

import fhirclient.models.patient as pat
import fhirclient.models.humanname as hn
import fhirclient.models.address as addr
import fhirclient.models.codeableconcept as conc
import fhirclient.models.coding as cde
import fhirclient.models.contactpoint as point
import fhirclient.models.fhirdate as dt
import random
from dateutil import parser
from faker import Faker
from vars import settings
from triageDB import addPatients,getallPatientIds,deletePatientByFhirId

class DataGenerator:

    faker = Faker()

    def generate_patients(self, count):

        patient_ids = []

        smart = client.FHIRClient(settings=settings)

        self.clear_orphan_patients()

        for ct in range(count):

            patient = pat.Patient()
            ##########################################
            is_male = bool(random.getrandbits(1))
            patient.gender = "male" if is_male else "female"
            birthdate = dt.FHIRDate()
            birthdate.date = parser.parse(self.faker.date())
            patient.birthDate = birthdate
            ##########################################
            concept = conc.CodeableConcept()
            code = cde.Coding()
            code.system = "https://terminology.hl7.org/2.0.0/CodeSystem-v3-MaritalStatus.html"
            marital_statuses = {'A':'Annulled','D':'Divorced','I':'Interlocutory','L':'Legally Separated',
                                'M':'Married','C':'Common Law','P':'Polygamous','T':'Domestic partner',
                                'U':'unmarried','S':'Never Married','W':'Widowed'}

            marital_choice = random.choice(list(marital_statuses.keys()))
            code.code = marital_choice
            code.display = marital_statuses[marital_choice]
            concept.text = marital_statuses[marital_choice]
            concept.coding = [code]
            patient.maritalStatus = concept
            ##########################################
            patient.language = "English"
            ##########################################
            name = hn.HumanName()
            name.given = [self.faker.first_name_male()] if is_male else [self.faker.first_name_female()]
            name.family = self.faker.last_name()
            patient.name = [name]
            ##########################################
            address = addr.Address()
            address.city = self.faker.city()
            address.state = self.faker.state()
            address.postalCode = self.faker.zipcode()
            patient.address = [address]
            ##########################################
            tele = point.ContactPoint()
            tele.system = 'phone'
            tele.value = self.faker.phone_number()
            patient.telecom = [tele]
            ##########################################
            tele = point.ContactPoint()
            tele.system = 'email'
            tele.value = self.faker.email()
            patient.telecom = [tele]
            ##########################################
            #is_male = bool(random.getrandbits(1))
            #patient.gender = "male" if is_male else "female"
            #emergency_contact = PatientContact()
            #emergency_contact.

            status = patient.create(smart.server)
            if (
                    status is not None
                    and 'resourceType' in status
                    and status['resourceType'] == 'Patient'
            ):
                addPatients(status['id'])
                patient_ids.append(status['id'])
            else:
                print(status)

        return patient_ids

    def clear_orphan_patients(self):
        smart = client.FHIRClient(settings=settings)
        database_patients = getallPatientIds()

        for patient in database_patients:
            try:
                patient = pat.Patient.read(patient[0], smart.server)
            except:
                deletePatientByFhirId(patient[0])



gen = DataGenerator()

gen.generate_patients(5)