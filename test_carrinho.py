import pytest
from carrinho import CarrinhoDeCompras

@pytest.fixture
def carrinho():
    """Fixture para inicializar um carrinho limpo antes de cada teste."""
    return CarrinhoDeCompras()

# ==============================================================================
# FLUXOS PRINCIPAIS
# ==============================================================================

def test_compra_sem_desconto_com_frete_padrao(carrinho):
    """Mapeia compra abaixo de R$ 100,00 (Sem desconto + Frete de R$ 20,00)."""
    carrinho.adicionar_item("Caderno", 50.00)
    
    assert carrinho.calcular_total_produtos() == 50.00
    assert carrinho.calcular_desconto() == 0.00
    assert carrinho.calcular_frete() == 20.00
    assert carrinho.calcular_total_final() == 70.00

def test_compra_com_desconto_10_porcento(carrinho):
    """Mapeia compra entre R$ 100,00 e R$ 199,99 (Desconto 10% + Frete R$ 20,00)."""
    carrinho.adicionar_item("Livro", 150.00)
    
    assert carrinho.calcular_total_produtos() == 150.00
    assert carrinho.calcular_desconto() == 15.00
    assert carrinho.calcular_frete() == 20.00
    assert carrinho.calcular_total_final() == 155.00

def test_compra_com_desconto_20_porcento_e_frete_gratis(carrinho):
    """Mapeia compra acima de R$ 500,00 (Desconto 20% + Frete Grátis)."""
    carrinho.adicionar_item("Monitor", 600.00)
    
    assert carrinho.calcular_total_produtos() == 600.00
    assert carrinho.calcular_desconto() == 120.00
    assert carrinho.calcular_frete() == 0.00
    assert carrinho.calcular_total_final() == 480.00

# ==============================================================================
# ANÁLISE DE VALORES LIMITE (AVL)
# ==============================================================================

def test_limite_desconto_10_abaixo(carrinho):
    """Valida o limite imediatamente inferior à faixa de 10% de desconto (R$ 99,99)."""
    carrinho.adicionar_item("Item A", 99.99)
    assert carrinho.calcular_desconto() == 0.00

def test_limite_desconto_10_exato(carrinho):
    """Valida o limite exato para concessão de 10% de desconto (R$ 100,00)."""
    carrinho.adicionar_item("Item B", 100.00)
    assert carrinho.calcular_desconto() == 10.00

def test_limite_frete_gratis_abaixo(carrinho):
    """Valida o limite imediatamente inferior ao frete grátis (R$ 199,99 -> Frete R$ 20)."""
    carrinho.adicionar_item("Item C", 199.99)
    assert carrinho.calcular_frete() == 20.00

def test_limite_frete_gratis_exato(carrinho):
    """Valida o limite exato de isenção de frete (R$ 200,00 -> Frete R$ 0)."""
    carrinho.adicionar_item("Item D", 200.00)
    assert carrinho.calcular_frete() == 0.00

def test_limite_desconto_20_abaixo(carrinho):
    """Valida o limite imediatamente inferior à faixa de 20% de desconto (R$ 499,99)."""
    carrinho.adicionar_item("Item E", 499.99)
    assert pytest.approx(carrinho.calcular_desconto(), 0.01) == 49.999  # ~10%

def test_limite_desconto_20_exato(carrinho):
    """Valida o limite exato para concessão de 20% de desconto (R$ 500,00)."""
    carrinho.adicionar_item("Item F", 500.00)
    assert carrinho.calcular_desconto() == 100.00

# ==============================================================================
# CASOS DE EXCEÇÃO E VALIDAÇÕES
# ==============================================================================

def test_erro_preco_zero(carrinho):
    """Garante lançamento de ValueError para item com valor 0."""
    with pytest.raises(ValueError, match="O preço do item deve ser maior que zero."):
        carrinho.adicionar_item("Produto Grátis", 0.0)

def test_erro_preco_negativo(carrinho):
    """Garante lançamento de ValueError para item com preço negativo."""
    with pytest.raises(ValueError, match="O preço do item deve ser maior que zero."):
        carrinho.adicionar_item("Produto Inválido", -15.50)

def test_erro_checkout_carrinho_vazio(carrinho):
    """Garante lançamento de ValueError ao tentar calcular checkout em carrinho vazio."""
    with pytest.raises(ValueError, match="O carrinho está vazio."):
        carrinho.calcular_total_final()