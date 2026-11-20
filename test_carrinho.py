import unittest
from carrinho import CarrinhoDeCompras


class TestQualidade(unittest.TestCase):
    def setUp(self):
        """Inicializa um carrinho limpo antes de cada teste."""
        self.carrinho = CarrinhoDeCompras()

    # ==========================================================================
    # TESTES LEGADOS (DO PROJETO ORIGINAL - REGRESSÃO)
    # ==========================================================================

    def test_compra_sem_desconto_com_frete(self):
        """Compra abaixo de R$ 100,00 (Sem desconto + Frete R$ 15,00)."""
        self.carrinho.adicionar_item("Caderno", 50.00)
        self.assertEqual(self.carrinho.calcular_total_produtos(), 50.00)
        self.assertEqual(self.carrinho.calcular_desconto(), 0.00)
        self.assertEqual(self.carrinho.calcular_frete(), 15.00)
        self.assertEqual(self.carrinho.calcular_total_final(), 65.00)

    def test_compra_com_desconto_20_porcento_e_frete_gratis(self):
        """Compra acima de R$ 500,00 sem cupom (Desconto 20% + Frete Grátis)."""
        self.carrinho.adicionar_item("Monitor", 600.00)
        self.assertEqual(self.carrinho.calcular_total_produtos(), 600.00)
        self.assertEqual(self.carrinho.calcular_desconto(), 120.00)
        self.assertEqual(self.carrinho.calcular_frete(), 0.00)
        self.assertEqual(self.carrinho.calcular_total_final(), 480.00)

    def test_erro_preco_zero(self):
        """Garante lançamento de ValueError para item com valor 0."""
        with self.assertRaises(ValueError):
            self.carrinho.adicionar_item("Produto Grátis", 0.0)

    def test_erro_checkout_carrinho_vazio(self):
        """Garante lançamento de ValueError ao calcular checkout em carrinho vazio."""
        with self.assertRaises(ValueError):
            self.carrinho.calcular_total_final()

    # ==========================================================================
    # NOVOS TESTES (ATIVIDADE AULA 06 - FRETE E CUPOM OFF50)
    # ==========================================================================

    def test_cenario_frete(self):
        """Compra de R$ 100,00 -> R$ 90,00 (10% desc) + R$ 15,00 (frete) = R$ 105,00."""
        self.carrinho.adicionar_item("Teclado", 100.00)
        self.assertEqual(self.carrinho.calcular_total_final(), 105.00)

    def test_cenario_cupom_valido(self):
        """Compra de R$ 800,00 com cupom 'OFF50' -> R$ 400,00 (50% desc + frete grátis)."""
        self.carrinho.adicionar_item("Notebook", 800.00)
        self.assertEqual(self.carrinho.calcular_total_final(cupom="OFF50"), 400.00)

    def test_cenario_cupom_invalido(self):
        """Compra de R$ 200,00 com cupom 'OFF50' -> ignora cupom e aplica 10% = R$ 180,00."""
        self.carrinho.adicionar_item("Mouse Gamer", 200.00)
        self.assertEqual(self.carrinho.calcular_total_final(cupom="OFF50"), 180.00)


if __name__ == "__main__":
    unittest.main()