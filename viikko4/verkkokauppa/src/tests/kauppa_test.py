import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote


class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.varasto_mock = Mock()
        self.viitegeneraattori_mock.uusi.return_value = 42

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 3
            if tuote_id == 3:
                return 0

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "Leipä", 10)
            if tuote_id == 3:
                return Tuote(3, "Eioo", 50)

        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock,
                             self.viitegeneraattori_mock)

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called()

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan_oikeilla_parametreilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 5)

    def test_kahden_eri_tuotteen_ostoksen_jalkeen_pankin_metodia_tilisiirto_kutsutaan_oikeilla_parametreilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("kalle", "54321")
        self.pankki_mock.tilisiirto.assert_called_with(
            "kalle", 42, "54321", "33333-44455", 15)

    def test_kahden_saman_tuotteen_ostoksen_jalkeen_pankin_metodia_tilisiirto_kutsutaan_oikeilla_parametreilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("kalle", "54321")
        self.pankki_mock.tilisiirto.assert_called_with(
            "kalle", 42, "54321", "33333-44455", 20)

    def test_loppuneen_tuotteen_ostoksen_jalkeen_pankin_metodia_tilisiirto_kutsutaan_oikeilla_parametreilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("kalle", "54321")
        self.pankki_mock.tilisiirto.assert_called_with(
            "kalle", 42, "54321", "33333-44455", 10)

    def test_aloita_asiointi_nollaa_edellisen_ostoksen_tiedot(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)

        self.kauppa.tilimaksu("ville", "11111")
        self.pankki_mock.tilisiirto.assert_called_with(
            ANY, ANY, ANY, ANY, 5)

    def test_kauppa_pyytää_uuden_viitenumeron_maksutapahtumalle(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("ville", "11111")
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 1)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("ville", "11111")
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 2)

    def test_kauppa_poista_korista_metodi_poistaa_tuotteen_korista_ja_palauttaa_varastoon(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.poista_korista(2)
        # saldon pitäisi olla nyt 3 ja tuotteen palautettu varastoon

        self.kauppa.tilimaksu("ville", "11111")
        self.pankki_mock.tilisiirto.assert_called_with(
            ANY, ANY, ANY, ANY, 0)

        self.kauppa.lisaa_koriin(2)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.lisaa_koriin(2)

        self.kauppa.tilimaksu("ville", "11111")
        self.pankki_mock.tilisiirto.assert_called_with(
            ANY, ANY, ANY, ANY, 30)
