
BUTTON_ENTER = "/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div/button" # Кнопка "Войти" в хедере
BUTTON_TOUR_SELLER = "/html/body/div/ion-app/ion-router-outlet/div/div/div[4]/div[2]/div" # Кнопка "Организатор туров" 
BUTTON_SEARCH_TOURS = "/html/body/div/ion-app/ion-modal/div/div[2]/button" # Кнопка "Искать туры" 
INPUT_LOGIN_SELLER = "/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[1]/input" # Поле логин/емаил продавца для ввода текста  
INPUT_PASSWORD_SELLER = "/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[2]/input" # Поле пароль продавца для ввода текста
BUTTON_ENTER_SELLER = "/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/button" # Кнопка "Войти" в авторизации продавца
DIV_LOGIN_SELLER_BORDER = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[1]' #  Граница поля логин/емаил продавца для ввода текста 
DIV_PASSWORD_SELLER_BORDER = '/html/body/div/ion-app/ion-router-outlet/div/div/div[2]/div[2]/div/div/form/div[2]' # Граница поля пароль продавца для ввода текста


LOCATORS = {
    'кнопка Вход': BUTTON_ENTER,
    'кнопка Организатор туров': BUTTON_TOUR_SELLER,
    'кнопка Искать туры': BUTTON_SEARCH_TOURS,
    'поле Логин': INPUT_LOGIN_SELLER,
    'поле Пароль': INPUT_PASSWORD_SELLER,
    'кнопка Вход в авторизации продавца': BUTTON_ENTER_SELLER,
    'границы поля Логин': DIV_LOGIN_SELLER_BORDER,
    'границы поля Пароль': DIV_PASSWORD_SELLER_BORDER
}