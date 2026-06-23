
# Главная
BUTTON_ENTER = "/html/body/div[1]/ion-app/div/ion-content/div[1]/div[2]/div/div[2]/div/button" # кнопка "Войти" в хедере
BUTTON_TOUR_SELLER = "/html/body/div[1]/ion-app/div[1]/ion-content/div[1]/div[4]/div[2]/div" # кнопка "Организатор туров" 
BUTTON_CLIENT_PROFILE = "//button[.//div[contains(normalize-space(.), 'Профиль')]]" # кнопка Профиль
BUTTON_CLIENT_PROFILE_PROFILE = '/html/body/div[1]/ion-app/div[2]/div[1]/div[2]/div/div/div[3]/div/div/a[2]/p' # кнопка Профиль>Профиль
BUTTON_ESCAPE = '/html/body/div[1]/ion-app/div[2]/main/div/div/div/div[3]/button[2]' #Выйти > Профиль из карточки тура
BUTTON_ESCAPE_BOOKING = '/html/body/div[1]/ion-app/div[2]/div[1]/div[2]/div/div[2]/div[3]/div/div/button' #Выйти > Профиль из карточки тура
BUTTON_CLIENT_PROFILE_TOURCARD = '/html/body/div[1]/ion-app/div[2]/div[1]/div[2]/div/div/div/div/button[2]' # кнопка Профиль из карточки тура
BUTTON_CLOSE_POPPAP = '/html/body/div[2]/div[2]'
BUTTON_CLOSE_POPPAP2 = '/html/body/div[3]/div[2]'


LOCATOR_MAIN_PAGE = {
    # Главная
    'кнопка Вход': BUTTON_ENTER, 
    'кнопка Организатор туров': BUTTON_TOUR_SELLER,
    'кнопка Профиль у клиента': BUTTON_CLIENT_PROFILE,
    'кнопка Профиль>Профиль у клиента': BUTTON_CLIENT_PROFILE_PROFILE,
    'кнопка Выйти':BUTTON_ESCAPE,
    'кнопка Выйти бронирование':BUTTON_ESCAPE_BOOKING,
    'кнопка Профиль из карточки тура':BUTTON_CLIENT_PROFILE_TOURCARD,
    'кнопка закрыть поппап':BUTTON_CLOSE_POPPAP,
    'кнопка закрыть поппап2':BUTTON_CLOSE_POPPAP2,
}
