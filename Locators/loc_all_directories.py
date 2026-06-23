from Locators.Seller.seller_auth.loc_seller_auth import LOCATORS_SELLER_AUTH
from Locators.Seller.seller_registration.loc_seller_registration import LOCATORS_SELLER_REGISTRATION
from Locators.Seller.seller_registration_confirm_phone.loc_seller_registration_confirm_phone import LOCATORS_SELLER_REGISTRATION_CONFIRM_PHONE
from Locators.locator_main_page import LOCATOR_MAIN_PAGE
from Locators.Seller.loc_seller_mainmenu import LOCATORS_SELLER_MAINPAGE
from Locators.Seller.seller_settings.seller_company_data.loc_seller_company_data import LOC_SELLER_COMPANY_DATA
from Locators.Client.client_auth_and_registration.loc_client_auth_and_registration import LOCATORS_SELLER_AURH_AND_REGISTRATION
from Locators.Client.client_auth_and_registration.loc_client_auth_and_registration_confirm_phone import LOCATORS_CLIENT_AUTH_AND_REGISTRATION_CONFIRM_PHONE
from Locators.Seller.seller_tours.loc_seller_tours import LOCATORS_SELLER_TOURS
from Locators.Seller.seller_tours.seller_tour_card.loc_seller_tour_card import LOCATORS_SELLER_TOUR_CARD
from Locators.Seller.seller_tours.seller_tour_card.seller_tour_parametrs.loc_seller_tour_parametrs import LOCATORS_SELLER_TOUR_CREATE_UPDATE
from Locators.Seller.seller_tours.seller_tour_card.seller_tour_parametrs.seller_tour_waypoints.loc_seller_tour_waypoints import LOCATORS_SELLER_TOUR_CREATE_WAYPOINTS
from Locators.Client.client_basket.loc_client_basket import LOCATORS_CLIENT_BASKET
from Locators.Client.client_tour_card.loc_client_tour_card import LOCATORS_CLIENT_TOUR_CARD
from Locators.Seller.seller_profile.loc_seller_profile import LOCATORS_SELLER_PROFILE
from Locators.Seller.seller_summary.loc_seller_symmary import LOC_SELLER_SUMMARY


ALL_LOCATORS = {
    **LOCATORS_SELLER_AUTH,
    **LOCATORS_SELLER_REGISTRATION,
    **LOCATORS_SELLER_REGISTRATION_CONFIRM_PHONE,
    **LOCATOR_MAIN_PAGE,
    **LOCATORS_SELLER_MAINPAGE,
    **LOC_SELLER_COMPANY_DATA,
    **LOCATORS_SELLER_AURH_AND_REGISTRATION,
    **LOCATORS_CLIENT_AUTH_AND_REGISTRATION_CONFIRM_PHONE,
    **LOCATORS_SELLER_TOURS,
    **LOCATORS_SELLER_TOUR_CARD,
    **LOCATORS_SELLER_TOUR_CREATE_UPDATE,
    **LOCATORS_SELLER_TOUR_CREATE_WAYPOINTS,
    **LOCATORS_CLIENT_BASKET,
    **LOCATORS_CLIENT_TOUR_CARD,
    **LOCATORS_SELLER_PROFILE,
    **LOC_SELLER_SUMMARY

}

