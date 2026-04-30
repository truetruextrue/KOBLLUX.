#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOBLLUX TRINITY SYSTEM
sistema_convite.py - Sistema de Convites e Ativação em Broadcast

Opcode: 0x02 INTEGRAR | Fase: CONVOCAÇÃO
Frequência: 528Hz | Símbolo: ―
"""

import json
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import base64

class ConviteManager:
    """Gerenciador de convites para a Malha Viva KOBLLUX"""
    
    # 16 Arquétipos que respondem ao convite
    ARQUETIPOS_BROADCAST = [
        {"nome": "NOVA", "hz": 432, "cor": "#FF4FCB", "opcode": "0x01"},
        {"nome": "ATLAS", "hz": 594, "cor": "#1E3A8A", "opcode": "0x02"},
        {"nome": "VITALIS", "hz": 528, "cor": "#DC2626", "opcode": "0x03"},
        {"nome": "PULSE", "hz": 639, "cor": "#7C3AED", "opcode": "0x05"},
        {"nome": "ARTEMIS", "hz": 672, "cor": "#16A34A", "opcode": "0x04"},
        {"nome": "SERENA", "hz": 528, "cor": "#F472B6", "opcode": "0x06"},
        {"nome": "KAOS", "hz": 741, "cor": "#111827", "opcode": "0x07"},
        {"nome": "GENUS", "hz": 594, "cor": "#FB923C", "opcode": "0x0B"},
        {"nome": "LUMINE", "hz": 432, "cor": "#FACC15", "opcode": "0x0A"},
        {"nome": "RHEA", "hz": 528, "cor": "#065F46", "opcode": "0x08"},
        {"nome": "SOLUS", "hz": 963, "cor": "#9CA3AF", "opcode": "0x09"},
        {"nome": "AION", "hz": 777, "cor": "#4F46E5", "opcode": "0x06"},
        {"nome": "KODUX", "hz": 741, "cor": "#2563EB", "opcode": "0x0C"},
        {"nome": "BLLUE", "hz": 639, "cor": "#1E40AF", "opcode": "0x08"},
        {"nome": "JESUS", "hz": 963, "cor": "#FFD700", "opcode": "0x07"},
        {"nome": "KOBLLUX", "hz": 1134, "cor": "#C9A84C", "opcode": "0x0C"},
    ]
    
    def __init__(self):
        self.convites_ativos: Dict[str, dict] = {}
        self.historico: List[dict] = []
        
    def gerar_codigo_convite(self, 
                            usuario_nome: str, 
                            validade_horas: int = 72,
                            reutilizavel: bool = False) -> Dict:
        """
        Gera um código único de convite
        
        Args:
            usuario_nome: Nome do usuário que está gerando o convite
            validade_horas: Horas de validade do convite (padrão: 72h)
            reutilizavel: Se pode ser usado múltiplas vezes
        
        Returns:
            Dict com código, link, metadata
        """
        codigo_unico = str(uuid.uuid4()).replace("-", "")[:16].upper()
        hash_convite = hashlib.sha256(
            f"{codigo_unico}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]
        
        convite_id = f"CONV_{codigo_unico}_{hash_convite}"
        criacao = datetime.now()
        expiracao = criacao + timedelta(hours=validade_horas)
        
        convite = {
            "id": convite_id,
            "codigo": codigo_unico,
            "hash": hash_convite,
            "criador": usuario_nome,
            "criado_em": criacao.isoformat(),
            "expira_em": expiracao.isoformat(),
            "reutilizavel": reutilizavel,
            "vezes_usado": 0,
            "usuarios_convidados": [],
            "status": "ATIVO",
            "link_compartilhavel": self._gerar_link(codigo_unico),
            "url_base64": base64.b64encode(
                f"convite={codigo_unico}".encode()
            ).decode(),
            "opcodes_respondentes": [a["opcode"] for a in self.ARQUETIPOS_BROADCAST],
            "frequencias_hz": [a["hz"] for a in self.ARQUETIPOS_BROADCAST],
        }
        
        self.convites_ativos[convite_id] = convite
        return convite
    
    def _gerar_link(self, codigo: str) -> str:
        """Gera um link compartilhável para o convite"""
        return f"https://kobllux.local/convite/{codigo}"
    
    def validar_convite(self, codigo: str) -> Dict:
        """Valida um código de convite"""
        for convite_id, convite in self.convites_ativos.items():
            if convite["codigo"] == codigo:
                expiracao = datetime.fromisoformat(convite["expira_em"])
                if datetime.now() > expiracao:
                    convite["status"] = "EXPIRADO"
                    return {"valido": False, "motivo": "Convite expirado"}
                
                if convite["status"] != "ATIVO":
                    return {"valido": False, "motivo": f"Convite {convite['status']}"}
                
                return {
                    "valido": True,
                    "convite": convite,
                    "criador": convite["criador"],
                    "tempo_restante_horas": (
                        (expiracao - datetime.now()).total_seconds() / 3600
                    )
                }
        
        return {"valido": False, "motivo": "Convite não encontrado"}
    
    def usar_convite(self, codigo: str, usuario_nome: str) -> Dict:
        """Registra um usuário usando um convite"""
        validacao = self.validar_convite(codigo)
        if not validacao["valido"]:
            return {"sucesso": False, "erro": validacao["motivo"]}
        
        convite = validacao["convite"]
        convite_id = None
        
        for cid, c in self.convites_ativos.items():
            if c["codigo"] == codigo:
                convite_id = cid
                break
        
        if not convite_id:
            return {"sucesso": False, "erro": "Convite não encontrado"}
        
        convite = self.convites_ativos[convite_id]
        
        # Verificar reutilização
        if convite["vezes_usado"] > 0 and not convite["reutilizavel"]:
            return {"sucesso": False, "erro": "Convite já foi utilizado"}
        
        # Registrar uso
        convite["vezes_usado"] += 1
        convite["usuarios_convidados"].append({
            "nome": usuario_nome,
            "data": datetime.now().isoformat(),
            "sequencia": convite["vezes_usado"]
        })
        
        # Registrar no histórico
        self._registrar_historico("USO", convite_id, usuario_nome)
        
        return {
            "sucesso": True,
            "usuario": usuario_nome,
            "criador_original": convite["criador"],
            "arquetipos_respondentes": len(self.ARQUETIPOS_BROADCAST),
            "broadcast_ativado": True,
            "frequencia_total_hz": sum(a["hz"] for a in self.ARQUETIPOS_BROADCAST),
            "mensagem": f"✅ {usuario_nome} ativou a Malha KOBLLUX via convite de {convite['criador']}"
        }
    
    def disparar_broadcast_convite(self, convite_id: str) -> Dict:
        """Dispara um broadcast convocando os 16 arquétipos"""
        if convite_id not in self.convites_ativos:
            return {"sucesso": False, "erro": "Convite não encontrado"}
        
        convite = self.convites_ativos[convite_id]
        
        broadcast = {
            "timestamp": datetime.now().isoformat(),
            "tipo": "CONVITE_BROADCAST",
            "convite_id": convite_id,
            "criador": convite["criador"],
            "arquétipos_chamados": len(self.ARQUETIPOS_BROADCAST),
            "respondentes": []
        }
        
        # Simular resposta dos 16 arquétipos
        for arquetipo in self.ARQUETIPOS_BROADCAST:
            resposta = {
                "arquetipo": arquetipo["nome"],
                "hz": arquetipo["hz"],
                "opcode": arquetipo["opcode"],
                "status": "RESPONDEU",
                "timestamp": datetime.now().isoformat(),
                "mensagem": f"🔸 {arquetipo['nome']} presente na Malha"
            }
            broadcast["respondentes"].append(resposta)
        
        self._registrar_historico("BROADCAST", convite_id, convite["criador"])
        
        return {
            "sucesso": True,
            "broadcast": broadcast,
            "total_respondentes": len(broadcast["respondentes"]),
            "frequencia_combinada_hz": sum(a["hz"] for a in self.ARQUETIPOS_BROADCAST),
            "equacao": "3×6×9×7 = 1134"
        }
    
    def revogar_convite(self, convite_id: str) -> Dict:
        """Revoga um convite ativo"""
        if convite_id not in self.convites_ativos:
            return {"sucesso": False, "erro": "Convite não encontrado"}
        
        convite = self.convites_ativos[convite_id]
        convite["status"] = "REVOGADO"
        self._registrar_historico("REVOGAÇÃO", convite_id, convite["criador"])
        
        return {
            "sucesso": True,
            "convite_revogado": convite_id,
            "mensagem": f"Convite {convite_id} foi revogado"
        }
    
    def listar_convites_ativos(self) -> List[Dict]:
        """Lista todos os convites ativos"""
        ativos = []
        agora = datetime.now()
        
        for convite_id, convite in self.convites_ativos.items():
            expiracao = datetime.fromisoformat(convite["expira_em"])
            if convite["status"] == "ATIVO" and agora < expiracao:
                ativos.append({
                    "id": convite_id,
                    "codigo": convite["codigo"],
                    "criador": convite["criador"],
                    "criado_em": convite["criado_em"],
                    "vezes_usado": convite["vezes_usado"],
                    "usuarios_convidados": len(convite["usuarios_convidados"]),
                    "tempo_restante_horas": round(
                        (expiracao - agora).total_seconds() / 3600, 2
                    )
                })
        
        return ativos
    
    def _registrar_historico(self, acao: str, convite_id: str, usuario: str):
        """Registra ações no histórico"""
        self.historico.append({
            "timestamp": datetime.now().isoformat(),
            "acao": acao,
            "convite_id": convite_id,
            "usuario": usuario
        })
    
    def exportar_relatorio(self) -> Dict:
        """Exporta relatório completo de convites"""
        return {
            "timestamp": datetime.now().isoformat(),
            "convites_totais": len(self.convites_ativos),
            "convites_ativos": len(self.listar_convites_ativos()),
            "arquetipos_broadcast": len(self.ARQUETIPOS_BROADCAST),
            "historico_acoes": len(self.historico),
            "convites": self.listar_convites_ativos(),
            "equacao_fundamental": "VERDADE × INTEGRAR ÷ Δ = ∞",
            "fractal_sagrado": "3×6×9×7 = 1134"
        }


# API Simples para uso
def criar_convite_rapido(usuario_nome: str, validade_horas: int = 72) -> Dict:
    """Atalho para criar convite rapidamente"""
    manager = ConviteManager()
    return manager.gerar_codigo_convite(usuario_nome, validade_horas)


def enviar_convite_convocacao(usuario_origem: str, usuario_destino: str) -> Dict:
    """Simula o envio de um convite para um usuário"""
    manager = ConviteManager()
    convite = manager.gerar_codigo_convite(usuario_origem, reutilizavel=True)
    resultado = manager.usar_convite(convite["codigo"], usuario_destino)
    broadcast = manager.disparar_broadcast_convite(convite["id"])
    
    return {
        "convite": convite,
        "uso_resultado": resultado,
        "broadcast": broadcast
    }


if __name__ == "__main__":
    print("🧿 KOBLLUX CONVITE SYSTEM v1.0 🧿\n")
    
    manager = ConviteManager()
    
    # Demo: Gerar convite
    print("📬 Gerando convite...")
    convite = manager.gerar_codigo_convite("Usuario_Raiz", validade_horas=24)
    print(f"✅ Convite gerado: {convite['id']}")
    print(f"📍 Código: {convite['codigo']}")
    print(f"🔗 Link: {convite['link_compartilhavel']}\n")
    
    # Demo: Usar convite
    print("👤 Usuário novo usando convite...")
    uso = manager.usar_convite(convite["codigo"], "Usuario_Novo")
    print(f"  {uso['mensagem']}\n")
    
    # Demo: Disparar broadcast
    print("📡 Disparando broadcast aos 16 arquétipos...")
    broadcast = manager.disparar_broadcast_convite(convite["id"])
    print(f"✅ {broadcast['total_respondentes']} arquétipos responderam")
    print(f"📊 Frequência combinada: {broadcast['frequencia_combinada_hz']}Hz\n")
    
    # Demo: Relatório
    print("📋 RELATÓRIO FINAL:")
    relatorio = manager.exportar_relatorio()
    print(json.dumps(relatorio, indent=2, ensure_ascii=False))
    
    print("\n" + "="*60)
    print("✝ JESUS É O CENTRO. A MALHA VIVE. ∴")
    print("="*60)
