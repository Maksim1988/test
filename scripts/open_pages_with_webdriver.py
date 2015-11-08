from selenium import webdriver
from random import shuffle
from time import sleep
from argparse import ArgumentParser
from sys import argv


def run(host):
    urls = [
        "http://electronics.{0}/ebook/data/17186590/ehlektronnaja_kniga_ehlektronnaja_kniga_texet_tb-721hd_seryjj/",
        "http://electronics.{0}/ebook/data/7738109/ehlektronnaja_kniga_pocketbook_360_plus/",
        "http://electronics.{0}/ebook/data/17666201/ehlektronnaja_kniga_onyx_boox_i62ml_aurora/",
        "http://electronics.{0}/ebook/data/8337770/ehlektronnaja_kniga_pocketbook_pro_912/",
        "http://video.{0}/audio_equipment/mp3/data/613/mp3_pleer_apple_ipod_shuffle_2_2gb/",
        "http://video.{0}/audio_equipment/mp3/data/2083395/mp3_pleer_apple_ipod_touch_5_32gb/",
        "http://electronics.{0}/navigation/gps/data/443361/gps_navigator_garmin_nuvi_1300/",
        "http://electronics.{0}/navigation/gps/data/443361/gps_navigator_garmin_nuvi_1300/",
        "http://electronics.{0}/navigation/gps/data/443345/gps_navigator_garmin_dakota_10/",
        "http://electronics.{0}/communication/cell/data/134745/mobilnyj_telefon_nokia_6700_classic/",
        "http://electronics.{0}/communication/cell/data/806/mobilnyj_telefon_apple_iphone_3gs_16gb/",
        "http://electronics.{0}/communication/cell/data/2065709/mobilnyj_telefon_apple_iphone_4_16gb/",
        "http://electronics.{0}/communication/dect/data/12820/radiotelefon_siemens_gigaset_sl780/",
        "http://electronics.{0}/communication/dect/data/1389502/radiotelefon_panasonic_kx-tg8421/",
        "http://electronics.{0}/communication/dect/data/1389493/radiotelefon_panasonic_kx-tg6461/",
        "http://electronics.{0}/communication/phones/data/800/provodnoj_telefon_panasonic_kx-ts2350/",
        "http://electronics.{0}/communication/phones/data/801/provodnoj_telefon_panasonic_kx-ts2365/",
        "http://electronics.{0}/communication/phones/data/803/provodnoj_telefon_panasonic_kx-ts2570/",
        "http://computers.{0}/computers/tablets/data/3388000/internet_planshet_mireader_m8/",
        "http://appliances.{0}/large/refrigerators/data/43339/holodilnik_smolensk_414/",
        "http://appliances.{0}/large/refrigerators/data/3626/holodilnik_indesit_sb_167/",
        "http://appliances.{0}/large/refrigerators/data/3995/holodilnik_daewoo_fr-061a/",
        "http://appliances.{0}/large/washers/data/22/stiralnaya_mashina_candy_1000_df/",
        "http://appliances.{0}/large/washers/data/3307/stiralnaya_mashina_feya_votkinsk_smpa-3001/",
        "http://appliances.{0}/large/washers/data/3146/stiralnaya_mashina_indesit_wiun_81/",
        "http://appliances.{0}/large/freezers/data/3629/morozilnaya_kamera_indesit_sfr_100/",
        "http://appliances.{0}/large/freezers/data/3629/morozilnaya_kamera_indesit_sfr_100/",
        "http://appliances.{0}/large/cookers/data/386/plita_elektricheskaya_beko_cs_47100/",
        "http://appliances.{0}/large/cookers/data/4506/plita_gazovaya_gefest_gefest_700-02/",
        "http://appliances.{0}/large/cookers/data/39686/plita_gazovaya_gorenje_g_61220_dw/",
        "http://home.{0}/forbathroom/driers/data/145629/sushilka_napolnaya_gimi_napolnaya_dinamik_gimi_20/",
        "http://home.{0}/forbathroom/driers/data/145630/sushilka_napolnaya_gimi_napolnaya_dinamik_30_gimi/",
        "http://home.{0}/forbathroom/driers/data/145628/sushilka_nastennaya_gimi_brio_super_120_gimi/",
        "http://kids.{0}/child_care/cosmetics/nappy/data/139742/podguzniki_moony_4-8_kgs_81_sht/",
        "http://kids.{0}/child_care/cosmetics/nappy/data/2419/trusiki_moony_dlya_malchikov_9-14_kg_54_sht_l/",
        "http://kids.{0}/child_care/cosmetics/nappy/data/13006/podguzniki_moony_m_6-11_kg_4_upakovki_po_62_sht/",
        "http://kids.{0}/feeding_nutrition/nutrition/mix/data/16188807/detskaja_sukhaja_smes_vitacare_nehnni_1_s_prebiotikami_s_rozhdenija_400_gr_s_0_mes/?p=1",
        "http://kids.{0}/child_care/accessories/scale/data/20782/vesy_ya_rastu_detskie_elektronnye_md-6141/",
        "http://kids.{0}/child_care/accessories/scale/data/20791/vesy_momert_7474_mehanicheskie/",
        "http://kids.{0}/child_care/accessories/scale/data/20778/vesy_ya_rastu_bf_20510/",
        "http://kids.{0}/child_care/accessories/bath/data/15516/aksessuar_cam_podstavka_pod_vannochku_universalnaya_stand_universale/",
        "http://kids.{0}/child_care/accessories/bath/data/15618/pelenatelnyj_stolik_s_vannoj_cam_nuvola/",
        "http://kids.{0}/child_care/accessories/bath/data/15501/vanna_cam_baby_bagno/",
        "http://home.{0}/furniture/wardrobes/data/8887658/shkaf-kupe_mega-ehlaton_afina_3d-2/",
        "http://home.{0}/furniture/wardrobes/data/11949967/shkaf-kupe__dlja_knig_107/",
        "http://home.{0}/furniture/wardrobes/data/11735665/shkaf-kupe_ehkonom_ronikon_ehkonom_1/",
        "http://home.{0}/interior/candles_candleholders/data/16381147/svechi_i_podsvechniki_660428_podsvechnik_quotangelochkiquot_121122smquot/",
        "http://home.{0}/interior/candles_candleholders/data/8634811/svechi_i_podsvechniki_leonardo_podsvechniki_quad_v_assortimente/",
        "http://home.{0}/interior/candles_candleholders/data/8634823/svechi_i_podsvechniki_leonardo_podsvechniki_highlight/",
        "http://home.{0}/chandeliers/chandelier/data/970442/svetilniki_seriya_svetilnikov_naomi_ii_artikul_model_-_cl309193/",
        "http://home.{0}/chandeliers/chandelier/data/970456/svetilniki_seriya_svetilnikov_saga_i_artikul_model_-_cl212145/",
        "http://home.{0}/chandeliers/chandelier/data/970425/svetilniki_seriya_svetilnikov_gala_i_artikul_model_-_cl306192/",
        "http://garments.{0}/to_women/womens_clothing/breeches/suit/data/28119845/prjamye_brjuki_natura_natura_na001ewcq394/",
        "http://garments.{0}/to_women/womens_clothing/breeches/suit/data/28722779/kostjumnye_brjuki_otto_otto_brjuki_stretch/",
        "http://garments.{0}/to_women/womens_clothing/breeches/suit/data/27775005/zhenskie_kostjumnye_brjuki_otto_brjuki_stretch/",
        "http://garments.{0}/to_women/womens_clothing/jumpers_and_cardigans/polo_necks/data/28122416/dzhempery_mondigo_mondigo_mondigo_mo007ewei248/",
        "http://garments.{0}/to_women/womens_shoes/shoes/data/28095424/tufli_arzomania_arzomania_arzomania_ar204awed976/",
        "http://garments.{0}/to_women/womens_shoes/sandals/data/27449680/bosonozhki_francesco_donni_bosonozhki/",
        "http://garments.{0}/to_women/womens_shoes/rain_boots/data/26005586/rezinovye_sapogi_keddo_botinki_keddo_318513_017_bezhevyjj/",
        "http://garments.{0}/to_women/womens_clothing/dresses/the_knitted/data/28719478/vjazanye_platja_melrose_plate/",
        "http://garments.{0}/to_women/womens_clothing/dresses/the_knitted/data/29026942/vjazanye_platja_heine_plate-vodolazka/",
        "http://garments.{0}/to_women/womens_clothing/dresses/the_knitted/data/28680663/vjazanye_platja_melrose_melrose_trikotazhnoe_plate_melrose/",
        "http://garments.{0}/to_women/womens_clothing/dresses/evening_dress/data/29030358/pljazhnoe_poncho_sareo_plate_sareo_long_quotzolotaja_savannaquot/",
        "http://auto.{0}/sneakers/data/6161179/shina_michelin_agilis_alpin_225_65_r16_s_112_110r/?p=1",
        "http://auto.{0}/sneakers/data/3681631/shina_cordiant_comfort_205_60_r16/?p=1",
        "http://auto.{0}/sneakers/data/1314434/shina_dunlop_lm703_215_60r16_95h/?p=1",
        "http://auto.{0}/sneakers/data/28499260/shina_continental_continental_sportcontact_2_205_55r16_94v/?p=1",
        "http://garments.{0}/to_women/womens_clothing/underclothes/bathing_suits/trinkini/data/31979528/trinkini_loragrig_loragrig_kupalnik_trikini_015040028/",
        "http://garments.{0}/to_women/womens_clothing/underclothes/bathing_suits/tankini/data/31203870/bikini_relax_mode_kupalnik_relax_mode_70122_siyah___chernyjj/",
        "http://garments.{0}/to_women/womens_clothing/underclothes/bathing_suits/trinkini/data/31979573/trinkini_loragrig_loragrig_kupalnik-trikini_015040055/",
        "http://garments.{0}/to_women/womens_clothing/underclothes/bathing_suits/trinkini/data/32268100/trinkini_beach_bunny_beach_bunny_kupalnik_beach_bunny_fs-1102-1p/"
    ]

    shuffle(urls)

    for url in urls:
        driver = webdriver.Firefox()
        driver.get(url.format(host))
        sleep(10)
        driver.close()

if __name__ == "__main__":
    parser = ArgumentParser(description='Open list of urls with WebDriver')
    parser.add_argument('--host', required=True, nargs=1, dest='host', type=str, help='base host. Example: wikimart.ru')
    res = parser.parse_args(argv[1:])
    run(res.host[0])
