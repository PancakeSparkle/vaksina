#!/usr/bin/env python3

import json
import vaksina

def main():
    smart_json = None
    with open("smart_bundle.json", "r") as f:
        fhir_json = json.loads(f.read())
    

    parser = vaksina.FHIRParser.parse_bundle_to_persons(fhir_json['vc']['credentialSubject']['fhirBundle'])

if __name__ == '__main__':
    main()