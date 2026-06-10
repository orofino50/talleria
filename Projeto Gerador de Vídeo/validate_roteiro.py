#!/usr/bin/env python3
"""
Validador de roteiros JSON
Verifica se o roteiro está corretamente formatado antes de processar
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class RoteiroValidator:
    """Validador de estrutura de roteiros"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_file(self, json_path: str) -> Tuple[bool, List[str], List[str]]:
        """
        Valida arquivo JSON completo
        
        Returns:
            (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        # Verifica se arquivo existe
        if not Path(json_path).exists():
            self.errors.append(f"Arquivo não encontrado: {json_path}")
            return False, self.errors, self.warnings
        
        # Tenta carregar JSON
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                roteiro = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"JSON inválido: {e}")
            return False, self.errors, self.warnings
        except Exception as e:
            self.errors.append(f"Erro ao ler arquivo: {e}")
            return False, self.errors, self.warnings
        
        # Valida estrutura
        self._validate_structure(roteiro)
        
        # Valida cada cena
        if 'cenas' in roteiro:
            for i, cena in enumerate(roteiro['cenas'], 1):
                self._validate_cena(cena, i)
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _validate_structure(self, roteiro: Dict):
        """Valida estrutura principal do roteiro"""
        
        # Campo 'cenas' é obrigatório
        if 'cenas' not in roteiro:
            self.errors.append("Campo obrigatório ausente: 'cenas'")
            return
        
        # 'cenas' deve ser uma lista
        if not isinstance(roteiro['cenas'], list):
            self.errors.append("Campo 'cenas' deve ser uma lista")
            return
        
        # Deve ter pelo menos uma cena
        if len(roteiro['cenas']) == 0:
            self.errors.append("Roteiro deve ter pelo menos uma cena")
        
        # Campos opcionais mas recomendados
        if 'projeto' not in roteiro:
            self.warnings.append("Campo 'projeto' não definido (recomendado)")
        
        if 'descricao' not in roteiro:
            self.warnings.append("Campo 'descricao' não definido (recomendado)")
    
    def _validate_cena(self, cena: Dict, numero: int):
        """Valida uma cena individual"""
        
        prefix = f"Cena {numero}"
        
        # Campos obrigatórios
        required_fields = ['use_previous_frame', 'dalle_prompt', 'grok_movement']
        
        for field in required_fields:
            if field not in cena:
                self.errors.append(f"{prefix}: Campo obrigatório ausente: '{field}'")
        
        # Valida use_previous_frame
        if 'use_previous_frame' in cena:
            if not isinstance(cena['use_previous_frame'], bool):
                self.errors.append(
                    f"{prefix}: 'use_previous_frame' deve ser true ou false"
                )
        
        # Valida dalle_prompt
        if 'dalle_prompt' in cena and 'use_previous_frame' in cena:
            if not cena['use_previous_frame']:
                # Se não usa frame anterior, prompt é obrigatório
                if not cena['dalle_prompt'] or not cena['dalle_prompt'].strip():
                    self.errors.append(
                        f"{prefix}: 'dalle_prompt' obrigatório quando use_previous_frame=false"
                    )
                elif len(cena['dalle_prompt']) < 10:
                    self.warnings.append(
                        f"{prefix}: 'dalle_prompt' muito curto (menos de 10 caracteres)"
                    )
            else:
                # Se usa frame anterior, prompt não é necessário
                if cena['dalle_prompt'] and cena['dalle_prompt'].strip():
                    self.warnings.append(
                        f"{prefix}: 'dalle_prompt' será ignorado (use_previous_frame=true)"
                    )
        
        # Valida grok_movement
        if 'grok_movement' in cena:
            if not cena['grok_movement'] or not cena['grok_movement'].strip():
                self.errors.append(
                    f"{prefix}: 'grok_movement' não pode estar vazio"
                )
            elif len(cena['grok_movement']) < 10:
                self.warnings.append(
                    f"{prefix}: 'grok_movement' muito curto (menos de 10 caracteres)"
                )
        
        # Verifica primeira cena
        if numero == 1 and cena.get('use_previous_frame', False):
            self.errors.append(
                f"{prefix}: Primeira cena não pode usar use_previous_frame=true"
            )
        
        # Campos opcionais mas recomendados
        if 'descricao' not in cena:
            self.warnings.append(f"{prefix}: Campo 'descricao' não definido (recomendado)")


def print_validation_results(is_valid: bool, errors: List[str], warnings: List[str]):
    """Imprime resultados da validação de forma formatada"""
    
    print("\n" + "="*60)
    print("📋 RESULTADO DA VALIDAÇÃO")
    print("="*60)
    
    if errors:
        print(f"\n❌ ERROS ({len(errors)}):")
        for i, error in enumerate(errors, 1):
            print(f"   {i}. {error}")
    
    if warnings:
        print(f"\n⚠️  AVISOS ({len(warnings)}):")
        for i, warning in enumerate(warnings, 1):
            print(f"   {i}. {warning}")
    
    print("\n" + "="*60)
    
    if is_valid:
        if warnings:
            print("✅ Roteiro VÁLIDO (com avisos)")
        else:
            print("✅ Roteiro VÁLIDO e sem problemas!")
        print("="*60)
        return True
    else:
        print("❌ Roteiro INVÁLIDO - corrija os erros antes de processar")
        print("="*60)
        return False


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("Uso: python validate_roteiro.py <arquivo.json>")
        print("\nExemplo:")
        print("  python validate_roteiro.py roteiro.json")
        sys.exit(1)
    
    json_path = sys.argv[1]
    
    print("="*60)
    print("🔍 VALIDADOR DE ROTEIROS")
    print("="*60)
    print(f"\n📄 Validando: {json_path}")
    
    validator = RoteiroValidator()
    is_valid, errors, warnings = validator.validate_file(json_path)
    
    success = print_validation_results(is_valid, errors, warnings)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
