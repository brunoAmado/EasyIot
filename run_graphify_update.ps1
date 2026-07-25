<#
.SYNOPSIS
    Script para atualizar o grafo AST do Graphify de forma local (sem custo de API).
#>

Write-Host "🚀 A iniciar a atualização do grafo do Graphify (AST-only)..." -ForegroundColor Cyan

# Calcular limite de workers para máquinas Windows de múltiplos núcleos (limite máximo de 61)
$MaxWorkers = [math]::Min(61, [math]::Max(2, [int]($env:NUMBER_OF_PROCESSORS * 0.75)))

# Definir a variável de ambiente para o Graphify
$env:GRAPHIFY_MAX_WORKERS = $MaxWorkers

Write-Host "✅ Variáveis de ambiente configuradas:" -ForegroundColor Green
Write-Host "   GRAPHIFY_MAX_WORKERS = $env:GRAPHIFY_MAX_WORKERS"

Write-Host "🧠 A executar 'graphify update .'..." -ForegroundColor Cyan
.\.venv\Scripts\python.exe -m graphify update .

Write-Host "✨ Atualização concluída com sucesso!" -ForegroundColor Green
