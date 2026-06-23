
CLIENT_AUTH_FIELD_PHONE = '/html/body/div[3]/div/div[2]/div/div/div[1]/input'        
CLIENT_AUTH_FIELD_PHONE_TOURCARD = '/html/body/div[4]/div/div[2]/div/div/div[1]/input'         
CLIENT_AUTH_BUTTON_CONTINUE = '/html/body/div[3]/div/div[2]/div/div/button'
CLIENT_AUTH_BUTTON_CONTINUE_TOURCARD = '/html/body/div[4]/div/div[2]/div/div/button'
# Соглашения
CLIENT_AUTH_A_PERSONAL_DATA = '/html/body/div[3]/div/div[2]/div/div/p/a[1]'
CLIENT_AUTH_A_DATA_POLICY = '/html/body/div[3]/div/div[2]/div/div/p/a[2]'
CLIENT_AUTH_A_USER_AGREEMENT = '/html/body/div[3]/div/div[2]/div/div/p/a[3]'
CLIENT_AUTH_A_PERSONAL_DATA_CHECKBOX = '/html/body/div[3]/div/div[2]/div/div/div[2]/div[1]/input'
CLIENT_AUTH_A_DATA_POLICY_CHECKBOX = '/html/body/div[3]/div/div[2]/div/div/div[2]/div[2]/input'
CLIENT_AUTH_A_USER_AGREEMENT_CHECKBOX = '/html/body/div[3]/div/div[2]/div/div/div[2]/div[3]/input'
# Ошибки
CLIENT_AUTH_ERROR_FIELD = '/html/body/div[1]/ion-app/ion-modal/div/div/div[3]/div[2]/div/div/div'
CLIENT_AUTH_TOAST = '/html/body/div[1]/ion-app/ion-toast//div/div/div/div'
CLIENT_AUTH_BORDER_PHONE = '/html/body/div[1]/ion-app/ion-modal/div/div/div[3]/div[1]'
#Войти по почте

# Альфа ID
CLIENT_AUTH_BUTTON_ALFA = '/html/body/div[3]/div/div[2]/div/div/div[4]/button'
# VK ID
CLIENT_AUTH_BUTTON_VK = '/html/body/div[3]/div/div[2]/div/div/div[5]/button'

LOCATORS_SELLER_AURH_AND_REGISTRATION = {
    'Поле с телефоном в авторизации/регистрации клиент': CLIENT_AUTH_FIELD_PHONE,
    'Поле с телефоном в авторизации/регистрации клиент из карточки тура': CLIENT_AUTH_FIELD_PHONE_TOURCARD,
    'Кнопка Продолжить в модалке авторизации клиента': CLIENT_AUTH_BUTTON_CONTINUE,
    'Кнопка Продолжить в модалке авторизации клиента из карточки тура': CLIENT_AUTH_BUTTON_CONTINUE_TOURCARD,
    # Соглашения
    'Ссылка Обработку персональных данных в авторизации клиента': CLIENT_AUTH_A_PERSONAL_DATA,
    'Ссылка Политика обработки данных в авторизации клиента': CLIENT_AUTH_A_DATA_POLICY,
    'Ссылка Пользовательское соглашение в авторизации клиента': CLIENT_AUTH_A_USER_AGREEMENT,
    'Чекбокс согласия на обработку данных в авторизации клиента': CLIENT_AUTH_A_PERSONAL_DATA_CHECKBOX,
    'Чекбокс согласия с политикой обработки данных в авторизации клиента': CLIENT_AUTH_A_DATA_POLICY_CHECKBOX,
    'Чекбокс согласия с пользовательским соглашением в авторизации клиента': CLIENT_AUTH_A_USER_AGREEMENT_CHECKBOX,
    # Ошибки
    'Ошибка в авторизации клиента': CLIENT_AUTH_ERROR_FIELD,
    'Всплывающая ошибка в авторизации клиента': CLIENT_AUTH_TOAST,
    'Граница поля телефон в авторизации клиента': CLIENT_AUTH_BORDER_PHONE,
    #Войти по почте

    # Альфа ID
    'Кнопка Войти по Альфа ID в модалке авторизации клиента': CLIENT_AUTH_BUTTON_ALFA,
    # VK ID
    'Кнопка Войти по Альфа ID в модалке авторизации клиента': CLIENT_AUTH_BUTTON_VK,
}   


