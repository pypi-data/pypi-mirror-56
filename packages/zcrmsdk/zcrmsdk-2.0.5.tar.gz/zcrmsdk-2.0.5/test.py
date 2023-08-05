import zcrmsdk

# localzoho_config = \
#     {
#             "currentUserEmail": "aswinkumar.m+oauth@zohocorp.com",
#             "client_id": "1000.ZAHF113KIJX9EHKDJ0BIMCJ842LGVH",
#             "client_secret": "2e0c334ee2795ea585b72630febce766d5f84aa3df",
#             "redirect_uri": "https://crm.zoho.com",
#             "accounts_url": "https://accounts.localzoho.com",
#             "apiBaseUrl": "https://crm.localzoho.com"
#     }

localzoho_config = \
            {
                "currentUserEmail": "aswinkumar.m+apiautomation@zohocorp.com",
                "client_id": "1000.8TAE9Z2NUVCY20458BMAR9XSXW2ENH",
                "client_secret": "927df925ab8e7c3b1a4603b14173311a84dd064f4d",
                "redirect_uri": "https://crm.zoho.com",
                "accounts_url": "https://accounts.localzoho.com",
                "apiBaseUrl": "https://crm.localzoho.com"
            }

zcrmsdk.ZCRMRestClient.initialize(localzoho_config)


# zcrmsdk.ZohoOAuth.get_client_instance().generate_access_token('1000.e5d0e6aeaf1c78a48158a7324d14189f.4ae59ba1c57d1ba4e3e45e28eec77463')
# zcrmsdk.ZohoOAuth.get_client_instance().refresh_access_token('1000.ddf509aff982e32294f4f51e4698e7b3.652a2f6e22236732ea7d322b3a42ccb0','aswinkumar.m+oauth@zohocorp.com')
zcrmsdk.ZohoOAuth.get_client_instance().refresh_access_token('1000.328af2e3e223048a9fedaeb5c8eae8a8.0377d626c7c2c00a897af34bd2e92920','aswinkumar.m+apiautomation@zohocorp.com')

# test_resp = zcrmsdk.ZCRMRecord.get_instance('Leads','525508000004139013').upload_link_as_attachment('www.zoho123z.com')

record_inst = zcrmsdk.ZCRMModule.get_instance('Leads').get_records()
# record_inst.field_data['Last_Name'] = 'FFF'
# resp = record_inst.create()
# print("here")
