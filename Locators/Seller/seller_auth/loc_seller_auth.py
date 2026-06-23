# Авторизация продавца
INPUT_LOGIN_SELLER = "/html/body/div[3]/div/div[2]/div/div/div[1]/input" # поле логин/емаил продавца для ввода текста  
INPUT_PASSWORD_SELLER = "/html/body/div[3]/div/div[2]/div/div/div[2]/div/input" # поле пароль продавца для ввода текста
BUTTON_EMAIL_ENTER = '/html/body/div[3]/div/div[2]/div/div/div[4]/button' # кнопка "Войти по почте" в авторизации продавца
BUTTON_ENTER_SELLER = "/html/body/div[3]/div/div[2]/div/div/button" # кнопка "Войти" в авторизации продавца
DIV_LOGIN_SELLER_BORDER = '/html/body/div[1]/ion-app/div[1]/main/div/div/div[2]/div/div/form/div[1]' #  граница поля логин/емаил продавца для ввода текста 
DIV_PASSWORD_SELLER_BORDER = '/html/body/div[1]/ion-app/div[1]/main/div/div/div[2]/div/div/form/div[2]' # граница поля пароль продавца для ввода текста
# Соглашения
SELLER_AUTH_A_PERSONAL_DATA_CHECKBOX = '/html/body/div[3]/div/div[2]/div/div/div[3]/div[1]/input'
SELLER_AUTH_A_DATA_POLICY_CHECKBOX = '/html/body/div[3]/div/div[2]/div/div/div[3]/div[2]/input'
SELLER_AUTH_A_USER_AGREEMENT_CHECKBOX = '/html/body/div[3]/div/div[2]/div/div/div[3]/div[3]/input'


LOCATORS_SELLER_AUTH = {

    # Авторизация продавца
    'поле Логин': INPUT_LOGIN_SELLER,
    'поле Пароль': INPUT_PASSWORD_SELLER,
    'кнопка Войти по почте': BUTTON_EMAIL_ENTER,
    'кнопка Вход в авторизации продавца': BUTTON_ENTER_SELLER,
    'границы поля Логин': DIV_LOGIN_SELLER_BORDER,
    'границы поля Пароль': DIV_PASSWORD_SELLER_BORDER,
    # Соглашения
    'Чекбокс согласия на обработку данных в авторизации продавца': SELLER_AUTH_A_PERSONAL_DATA_CHECKBOX,
    'Чекбокс согласия с пользовательским соглашением в авторизации продавца': SELLER_AUTH_A_DATA_POLICY_CHECKBOX,
    'Чекбокс согласия с политикой обработки данных в авторизации продавца': SELLER_AUTH_A_USER_AGREEMENT_CHECKBOX,
}