from fhirclient import client
import fhirclient.models.patient as pat
import fhirclient.models.humanname as hn
import fhirclient.models.address as addr
import fhirclient.models.codeableconcept as conc
import fhirclient.models.coding as cde
import fhirclient.models.contactpoint as point
import fhirclient.models.fhirdate as dt
import fhirclient.models.practitioner as pract
import fhirclient.models.practitionerrole as practrole
import fhirclient.models.fhirreference as ref
from fhirclient.models.patient import PatientContact
import random
from dateutil import parser
from faker import Faker
from vars import settings
from triageDB import *


class DataGenerator:

    faker = Faker()

    def generate_patients(self, count):

        patient_ids = []

        smart = client.FHIRClient(settings=settings)

        patientCount = self.clear_orphan_patients()

        if patientCount > count:
            return
        else:
            count = count - patientCount
            print("Generating " + str(count) + " Patients")

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
            patient.telecom.append(tele)
            ##########################################
            patient.contact = [self.generate_emergency_contact(),self.generate_emergency_contact()]
            status = patient.create(smart.server)
            if (
                    status is not None
                    and 'resourceType' in status
                    and status['resourceType'] == 'Patient'
            ):
                addPatients(status['id'])
                print(status['id'])
                patient_ids.append(status['id'])
            else:
                print(status)

        return patient_ids

    def generate_emergency_contact(self):
        is_male = bool(random.getrandbits(1))
        emergency_contact = PatientContact()
        name = hn.HumanName()
        name.given = [self.faker.first_name_male()] if is_male else [self.faker.first_name_female()]
        name.family = self.faker.last_name()
        emergency_contact.name = name
        emergency_contact.gender = "male" if is_male else "female"
        contact_addr = addr.Address()
        contact_addr.city = self.faker.city()
        contact_addr.state = self.faker.state()
        contact_addr.postalCode = self.faker.zipcode()
        emergency_contact.address = contact_addr
        tele = point.ContactPoint()
        tele.system = 'phone'
        tele.value = self.faker.phone_number()
        emergency_contact.telecom = [tele]
        concept = conc.CodeableConcept()
        concept.text = "Family"
        emergency_contact.relationship = [concept]
        return emergency_contact

    def clear_orphan_patients(self):
        smart = client.FHIRClient(settings=settings)
        database_patients = getallPatientIds()

        count = len(database_patients)

        for patient in database_patients:
            try:
                patient = pat.Patient.read(patient[0], smart.server)
            except:
                deletePatientByFhirId(patient[0])
                count = count - 1

        return count

    def generate_practitioners(self, count):

        practitioner_ids = []

        smart = client.FHIRClient(settings=settings)

        practitionerCount = self.clear_orphan_practitioners()

        if practitionerCount > count:
            return
        else:
            count = count - practitionerCount
            print("Generating " + str(count) + " Practitioners")

        for ct in range(count):

            practitioner = pract.Practitioner()
            ##########################################
            is_male = bool(random.getrandbits(1))
            practitioner.gender = "male" if is_male else "female"
            birthdate = dt.FHIRDate()
            birthdate.date = parser.parse(self.faker.date())
            practitioner.birthDate = birthdate
            practitioner.language = "English"
            ##########################################
            name = hn.HumanName()
            name.given = [self.faker.first_name_male()] if is_male else [self.faker.first_name_female()]
            name.family = self.faker.last_name()
            practitioner.name = [name]
            ##########################################
            address = addr.Address()
            address.city = self.faker.city()
            address.state = self.faker.state()
            address.postalCode = self.faker.zipcode()
            practitioner.address = [address]
            ##########################################
            tele = point.ContactPoint()
            tele.system = 'phone'
            tele.value = self.faker.phone_number()
            practitioner.telecom = [tele]
            ##########################################
            tele = point.ContactPoint()
            tele.system = 'email'
            tele.value = self.faker.email()
            practitioner.telecom.append(tele)
            ##########################################
            status = practitioner.create(smart.server)
            if (
                    status is not None
                    and 'resourceType' in status
                    and status['resourceType'] == 'Practitioner'
            ):
                addPractioner(status['id'], None, "Doctor")
                print(status['id'])
                practitioner_ids.append(status['id'])
                gen.generate_practitioner_role(status['id'])
            else:
                print(status)

        return practitioner_ids

    def generate_practitioner_role(self, practitioner_id):

        role = practrole.PractitionerRole()

        smart = client.FHIRClient(settings=settings)

        role.active = True
        reference = ref.FHIRReference()
        reference.reference = "Practitioner/"+practitioner_id
        role.practitioner = reference

        concept = conc.CodeableConcept()
        code = cde.Coding()
        code.system = "http://terminology.hl7.org/CodeSystem/practitioner-role"
        code.code = "doctor"
        code.display = "Doctor"
        concept.coding = [code]
        role.code = [concept]

        concept = conc.CodeableConcept()
        code = cde.Coding()
        code.system = "http://terminology.hl7.org/CodeSystem/c80-practice-codes"
        code.code = "Emergency"
        code.display = "Emergency"
        concept.coding = [code]
        role.specialty = [concept]

        status = role.create(smart.server)
        if (
                status is not None
                and 'resourceType' in status
                and status['resourceType'] == 'PractitionerRole'
        ):
            print(status['id'])
        else:
            print(status)

    def clear_orphan_practitioners(self):
        smart = client.FHIRClient(settings=settings)
        database_practitioners = getAllPractitionerIds()

        count = len(database_practitioners)

        for practitioner in database_practitioners:
            try:
                practitioner = pract.Practitioner.read(practitioner[0], smart.server)
            except:
                deletePractitionerbyFhirId(practitioner[0])
                count = count - 1

        return count
