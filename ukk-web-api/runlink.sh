#!/bin/bash
cp -R ./.env ./crm/.env
cp -R ./.env ./engineering/.env
cp -R ./.env ./finance/.env
cp -R ./.env ./identity/.env
cp -R ./.env ./procurement/.env
cp -R ./.env ./project-management/.env
cp -R ./.env ./hris/.env
cp -R ./.env ./queue/.env

cp -R ./storage_config.json.sample ./crm/storage_config.json
cp -R ./storage_config.json.sample ./engineering/storage_config.json
cp -R ./storage_config.json.sample ./finance/storage_config.json
cp -R ./storage_config.json.sample ./identity/storage_config.json
cp -R ./storage_config.json.sample ./procurement/storage_config.json
cp -R ./storage_config.json.sample ./project-management/storage_config.json
cp -R ./storage_config.json.sample ./hris/storage_config.json
# UTILS
# audit_trail.py
cp -R ./identity/src/utils/audit_trail.py ./crm/src/utils/
cp -R ./identity/src/utils/audit_trail.py ./engineering/src/utils/
cp -R ./identity/src/utils/audit_trail.py ./finance/src/utils/
cp -R ./identity/src/utils/audit_trail.py ./procurement/src/utils/
cp -R ./identity/src/utils/audit_trail.py ./project-management/src/utils/
cp -R ./identity/src/utils/audit_trail.py ./hris/src/utils/

# responses.py
cp -R ./identity/src/utils/responses.py ./crm/src/utils/
cp -R ./identity/src/utils/responses.py ./engineering/src/utils/
cp -R ./identity/src/utils/responses.py ./finance/src/utils/
cp -R ./identity/src/utils/responses.py ./procurement/src/utils/
cp -R ./identity/src/utils/responses.py ./project-management/src/utils/
cp -R ./identity/src/utils/responses.py ./hris/src/utils/

# std_service.py
cp -R ./identity/src/utils/std_service.py ./crm/src/utils/
cp -R ./identity/src/utils/std_service.py ./engineering/src/utils/
cp -R ./identity/src/utils/std_service.py ./finance/src/utils/
cp -R ./identity/src/utils/std_service.py ./procurement/src/utils/
cp -R ./identity/src/utils/std_service.py ./project-management/src/utils/
cp -R ./identity/src/utils/std_service.py ./hris/src/utils/

# helpers
cp -R ./identity/src/utils/helpers ./crm/src/utils/
cp -R ./identity/src/utils/helpers ./engineering/src/utils/
cp -R ./identity/src/utils/helpers ./finance/src/utils/
cp -R ./identity/src/utils/helpers ./procurement/src/utils/
cp -R ./identity/src/utils/helpers ./project-management/src/utils/
cp -R ./identity/src/utils/helpers ./hris/src/utils/

# notification
# cp -R ./identity/src/utils/notification ./crm/src/utils/
# cp -R ./identity/src/utils/notification ./engineering/src/utils/
# cp -R ./identity/src/utils/notification ./finance/src/utils/
# cp -R ./identity/src/utils/notification ./procurement/src/utils/
# cp -R ./identity/src/utils/notification ./project-management/src/utils/
# cp -R ./identity/src/utils/notification ./hris/src/utils/

# repo
cp -R ./identity/src/utils/repo ./crm/src/utils/
cp -R ./identity/src/utils/repo ./engineering/src/utils/
cp -R ./identity/src/utils/repo ./finance/src/utils/
cp -R ./identity/src/utils/repo ./procurement/src/utils/
cp -R ./identity/src/utils/repo ./project-management/src/utils/
cp -R ./identity/src/utils/repo ./hris/src/utils/

# storage
cp -R ./identity/src/utils/storage ./crm/src/utils/
cp -R ./identity/src/utils/storage ./engineering/src/utils/
cp -R ./identity/src/utils/storage ./finance/src/utils/
cp -R ./identity/src/utils/storage ./procurement/src/utils/
cp -R ./identity/src/utils/storage ./project-management/src/utils/
cp -R ./identity/src/utils/storage ./hris/src/utils/

# storage
# cp -R ./identity/src/utils/uploader ./crm/src/utils/
# cp -R ./identity/src/utils/uploader ./engineering/src/utils/
# cp -R ./identity/src/utils/uploader ./finance/src/utils/
# cp -R ./identity/src/utils/uploader ./procurement/src/utils/
# cp -R ./identity/src/utils/uploader ./project-management/src/utils/
# cp -R ./identity/src/utils/uploader ./hris/src/utils/
