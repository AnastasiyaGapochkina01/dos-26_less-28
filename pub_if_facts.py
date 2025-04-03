#!/usr/bin/python3

DOCUMENTATION = '''
---
module: get_pubip
short description: Retrieve public IP
version: v1
options:
    api_url
author:
    anestesia (anastasiya.gapochkina01@yandex.ru)
'''
EXAMPLES = '''
Examples:
# Get pub ip from api.ipify.org
- name: Get public ip
  get_pubip:

# Get pub ip from 2ip.ru
- name: Get pub ip
  git_pubip:
    api_url: https://2ip.ru
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url
from ansible.module_utils.common.text.converters import to_text
import json

class PubIpFacts:
    def __init__(self, module):
        # Получаем объект модуля через конструктор
        self.module = module
        self.api_url = module.params['api_url']

    def run(self):
        result = {'public_ip': None}

        response, info = fetch_url(
            module=self.module,
            url=self.api_url + "?format=json",
            force=True
        )

        if not response:
            self.module.fail_json(msg="No valid response from API")

        try:
            data = json.loads(to_text(response.read()))
            result['public_ip'] = data.get('ip')
            return result
        except Exception as e:
            self.module.fail_json(msg=f"Failed to parse response: {str(e)}")

def main():
    module = AnsibleModule(
        argument_spec=dict(
            api_url=dict(type='str', default='https://api.ipify.org/')
        ),
        supports_check_mode=True
    )

    try:
        pub_ip = PubIpFacts(module).run()
        module.exit_json(
            changed=False,
            ansible_facts={'pub_ip': pub_ip}
        )
    except Exception as e:
        module.fail_json(msg=str(e))

if __name__ == "__main__":
    main()
