class CarrinhoDeCompras:
    def __init__(self):
        self.itens = []
        self.cupom = None

    def adicionar_item(self, nome: str, preco: float):
        if preco <= 0:
            raise ValueError("O preço do item deve ser maior que zero.")
        self.itens.append({"nome": nome, "preco": preco})

    def aplicar_cupom(self, cupom: str):
        self.cupom = cupom

    def calcular_total_produtos(self) -> float:
        return sum(item["preco"] for item in self.itens)

    def calcular_desconto(self, cupom: str = None) -> float:
        total = self.calcular_total_produtos()
        cupom_ativo = cupom if cupom is not None else self.cupom

        # Nova regra: Cupom "OFF50" dá 50% de desconto se valor bruto > R$ 600,00
        if cupom_ativo == "OFF50" and total > 600.00:
            return total * 0.50

        # Regra padrão legada (mantida para não quebrar o código existente!)
        if total >= 500:
            return total * 0.20
        elif total >= 100:
            return total * 0.10
        return 0.0

    def calcular_frete(self, cupom: str = None) -> float:
        total = self.calcular_total_produtos()
        if total == 0:
            return 0.0

        # Nova regra de frete: baseada no valor final pós-desconto (< R$ 150,00 -> R$ 15,00)
        valor_pos_desconto = total - self.calcular_desconto(cupom)
        if valor_pos_desconto < 150.00:
            return 15.00
        return 0.0

    def calcular_total_final(self, cupom: str = None) -> float:
        if not self.itens:
            raise ValueError("O carrinho está vazio.")
        desconto = self.calcular_desconto(cupom)
        frete = self.calcular_frete(cupom)
        return (self.calcular_total_produtos() - desconto) + frete