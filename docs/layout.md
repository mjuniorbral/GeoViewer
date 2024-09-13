O problema de o gráfico ficar pequeno quando a legenda é posicionada fora do `Axes` ocorre porque o espaço disponível para o gráfico se reduz ao adicionar a legenda. Uma forma de resolver isso é ajustar o layout da figura para garantir que o gráfico ocupe o máximo de espaço disponível, mantendo a legenda posicionada corretamente.

Aqui estão algumas abordagens para resolver esse problema:

### 1. **Usar `tight_layout()`**

O `tight_layout()` ajusta automaticamente o espaçamento entre os elementos da figura (como o gráfico e a legenda):

```python
plt.tight_layout()
```

Isso ajusta o gráfico e a legenda para evitar sobreposição ou um gráfico excessivamente pequeno.

### 2. **Usar `bbox_inches='tight'` ao Salvar a Imagem**

Se você estiver salvando o gráfico em um arquivo, use a opção `bbox_inches='tight'` no método `savefig`:

```python
plt.savefig('meu_grafico.png', bbox_inches='tight')
```

Isso ajusta automaticamente os espaçamentos e salva a figura sem grandes margens.

### 3. **Ajustar o Tamanho da Figura Manualmente**

Você pode definir um tamanho de figura maior para acomodar a legenda fora do `Axes`. O `figsize` no `plt.figure()` controla o tamanho da figura:

```python
fig, ax = plt.subplots(figsize=(12, 8))  # Ajuste conforme necessário
```

### 4. **Aumentar o Espaço à Direita com `subplots_adjust()`**

Se o problema for a falta de espaço à direita por conta da legenda, você pode ajustar manualmente o espaço:

```python
plt.subplots_adjust(right=0.8)  # Ajuste o valor conforme necessário
```

Isso reserva mais espaço à direita da figura para a legenda, evitando que o gráfico fique pequeno.

### 5. **Usar `constrained_layout` para Melhor Controle**

O `constrained_layout` é uma opção mais avançada que organiza automaticamente os elementos da figura:

```python
plt.figure(constrained_layout=True)
```

Isso ajusta a posição de todos os elementos, incluindo o gráfico e a legenda, para garantir que haja espaço suficiente para ambos.

### Resumo

A melhor solução pode variar de acordo com o layout do seu gráfico. Você pode experimentar combinar:

- Aumentar o `figsize` para dar mais espaço geral.
- Usar `tight_layout()` para ajuste automático.
- Ajustar o espaço à direita com `subplots_adjust()` se necessário.

Essas soluções devem resolver o problema de o gráfico ficar pequeno com a legenda posicionada fora.