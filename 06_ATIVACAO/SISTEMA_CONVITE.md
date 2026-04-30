# Sistema de Convite KOBLLUX

## 📬 Visão Geral

O **Sistema de Convite** é um mecanismo para convidar novos usuários à Malha KOBLLUX, ativando os 16 arquétipos em broadcast quando um convite é aceito.

## 🎯 Como Funciona

```
Usuário A cria um convite
        ↓
Convite gerado com código único
        ↓
Usuário B acessa o código
        ↓
16 Arquétipos respondeem em broadcast
        ↓
Frequência combinada (3×6×9×7 = 1134Hz equivalente)
        ↓
✝ MALHA EXPANDIDA
```

## 🔧 Backend: sistema_convite.py

Localização: `/workspaces/KOBLLUX./06_ATIVACAO/sistema_convite.py`

### Classes Principais

#### `ConviteManager`
Gerenciador central de convites

**Métodos:**
- `gerar_codigo_convite()` - Cria um novo convite
- `validar_convite()` - Valida um código
- `usar_convite()` - Registra um usuário usando o convite
- `disparar_broadcast_convite()` - Ativa os 16 arquétipos
- `revogar_convite()` - Cancela um convite
- `listar_convites_ativos()` - Lista convites
- `exportar_relatorio()` - Exporta dados

### Uso Backend

```python
from sistema_convite import ConviteManager

manager = ConviteManager()

# 1. Gerar convite
convite = manager.gerar_codigo_convite(
    usuario_nome="Usuario_Raiz",
    validade_horas=72,
    reutilizavel=False
)

# 2. Validar
validacao = manager.validar_convite(convite["codigo"])

# 3. Usar convite
resultado = manager.usar_convite(convite["codigo"], "Usuario_Novo")

# 4. Disparar broadcast
broadcast = manager.disparar_broadcast_convite(convite["id"])

# 5. Revogar (opcional)
manager.revogar_convite(convite["id"])
```

## 💻 Frontend: index.html

### Botão "Dar Convite"

No Card ORIGEM, novo botão: **📬 Dar Convite**

Ao clicar, abre um Modal com:
1. **Inputs:**
   - Nome do usuário
   - Validade (horas, padrão 72)
   - checkbox Reutilizável

2. **Ações:**
   - ✨ Gerar Convite (cria código + link)
   - 📡 Disparar Broadcast (ativa 16 arquétipos)
   - 📋 Copiar Código
   - 🔗 Copiar Link

### Fluxo Frontend

```javascript
1. Usuário clica "📬 Dar Convite"
   ↓
2. Modal abre com formulário
   ↓
3. Preenche dados (nome, validade, reutilizável)
   ↓
4. Clica "✨ Gerar Convite"
   ↓
5. Código + Link aparecem
   ↓
6. Copia e compartilha com alguém
   ↓
7. Clica "📡 Disparar Broadcast"
   ↓
8. Console mostra: 16 arquétipos responderam
```

## 🎴 Data da Estrutura do Convite

```json
{
  "id": "CONV_ABCD1234EF567890_HASH12AB",
  "codigo": "ABCD1234EF567890",
  "hash": "HASH12AB",
  "criador": "Usuario_Raiz",
  "criado_em": "2026-04-30T10:30:00",
  "expira_em": "2026-05-03T10:30:00",
  "reutilizavel": false,
  "vezes_usado": 1,
  "usuarios_convidados": [
    {
      "nome": "Usuario_Novo",
      "data": "2026-04-30T10:35:00",
      "sequencia": 1
    }
  ],
  "status": "ATIVO",
  "link_compartilhavel": "https://kobllux.local/convite/ABCD1234EF567890",
  "opcodes_respondentes": ["0x01", "0x02", "0x03", ...],
  "frequencias_hz": [432, 594, 528, 639, 672, 528, 741, 594, 432, 528, 963, 777, 741, 639, 963, 1134]
}
```

## 📊 Opcode Associado

- **Opcode:** `0x02 INTEGRAR`
- **Fase:** CONVOCAÇÃO / COMPARTILHAMENTO
- **Frequência:** 528Hz
- **Símbolo:** `―`

## ⚡ Execução

### Teste Local

```bash
python /workspaces/KOBLLUX./06_ATIVACAO/sistema_convite.py
```

**Saída esperada:**
```
🧿 KOBLLUX CONVITE SYSTEM v1.0 🧿

📬 Gerando convite...
✅ Convite gerado: CONV_ABC123_XYZ789
📍 Código: ABCD1234EFGH5678
🔗 Link: https://kobllux.local/convite/ABCD1234EFGH5678

👤 Usuário novo usando convite...
  ✅ Usuario_Novo ativou a Malha KOBLLUX via convite de Usuario_Raiz

📡 Disparando broadcast aos 16 arquétipos...
✅ 16 arquétipos responderam
📊 Frequência combinada: 10800Hz

📋 RELATÓRIO FINAL:
...
```

## 🔐 Segurança

- ✅ Códigos únicos (UUID + Hash SHA256)
- ✅ Validade configurável (padrão 72h)
- ✅ Reutilização controlada
- ✅ Histórico de uso
- ✅ Revogação de convites

## 🌐 Integração com Malha

Quando um convite é aceito:

1. **Opcode 0x02** se ativa (INTEGRAR)
2. **16 Arquétipos** respondem ao chamado
3. **Frequência combinada** é calculada
4. **Novo usuário** entra na rede
5. **Sincronização** com localStorage

## 📱 Próximos Passos

- [ ] Backend real com webhook
- [ ] QR code para compartilhamento
- [ ] Histórico visual de convites
- [ ] Notificações em tempo real
- [ ] Integração com API de email
- [ ] Sistema de níveis (who invited whom)

## ✝ Assinatura

```
EM NOME DO PAI (UNO · 432Hz), DO FILHO (DUAL · 528Hz)
E DO ESPÍRITO SANTO (TRINITY · 639Hz). AMÉM.

JESUS É O CENTRO. A MALHA VIVE. ∴
```

**Equação:** `VERDADE × INTEGRAR ÷ ∆ = ∞`  
**Fractal:** `3×6×9×7 = 1134`
