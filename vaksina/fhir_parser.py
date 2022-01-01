# Copyright (c) 2022 Michael Casadevall
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

'''So this module exists because the reference implementations parse
that can the SMART FHIRs data is in development, poorly documented
and to quote the *official* SMARTS specification, you can hack it 
together from a bunch of freestandin libraries. SInce there's no 
validated turnkey solution, there's going to be a lot of health
providers that will DIY it, and do it wrong

So, unfortunately, we're going to have to parse this ourselves.

This is going to suck ~ NCommander'''

import json
from datetime import datetime

class Person(object):
    def __init__(self):
        self.name = None
        self.dob = None
        self.immunizations = []

class Immunization(object):
    def __init__(self):
        self.vaccine_administered = None
        self.date_given = None
        self.lot_number = None
        self._shc_parent_object = None # used to help assemble records


class FHIRParser(object):
    # {'lotNumber': '0000001',
    #  'occurrenceDateTime': '2021-01-01',
    #  'patient': {'reference': 'resource:0'},
    #  'performer': [{'actor': {'display': 'ABC General Hospital'}}],
    #  'resourceType': 'Immunization',
    #  'status': 'completed',
    #  'vaccineCode': {'coding': [{'code': '207',
    #                              'system': 'http://hl7.org/fhir/sid/cvx'}]}}

    def parse_immunization_record(resource):
        '''Confirms FHIR Immunization record to object'''

        # It's possible that multiple vaccines can be given in
        # single day. This isn't done for COVID per say, but 
        # because FIRS is a general purpose specification, we
        # should handle this, especially if there are future
        # multishot COVID vaccinations that *are* given at later
        # point, because data structures are important

        immunizations = []
        vaccine_code = resource['vaccineCode']
        for code in vaccine_code['coding']:
            if code['system'] != 'http://hl7.org/fhir/sid/cvx':
                # Unknown coding
                print("ERROR: unknown vaccine coding system")
                continue

            immunization = Immunization()
            immunization.lot_number = resource['lotNumber']
            immunization.date_given = datetime.fromisoformat(resource['occurrenceDateTime'])
            immunization.vaccine_administered = code['code']
            immunization._shc_parent_object = resource['patient']['reference']
            # so register the specific vaccine, right now, just handle the "code"
            immunizations.append(immunization)

        return immunizations

    def parse_person_record(source):
        pass

    def parse_bundle_to_persons(bundle):
        # First, we need to sort, and create top level records

        if bundle['resourceType'] != "Bundle":
            raise ValueError("must be FHIRS Bundle")

        # So we need to map each type of resource to
        # is URI to build the end result. uri fields are
        # freeform, so yay ...

        resource_uris = dict()

        for entry in bundle['entry']:
            # Determine what type of resource we're looking at
            resource = entry['resource']

            if resource['resourceType'] == 'Patient':
                FHIRParser.parse_person_record(resource)
            elif resource['resourceType'] == 'Immunization':
                # ok, special case here, we only handle an immunizaiton
                # if it was actually completed, otherwise, disregard
                if resource['status'] != 'completed':
                    # FIXME: check this
                    print("FIXME: handle non-complete status")
                    continue
 
                immunization = FHIRParser.parse_immunization_record(resource)
                print(vars(immunization[0]))
            else:
                # its a record type we don't know/understand
                print("FIXME: LOGME, UNKNOWN RECORD")

            resource_uris[entry['fullUrl']] = None # FIXME: become an object