from Constants.const_general import URL
import json

CLIENT_LOGIN_REQUEST_URL = f'{URL}api/auth/auth-by-phone'
CLIENT_CONFIRM_REQUEST_URL = f'{URL}api/auth/confirm-phone'
CLIENT_CONFIRM_PHONE_CODE = ''
#Авторизация клиента

CLIENT_LOGIN1 = 'avtotestclientsmorodina1@gmail.com'
CLIENT_PASSWORD1 = 'Nik123'
CLIENT_PHONE1 = ''
CLIENT_PHONE2 = ''

EXPECTED_URL_AFTER_LOGIN_CLIENT = URL
EXPECTED_URL_AFTER_A_PERSONAL_DATA = 'https://smorodina.ru/documents/c%D0%BE%D0%B3%D0%BB%D0%B0%D1%81%D0%B8%D0%B5_%D0%BD%D0%B0_%D0%BE%D0%B1%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D1%83_%D0%BF%D0%B5%D1%80%D1%81_%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85_%D0%BD%D0%B0_c%D0%B0%D0%B9%D1%82_c%D0%BC%D0%BE%D1%80%D0%BE%D0%B4%D0%B8%D0%BD%D0%B0.pdf'
EXPECTED_URL_AFTER_A_DATA_POLICY = 'https://smorodina.ru/documents/%D0%BE%D0%B1%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0_%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D1%85_%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85_Smorodina.pdf'
EXPECTED_URL_AFTER_A_AGREEMENT = 'https://smorodina.ru/documents/%D1%81%D0%BE%D0%B3%D0%BB%D0%B0%D1%88%D0%B5%D0%BD%D0%B8%D0%B5_%D0%BF%D0%BE%D0%BA%D1%83%D0%BF%D0%B0%D1%82%D0%B5%D0%BB%D1%8C_Smorodina.pdf'
C_CLIENT_CONFIRM_ERROR1 = 'Неверный код'

C_CLIENT_ERROR1 = 'Пользователь зарегистрирован как продавец'

C_CLIENT_STATUS_ACTIVE = 1
C_CLIENT_CONSENT = json.loads('''{
  "consent_personal_data": 1,
  "consent_privacy_policy": 1,
  "consent_terms_traveller": 1
}''')

