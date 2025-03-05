
# 
BUTTON_ENTER = "/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div/button" # кнопка "Войти" в хедере
BUTTON_TOUR_SELLER = "/html/body/div/ion-app/ion-router-outlet/div/div/div[4]/div[2]/div" # кнопка "Организатор туров" 
BUTTON_SEARCH_TOURS = "/html/body/div/ion-app/ion-modal/div/div[2]/button" # кнопка "Искать туры" 
# Авторизация продавца
INPUT_LOGIN_SELLER = "/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[1]/input" # поле логин/емаил продавца для ввода текста  
INPUT_PASSWORD_SELLER = "/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[2]/input" # поле пароль продавца для ввода текста
BUTTON_ENTER_SELLER = "/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/button" # кнопка "Войти" в авторизации продавца
DIV_LOGIN_SELLER_BORDER = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[1]' #  граница поля логин/емаил продавца для ввода текста 
DIV_PASSWORD_SELLER_BORDER = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[2]' # граница поля пароль продавца для ввода текста
# Регистрация продавца
DIV_CREATE_SELLER = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/div[3]/div[2]' # кнопка Создать аккаунт организатора
SELLER_REGISTRATION_NAME_COMPANY = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[1]/input' #   поле название компании
SELLER_REGISTRATION_PHONE = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[2]/input' # поле номер телефона
SELLER_REGISTRATION_EMAIL = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[3]/input' # поле email
SELLER_REGISTRATION_PASSWORD = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[4]/div/input' # поле придумайте пароль
SELLER_REGISTRATION_REPEAT_PASSWORD = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[5]/input' # поле пароль еще раз
SELLER_REGISTRATION_PRIVACY_POLICY = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[6]/input' # чекбокс Соглашаюсь с политикой обработки данных
SELLER_REGISTRATION_SERVICE_POLICY = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[7]/input' # чекбокс Принимаю пользовательское соглашение
SELLER_REGISTRATION_PROMOTIONAL_MATERIALS = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[8]/input' # чекбокс Соглашаюсь получать рекламные материалы
SELLER_REGISTRATION_BUTTON_REGISTER= '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/button' # кнопка Зарегистрироваться
SELLER_REGISTRATION_DIV_HAVE_ACCOUNT= '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/div[2]/div' # кнопка Уже есть аккаунт
SELLER_REGISTRATION_DIV_PHONE_BORDER = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[2]' # Граница поля телефон в регистрации продавца
SELLER_REGISTRATION_DIV_EMAIL_BORDER = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[3]' # Граница email телефон в регистрации продавца
# Подтверждение телефона продавца
SELLER_INPUT_FIRST_NUMBER = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[1]/input[1]' # Первая цифра
SELLER_INPUT_FIRST_NUMBER = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[1]/input[2]' # Вторая цифра
SELLER_INPUT_FIRST_NUMBER = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[1]/input[3]' # Третья цифра
SELLER_INPUT_FIRST_NUMBER = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[1]/input[4]' # Четвертая цифра
SELLER_BUTTON_ENTER_CONFIRM_PHONE = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[2]/button' # Кнопка Войти в подтверждении телефона


# BUTTON_TRAVELLER = '/html/body/div/ion-app/ion-router-outlet/div/div/div[1]/div[4]/div[1]/div/h4' # Кнопка "Путешественник" 

LOCATORS = {
    'кнопка Вход': BUTTON_ENTER,
    'кнопка Организатор туров': BUTTON_TOUR_SELLER,
    'кнопка Искать туры': BUTTON_SEARCH_TOURS,
    # Авторизация продавца
    'поле Логин': INPUT_LOGIN_SELLER,
    'поле Пароль': INPUT_PASSWORD_SELLER,
    'кнопка Вход в авторизации продавца': BUTTON_ENTER_SELLER,
    'границы поля Логин': DIV_LOGIN_SELLER_BORDER,
    'границы поля Пароль': DIV_PASSWORD_SELLER_BORDER,
    # Регистрация продавца
    'кнопка Создать аккаунт организатора': DIV_CREATE_SELLER,
    'поле Название компании': SELLER_REGISTRATION_NAME_COMPANY,
    'поле Номер телефона': SELLER_REGISTRATION_PHONE ,
    'поле Email': SELLER_REGISTRATION_EMAIL,
    'поле Придумайте пароль': SELLER_REGISTRATION_PASSWORD,
    'поле Пароль еще раз': SELLER_REGISTRATION_REPEAT_PASSWORD,
    'чекбокс Соглашаюсь с политикой обработки данных': SELLER_REGISTRATION_PRIVACY_POLICY,
    'чекбокс Принимаю пользовательское соглашение': SELLER_REGISTRATION_SERVICE_POLICY,
    'Соглашаюсь получать рекламные материалы': SELLER_REGISTRATION_PROMOTIONAL_MATERIALS,
    'кнопка Зарегистрироваться': SELLER_REGISTRATION_BUTTON_REGISTER,
    'Уже есть аккаунт': SELLER_REGISTRATION_DIV_HAVE_ACCOUNT,
    'границы поля телефон в регистрации': SELLER_REGISTRATION_DIV_PHONE_BORDER,
     'границы поля email в регистрации': SELLER_REGISTRATION_DIV_EMAIL_BORDER,
    # Подтверждение телефона продавца
    'Первая цифра': SELLER_INPUT_FIRST_NUMBER,
    'Вторая цифра': SELLER_INPUT_FIRST_NUMBER, 
    'Третья цифра': SELLER_INPUT_FIRST_NUMBER, 
    'Четвертая цифра': SELLER_INPUT_FIRST_NUMBER, 
    'Кнопка Войти в подтверждении телефона': SELLER_BUTTON_ENTER_CONFIRM_PHONE
   


    # 'кнопка Путешественник': BUTTON_TRAVELLER
}