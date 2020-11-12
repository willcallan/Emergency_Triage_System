from flask import Blueprint
from flask import request
from fhirclient import client
import json
import fhirclient.models.practitioner as pract
import fhirclient.models.practitionerrole as prole
import fhirclient.models.contactpoint as cnt
import fhirclient.models.humanname as nm


from vars import settings
from flasgger.utils import swag_from

practitioner_endpoint = Blueprint('practitioner_endpoint',__name__)


@practitioner_endpoint.route("/staff", methods=['GET'])
@practitioner_endpoint.route("/practitioner", methods=['GET'])
def search_staff():

    staff_id = request.args.get("id")

    if not staff_id:
        return ''

    smart = client.FHIRClient(settings=settings)
    practitioner = pract.Practitioner.read(staff_id,smart.server)
    roleSearch = prole.PractitionerRole.where(struct={'practitioner': staff_id})
    results = roleSearch.perform(smart.server)
    roles, specialties = get_main_role_and_specialty(results)

    ret_dict = {}

    if practitioner:
        ret_dict['professionType'] = roles
        ret_dict['name'] = smart.human_name(practitioner.name[0])
        ret_dict['specialty'] = specialties
        ret_dict['email'] = get_email(practitioner.telecom)
        ret_dict['contact'] = get_phone(practitioner.telecom)

    return json.dumps(ret_dict,indent=4)


@practitioner_endpoint.route("/staff/save", methods=['POST'])
@practitioner_endpoint.route("/practitioner/save", methods=['POST'])
def save_or_update_staff():

    req_data = request.json

    if not req_data:
        return ''

    smart = client.FHIRClient(settings=settings)

    if req_data['id']:
        return update_practitioner(req_data,smart)


def update_practitioner(req_data,smart):
    practitioner = pract.Practitioner.read(req_data['id'], smart.server)
    role_search = prole.PractitionerRole.where(struct={'practitioner': req_data['id']})
    results = role_search.perform(smart.server)
    old_roles, old_specialties = get_main_role_and_specialty(results)

    old_roles = old_roles.split(", ")
    old_specialties = old_specialties.split(", ")

    names = req_data['name'].split(" ")

    if not practitioner.name:
        practitioner.name = [nm.HumanName()]

    if len(names) == 3:
        if practitioner.name[0].prefix:
            practitioner.name[0].prefix[0] = names[0]
        else:
            practitioner.name[0].prefix = [names[0]]

        if practitioner.name[0].given:
            practitioner.name[0].given[0] = names[1]
        else:
            practitioner.name[0].given = [names[1]]

        practitioner.name[0].family = names[2]

    elif len(names) == 2:
        practitioner.name[0].given[0] = names[0]
        practitioner.name[0].family = names[1]

    if req_data['email'] and req_data['email'] != "":
        if practitioner.telecom:
            email_update = False
            for com in practitioner.telecom:
                if com.system == "email":
                    com.value = req_data['email']
                    email_update = True

            if not email_update:
                if practitioner.telecom:
                    point = cnt.ContactPoint()
                    point.system = "email"
                    point.value = req_data["email"]
                    practitioner.telecom.append(point)

    if req_data['contact'] and req_data['contact'] != "":
        if practitioner.telecom:
            phone_update = False
            for com in practitioner.telecom:
                if com.system == "phone":
                    com.value = req_data['contact']
                    email_update = True

            if not phone_update:
                if practitioner.telecom:
                    point = cnt.ContactPoint()
                    point.system = "phone"
                    point.value = req_data["contact"]
                    practitioner.telecom.append(point)

    practitioner.update(smart.server)

    return 'OK'



def get_email(telecoms):
    if telecoms is not None:
        for tele in telecoms:
            if tele.system == 'email':
                return tele.value
    return ''


def get_phone(telecoms):
    if telecoms is not None:
        for tele in telecoms:
            if tele.system == 'phone':
                return tele.value
    return ''


def get_main_role_and_specialty(roleSearchResults):
    if roleSearchResults.total > 0:
        role_set = set([])
        specialty_set = set([])
        try:
            for role in roleSearchResults.entry:
                if role.resource.code is not None:
                    for code in role.resource.code:
                        for coding in code.coding:
                            role_set.add(coding.display)
                if role.resource.specialty is not None:
                    for specialty in role.resource.specialty:
                        for coding in specialty.coding:
                            specialty_set.add(coding.display)

            return ', '.join(role_set), ', '.join(specialty_set)

        except:
            return '',''
    return '',''

