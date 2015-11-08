# -*- coding: utf-8 -*-
"""
Feature: Фавикон, заголовок, описание для Главной страницы сайта
"""
import urllib
from support.utils.common_utils import priority
from tests.front_office.authorization.classes.class_front import HelpAuthCheckMethods
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateData
from tests.front_office.not_sorted.classes.class_navigate import HelpNavigateCheckMethods
from support import service_log
from tests.front_office.not_sorted.classes.class_ware_life_cycle import HelpLifeCycleMethods



class TestFaviconMainPage(HelpNavigateCheckMethods, HelpNavigateData, HelpAuthCheckMethods):
    """
    Story: Фавикон, заголовок, описание для Главной страницы сайта
    """
    driver = None

    @classmethod
    def setUp(cls):
        # Подготовка работы с selenium
        cls.driver = HelpLifeCycleMethods.get_driver()
        service_log.preparing_env(cls)
        cls.go_to_main_page(cls.driver)
        cls.source = cls.driver.page_source


    @priority("Must")
    def test_favicon(self):
        """
        Title: В названии вкладки браузера отображается favicon с логотипом УУРРАА
        """
        #href = u"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAI0ElEQVRYR9WXeXBV9RXHP7/77n37" \
        #       u"HhJCwpIYISBLwhaBgA0gKAKChiBbtAqCoRgmoKO4xggVECw2U" \
        #       u"kEopSgFUYKCjjNISZWgBQURJVIWDVt2sr8sb7m3895DR0UNnXHG6f3zzrnnfH7nnO/5nSv4jR/xG8fn/wtgRwa6/k3I" \
        #       u"XisWsEYbbeZeOjxDFXy9dWZjB53QNBV/qV+n/8inKPvsUvVZlwmPyMX/c5luNwPBoL3BoXiUrnrZN9ykY7BB0F3RS11" \
        #       u"kvXAJSTIKWeiQNCQ0kFQ0nRoIyNSpsnzKr+j3S4r8tlnn/kLklrT+GORnAQrTkG0S3SJauclo5m6TQU4zWazo3RHgdo" \
        #       u"E7BtyRYLWD3gwEoMUDNWWolRfQak8j+erAoKIZdT5keY0kG9eJ3Pqvvw/xkwCHUohwQYZNsMDmsvc2J3RH9OkPN9wE1" \
        #       u"w+AqDiQLT88jOYDzYcmCQItjQSKD6IWbUNXvA9F1CIcgoBef1DV2x/UP1X12bcfXwXw8RB9r+gGb67LbZtqTxmKuOVO" \
        #       u"SJ0KFtfPC6bqGBzOh/pisFkgIhH6/h6/bTDNhZsRu/MwN32DzgGq0XTUZ425y7jk7Jmgwx8AHOlDvyg/myPi4/ub5uT" \
        #       u"A5PtBMrav1OrP4B+ZcPEERACNoDpBTN+DiJ1AffGHaOvvw+45i+SS8NpjCmpNN9wd/fBez3cAnw6ka2QzO6P63TDI+O" \
        #       u"QG6D2s/cDftzi6GvY+AuYA6MFfA80pczH/bjWyYqWmaDv6V+djEbWobgctnQak27ILC0IAhWkYY2v4a+fOXWaY8nfBd" \
        #       u"QOvuNZ+nCSoPgM150E2o8X2RhhsYdsTW2B3NlAPNgg0QkPybAxpqzGbHCEd1v9pCvbjBSgWjdYuye8ZjxybGAI4nsxt" \
        #       u"0WbLu5F5L8PoTLh8EQ68g2Y2Q9qdCL0V/D448ia8uQrKi8FsR02djDbpGSRHNOLYOnjnYRBNBKeE2giNg+Yij1yJ2eg" \
        #       u"I1br2g00Yty7GGKgjEN25riJ1zkhRCHLn/rqCuJFjJsqr30OruYRYngWv7SGQaKdl6Tr0qdPRf7obns2AOi9EQfBImg" \
        #       u"faZi1Al/kiyucb4M1s0HvBCAEPNKYuRkl7BrPeEgJoulCMuiodS/1JhMtJ+egn1ooDI51JCV72d8rLd6up6Yj8RxCr8" \
        #       u"qEzBPxQlzkHefErONZmwqtb4XrAeqUyFdDaOQHt6X9h+uYd2J4VSj8y+FqgYexKLMMWYpT1oSq11tfS+uw4bJWHEA4L" \
        #       u"VWmPHhSHR5jzujvdjzs3H5J8qkBZMB4+/gxSQCuBpsFptK18g4i/L0bs2AJdwgGQgh6hzRlLIKcA09e7EbuXQSSgQhs" \
        #       u"Gmu54DXtyOooI93pLYwOteWOxlx5COB2Ujv/jXnF4IHt7JsaPMf3tBJqQkbetQqx4DDoS9ILX2JWGFRuxV3yF/vmFYZ" \
        #       u"kFZ1DQZyO0xSXhz1qPuSgfcXBrGLARPO5utM58G0e3JGRNAyFoqriAb+lEHGWf44/tGiiZ9lKe+ChFvNUnrtsk48Yjq" \
        #       u"DY3SukppOwJ8OVpiAf1okzDPfejy3gA26O3QmkZdLsikjJoGjsT7piHdUsOXDoSBq+Fmn7j0WZswuWIQqgqQpKo/Xw/" \
        #       u"ygv3Yq09T2NSannx9GdGiw9HWB/oa7LkW/68W/YmpmDwtyFtWoq0bCn0DDtrccbR/PIunF8VoXv8wXATKuBrg8Znd2H" \
        #       u"xlmNYnw1OX+i9vxkqJ6/EPi4Hq6RD0zRUSaJqx3M4X1uKUWmhdHTWroORadPEnqERsYO05gORsxfGN815DlOwvP/5BP" \
        #       u"kPk8KnTQDtjMBz+yyk5Rsxb3wS1q7EF4CGhY9hSH8A64oMKD4EcUAdNDg7ULdgD9E9hiD7fEiKQk1rC74nJxFV9D7NN" \
        #       u"w7g7ISHpiSNmbEzWElRnMzq6xLicwJr9+PrGIfR14ayIRcpdzn0BXSgluhoy3oIfc5yxNFCmptbYehozJuWIG17IaSa" \
        #       u"4ATUquFC2iwM89bRwWBGUgN4ZZnKd18h4rlFmC1+zk3O/uDwtCWTprrd9eFJOFDfszfejyJGTXDVLy9ASArmsjMoizI" \
        #       u"Q7x0LKSLY2VoZaFNmw/wlqDYX8pblsHUNOHzQITwEG2UDZYveInborVj8AXyyjooLxZiyJhNRcprKjCmBU7fMTx0xdN" \
        #       u"ShH1xGJwYzq6uPzYbxU3SenBfRImIwlHyBaclcxN5/QyyhAROUHp3iwztA+Ymw7oPKCAJWw+kx0zFkb6Sb3YwPKK+vQ" \
        #       u"pedTsy+A9ROGM6pjAcfHjLmrlVXX8eaJs4li5kxfpaL5AGxLTMW4L9lJlLAh2HbRuQdG9BdOgGecKoJ7iBBOQabRgk3" \
        #       u"a4XFSVleAb1SRob8X6o8h2HRbGLe/yd1tw3j7O33rVh7x+zczUJ8txldtQ/UJTLIFiBbRLnHBfr17OAbNY1A0o3oKku" \
        #       u"RTn2BrrQE6ct9SBXnw4GDA6kJ2qrhZE4uEfOeDiWl+oO3sS57iqiTx6kZO5yz4zKXFabPff5RIerb3Yi0vrioow+Cmw" \
        #       u"ORriFqQsdkLS4+Su3SC0xmTSkqELrTwQspfCdQDcVT5tP81FqiL19C5OfhfH07ikml8ubR5edGpT+x79bMbblCNF/zT" \
        #       u"hg01MJVd/oj6YFDNgW6dUqQzZ7Hdd6mGFRvyIAWOJ84nPJZj9C15CSurS8hKs7R3LMf1Sk3vX582Mg121Pv/OQNIQI/" \
        #       u"tWC0uxV//yNtFFma4EURTL4uvIeqwQq4uyB7ZYxVl2jqEEN1r8GFl/sMXFeZlPr+hH4jan9ps7lmAG2cch8+/xpUzRY" \
        #       u"6+ZUUqYqM32THY42pr++SuLM6vsfOb7p2/6R43L2Xc4UI8v3ic00A2kTrVNXv/YumEaEKxasqJq9fb6ny2lwlHlvH4s" \
        #       u"aY64u87tijfs17cdDcp1sQ4lvE9uK3/2um9UbfOKDHPQ1RCfParO5zXpPj4xaj9ZSmSMU1srPKxdfNA+eu94v/IWi7K" \
        #       u"mgX+1c0uKYS/IrxrnL1X2YZM70WZmRuAAAAAElFTkSuQmCC"
        href_start = self.source.find(u"shortcut icon\" href=\"")
        href_end = self.source.find(u" type=\"image/png\" media=\"all\"")
        href = self.source[href_start+21:href_end-1]
        webFile = urllib.urlopen(href)
        webFile.close()
        self.assertEqual(webFile.headers.dict['content-type'], 'image/png')

    @priority("Must")
    def test_title(self):
        """
        Title: В названии вкладки браузера отображается текст title
        """
        self.assertEqual(self.driver.title,
                         u"Одежда, обувь, детские товары, все для дома и сада оптом на интернет-площадке УУРРАА",
                         "Title не совпадает с заданным в тесте.")

    @priority("Medium")
    def test_description(self):
        """
        Title: В коде главной страницы присутствует description для SEO
        """
        p = u'<meta name="description" content="Оптовая торговля на интернет-площадке УУРРАА. Тысячи товаров, ' \
            u'поставщиков и покупателей на одном сайте. Всегда выгодные условия сделки." />'
        self.assertNotEqual(self.source.find(p), -1, "Description не совпадает с заднным в тесте.")

    @priority("Medium")
    def test_keywords(self):
        """
        Title: В коде главной страницы присутствует keywords для SEO
        """
        self.assertIn(u"<meta name=\"keywords\" content=\"oorraa.com, oorraa, уурраа.com, уурраа, опт, оптовая "
                      u"торговля, оптовые закупки цены продажи поставщики, купить оптом, женская мужская детская "
                      u"одежда детские товары обувь оптом, оптом от производителя, оптом дешевле, "
                      u"оптовый интернет-магазин\" />", self.source, "Keywords не совпадает с заднным в тесте.")

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        service_log.end()