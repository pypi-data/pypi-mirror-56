keyvault = {
    "name": "kvdvldev",
    "secret_name": "REGISTRY-PASSWORD"
}

auth = {
    "resource_group": "RG-APPLI-DVL-DEV",
    "managed_identity": "mi-dvl-dev-001",
    "subscription_id": "146f1dc4-e9bd-4cd1-90b8-4d9701f550f2",
}

blob = {
    "storage_account_name": "zstalrsdvllogdev01",
    "storage_key": "z++1cFPTnrNBNIM6QONcnjYUXa1VZuCs6DpsP+x9ELEuItoAZyM/W+FQLqlxsy/DWfjxywsJu5FjW2O7Wc3P1A==",
    "sas_key": "?sv=2018-03-28&ss=bfqt&srt=sco&sp=rwdlacup&se=2019-12-30T23:46:17Z&st=2019-10-10T14:46:17Z&spr=https&sig=zM%2BGVBxjpaXTMd58XLrREzVgQX4ZViIf0o9TolQKflc%3D",
    "container_name": "unittest-taz",
    "path": "test.csv",
    "data": "col1,col2,col3\nval11,val12,val13\nval21,val22,val23",
}

acr = {
    "resource_group": "RG-APPLI-DVL-DEV",
    "registry_name": "crdvldev",
    "subscription_id": "146f1dc4-e9bd-4cd1-90b8-4d9701f550f2",
    "image_name": "hello-world",
}

aci = {
    "resource_group": "RG-APPLI-DVL-DEV",
    "container_group_name": "cg-taz-test-unit",
    "location": "northeurope",
    "subscription_id": "146f1dc4-e9bd-4cd1-90b8-4d9701f550f2",
}

dls = {
    "dls_name": "lemanhprod",
    "tenant_id": "4a7c8238-5799-4b16-9fc6-9ad8fce5a7d9",
    "client_id": "e3952129-496b-416b-a244-67c43bd5bddd",
    "client_secret": "/KauQDlt2yiL34n9xsCxPLJMgKVzf.==",
    "https_proxy": "localhost:3128",
    "path": "SNCF/landing/input/METEOFRANCE/data_files/OBSERVATIONS_5MN/2019",
    "file_name": "matriceSNCF_201905201520.csv",
    "gz_file_name": "SNCF/landing/input/METEOFRANCE/data_files/PREVISIONS/20190123/previsions_20190123_J1.csv.gz",
    "tmp_file_name": "/tmp/taz.tmp"
}