# Регистрация продавца
DIV_CREATE_SELLER = '/html/body/div[1]/ion-app/div[1]/main/div/div/div[2]/div/div/div[3]/div[2]' # кнопка Создать аккаунт организатора
SELLER_REGISTRATION_NAME_COMPANY = '/html/body/div[1]/ion-app/div[1]/main/div/div/div[2]/div/div/form/div[1]/input' #   поле название компании
SELLER_REGISTRATION_PHONE = '/html/body/div[1]/ion-app/div[1]/main/div/div/div[2]/div/div/form/div[2]/input' # поле номер телефона
SELLER_REGISTRATION_EMAIL = '/html/body/div[1]/ion-app/div[1]/main/div/div/div[2]/div/div/form/div[3]/input' # поле email
SELLER_REGISTRATION_PASSWORD = '/html/body/div[1]/ion-app/div[1]/main/div/div/div[2]/div/div/form/div[4]/div/input' # поле придумайте пароль
SELLER_REGISTRATION_REPEAT_PASSWORD = '/html/body/div[1]/ion-app/div[1]/main/div/div/div[2]/div/div/form/div[5]/input' # поле пароль еще раз
SELLER_REGISTRATION_PERSONAL_CONSENT = '/html/body/div[1]/ion-app/div[1]/main/div/div/div[2]/div/div/form/div[6]/div[1]/input'
SELLER_REGISTRATION_PRIVACY_POLICY = '/html/body/div[1]/ion-app/div[1]/main/div/div/div[2]/div/div/form/div[6]/div[2]/input' # чекбокс Соглашаюсь с политикой обработки данных
SELLER_REGISTRATION_SERVICE_POLICY = '/html/body/div[1]/ion-app/div[1]/main/div/div/div[2]/div/div/form/div[6]/div[3]/input' # чекбокс Принимаю пользовательское соглашение
SELLER_REGISTRATION_PROMOTIONAL_MATERIALS = '/html/body/div[1]/ion-app/div[1]/main/div/div/div[2]/div/div/form/div[6]/div[4]/input' # чекбокс Соглашаюсь получать рекламные материалы
SELLER_REGISTRATION_BUTTON_REGISTER= '/html/body/div[1]/ion-app/div[1]/main/div/div/div[2]/div/div/form/button' # кнопка Зарегистрироваться                 
SELLER_REGISTRATION_DIV_HAVE_ACCOUNT= '/html/body/div[1]/ion-app/div[1]/main/div/div/div[2]/div/div/div[2]/div' # кнопка Уже есть аккаунт
SELLER_REGISTRATION_DIV_PHONE_BORDER = '/html/body/div[1]/ion-app/div[1]/main/div/div/div[2]/div/div/form/div[2]' # Граница поля телефон в регистрации продавца
SELLER_REGISTRATION_DIV_EMAIL_BORDER = '/html/body/div[1]/ion-app/div[1]/main/div/div/div[2]/div/div/form/div[3]' # Граница email телефон в регистрации продавца
SELLER_REGISTRATION_DIV_PASSWORD_BORDER = '/html/body/div[1]/ion-app/div[1]/main/div/div/div[2]/div/div/form/div[4]/div' # Граница придумайте пароль в регистрации продавца




LOCATORS_SELLER_REGISTRATION = {
     # Регистрация продавца
    'кнопка Создать аккаунт организатора': DIV_CREATE_SELLER,
    'поле Название компании': SELLER_REGISTRATION_NAME_COMPANY,
    'поле Номер телефона': SELLER_REGISTRATION_PHONE ,
    'поле Email': SELLER_REGISTRATION_EMAIL,
    'поле Придумайте пароль': SELLER_REGISTRATION_PASSWORD,
    'поле Пароль еще раз': SELLER_REGISTRATION_REPEAT_PASSWORD,
    'Чекбокс Обработку персональных данных в регистрации продавца': SELLER_REGISTRATION_PERSONAL_CONSENT,
    'чекбокс Соглашаюсь с политикой обработки данных': SELLER_REGISTRATION_PRIVACY_POLICY,
    'чекбокс Принимаю пользовательское соглашение': SELLER_REGISTRATION_SERVICE_POLICY,
    'Соглашаюсь получать рекламные материалы': SELLER_REGISTRATION_PROMOTIONAL_MATERIALS,
    'кнопка Зарегистрироваться': SELLER_REGISTRATION_BUTTON_REGISTER,
    'Уже есть аккаунт': SELLER_REGISTRATION_DIV_HAVE_ACCOUNT,
    'границы поля телефон в регистрации': SELLER_REGISTRATION_DIV_PHONE_BORDER,
     'границы поля email в регистрации': SELLER_REGISTRATION_DIV_EMAIL_BORDER,
     'границы придумайте пароль в регистрации продавца': SELLER_REGISTRATION_DIV_PASSWORD_BORDER,
}