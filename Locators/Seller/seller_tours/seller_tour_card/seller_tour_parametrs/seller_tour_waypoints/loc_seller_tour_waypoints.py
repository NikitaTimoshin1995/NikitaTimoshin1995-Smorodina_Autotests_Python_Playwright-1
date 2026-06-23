
#В параметрах тура
SELLER_TOUR_CREATE_WAYPOINTS_ALL = '/html/body/div[1]/ion-app/div[2]/ion-router-outlet/ion-content/div/div[2]/div[2]/div[9]/div[1]/div[2]/div[3]'
SELLER_TOUR_CREATE_TIMEZONE_ALL = '/html/body/div[1]/ion-app/div[2]/ion-router-outlet/ion-content/div/div[2]/div[2]/div[9]/div[1]/div[2]/div[4]'
SELLER_TOUR_CREATE_WAYPOINTS_ENTER = '/html/body/div[1]/ion-app/div[2]/ion-router-outlet/ion-content/div/div[2]/div[2]/div[9]/div[1]/div[2]/div[4]/div[3]/button'
SELLER_TOUR_CREATE_TIMEZONE ='/html/body/div[1]/ion-app/div[2]/ion-router-outlet/ion-content/div/div[2]/div[2]/div[9]/div[1]/div[2]/div[4]/div[1]/span[1]'
#В маршруте
SELLER_TOUR_CREATE_WAYPOINTS_ROUTE_TIMEZONE ='/html/body/div[1]/ion-app/ion-modal/div/div/div[2]/div[2]/div[1]/div[1]/div/span'
SELLER_TOUR_CREATE_WAYPOINTS_ROUTE_CROSS = '/html/body/div[1]/ion-app/ion-modal/div/div/div[2]/div[1]'
SELLER_TOUR_CREATE_WAYPOINTS_TIMEZONE1 ='/html/body/div[3]/div/ul/li[2]'
SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_ENTER = '/html/body/div[1]/ion-app/ion-modal/div/div/div[2]/div[2]/div[2]/div'
# Точка сбора
SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_BUTTON_SAVE = '/html/body/div[1]/ion-app/ion-modal/div/div/div[2]/div[2]/button'
SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_DAY = '/html/body/div[1]/ion-app/ion-modal/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/div/div'
SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_INPUT_ADDRESS= '/html/body/div[1]/ion-app/ion-modal/div/div/div[1]/div/div[1]/div/span/input'
SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_ADDRESS_FIRST_CHOICE ='/html/body/div[3]/div/ul/li[1]'
SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_CORDS = '/html/body/div[1]/ion-app/ion-modal/div/div/div[2]/div[1]/div[1]/div/p[2]'
SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_DAY_VALUE = '/html/body/div[1]/ion-app/ion-modal/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/div/div/div[1]/input'
SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_TIME = '/html/body/div[1]/ion-app/ion-modal/div/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/input'
SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_TITLE = '/html/body/div[1]/ion-app/ion-modal/div/div/div[2]/div[1]/div[2]/div[2]/input'
SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_DESCRIPTION = '/html/body/div[1]/ion-app/ion-modal/div/div/div[2]/div[1]/div[2]/div[3]/div[2]/div[1]'
SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_PHOTO_LOAD = '/html/body/div[1]/ion-app/ion-modal/div/div/div[2]/div[1]/div[2]/div[5]/label'


LOCATORS_SELLER_TOUR_CREATE_WAYPOINTS = {
    #В параметрах тура
    'Блок маршрут в параметрах тура': SELLER_TOUR_CREATE_WAYPOINTS_ALL,
    'Блок часовой пояс в параметрах тура': SELLER_TOUR_CREATE_TIMEZONE_ALL,
    'Кнопка Настроить маршрут в создании тура продавца': SELLER_TOUR_CREATE_WAYPOINTS_ENTER,
    'Часовой пояс в создании тура продавца': SELLER_TOUR_CREATE_TIMEZONE,
    #В маршруте
    'Часовой пояс маршрута в создании тура продавца': SELLER_TOUR_CREATE_WAYPOINTS_ROUTE_TIMEZONE,
    'Крестик в маршруте в создании тура продавца': SELLER_TOUR_CREATE_WAYPOINTS_ROUTE_CROSS,
    'Первый часовой пояс': SELLER_TOUR_CREATE_WAYPOINTS_TIMEZONE1,
    'Точка сбора в маршруте в создании тура продавца': SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_ENTER, 
    # Точка сбора
    'Кнопка Сохранить в точке сбора в создании тура продавца': SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_BUTTON_SAVE,
    'День в точке сбора в создании тура продавца': SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_DAY,
    'Адрес в точке сбора в создании тура продавца': SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_INPUT_ADDRESS,
    'Первый предложенный адрес в точке сбора в создании тура продавца': SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_ADDRESS_FIRST_CHOICE,
    'Координаты в точке сбора в создании тура продавца': SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_CORDS,
    'Значение дня в точке сбора в создании тура продавца': SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_DAY_VALUE,
    'Время в точке сбора в создании тура продавца': SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_TIME,
    'Название в точке сбора в создании тура продавца': SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_TITLE,
    'Описание в точке сбора в создании тура продавца': SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_DESCRIPTION,
    'Загрузка фото в точке сбора в создании тура продавца ': SELLER_TOUR_CREATE_WAYPOINTS_COLLECTION_POINT_PHOTO_LOAD
}