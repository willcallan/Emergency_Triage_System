from flask import Blueprint
from flask import request
from fhirclient import client
import json
import fhirclient.models.practitioner as pract
import fhirclient.models.practitionerrole as prole


from vars import settings
from flasgger.utils import swag_from

staff_endpoint = Blueprint('staff_endpoint',__name__)


@staff_endpoint.route("/staff", methods=['GET'])
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

