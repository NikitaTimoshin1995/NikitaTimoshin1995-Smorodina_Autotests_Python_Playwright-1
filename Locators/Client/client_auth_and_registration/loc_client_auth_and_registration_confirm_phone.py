# Подтверждение телефона продавца
CLIENT_INPUT_FIRST_NUMBER = '/html/body/div[3]/div/div[2]/div/div/div[1]/input[1]' # Первая цифра
CLIENT_INPUT_FIRST_NUMBER = '/html/body/div[3]/div/div[2]/div/div/div[1]/input[2]' # Вторая цифра
CLIENT_INPUT_FIRST_NUMBER = '/html/body/div[3]/div/div[2]/div/div/div[1]/input[3]' # Третья цифра
CLIENT_INPUT_FIRST_NUMBER = '/html/body/div[3]/div/div[2]/div/div/div[1]/input[4]' # Четвертая цифра
CLIENT_CONFIRM_PHONE_ERROR1 = '/html/body/div[3]/div/div[2]/div/div/div[2]/div/div/div'
# Подтверждение телефона продавца из карточки тура
CLIENT_INPUT_FIRST_NUMBER_TOURCARD = '/html/body/div[2]/div/div[2]/div/div/div[1]/input[1]'
CLIENT_INPUT_FIRST_NUMBER_TOURCARD = '/html/body/div[2]/div/div[2]/div/div/div[1]/input[2]'
CLIENT_INPUT_FIRST_NUMBER_TOURCARD = '/html/body/div[2]/div/div[2]/div/div/div[1]/input[3]' 
CLIENT_INPUT_FIRST_NUMBER_TOURCARD = '/html/body/div[2]/div/div[2]/div/div/div[1]/input[4]' 



LOCATORS_CLIENT_AUTH_AND_REGISTRATION_CONFIRM_PHONE = {
    # Подтверждение телефона продавца
    'Первая цифра у клиента': CLIENT_INPUT_FIRST_NUMBER,
    'Вторая цифра у клиента': CLIENT_INPUT_FIRST_NUMBER, 
    'Третья цифра у клиента': CLIENT_INPUT_FIRST_NUMBER, 
    'Четвертая цифра у клиента': CLIENT_INPUT_FIRST_NUMBER, 
    'Ошибка в Введите код из смс': CLIENT_CONFIRM_PHONE_ERROR1, 
    # Подтверждение телефона продавца из карточки тура
    'Первая цифра у клиента из карточки тура': CLIENT_INPUT_FIRST_NUMBER_TOURCARD,
    'Вторая цифра у клиента из карточки тура': CLIENT_INPUT_FIRST_NUMBER_TOURCARD, 
    'Третья цифра у клиента из карточки тура': CLIENT_INPUT_FIRST_NUMBER_TOURCARD, 
    'Четвертая цифра у клиента из карточки тура': CLIENT_INPUT_FIRST_NUMBER_TOURCARD, 

}